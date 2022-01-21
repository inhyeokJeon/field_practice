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

class storeZoneOne(setup): # 1. 지정 상권조회
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


class storeZoneInRadius(setup): # 2. 반경내 상권조회
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeZoneInRadiusAddxy \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt, x, y, radius)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s,%s,%s,%s)"

    def set_url(self, cx, cy):
        queryParams = f'storeZoneInRadius?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('radius'): 1000, #반지름 1000m
            quote_plus('cx'): cx,
            quote_plus('cy'): cy,
            quote_plus('type'): 'json'})

        self.url_result = self.url + queryParams
    '''
    오래된버전
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
             

class storeZoneInRectangle(setup): # 3. 사각형 내 상권 조회
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeZoneInRectangle \
                    (trarNo, mainTrarNm, ctprvnCd, ctprvnNm, signguCd, signguNm, trarArea, coordNum, coords, stdrDt)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,ST_GeomFromText(%s),%s)"
        
        #좌표 중심으로 0.003(대략333m) 정도로 사각형을 나타낸다. 
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
                    #엑셀파일의 좌표값을 기준으로 가로 세로 각 666미터정도 사각형을 기준으로한다.
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
                #엑셀파일의 좌표값을 기준으로 가로 세로 각 666미터정도 사각형을 기준으로한다.
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
        

    

class storeZoneInAdmi(setup): # 4. 행정구역 단위 상권조회
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
        #행정동 테이블로부터 행정동코드를 참조해 url을 설정한다.
        for row in super().get_db_data('SELECT adongCd FROM aDong'):
            print(row)
            self.set_url(row['adongCd'])

            for item in super().get_api_data():
                print(item)
                var = (item['trarNo'], item['mainTrarNm'], item['ctprvnCd'], item['ctprvnNm'], item['signguCd'],
                       item['signguNm'], item['trarArea'], item['coordNum'], item['coords'], item['stdrDt'], row['adongCd'])

                self.set_db_data(self.sql, var)


class storeOne(setup): #5. 단일 상가업소 조회
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
        #상가업소번호 테이블로부터 상가업소번호를 참조해 url을 설정한다.

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


class storeListInBuilding(setup): #6. 건물 단위 상가업소 조회
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
        #건물단위번호 테이블로부터 건물단위번호를 참조해 url을 설정한다.
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
    
    
class storeListInPnu(setup): #7. 지번 단위 상가업소 조회
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
        ##지번번호 테이블로부터 지번번호를 참조해 url을 설정한다.
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
    
    
class storeListInDong(setup): #8. 행정동 단위 상가업소 조회
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

    #Adong table 로 부터 data를 받아와 parmameter를 구하고 url을 설정하여 db 에 적재한다.
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


class storeListInArea(setup): #9 상권내 상가업소 조회
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
        #좌표와 상권번호를 저장해놓은 테이블로부터 상권번호를 참조해 url을 설정한다.
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
    
    
class storeListInRadius(setup): #10 반경내 상가업소 조회
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
            quote_plus('radius'): 1000, #반경 1km
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


class storeListInRectangle(setup): # 11. 사각형내 상가업소 조회
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
        
        #좌표 중심으로 0.003(대략333m) 정도로 사각형을 나타낸다.
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
                #엑셀파일의 좌표값을 기준으로 가로 세로 각 666미터정도 사각형을 기준으로한다.
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


class storeListInPolygon(setup): #12. 다각형내 상가업소 조회
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
        #trarNo_coords 테이블의 coords값을 뽑아서 url을 설정해준다.
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


class storeListInUpjong(setup): #13. 업종별 상가업소 조회
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
        #대분류 코드를 이용해 업종별 상가업소조회
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

#2015년 12월 18일 이후부터 오늘날까지 생성,수정,삭제 된 업소목록을 db에 적재한다.
class storeListByDate(setup): #14. 수정일자기준 상가업소 조회
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO storeListByDate (bizesId,bizesNm,brchNm,indsLclsCd,\
                indsLclsNm,indsMclsCd,indsMclsNm,indsSclsCd,indsSclsNm,ksicCd,ksicNm,\
                ctprvnCd,ctprvnNm,signguCd,signguNm,adongCd,adongNm,ldongCd,ldongNm,\
                lnoCd,plotSctCd,plotSctNm,lnoMnno,lnoSlno,lnoAdr,rdnmCd,rdnm,bldMnno,\
                bldSlno,bldMngNo,bldNm,rdnmAdr,oldZipcd,newZipcd,dongNo,flrNo,hoNo,lon,lat,chgGb,chgDt) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        #기준날짜 설정    
        self.start_date = datetime(2018,7,26)
        self.day = (datetime.today()-self.start_date).days
    
    def set_url(self,key):
        queryParams = f'storeListByDate?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('key'): key,
            quote_plus('type'): 'json'})
        self.url_result = self.url + queryParams

    def start(self):
        for row in range(self.day):
            #res는 기준날짜로부터 오늘날까지
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
''' 변경요청은 필요없을것 같습니다.
class reqStoreModify(setup): #15. 상가업소정보 변경요청
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO reqStoreModify (bizesId,result,message) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    
'''


class storeStatsUpjongInAdmi(setup): # 16. 행정구역내 업종별 상가업소 통계
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

    #시군구 ,시도, 행정동을 선택해 조회한다.
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


class storeStatsUpjongInBuilding(setup): # 17. 건물내 업종별 상가업소 통계
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
        ##건물번호 테이블로부터 건물번호를 참조해 url을 설정한다.    
        for row in super().get_db_data('SELECT bldMngNo FROM bldMngNo where bldMngNo>=2826010600107990016000001'):
            print(row)
            self.set_url(row['bldMngNo'])

            for item in super().get_api_data():
                var = (row['bldMngNo'],item['indsLclsCd'], item['indsLclsNm'], item['indsMclsCd'], item['indsMclsNm'],
                       item['indsSclsCd'], item['indsSclsNm'], item['statCnt'])

                self.set_db_data(self.sql, var)


class storeStatsUpjongInRadius(setup):  # 18. 반경내 업종별 상가업소 통계
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeStatsUpjongInRadiusAddxy \
                    (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd, indsSclsNm, statCnt, cx, cy, radius)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def set_url(self, cx, cy):
        queryParams = f'storeStatsUpjongInRadius?{quote_plus("ServiceKey")}={self.key}&' + urlencode({
            quote_plus('radius'): 1000, #반경 1km
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


class storeStatsUpjongInRectangle(setup):  # 19. 사각형 내 업종별 상가업소 통계
    def __init__(self, file):
        super().__init__()
        self.filepath = file
        self.sql = "INSERT INTO storeStatsUpjongInRectangleAddxy \
                    (indsLclsCd, indsLclsNm, indsMclsCd, indsMclsNm, indsSclsCd,\
                     indsSclsNm, statCnt, minx, miny, maxx, maxy)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #좌표 중심으로 0.003(대략333m) 정도로 사각형을 나타낸다. 
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

class storeStatsUpjongInPolygon(setup): #20. 다각형내 상가업소통계 조회
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
        #좌표값 테이블로부터 좌표값을 받아와 url을 설정한다.
        for row in super().get_db_data('SELECT ST_AsText(coords) FROM trarNo_coords'):
            self.set_url(row['ST_AsText(coords)'])

            for item in super().get_api_data():
                var = (item['indsLclsCd'],item['indsLclsNm'],item['indsMclsCd'],\
                    item['indsMclsNm'],item['indsSclsCd'],item['indsSclsNm'],item['statCnt'])

                self.set_db_data(self.sql, var)


class largeUpjongList(setup): # 21. 상권정보 업종 대분류 조회
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


class middleUpjongList(setup): # 22. 상권정보 업종 중분류 조회
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


class smallUpjongList(setup): # 23. 상권정보 업종 소분류 조회 
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


class siDo(setup): # 24. 시도 조회
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


class siGnGu(setup): # 25. 시군구 조회
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


class aDong(setup): # 26. 행정동 조회

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


class lDong(setup): # 27. 법정동 조회
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

class bizesId(setup): # 28. 상가업소번호 저장
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO bizesId (bizesId) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT bizesId FROM storeListInDong'):
            print(row['bizesId'])
            self.set_db_data(self.sql, row['bizesId'])


class lnoCd(setup): # 29. PNU코드 저장
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO lnoCd (lnoCd) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT lnoCd FROM storeListInDong'):
            print(row['lnoCd'])
            self.set_db_data(self.sql, row['lnoCd'])


class bldMngNo(setup): # 30. 건물관리번호 저장
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO bldMngNo (bldMngNo) values (%s)"

    def start(self):
        for row in super().get_db_data('SELECT bldMngNo FROM storeListInDong'):
            print(row['bldMngNo'])
            self.set_db_data(self.sql, row['bldMngNo'])


class trarNo(setup): # 31. 상권번호 and 좌표값 저장
    def __init__(self):
        super().__init__()
        self.sql = "INSERT INTO trarNo_coords (trarNo,coords) values (%s,%s)"

    def start(self):
        for row in super().get_db_data('SELECT trarNo, coords FROM storeZoneOne'):
            print(row['trarNo'])
            var = (row['trarNo'],row['coords'])
            self.set_db_data(self.sql, var)
