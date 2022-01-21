import urllib.request
import requests
import json
from urllib.parse import quote_plus, urlencode
import pymysql
class setup:
    def __init__(self):
        #open API url
        self.url = "http://apis.data.go.kr/B553077/api/open/sdsc/"
        #open API key
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D&"
        #data 받아올 type
        self.data_type = "type=json"
        #url 다 합친것들
        self.url_result = ""
        #database connector
        self.conn = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='dev',
            cursorclass = pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()
    def read_data(self):
        response = requests.get(self.url_result)
        json_object = response.json()
        return json_object.get("body").get("items")
    def data_load(self):
        pass
    def set_param(self):
        pass
    def set_url(self):
        pass
    def store_data(self):
        pass

class storeZoneOne(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeZoneOne (trarNo,mainTrarNm,ctprvnCd,ctprvnNm,\
                signguCd,signguNm,trarArea,coordNum,coords,stdrDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s)" 
        self.operation = 'storeZoneOne'

    def data_load(self):        
        self.set_param()
        super().read_data()
        for item in self.data:
            val = (item['trarNo'],item['mainTrarNm'],item['ctprvnCd'],item['ctprvnNm'],item['signguCd'],item['signguNm'],\
                    item['trarArea'],item['coordNum'],item['coords'],item['stdrDt'])                  
            try:
                self.cur.execute(self.sql,val)                
            except Exception as e:
                print(str(e)) 
        self.conn.commit()

    def set_param(self):
        self.param = input("상권번호를 입력하세요(전부넣고싶으면 입력 z)  ")
        self.set_url(self.param)

    def set_url(self,param):
        if(param == 'z'):
            self.url_result = self.url+self.operation+'?&'\
                'ServiceKey=' \
                + self.key + self.data_type
        else:
            self.url_result = self.url+self.operation+'?key='\
            + self.param+'&'+ 'ServiceKey=' \
            + self.key + self.data_type
        

#class storeZoneInRadius(setup):


#수정 해야합니다 좌표값 받으면.
#class storeZoneInRectangle(setup):
 


class storeZoneInAdmi(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeZoneInAdmi (trarNo,mainTrarNm,ctprvnCd,ctprvnNm,\
                signguCd,signguNm,trarArea,coordNum,coords,stdrDt,adongCd) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s,%s)" 
        self.operation = 'storeZoneInAdmi'
        
    #Adong table 로 부터 data를 받아와 parmameter를 구하고 url을 설정하여 db 에 적재한다. 
    def data_load(self):
        for rows in self.GetCodefromAdong():
            adongCd = rows['adongCd']
            self.set_param(adongCd)
            for item in super().read_data():
                val = (item['trarNo'],item['mainTrarNm'],item['ctprvnCd'],item['ctprvnNm'],item['signguCd'],item['signguNm'],\
                        item['trarArea'],item['coordNum'],item['coords'],item['stdrDt'],adongCd)                  
                try:
                    self.cur.execute(self.sql,val)                
                except Exception as e:
                    print(str(e))
            self.conn.commit()
        
    def set_param(self,param):
        self.set_url(str(param))

    def set_url(self,param):
        #행정동 기준으로 url설정
        self.url_result = self.url+self.operation+'?divId=adongCd&key='\
                        + param+'&'+ 'ServiceKey=' \
                        + self.key + self.data_type
    #aDong table 로 부터 adongCd 값을 받아온다.
    def GetCodefromAdong(self):
        try:
            self.cur.execute('SELECT adongCd FROM aDong')
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(str(e))

'''
class storeOne(setup):
class storeListInBuilding(setup):
class storeListInPnu(setup):
'''

class storeListInDong(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInDong (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        self.operation = 'storeListInDong'
        
    #Adong table 로 부터 data를 받아와 parmameter를 구하고 url을 설정하여 db 에 적재한다. 
    def data_load(self):
        for rows in self.GetCodefromAdong():
            adongCd = rows['adongCd']
            self.set_param(adongCd)
            print(adongCd)
            for item in super().read_data():
                val = (item['bizesId'],item['bizesNm'],item['brchNm'],\
                    item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],\
                    item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],\
                    item['ksicCd'],item['ksicNm'],item['ctprvnCd'],item['ctprvnNm'],\
                    item['signguCd'],item['signguNm'],item['adongCd'],item['adongNm'],\
                    item['ldongCd'],item['ldongNm'],item['lnoCd'],item['plotSctCd'],\
                    item['plotSctNm'],item['lnoMnno'],item['lnoSlno'],item['lnoAdr'],\
                    item['rdnmCd'],item['rdnm'],item['bldMnno'],item['bldSlno'],\
                    item['bldMngNo'],item['bldNm'],item['rdnmAdr'],item['oldZipcd'],\
                    item['newZipcd'],item['dongNo'],item['flrNo'],item['hoNo'],\
                    item['lon'],item['lat'])                  
                try:
                    self.cur.execute(self.sql,val)                
                except Exception as e:
                    print(str(e))
            self.conn.commit()
        
    def set_param(self,param):
        self.set_url(str(param))

    def set_url(self,param):
        #행정동 기준으로 url설정
        self.url_result = self.url+self.operation+'?divId=adongCd&key='\
                        + param+'&'+ 'ServiceKey=' \
                        + self.key + self.data_type

    #aDong table 로 부터 adongCd 값을 받아온다.
    def GetCodefromAdong(self):
        try:
            self.cur.execute('SELECT adongCd FROM aDong where adongCd > 4413350000')
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(str(e))
'''
class storeListInArea(setup):
class storeListInRadius(setup):
class storeListInRectangle(setup):
class storeListInPolygon(setup):
class storeListInUpjong(setup):
class storeListByDate(setup):
class reqStoreModify(setup):

class storeStatsUpjongInAdmi(setup):
class storeStatsUpjongInBuilding(setup):
class storeStatsUpjongInRadius(setup):
class storeStatsUpjongInRectangle(setup):
class storeStatsUpjongInPolygon(setup):
'''
class largeUpjongList(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO largeUpjongList (indsLclsCd,indsLclsNm,stdrDt) \
            values (%s,%s,%s)"  
        self.operation = 'largeUpjongList'
        
    def data_load(self):
        self.set_param()
        super().read_data()
        for item in self.data:
            val = (item['indsLclsCd'],item['indsLclsNm'],item['stdrDt'])                 
            try:
                self.cur.execute(self.sql,val)                
            except Exception as e:
                print(str(e))
        self.conn.commit()
        
    def set_param(self):
        self.set_url()

    def set_url(self):
        #행정동 기준으로 url설정
        self.url_result = self.url+self.operation+\
                        '?ServiceKey=' \
                        + self.key + self.data_type

class middleUpjongList(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO middleUpjongList (indsLclsCd,indsLclsNm,indsMclsCd,indsMclsNm,stdrDt) \
            values (%s,%s,%s,%s,%s)"   
        self.operation = 'middleUpjongList'
        
    def data_load(self):
        self.set_param()
        super().read_data()
        for item in self.data:
            val = (item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],item['indsMclsNm'],item['stdrDt'])                 
            try:
                self.cur.execute(self.sql,val)                
            except Exception as e:
                print(str(e))
        self.conn.commit()
        
    def set_param(self):
        self.set_url()

    def set_url(self):
        #행정동 기준으로 url설정
        self.url_result = self.url+self.operation+\
                        '?ServiceKey=' \
                        + self.key + self.data_type


class smallUpjongList(setup):
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO smallUpjongList (indsLclsCd,indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,stdrDt) \
            values (%s,%s,%s,%s,%s,%s,%s)"  
        self.operation = 'smallUpjongList'
        
    def data_load(self):
        self.set_param()
        super().read_data()
        for item in self.data:
            val = (item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],item['stdrDt'])                 
            try:
                self.cur.execute(self.sql,val)                
            except Exception as e:
                print(str(e))
        self.conn.commit()
        
    def set_param(self):
        self.set_url()

    def set_url(self):
        #행정동 기준으로 url설정
        self.url_result = self.url+self.operation+\
                        '?ServiceKey=' \
                        + self.key + self.data_type


