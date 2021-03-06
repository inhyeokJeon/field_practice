import pymysql
import requests
from urllib.parse import quote_plus, urlencode
import csv
from datetime import datetime, timedelta
from threading import Thread
import time
import mmap
from tqdm import tqdm

class setup:
    def __init__(self):
        self.url = "http://apis.data.go.kr/B553077/api/open/sdsc/"
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        self.url_result = ""
        self.connection()
        self.request_session = requests.Session()
    def connection(self):
        self.con = pymysql.connect(
          host='1.234.5.16',
          user='dev22',
          password='aimypie111@',
          charset='utf8',
          db='dev',
          cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def get_api_data(self):
        try:
            print(self.url_result)
            response = self.request_session.get(self.url_result)
            #response = requests.get(self.url_result)
            print(response.status_code)
        except Exception as e:
            print(e , " and try again after 3 second  get _api get error")
            #time.sleep(3)
            #response = requests.get(self.url_result)
        
        if(response.status_code == 200):
            try :
                json_object = response.json()
                return json_object['body']['items']
            except Exception as e:
                print(e , "and try again after 3 second get_api json error")
                #time.sleep(3)
                #json_object = response.json()
                #return json_object['body']['items']
        else:
            print(response.status_code)
        
        
        

    def get_db_data(self, query):
        try:
            self.cur.execute(query)            
            rows = self.cur.fetchall()
            return rows

        except Exception as e:
            print(e," and try again after 3 second  get_db")
            time.sleep(3)
            self.connection()
            self.cur.execute(query)            
            rows = self.cur.fetchall()
            return rows
            

    def set_db_data(self, sql, var):
        try:
            self.cur.execute(sql, var)
            self.con.commit()

        except Exception as e:
            print(e)

    def get_num_lines(self,file_path):
        fp = open(file_path, "r")
        rdr = csv.reader(fp)
        lines = len(list(rdr))
        return lines

class storeZoneOne(setup): # 1. ?????? ????????????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeZoneOne \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s)"

    def set_url(self):
        queryParams = f'storeZoneOne?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        self.set_url()

        for item in super().get_api_data():
            print(item)
            var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'],
                   item['signguCd'], item['signguNm'], item['trarArea'], item['coordNum'], item['coords'], item['stdrDt'])

            self.set_db_data(self.sql, var)


class storeZoneInRadius(setup): # 2. ????????? ????????????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeZoneInRadiusAddxy \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt, x, y, radius)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s,%s,%s,%s)"

    def set_url(self, cx, cy):
        queryParams = f'storeZoneInRadius?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('radius'): 1000, #????????? 1000m
            quote_plus('cx'): cx,
            quote_plus('cy'): cy,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams
    '''
    ???????????????
    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')
        count = 1
        rdr = csv.reader(f)
        
        for line in rdr:
            print(count)
            if line[0] != 'cx':
                cx = line[0]
                cy = line[1]
                self.set_url(cx, cy)
                for item in super().get_api_data():
                    var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'],
                           item['signguCd'], item['signguNm'], item['trarArea'], item['coordNum'], item['coords'], item['stdrDt'], cx, cy, 1000)

                    self.set_db_data(self.sql, var)
            count+=1
        f.close()
        #bar.finish()
    '''
    def start(self):
        with open(self.filepath) as file:
            for lines in tqdm(file, total = self.get_num_lines(self.filepath)):
                lines = lines.replace('\n','')
                line = lines.split(',')
                if line[0] != 'cx':
                    cx = line[0]
                    cy = line[1]
                    self.set_url(cx, cy)
                    for item in super().get_api_data():
                        var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'],
                            item['signguCd'], item['signguNm'], item['trarArea'], item['coordNum'], item['coords'], item['stdrDt'], cx, cy, 1000)

                        self.set_db_data(self.sql, var)
             

