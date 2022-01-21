from molitBaseClass import *

class TradePrcIndex(setup):
    def __init__(self):
        super().__init__()
        self.url = 'http://openapi.kab.co.kr/OpenAPI_ToolInstallPackage/service/rest/TradePrcIndexSvc/getTradePrcIndex'
        self.tableName = "TradePrcIndex"
        self.startmonth = 201701
        self.endmonth = 202102
        self.dict_template ={
            'aptTypeNm':"",
            'regionCd':"",
            'regionNm':"",
            'rsRow':""}
            
    def make_url(self, region_code,building_type):
        queryParams = f'?{quote_plus("ServiceKey")}={self.key}&' + \
                      urlencode({quote_plus('startmonth'): self.startmonth,
                                 quote_plus('endmonth'): self.endmonth,
                                 quote_plus('region'): region_code,
                                 quote_plus('buildingtype'):building_type})
        return self.url + queryParams
    
    def split_rsRow_into_date_and_price(self, rsRow:str):
        text = rsRow.split("|")
        date_list =[]
        price_list = []
        for DP in text:
            temp = DP.split(',')
            date_list.append(temp[0])
            price_list.append(temp[1])
        return (date_list,price_list,len(text))

    def insert_into_db(self, item_list):
        sql = 'INSERT INTO TradePrcIndex (date,TradePrcIndex,\
            aptTypeNm, regionCd, regionNm) \
            VALUES (%s,%s,%s,%s,%s)'

        for items in item_list:
            item = self.get_sql_dict_item(items)
            date_list,price_list,Length = self.split_rsRow_into_date_and_price(item['rsRow'])
            for numberth in range(Length):
                var = (date_list[numberth],price_list[numberth],item['aptTypeNm'],
                item['regionCd'],item['regionNm'])
                try:
                    self.cur.execute(sql, var)
                    self.con.commit()

                except Exception as e:
                    print(str(e))
                    return 1

        return 0

    
    def get_latest_db_value(self):
        # STEP 1. 데이터베이스의 가장 큰 지역 날짜 받아옴.
        sql = "SELECT MAX(date) FROM %(tableName)s"
        try:
            self.cur.execute(sql % {"tableName": self.tableName})
            item = self.cur.fetchall()
            Max_date = item[0]['MAX(date)']
            
        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("(STEP 1)최근값 조회 중 오류가 발생했습니다. 프로그램을 종료합니다.")
            sys.exit()

        if not Max_date:  # 데이터베이스가 비워져 있음.
            print("INSERT INTO EMPTY TABLE")
            return 0

        return Max_date
    #지역코드 테이블로부터 지역코드 받아옴
    def get_region_code_list_from_region_code(self):
        print("region_code CALCULATING...")
        sql = "SELECT region_code FROM region_code"
        try:
            self.cur.execute(sql)
            dict_region_code = self.cur.fetchall()
        except Exception as e:
            print(str(e))

        list_region_code =[]

        for region in dict_region_code:
            list_region_code.append(region['region_code'][0:5])

        print("region_code SUCCESS")
        return list_region_code
    #빌딩타입테이블로부터 빌딩 코드 받아옴 
    def get_building_type_list_from_building_type(self):
        print("building type CALCULATING...")
        sql = "SELECT building_type_code FROM building_type"
        try:
            self.cur.execute(sql)
            dict_building_type = self.cur.fetchall()
        except Exception as e:
            print(str(e))

        list_building_type =[]

        for building in dict_building_type:
            list_building_type.append(building['building_type_code'])

        print("building type SUCCESS")
        return list_building_type

    #------------------------------------------------------------------------
    def request_api_and_insert_into_db(self, region_code ,building_code):
        
        print("request_api_and_insert_into_db CALCULATING...")
        for region in tqdm(region_code, total=len(region_code)):
            for building in tqdm(building_code, total=len(building_code)):

                url = self.make_url(region, building)
                # STEP 1. url request -> xml to dict.
                try:
                    response = Request(url)
                    response.get_method = lambda: 'GET'
                    response_body = urlopen(response).read()
                    my_dict = xmltodict.parse(response_body)
                except Exception as e:  # API 요청에 문제가 생겼을 때.
                    print(str(e))
                    continue
                #Nonetype 일때
                if(my_dict['response']['body'] == None):
                    continue
                
                # STEP 2. Distinguishing api result.
                resultCode = my_dict['response']['header']['resultCode']
                if resultCode != '00':  # 서버가 비정상일 때.
                    print("resultCodeError")
                    continue
                
                # STEP 3. 요청 메시지에 대한 응답 값이 존재하는 지 판별.
                items = my_dict['response']['body']['item']
                if not items:  # 응답 값이 존재하지 않을 때.
                    continue

                # STEP 4. 응답 메시지 값 디비에 저장.
                if type(items) is list:
                    isError = self.insert_into_db(items)
                else:  # 응답 메시지 값이 하나일 경우 dict_list가 아닌 dict로 들어옴.
                    isError = self.insert_into_db([items, ])
                if isError:  # 데이터베이스에 문제가 생겼을 때.
                    continue

        print("request_api_and_insert_into_db SUCCESS")
    #--------------------------------------------------------------------------

    def start(self):
        temp_startmonth = self.get_latest_db_value()
        if(int(self.startmonth) < int(temp_startmonth)):
            self.startmonth = temp_startmonth
        # 지역 코드 리스트.
        region_code = self.get_region_code_list_from_region_code()
        print(region_code)
        #빌딩 코드 리스트.
        building_type_code = self.get_building_type_list_from_building_type()
        print(building_type_code)
        
        # API 요청 후 응답값 디비에 저장.
        self.request_api_and_insert_into_db(region_code,building_type_code)
        print("DONE")
        
function = TradePrcIndex()
function.start()