import pymysql
import requests
from urllib.parse import quote_plus, urlencode
from progress.bar import Bar
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
import sys

class setup:
    def __init__(self):
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        
        self.con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='nsdi',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.request_session = requests.Session()
        self.Year = [2017,2018,2019,2020]

    def get_list_ldcode_from_db(self):
        sql = "SELECT ldongCd FROM bubjungdong WHERE flag = 'Y'"
        try:
            self.cur.execute(sql)
            dict_ldcode = self.cur.fetchall()
        except Exception as e:
            print(str(e))

        list_ldcode = []
        for ldcode in dict_ldcode:
            list_ldcode.append(ldcode['ldongCd'])
        return list_ldcode

    def get_url(self, pnucode:str, pageNo:str):
        queryParams = f'?{quote_plus("ServiceKey")}={self.key}&' + \
                      urlencode({quote_plus('pnu'): pnucode,
                                 quote_plus('stdrYear'): '2019',
                                 quote_plus('format'): 'json',
                                 quote_plus('numOfRows'): '100',
                                 quote_plus('pageNo'): pageNo})
        return self.url + queryParams
    
    def get_latest_db_value(self):
        
        # STEP 1. 데이터베이스의 가장 큰 법정동 값 받아옴.
        sql = "SELECT MAX(ldCode) FROM %(tableName)s"
        try:
            self.cur.execute(sql % {"tableName": self.tableName})
            item = self.cur.fetchall()
            Max_ldCode = item[0]['MAX(ldCode)']
        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("(STEP 1)최근값 조회 중 오류가 발생했습니다 ldCode. 프로그램을 종료합니다.")
            sys.exit()

        if not Max_ldCode:  # 데이터베이스가 비워져 있음.
            print("INSERT INTO EMPTY TABLE")
            return (0)

        return Max_ldCode
    '''
    def get_latest_db_value(self):
        
        # STEP 1. 데이터베이스의 가장 큰 pnu코드 값 받아옴.
        sql = "SELECT MAX(pnu) FROM %(tableName)s"
        try:
            self.cur.execute(sql % {"tableName": self.tableName})
            item = self.cur.fetchall()
            Max_pnu = item[0]['MAX(pnu)']
            print(Max_pnu)
        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("(STEP 1)최근값 조회 중 오류가 발생했습니다 pnu. 프로그램을 종료합니다.")
            sys.exit()

        if not Max_pnu:  # 데이터베이스가 비워져 있음.
            print("INSERT INTO EMPTY TABLE")
            return (0, 0)
    '''
    def get_sql_dict_item(self, dict_item: dict):
        dict_template_copy: dict = self.dict_template.copy()
        try:
            for key in dict_item.keys():
                if dict_item[str(key)] == None:
                    continue
                dict_template_copy[str(key)] = dict_item[str(key)]
        except Exception as e:
            print(str(e))
            print("get_sql_dict_item 오류")
            sys.exit()
        return dict_template_copy