class storeZoneInRectangle(setup): # 3. ????????? ??? ?????? ??????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeZoneInRectangle \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s)"
        
        #?????? ???????????? 0.003(??????333m) ????????? ???????????? ????????????. 
        self.size = 0.003

    def set_url(self, minx, miny, maxx, maxy):
        queryParams = f'storeZoneInRectangle?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('minx'): minx,
            quote_plus('miny'): miny,
            quote_plus('maxx'): maxx,
            quote_plus('maxy'): maxy,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        with open(self.filepath) as file:
            for lines in tqdm(file, total = self.get_num_lines(self.filepath)):
                lines = lines.replace('\n','')
                line = lines.split(',')
                if line[0] != 'cx':
                    #??????????????? ???????????? ???????????? ?????? ?????? ??? 666???????????? ???????????? ??????????????????.
                    minx = float(line[0])-self.size
                    miny = float(line[1])-self.size
                    maxx = float(line[0])+-self.size
                    maxy = float(line[1])+-self.size
                    self.set_url(minx, miny, maxx, maxy)
                
                    for item in super().get_api_data():
                        var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'],
                            item['signguCd'], item['signguNm'], item['trarArea'], item['coordNum'], item['coords'],
                            item['stdrDt'])
                    
                        self.set_db_data(self.sql, var)
    '''
    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')
        rdr2 = csv.reader(f)
        for line in rdr:
            bar.next()
            if line[0] != 'cx':
                #??????????????? ???????????? ???????????? ?????? ?????? ??? 666???????????? ???????????? ??????????????????.
                minx = float(line[0])-self.size
                miny = float(line[1])-self.size
                maxx = float(line[0])+-self.size
                maxy = float(line[1])+-self.size
                self.set_url(minx, miny, maxx, maxy)
                
                for item in super().get_api_data():
                    var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'],
                           item['signguCd'], item['signguNm'], item['trarArea'], item['coordNum'], item['coords'],
                           item['stdrDt'])
                
                    self.set_db_data(self.sql, var)
            count+=1
        f.close()
    '''
        

    

class storeZoneInAdmi(setup): # 4. ???????????? ?????? ????????????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeZoneInAdmi \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt, adongCd)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s,%s)"

    def set_url(self, key):
        queryParams = f'storeZoneInAdmi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('divId'): 'adongCd',
            quote_plus('key'): key,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        #????????? ?????????????????? ?????????????????? ????????? url??? ????????????.
        for row in super().get_db_data('SELECT adongCd FROM aDong'):
            print(row)
            self.set_url(row['adongCd'])

            for item in super().get_api_data():
                print(item)
                var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'], item['signguCd'],
                       item['signguNm'], item['trarArea'], item['coordNum'], item['coords'], item['stdrDt'], row['adongCd'])

                self.set_db_data(self.sql, var)


