import json
import requests
import pymysql
import logging
import sys
from tqdm import tqdm
# 주소받아와서 좌표저장 #
class ONBID_MAP:
    def __init__(self):
        self.native_key = "48e7a85226b63e1025e59f1f5be242e1"
        # curl -v -X GET "https://dapi.kakao.com/v2/local/search/address.json" --data-urlencode "query=전북 삼성동 100" -H "Authorization: KakaoAK 29cce34372fad3fc129453f0e5fd3fe6"

        self.kakaomap_dict = {
            "kakaomap_url":"https://dapi.kakao.com/v2/local/search/address.json?query={ADDR}",
            "Host": "dapi.kakao.com",
            "headers":{
                "Authorization": "KakaoAK {REST_API_KEY}".format_map({
                    "REST_API_KEY": self.native_key
                })
            },
        }
        self.con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='onbid',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()


    def getGPSLocation(self,addr) -> dict:
        '''

        :param addr: 주소값을 넣으면
        :return: x ,y 좌표를 딕셔너리로 리턴
        '''
        self.req = requests.Session()

        self.map = {
            "tm_x": float(0.0),
            "tm_y": float(0.0)
        }

        map_result = self.req.get(url=self.kakaomap_dict["kakaomap_url"].format(ADDR=addr), headers=self.kakaomap_dict["headers"])

        if map_result.status_code == 200:
            map_result_data = map_result.json()

            if map_result_data['meta'] and map_result_data['meta']['is_end'] and map_result_data['meta']['total_count'] != 0:
                length = len(map_result_data['documents'])
                if length > 0:
                    tm_x = map_result_data['documents'][0]['x']
                    tm_y = map_result_data['documents'][0]['y']

                    self.map = {
                        "tm_x": float(tm_x),
                        "tm_y": float(tm_y)
                    }

                    self.req.close()
                    return self.map

        elif map_result.status_code == 429:
            print("API 요청 횟수를 초과했습니다")

        if self.req:
            self.req.close()

        return self.map

    def get_MNMT_No_and_Address_from_DB(self) -> list:
        '''
        UnifyUsageCltr 테이블로부터 주소와 물건관리번호를 grouping
        :return: dict로이루어진 list형태로리턴
        '''
        sql = "select CLTR_MNMT_NO,LDNM_ADRS from onbid.ONBID_UnifyUsageCltr_2 where (CLTR_MNMT_NO > '2018-1000-038352') group by CLTR_MNMT_NO,LDNM_ADRS"
        try:
            self.cur.execute(sql)
            item = self.cur.fetchall()
        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("(STEP 1)최근값 조회 중 오류가 발생했습니다. 프로그램을 종료합니다.")
            sys.exit()

        return item

    '''
    def DICTLIST_TO_LIST(self,CLTR_MNMT_NO):
        
        CLTR_MNMT_NO_LIST =[]
        for CLTR in CLTR_MNMT_NO:
            CLTR_MNMT_NO_LIST.append(CLTR['CLTR_MNMT_NO'])
        return CLTR_MNMT_NO_LIST
    '''
    def add_x_y(self, dict_list):
        for item in tqdm(dict_list, desc="dict에 x,y드가는중", total=len(dict_list)):
            dict_xy = self.getGPSLocation(item['LDNM_ADRS'])
            item['tm_x'] = dict_xy['tm_x']
            item['tm_y'] = dict_xy['tm_y']

        return (dict_list)


    def set_value(self,test_1) ->tuple:
        """

        :param test_1: 하나의 dictionary
        :return: dictionary를 tuple형태로 리턴
        """
        temp_list = []
        for i in test_1.keys():
            temp_list.append(test_1[i])
        return tuple(temp_list)

    def insert_into_db(self,DATA):
        """
        dictionary를 tuple로 변환하고 UnifyUsageCltr_MAP 에 적재한다.
        :param DATA: dictionary
        :return: NONE
        """
        var = self.set_value(DATA)
        sql = "insert into ONBID_UnifyUsageCltr_MAP (CLTR_MNMT_NO, LDNM_ADRS, tm_x, tm_y) values (%s,%s,%s,%s)"
        try:
            self.cur.execute(sql, var)
            self.con.commit()
        except Exception as e:
            print("Error")
            print(str(e))

    def start(self):
        """
        db로 부터 물건관리번호와 주소번호를 받아와 kakao api를 이용해 x,y좌표를 얻는다
        x,y좌표를 물건관리번호와 주소가 담긴 dictionary에 추가하고 데이터베이스에 적재한다.
        :return:
        """
        #print(self.getGPSLocation("경기 용인시 처인구 고림동 737"))
        # print(self.getGPSLocation('대구광역시 달서구 송현로 156, ( 송현동 , 송현여자고등학교 )'))
        print("db로부터 물건번호 주소 받아오는중")
        #x,y좌표를 물건관리번호와 주소가 담긴 dictionary에 추가한다
        dict_list = self.add_x_y(self.get_MNMT_No_and_Address_from_DB())
        print(dict_list[0])
        print(len(dict_list))
        for item in tqdm(dict_list, desc="db에 드가는중", total=len(dict_list)):
            self.insert_into_db(item)

        # print(dict_list)
        # CLTR_MNMT_NO = self.get_MNMT_No_and_Address_from_DB
        # CLTR_MNMT_NO_LIST = self.DICTLIST_TO_LIST(CLTR_MNMT_NO)
        #
        # print(CLTR_MNMT_NO_LIST)


def main():
    temp = ONBID_MAP()
    temp.start()


main()

