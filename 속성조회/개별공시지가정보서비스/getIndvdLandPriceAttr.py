import requests
from urllib.parse import quote_plus, urlencode
import pymysql


    
    
class getIndvdLandPriceAttr():
    def __init__(self):
        self.con = pymysql.connect(
          host='1.234.5.16',
          user='dev22',
          password='aimypie111@',
          charset='utf8',
          db='nsdi',
          cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.url = "http://apis.data.go.kr/1611000/nsdi/IndvdLandPriceService/attr/getIndvdLandPriceAttr"
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        self.url_result = ""
        self.sql = "INSERT INTO getIndvdLandPriceAttr (pnu,ldCode,ldCodeNm,regstrSeCode,\
                regstrSeCodeNm,mnnmSlno,stdrYear,stdrMt,pblntfPclnd,pblntfDe,stdLandAt,stdLandAt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"      
        
    def get_api_data(self):
        try:
            response = requests.get(self.url_result)
        except Exception as e:
            print(e,"gaa_api_error")
        
        try :
            json_object = response.json()
        
        except Exception as e:
            print(e,"ge_api_error")
        
        return json_object['indvdLandPrices']['field']

    def get_db_data(self, query):
        try:
            self.cur.execute(query)
            
            rows = self.cur.fetchall()

            return rows

        except Exception as e:
            print(e, "get_db_data_error")

    def set_db_data(self, sql, var):
        try:
            self.cur.execute(sql, var)
            self.con.commit()

        except Exception as e:
            print(str(e))

    def set_url(self, pnu, pageNo):
        
        queryParams = f'?{quote_plus("ServiceKey")}={self.key}&' + \
                urlencode({quote_plus('ldCode'): pnu,
                        quote_plus('stdrYear'): '2021',
                        quote_plus('format'): 'json',
                        quote_plus('numOfRows'): '100',
                        quote_plus('pageNo'): pageNo})

        self.url_result = self.url + queryParams    

    def start(self):
        for row in self.get_db_data('SELECT pnu FROM LandPriceAttribute'):
            print(row)
            for i in range(1,3):
                self.set_url(row['pnu'],i)
                for item in self.get_api_data():
                    var = (item['pnu'], item['ldCode'], item['ldCodeNm'], item['regstrSeCode'],
                        item['regstrSeCodeNm'], item['mnnmSlno'], item['stdrYear'], item['stdrMt'], 
                        item['pblntfPclnd'], item['pblntfDe'], item['stdLandAt'],item['lastUpdtDt'])
                    self.set_db_data(self.sql, var)
            
def main():
    test = getIndvdLandPriceAttr()
    test.start()


main()