class LandPriceAttribute(setup):
    def __init__(self):
        super().__init__()
        self.url = "http://apis.data.go.kr/1611000/nsdi/ReferLandPriceService/attr/getReferLandPriceAttr"
        self.sql ="INSERT INTO LandPriceAttribute (pnu,ldCode,ldCodeNm,regstrSeCode,\
                regstrSeCodeNm,mnnmSlno,stdLandSn,stdrYear,bsnsDstrcAr,lndcgrCode,lndcgrCodeNm,realLndcgrCode,realLndcgrCodeNm,\
                lndpclAr,prposArea1,prposAreaNm1,prposArea2,prposAreaNm2,prposDstrc1,prposDstrcNm1,prposDstrc2,\
                prposDstrcNm2,cnflcRt,ladUseSittn,ladUseSittnNm,tpgrphHgCode,tpgrphHgCodeNm,tpgrphFrmCode,tpgrphFrmCodeNm,\
                roadSideCode,roadSideCodeNm,roadDstncCode,roadDstncCodeNm,pblntfPclnd,stdlandPosesnSeCode,stdlandPosesnSeCodeNm,\
                posesnStle,posesnStleNm,lastUpdtDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.tableName = "LandPriceAttribute"
        self.now_ldonCd = 0
        self.dict_template ={
            'pnu':"",
            'ldCode':"",
            'ldCodeNm':"",
            'regstrSeCode':"",
            'regstrSeCodeNm':"",
            'mnnmSlno':"",
            'stdLandSn':"",
            'stdrYear':"",
            'bsnsDstrcAr':0,
            'lndcgrCode':"",
            'lndcgrCodeNm':"",
            'realLndcgrCode':"",
            'realLndcgrCodeNm':"",
            'lndpclAr':0,
            'prposArea1':"",
            'prposAreaNm1':"",
            'prposArea2':"",
            'prposAreaNm2':"",
            'prposDstrc1':"",
            'prposDstrcNm1':"",
            'prposDstrc2':"",
            'prposDstrcNm2':"",
            'cnflcRt':"",
            'ladUseSittn':"",
            'ladUseSittnNm':"",
            'tpgrphHgCode':"",
            'tpgrphHgCodeNm':"",
            'tpgrphFrmCode':"",
            'tpgrphFrmCodeNm':"",
            'roadSideCode':"",
            'roadSideCodeNm':"",
            'roadDstncCode':"",
            'roadDstncCodeNm':"",
            'posesnStle':"",
            'posesnStleNm':"",
            'lastUpdtDt':""
            }

    def get_dict_apart_price(self, list_ldcode):
        self.now_ldonCd = self.get_latest_db_value() 
        length = len(list_ldcode)

        for year in tqdm(self.Year, total = len(self.Year)):
            for ldcode in tqdm(list_ldcode, total = length):
                if (int(ldcode) < int(self.now_ldonCd)):
                    continue
                pageNo = 1
                while True:
                    try:
                        response = self.request_session.get(self.get_url(ldcode, pageNo,year))
                        json_object = response.json()
                        dict_item = json_object['referLandPrices']['field']
                    except Exception as e:
                        print(e)
                        break

                    if(dict_item== None):
                        print("Nonetype")
                        break
                        # STEP 3. 요청 메시지에 대한 응답 값이 존재하는 지 판별.

                    if not dict_item:  # 응답 값이 존재하지 않을 때.
                        break
                    resultCode = json_object['referLandPrices']['resultCode']   
                
                    # if(resultCode == None):
                    #     break
                    # if resultCode != 'null':  # 서버가 비정상일 때.
                    #     print("resultCodeError")
                    #     break
                    pageNo = pageNo + 1

                    if len(dict_item) != 0:
                        self.set_apart_price_into_db(dict_item)
                    break
    
    def set_apart_price_into_db(self, apart_price_list):
        for items in apart_price_list:
            item = self.get_sql_dict_item(items)
            var = (item['pnu'], item['ldCode'], item['ldCodeNm'], item['regstrSeCode'],
                        item['regstrSeCodeNm'], item['mnnmSlno'], item['stdLandSn'], item['stdrYear'], 
                        item['bsnsDstrcAr'], item['lndcgrCode'], item['lndcgrCodeNm'],item['realLndcgrCode'],item['realLndcgrCodeNm'], item['lndpclAr'], 
                        item['prposArea1'], item['prposAreaNm1'],item['prposArea2'],item['prposAreaNm2'],
                        item['prposDstrc1'],item['prposDstrcNm1'],item['prposDstrc2'],item['prposDstrcNm2'],
                        item['cnflcRt'],item['ladUseSittn'],item['ladUseSittnNm'],item['tpgrphHgCode'],
                        item['tpgrphHgCodeNm'],item['tpgrphFrmCode'],item['tpgrphFrmCodeNm'],item['roadSideCode'],
                        item['roadSideCodeNm'],item['roadDstncCode'],item['roadDstncCodeNm'],item['pblntfPclnd'],
                        item['stdlandPosesnSeCode'],item['stdlandPosesnSeCodeNm'],item['posesnStle'],item['posesnStleNm'],
                        item['lastUpdtDt'])
            try:
                self.cur.execute(self.sql, var)
                self.con.commit()

            except Exception as e:
                print(str(e))

    def get_url(self, ldcode:str, pageNo:str, year:str):
        queryParams = f'?{quote_plus("ServiceKey")}={self.key}&' + \
                      urlencode({quote_plus('ldCode'): ldcode,
                                 quote_plus('stdrYear'): year,
                                 quote_plus('format'): 'json',
                                 quote_plus('numOfRows'): '100',
                                 quote_plus('pageNo'): pageNo})
        return self.url + queryParams

    

    def start(self):
        list_ldcode = self.get_list_ldcode_from_db()
        self.get_dict_apart_price(list_ldcode)