class storeOne(setup): #5. ?????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeOne (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

    def start(self):
        #?????????????????? ?????????????????? ????????????????????? ????????? url??? ????????????.

        for row in super().get_db_data('SELECT bizesId FROM bizesId where bizesId >10158708'):
            print(row)
            self.set_url(row['bizesId'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)
    
    def set_url(self, key):
        queryParams = f'storeOne?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams


class storeListInBuilding(setup): #6. ?????? ?????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInBuilding (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

    def set_url(self, key):
        queryParams = f'storeListInBuilding?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        #?????????????????? ?????????????????? ????????????????????? ????????? url??? ????????????.
        for row in super().get_db_data('SELECT bldMngNo FROM bldMngNo'):
            print(row)
            self.set_url(row['bldMngNo'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)
    
    
class storeListInPnu(setup): #7. ?????? ?????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInPnu (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

    def set_url(self, key):
        queryParams = f'storeListInPnu?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        ##???????????? ?????????????????? ??????????????? ????????? url??? ????????????.
        for row in super().get_db_data('SELECT lnoCd FROM lnoCd'):
            print(row)
            self.set_url(row['lnoCd'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)
    
    
class storeListInDong(setup): #8. ????????? ?????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInDong (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self, key):
        queryParams = f'storeListInDong?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('divId'): 'adongCd',
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    #Adong table ??? ?????? data??? ????????? parmameter??? ????????? url??? ???????????? db ??? ????????????.
    def start(self):
        for row in super().get_db_data('SELECT adongCd FROM aDong'):
            print(row)
            self.set_url(row['adongCd'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)


class storeListInArea(setup): #9 ????????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInArea (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat,trarNo) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    
    def set_url(self,key):
        queryParams = f'storeListInArea?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        #????????? ??????????????? ??????????????? ?????????????????? ??????????????? ????????? url??? ????????????.
        for row in super().get_db_data('SELECT trarNo FROM trarNo_coords'):
            print(row)
            self.set_url(row['trarNo'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
                    item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],\
                    item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],\
                    item['ksicCd'],item['ksicNm'],item['ctprvnCd'],item['ctprvnNm'],\
                    item['signguCd'],item['signguNm'],item['adongCd'],item['adongNm'],\
                    item['ldongCd'],item['ldongNm'],item['lnoCd'],item['plotSctCd'],\
                    item['plotSctNm'],item['lnoMnno'],item['lnoSlno'],item['lnoAdr'],\
                    item['rdnmCd'],item['rdnm'],item['bldMnno'],item['bldSlno'],\
                    item['bldMngNo'],item['bldNm'],item['rdnmAdr'],item['oldZipcd'],\
                    item['newZipcd'],item['dongNo'],item['flrNo'],item['hoNo'],\
                    item['lon'],item['lat'],row['trarNo'])

                self.set_db_data(self.sql, var)
    
    
class storeListInRadius(setup): #10 ????????? ???????????? ??????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeListInRadius (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

    def set_url(self, cx, cy):
        queryParams = f'storeListInRadius?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('radius'): 1000, #?????? 1km
            quote_plus('cx'): cx,
            quote_plus('cy'): cy,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            if line[0] != 'cx':
                cx = line[0]
                cy = line[1]
                self.set_url(cx, cy)

                for item in super().get_api_data():
                    var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                    self.set_db_data(self.sql, var)
        f.close()


class storeListInRectangle(setup): # 11. ???????????? ???????????? ??????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeListInRectangle (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        
        #?????? ???????????? 0.003(??????333m) ????????? ???????????? ????????????.
        self.size = 0.03

    def set_url(self, minx, miny, maxx, maxy):
        queryParams = f'storeListInRectangle?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('minx'): minx,
            quote_plus('miny'): miny,
            quote_plus('maxx'): maxx,
            quote_plus('maxy'): maxy,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')

        rdr = csv.reader(f)

        for line in rdr:
            if line[0] != 'minx':
                #??????????????? ???????????? ???????????? ?????? ?????? ??? 666???????????? ???????????? ??????????????????.
                minx = line[0]-self.size
                miny = line[1]-self.size
                maxx = line[0]+-self.size
                maxy = line[1]+-self.size
                self.set_url(minx, miny, maxx, maxy)

                for item in super().get_api_data():
                    var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                    self.set_db_data(self.sql, var)
        f.close()


class storeListInPolygon(setup): #12. ???????????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInPolygon (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    
    def set_url(self,key):
        queryParams = f'storeListInPolygon?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        #trarNo_coords ???????????? coords?????? ????????? url??? ???????????????.
        for row in super().get_db_data('SELECT ST_AsText(coords) FROM trarNo_coords'):
            self.set_url(row['ST_AsText(coords)'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)


class storeListInUpjong(setup): #13. ????????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListInUpjong (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    
    def set_url(self,key):
        queryParams = f'storeListInUpjong?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('divId'): 'indsLclsCd',
            quote_plus('key'): key,
            quote_plus('numOfRows'): 1000,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        #????????? ????????? ????????? ????????? ??????????????????
        for row in super().get_db_data('SELECT indsLclsCd FROM largeUpjongList where indsLclsCd ="R"'):
            self.set_url(row['indsLclsCd'])
            print(row['indsLclsCd'])

            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
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

                self.set_db_data(self.sql, var)

#2015??? 12??? 18??? ???????????? ??????????????? ??????,??????,?????? ??? ??????????????? db??? ????????????.
class storeListByDate(setup): #14. ?????????????????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListByDate (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat,chgGb,chgDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        #???????????? ??????    
        self.start_date = datetime(2018,7,26)
        self.day = (datetime.today()-self.start_date).days
    
    def set_url(self,key):
        queryParams = f'storeListByDate?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        for row in range(self.day):
            #res??? ????????????????????? ???????????????
            res = (self.start_date+ timedelta(days=row)).strftime('%Y%m%d')
            self.set_url(res)
            print(res)
            for item in super().get_api_data():
                var = (item['bizesId'],item['bizesNm'],item['brchNm'],\
                    item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],\
                    item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],\
                    item['ksicCd'],item['ksicNm'],item['ctprvnCd'],item['ctprvnNm'],\
                    item['signguCd'],item['signguNm'],item['adongCd'],item['adongNm'],\
                    item['ldongCd'],item['ldongNm'],item['lnoCd'],item['plotSctCd'],\
                    item['plotSctNm'],item['lnoMnno'],item['lnoSlno'],item['lnoAdr'],\
                    item['rdnmCd'],item['rdnm'],item['bldMnno'],item['bldSlno'],\
                    item['bldMngNo'],item['bldNm'],item['rdnmAdr'],item['oldZipcd'],\
                    item['newZipcd'],item['dongNo'],item['flrNo'],item['hoNo'],\
                    item['lon'],item['lat'],item['chgGb'],item['chgDt'])
                
                self.set_db_data(self.sql, var)
''' ??????????????? ??????????????? ????????????.
class reqStoreModify(setup): #15. ?????????????????? ????????????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO reqStoreModify (bizesId,result,message) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    
'''


class storeStatsUpjongInAdmi(setup): # 16. ??????????????? ????????? ???????????? ??????
    def __init__(self, newDivID):
        super().__init__()
        self.sql = "INSERT INTO storeStatsUpjongInAdmiAddDividKey \
                    (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd, indsSclsNm, statCnt, divID, Cd)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.divId = newDivID

    def set_url(self, Cd):
        queryParams = f'storeStatsUpjongInAdmi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('divId'): self.divId,
            quote_plus('key'): Cd,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    #????????? ,??????, ???????????? ????????? ????????????.
    def start(self):
        if self.divId == 'ctprvnCd':
            rows = super().get_db_data('SELECT ctprvnCd FROM siDo')
        elif self.divId == 'signguCd':
            rows = super().get_db_data('SELECT signguCd FROM siGnGu')
        else:
            rows = super().get_db_data('SELECT adongCd FROM aDong')

        for row in rows:
            print(row)
            if self.divId == 'ctprvnCd':
                Cd = row['ctprvnCd']
            elif self.divId == 'signguCd':
                Cd = row['signguCd']
            else:
                Cd = row['adongCd']

            self.set_url(Cd)

            for item in super().get_api_data():
                var = (item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'],
                       item['indsSclsCd'], item['indsSclsNm'], item['statCnt'], self.divId, Cd)

                self.set_db_data(self.sql, var)


class storeStatsUpjongInBuilding(setup): # 17. ????????? ????????? ???????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeStatsUpjongInBuilding \
                    (bldMngNo, indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd, indsSclsNm, statCnt)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self, bldMngNo):
        queryParams = f'storeStatsUpjongInBuilding?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): bldMngNo,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        ##???????????? ?????????????????? ??????????????? ????????? url??? ????????????.    
        for row in super().get_db_data('SELECT bldMngNo FROM bldMngNo where bldMngNo>=2826010600107990016000001'):
            print(row)
            self.set_url(row['bldMngNo'])

            for item in super().get_api_data():
                var = (row['bldMngNo'],item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'],
                       item['indsSclsCd'], item['indsSclsNm'], item['statCnt'])

                self.set_db_data(self.sql, var)


class storeStatsUpjongInRadius(setup):  # 18. ????????? ????????? ???????????? ??????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeStatsUpjongInRadiusAddxy \
                    (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd, indsSclsNm, statCnt, cx, cy, radius)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self, cx, cy):
        queryParams = f'storeStatsUpjongInRadius?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('radius'): 1000, #?????? 1km
            quote_plus('cx'): cx,
            quote_plus('cy'): cy,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')

        rdr = csv.reader(f)

        for line in rdr:
            if line[0] != 'cx':
                cx = line[0]
                cy = line[1]
                self.set_url(cx, cy)

                for item in super().get_api_data():
                    print(item)
                    var = (item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'],
                            item['indsSclsCd'], item['indsSclsNm'], item['statCnt'], cx, cy, 1000)

                    self.set_db_data(self.sql, var)
        f.close()


