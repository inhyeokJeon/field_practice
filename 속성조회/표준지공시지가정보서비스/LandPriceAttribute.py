import requests
from urllib.parse import quote_plus, urlencode
import pymysql


    
    
class LandPriceAttribute():
    def __init__(self):
        self.con = pymysql.connect(
          host='1.234.5.16',
          user='dev22',
          password='aimypie111@',
          charset='utf8',
          db='nsdi',
          cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.url = "http://apis.data.go.kr/1611000/nsdi/ReferLandPriceService/attr/getReferLandPriceAttr"
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        self.url_result = ""
        self.sql = "INSERT INTO LandPriceAttribute (pnu,ldCode,ldCodeNm,regstrSeCode,\
                regstrSeCodeNm,mnnmSlno,stdLandSn,stdrYear,bsnsDstrcAr,lndcgrCode,lndcgrCodeNm,realLndcgrCode,realLndcgrCodeNm,\
                lndpclAr,prposArea1,prposAreaNm1,prposArea2,prposAreaNm2,prposDstrc1,prposDstrcNm1,prposDstrc2,\
                prposDstrcNm2,cnflcRt,ladUseSittn,ladUseSittnNm,tpgrphHgCode,tpgrphHgCodeNm,tpgrphFrmCode,tpgrphFrmCodeNm,\
                roadSideCode,roadSideCodeNm,roadDstncCode,roadDstncCodeNm,pblntfPclnd,stdlandPosesnSeCode,stdlandPosesnSeCodeNm,\
                posesnStle,posesnStleNm,lastUpdtDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"      
        
    def get_api_data(self):
        try:
            response = requests.get(self.url_result)
        except Exception as e:
            print(e,"gaa_api_error")
        
        try :
            json_object = response.json()
        
        except Exception as e:
            print(e,"ge_api_error")
        
        return json_object['referLandPrices']['field']

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

    def set_url(self, ldCode, pageNo):
        
        queryParams = f"?{quote_plus('ServiceKey')}={self.key}&" + \
                urlencode({quote_plus('ldCode'): ldCode,
                        quote_plus('stdrYear'): '2021',
                        quote_plus('format'): 'json',
                        quote_plus('numOfRows'): '100',
                        quote_plus('pageNo'): pageNo})
        self.url_result = self.url + queryParams    

    def start(self):
        for row in self.get_db_data('SELECT ldongCd FROM bubjungdong'):
            print(row)
            for i in range(1,3):
                self.set_url(row['ldongCd'],i)
                for item in self.get_api_data():
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
                    self.set_db_data(self.sql, var)
            
def main():
    test = LandPriceAttribute()
    test.start()


main()