class ApartHousingPriceAttribute(setup):
    def __init__(self):
        super().__init__()
        self.url = "http://apis.data.go.kr/1611000/nsdi/ApartHousingPriceService/attr/getApartHousingPriceAttr"
        self.sql = "INSERT INTO ApartHousingPriceAttribute \
                                    (pnu, ldCode, ldCodeNm, regstrSeCode, regstrSeCodeNm, mnnmSlno, stdrYear, stdrMt,\
                                     aphusCode, aphusSeCode, aphusSeCodeNm, spclLandNm, aphusNm, prvuseAr, pblntfPc,\
                                     dongNm, hoNm) \
                                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.dict_template ={
            'pnu':"",
            'ldCode':"",
            'ldCodeNm':"",
            'regstrSeCode':"",
            'regstrSeCodeNm':"",
            'mnnmSlno':"",
            'stdrYear':"",
            'stdrMt':0,
            'aphusCode':"",
            'aphusSeCode':"",
            'aphusSeCodeNm':"",
            'spclLandNm':"",
            'aphusNm':"",
            'prvuseAr':"",
            'pblntfPc':"",
            'lastUpdtDt':""
            }
        self.tableName = "ApartHousingPriceAttribute"

    def get_dict_apart_price(self, list_ldcode):
        self.now_ldongCd = self.get_latest_db_value() 
        length = len(list_ldcode)
        for year in tqdm(self.Year, total = len(self.Year)):
            for ldcode in tqdm(list_ldcode, total = length):
                if (int(ldcode) < int(self.now_ldongCd)):
                    continue
                pageNo = 1
                while True:
                    try:
                        response = self.request_session.get(self.get_url(ldcode, pageNo))
                        json_object = response.json()
                        dict_item = json_object['apartHousingPrices']['field']

                    except Exception as e:
                        print(e)
                        break
                    
                    if(dict_item== None):
                        print("Nonetype")
                        break
                        # STEP 3. 요청 메시지에 대한 응답 값이 존재하는 지 판별.

                    if not dict_item:  # 응답 값이 존재하지 않을 때.
                        break
                    resultCode = json_object['apartHousingPrices']['resultCode']   
                                
                    pageNo = pageNo + 1
                    if len(dict_item) != 0:
                        self.set_apart_price_into_db(dict_item)
                        continue
                    break
    
    def set_apart_price_into_db(self, apart_price_list):
        for dict_item in apart_price_list:
            tuple_item = (dict_item['pnu'], str(dict_item['ldCode']), str(dict_item['ldCodeNm']),
                          str(dict_item['regstrSeCode']), str(dict_item['regstrSeCodeNm']), str(dict_item['mnnmSlno']),
                          str(dict_item['stdrYear']), str(dict_item['stdrMt']), str(dict_item['aphusCode']),
                          str(dict_item['aphusSeCode']), str(dict_item['aphusSeCodeNm']), str(dict_item['spclLandNm']),
                          str(dict_item['aphusNm']), str(dict_item['prvuseAr']), str(dict_item['pblntfPc']),
                          str(dict_item['dongNm']), str(dict_item['hoNm']))
            try:
                self.cur.execute(self.sql, tuple_item)
                self.con.commit()
            except Exception as e:
                print(str(e))

    def start(self):
        list_ldcode = self.get_list_ldcode_from_db()
        self.get_dict_apart_price(list_ldcode)

