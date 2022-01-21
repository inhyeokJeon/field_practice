import pymysql
import requests
from urllib.parse import quote_plus, urlencode
from progress.bar import Bar
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class ApartHousingPriceAttribute:
    def __init__(self):
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        self.url = "http://apis.data.go.kr/1611000/nsdi/ApartHousingPriceService/attr/getApartHousingPriceAttr"
        self.con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='nsdi',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

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

    def get_url(self, ldcode, pageNo):
        queryParams = f'?{quote_plus("ServiceKey")}={self.key}&' + \
                      urlencode({quote_plus('pnu'): str(ldcode),
                                 quote_plus('stdrYear'): '2019',
                                 quote_plus('format'): 'json',
                                 quote_plus('numOfRows'): '100',
                                 quote_plus('pageNo'): str(pageNo)})
        return self.url + queryParams

    def get_api_result(self, ldcode):
        pageNo = 1
        result = []
        print(ldcode)
        while True:
            try:
                response = requests.get(self.get_url(ldcode, pageNo))
                json_object = response.json()
                dict_item = json_object['apartHousingPrices']['field']
                response.close()
            except Exception as e:
                print(str(e))
                if "Expecting value" in e:
                    time.sleep(5)
                    try:
                        response = requests.get(self.get_url(ldcode, pageNo))
                        json_object = response.json()
                        dict_item = json_object['apartHousingPrices']['field']
                        response.close()
                    except Exception as e:
                        print(str(e))

            pageNo = pageNo + 1
            if len(dict_item) != 0:
                result += dict_item
                continue
            break

        return result

    def get_dict_apart_price(self, list_ldcode):
        length = len(list_ldcode)
        bar = Bar('GET API DATA AND INSERT INTO TABLE', max=length)
        for ldcode in list_ldcode:
            bar.next()
            pageNo = 1
            while True:
                try:
                    response = requests.get(self.get_url(ldcode, pageNo))
                    json_object = response.json()
                    dict_item = json_object['apartHousingPrices']['field']
                except Exception as e:
                    print(str(e))
                    if "Expecting value" in e:
                        time.sleep(5)
                        try:
                            response = requests.get(self.get_url(ldcode, pageNo))
                            json_object = response.json()
                            dict_item = json_object['apartHousingPrices']['field']
                        except Exception as e:
                            print(str(e))

                pageNo = pageNo + 1
                if len(dict_item) != 0:
                    self.set_apart_price_into_db(dict_item)
                    continue
                break
        bar.finish()

    def set_apart_price_into_db(self, apart_price_list):
        sql = "INSERT INTO ApartHousingPriceAttribute \
                                    (pnu, ldCode, ldCodeNm, regstrSeCode, regstrSeCodeNm, mnnmSlno, stdrYear, stdrMt,\
                                     aphusCode, aphusSeCode, aphusSeCodeNm, spclLandNm, aphusNm, prvuseAr, pblntfPc,\
                                     dongNm, hoNm) \
                                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for dict_item in apart_price_list:

            tuple_item = (str(dict_item['pnu']), str(dict_item['ldCode']), str(dict_item['ldCodeNm']),
                          str(dict_item['regstrSeCode']), str(dict_item['regstrSeCodeNm']), str(dict_item['mnnmSlno']),
                          str(dict_item['stdrYear']), str(dict_item['stdrMt']), str(dict_item['aphusCode']),
                          str(dict_item['aphusSeCode']), str(dict_item['aphusSeCodeNm']), str(dict_item['spclLandNm']),
                          str(dict_item['aphusNm']), str(dict_item['prvuseAr']), str(dict_item['pblntfPc']),
                          str(dict_item['dongNm']), str(dict_item['hoNm']))
            try:
                self.cur.execute(sql, tuple_item)
                self.con.commit()
            except Exception as e:
                print(str(e))

    def start(self):
        print("GET ldongCd FROM DB")
        list_ldcode = self.get_list_ldcode_from_db()
        print("SUCCESS")
        # threads = []
        # with ThreadPoolExecutor(max_workers=20) as executor:
        #     for ldcode in list_ldcode:
        #         threads.append(executor.submit(self.get_api_result, ldcode))
        # 
        #     for task in as_completed(threads):
        #         print(task.result())

        self.get_dict_apart_price(list_ldcode)


func = ApartHousingPriceAttribute()

func.start()