class storeStatsUpjongInRectangle(setup):  # 19. ????????? ??? ????????? ???????????? ??????
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeStatsUpjongInRectangleAddxy \
                    (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd,\
                     indsSclsNm, statCnt, minx, miny, maxx, maxy)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #?????? ???????????? 0.003(??????333m) ????????? ???????????? ????????????. 
        self.size = 0.003

    def set_url(self, minx, miny, maxx, maxy):
        queryParams = f'storeStatsUpjongInRectangle?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('minx'): minx,
            quote_plus('miny'): miny,
            quote_plus('maxx'): maxx,
            quote_plus('maxy'): maxy,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        f = open(self.filepath, 'r', encoding='utf-8')
        count =1
        rdr = csv.reader(f)

        for line in rdr:
            if line[0] != 'cx':
                print(count)
                minx = float(line[0]) - self.size
                miny = float(line[1]) - self.size
                maxx = float(line[0]) + self.size
                maxy = float(line[1]) + self.size
                self.set_url(minx, miny, maxx, maxy)

                for item in super().get_api_data():
                    var = (item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'],
                            item['indsSclsCd'], item['indsSclsNm'], item['statCnt'], minx, miny, maxx, maxy)

                    self.set_db_data(self.sql, var)
                count += 1
        f.close()