class getIndvdHousingPriceAttr(setup):
    def __init__(self):
        super().__init__()
        self.url = "http://apis.data.go.kr/1611000/nsdi/IndvdHousingPriceService/attr/getIndvdHousingPriceAttr"
        self.sql = "INSERT INTO getIndvdHousingPriceAttr (pnu,ldCode,ldCodeNm,regstrSeCode,\
                regstrSeCodeNm,mnnmSlno,bildRegstrEsntlNo, stdrYear,stdrMt,dongCode,ladRegstrAr,calcPlotAr,buldAllTotAr,\
                buldCalcTotAr,housePc,housePc,lastUpdtDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def get_dict_apart_price(self, list_ldcode):
        length = len(list_ldcode)
        bar = Bar('GET API DATA AND INSERT INTO TABLE', max=length)
        for ldcode in list_ldcode:
            bar.next()
            pageNo = 1
            while True:
                try:
                    response = self.request_session.get(self.get_url(ldcode, pageNo))
                    json_object = response.json()
                    dict_item = json_object['indvdHousingPrices']['field']
                except Exception as e:
                    print(str(e),response.text)
                    if "Expecting value" in e:
                        time.sleep(5)
                        try:
                            response = self.request_session.get(self.get_url(ldcode, pageNo))
                            json_object = response.json()
                            dict_item = json_object['indvdHousingPrices']['field']
                        except Exception as e:
                            print(str(e))

                pageNo = pageNo + 1
                if len(dict_item) != 0:
                    self.set_apart_price_into_db(dict_item)
                    continue
                break
        bar.finish()
    
    def set_apart_price_into_db(self, apart_price_list):

        for item in apart_price_list:
            var = (item['pnu'], item['ldCode'], item['ldCodeNm'], item['regstrSeCode'],
                        item['regstrSeCodeNm'], item['mnnmSlno'], item['bildRegstrEsntlNo'],item['stdrYear'], item['stdrMt'], 
                        item['dongCode'], item['ladRegstrAr'], item['calcPlotAr'],item['buldAllTotAr'],item['buldCalcTotAr'],
                        item['housePc'])
            try:
                self.cur.execute(self.sql, var)
                self.con.commit()

            except Exception as e:
                print(str(e))
    def start(self):
        list_ldcode = self.get_list_ldcode_from_db()
        self.get_dict_apart_price(list_ldcode)
    
class getIndvdLandPriceAttr(setup):
    def __init__(self):
        super().__init__()
        self.url = "http://apis.data.go.kr/1611000/nsdi/IndvdLandPriceService/attr/getIndvdLandPriceAttr"
        self.sql = "INSERT INTO getIndvdLandPriceAttr (pnu,ldCode,ldCodeNm,regstrSeCode,\
                regstrSeCodeNm,mnnmSlno,stdrYear,stdrMt,pblntfPclnd,pblntfDe,stdLandAt,stdLandAt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

    def get_dict_apart_price(self, list_ldcode):
        length = len(list_ldcode)
        bar = Bar('GET API DATA AND INSERT INTO TABLE', max=length)
        for ldcode in list_ldcode:
            bar.next()
            pageNo = 1
            while True:
                try:
                    response = self.request_session.get(self.get_url(ldcode, pageNo))
                    json_object = response.json()
                    dict_item = json_object['indvdLandPrices']['field']
                except Exception as e:
                    print(str(e),response.text)
                    if "Expecting value" in e:
                        time.sleep(5)
                        try:
                            response = self.request_session.get(self.get_url(ldcode, pageNo))
                            json_object = response.json()
                            dict_item = json_object['indvdLandPrices']['field']
                        except Exception as e:
                            print(str(e))

                pageNo = pageNo + 1
                if len(dict_item) != 0:
                    self.set_apart_price_into_db(dict_item)
                    continue
                break
        bar.finish()
    
    def set_apart_price_into_db(self, apart_price_list):
        for item in apart_price_list:
            var = (item['pnu'], item['ldCode'], item['ldCodeNm'], item['regstrSeCode'],
                        item['regstrSeCodeNm'], item['mnnmSlno'], item['stdrYear'], item['stdrMt'], 
                        item['pblntfPclnd'], item['pblntfDe'], item['stdLandAt'],item['lastUpdtDt'])
            try:
                self.cur.execute(self.sql, var)
                self.con.commit()

            except Exception as e:
                print(str(e))
                
    def start(self):
        list_ldcode = self.get_list_ldcode_from_db()
        self.get_dict_apart_price(list_ldcode)