class storeStatsUpjongInPolygon(setup): #20. ???????????? ?????????????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeStatsUpjongInPolygon (indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,statCnt) \
                values (%s,%s,%s,%s,%s,%s,%s)" 
    
    def set_url(self,key):
        queryParams = f'storeStatsUpjongInPolygon?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('type'): 'json'})
        
        self.url_result = self.url + queryParams

    def start(self):
        #????????? ?????????????????? ???????????? ????????? url??? ????????????.
        for row in super().get_db_data('SELECT ST_AsText(coords) FROM trarNo_coords'):
            self.set_url(row['ST_AsText(coords)'])

            for item in super().get_api_data():
                var = (item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],\
                    item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],item['statCnt'])

                self.set_db_data(self.sql, var)


class largeUpjongList(setup): # 21. ???????????? ?????? ????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO largeUpjongList (indsLclsCd, indsLclsNm, stdrDt) values (%s,%s,%s)"

    def set_url(self):
        queryParams = f'largeUpjongList?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        self.set_url()

        for item in super().get_api_data():
            print(item)
            var = (item['indsLclsCd'], item['indsLclsNm'], item['stdrDt'])

            self.set_db_data(self.sql, var)


class middleUpjongList(setup): # 22. ???????????? ?????? ????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO middleUpjongList (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, stdrDt)\
                    values (%s,%s,%s,%s,%s)"

    def set_url(self):
        queryParams = f'middleUpjongList?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        self.set_url()

        for item in super().get_api_data():
            print(item)
            var = (item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'], item['stdrDt'])

            self.set_db_data(self.sql, var)


class smallUpjongList(setup): # 23. ???????????? ?????? ????????? ?????? 
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO smallUpjongList (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd, indsSclsNm, stdrDt)\
                    values (%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self):
        queryParams = f'smallUpjongList?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        self.set_url()

        for item in super().get_api_data():
            print(item)
            var = (item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'], item['indsSclsCd'], item['indsSclsNm'], item['stdrDt'])

            self.set_db_data(self.sql, var)


class siDo(setup): # 24. ?????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO siDo (ctprvnCd, ctprvnNm, stdrDt) values (%s,%s,%s)"

    def set_url(self):
        queryParams = f'baroApi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('resId'): 'dong',
            quote_plus('catId'): 'mega',
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):
        self.set_url()

        for item in super().get_api_data():
            print(item)
            var = (item['ctprvnCd'], item['ctprvnNm'], item['stdrDt'])

            self.set_db_data(self.sql, var)


class siGnGu(setup): # 25. ????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO siGnGu (signguCd,signguNm,ctprvnCd, ctprvnNm, stdrDt) values (%s,%s,%s,%s,%s)"

    def set_url(self, newCtprvnCd):
        queryParams = f'baroApi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('resId'): 'dong',
            quote_plus('catId'): 'cty',
            quote_plus('ctprvnCd'): newCtprvnCd,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):

        for row in super().get_db_data('SELECT ctprvnCd FROM siDo'):
            print(row)
            self.set_url(row['ctprvnCd'])

            for item in super().get_api_data():
                print(item)
                var = (item['signguCd'], item['signguCd'], item['ctprvnCd'], item['ctprvnNm'], item['stdrDt'])
                self.set_db_data(self.sql, var)


class aDong(setup): # 26. ????????? ??????

    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO aDong (adongCd,adongNm,signguCd,signguNm,ctprvnCd, ctprvnNm, stdrDt) \
            values (%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self,newSignguCd):
        queryParams = f'baroApi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('resId'): 'dong',
            quote_plus('catId'): 'admi',
            quote_plus('signguCd'): newSignguCd,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):

        for row in super().get_db_data('SELECT signguCd FROM siGnGu'):
            print(row)
            self.set_url(row['signguCd'])

            for item in super().get_api_data():
                print(item)
                var = (item['adongCd'], item['adongNm'], item['signguCd'], \
                       item['signguNm'], item['ctprvnCd'], item['ctprvnNm'], item['stdrDt'])

                self.set_db_data(self.sql, var)


class lDong(setup): # 27. ????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO lDong (ldongCd,ldongNm,signguCd,signguNm,ctprvnCd, ctprvnNm, stdrDt) \
            values (%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self, newSignguCd):
        queryParams = f'baroApi?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('resId'): 'dong',
            quote_plus('catId'): 'zone',
            quote_plus('signguCd'): newSignguCd,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams

    def start(self):

        for row in super().get_db_data('SELECT signguCd FROM siGnGu'):
            print(row)
            self.set_url(row['signguCd'])

            for item in super().get_api_data():
                print(item)
                var = (item['ldongCd'], item['ldongNm'], item['signguCd'], \
                       item['signguNm'], item['ctprvnCd'], item['ctprvnNm'], item['stdrDt'])

                self.set_db_data(self.sql, var)

class bizesId(setup): # 28. ?????????????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO bizesId (bizesId) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT bizesId FROM storeListInDong'):
            print(row['bizesId'])
            self.set_db_data(self.sql, row['bizesId'])


class lnoCd(setup): # 29. PNU?????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO lnoCd (lnoCd) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT lnoCd FROM storeListInDong'):
            print(row['lnoCd'])
            self.set_db_data(self.sql, row['lnoCd'])


class bldMngNo(setup): # 30. ?????????????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO bldMngNo (bldMngNo) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT bldMngNo FROM storeListInDong'):
            print(row['bldMngNo'])
            self.set_db_data(self.sql, row['bldMngNo'])


class trarNo(setup): # 31. ???????????? and ????????? ??????
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO trarNo_coords (trarNo,coords) values (%s,%s)"

    def start(self):
        for row in super().get_db_data('SELECT trarNo, coords FROM storeZoneOne'):
            print(row['trarNo'])
            var = (row['trarNo'],row['coords'])
            self.set_db_data(self.sql, var)
