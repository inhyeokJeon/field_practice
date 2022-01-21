import logging
import sys
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request
import xmltodict
from tqdm import tqdm
from setup import *


class UnifyUsageCltr(setup):
    def __init__(self):
        super().__init__()
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltr"
        self.item_Value ="item"
        self.tableName = "ONBID_UnifyUsageCltr_2"
        self.dict_template = {
            "CTGR_HIRK_ID" : "",
            "PLNM_NO" : "",
            "PBCT_NO" : "",
            "ORG_BASE_NO" : "",
            "ORG_NM" : "",
            "CLTR_NO" : "",
            "PBCT_CDTN_NO" : "",
            "CLTR_HSTR_NO" : "",
            "SCRN_GRP_CD" : "",
            "CTGR_FULL_NM" : "",
            "BID_MNMT_NO" : "",
            "CLTR_NM" : "",
            "CLTR_MNMT_NO" : "",
            "LDNM_ADRS" : "",
            "NMRD_ADRS" : "",
            "ROD_NM" : "",
            "BLD_NO" : "",
            "DPSL_MTD_CD" : "",
            "DPSL_MTD_NM" : "",
            "BID_MTD_NM" : "",
            "MIN_BID_PRC" : "",
            "APSL_ASES_AVG_AMT" : "",
            "FEE_RATE" : "",
            "PBCT_BEGN_DTM" : "",
            "PBCT_CLS_DTM" : "",
            "PBCT_CLTR_STAT_NM" : "",
            "USCBD_CNT" : "",
            "IQRY_CNT" : "",
            "GOODS_NM" : "",
            "MANF" : "",
            "MDL" : "",
            "NRGT" : "",
            "GRBX" : "",
            "ENDPC" : "",
            "VHCL_MLGE" : "",
            "FUEL" : "",
            "SCRT_NM" : "",
            "TPBZ" : "",
            "ITM_NM" : "",
            "MMB_RGT_NM" : ""
        }

        self.sql = "INSERT INTO ONBID_UnifyUsageCltr_2 (CTGR_HIRK_ID, PLNM_NO, PBCT_NO, ORG_BASE_NO, \
            ORG_NM, CLTR_NO, PBCT_CDTN_NO, CLTR_HSTR_NO, SCRN_GRP_CD, CTGR_FULL_NM, BID_MNMT_NO, \
            CLTR_NM, CLTR_MNMT_NO, LDNM_ADRS, NMRD_ADRS, ROD_NM, BLD_NO, DPSL_MTD_CD, DPSL_MTD_NM, \
            BID_MTD_NM, MIN_BID_PRC, APSL_ASES_AVG_AMT, FEE_RATE, PBCT_BEGN_DTM, PBCT_CLS_DTM, \
            PBCT_CLTR_STAT_NM, USCBD_CNT, IQRY_CNT, GOODS_NM, MANF, MDL, NRGT, GRBX, ENDPC, \
            VHCL_MLGE, FUEL, SCRT_NM, TPBZ, ITM_NM, MMB_RGT_NM) VALUES (%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s)" # 40

    def set_url(self,CTGR_HIRK_ID:str,pageNo:int):
        """

        :param CTGR_HIRK_ID: CTGR_HIRK_ID를 url parameter에 추가
        :param pageNo: pageNo를 url parameter 에 추가
        :return: None
        """
        queryParams = f'?{quote_plus("serviceKey")}={self.key}&' + urlencode({
                                                                quote_plus('CTGR_HIRK_ID'):CTGR_HIRK_ID,
                                                                quote_plus('numOfRows'): 100,
                                                                quote_plus('pageNo'): pageNo})
        self.url_result = self.url + queryParams                                             

    def COMPARE_TEMPLATE(self, dict_item: dict,CTGR_HIRK_ID : str) ->dict:
        """
        :param dict_item: API요청으로부터 받아온 data dictionary
        :param CTGR_HIRK_ID:  요청값으로 주고있는 CTGR_HIRK_ID(카테고리코드)
        :return: TEMPLATE형태의 dictionary로 리턴
        """
        dict_template_copy: dict = self.dict_template.copy()
        try:
            for key in dict_item.keys():
                #api 로 받은 key 값에 대해서
                if dict_item[str(key)] == None:
                    continue
                if dict_item[str(key)] == 'RNUM':
                    continue

                dict_template_copy[str(key)] = dict_item[str(key)]
            dict_template_copy['CTGR_HIRK_ID'] =CTGR_HIRK_ID
        except Exception as e:
            print(str(e))
        return dict_template_copy

    def get_latest_db_value(self):
        """
        가장큰 CTGR_HIRK_ID를 table로 부터 가져와 리턴
        :return: Max(CTGR_HIRK_ID)
        """
        # STEP 1. 데이터베이스의 가장 큰 카테고리코드 받아옴.
        sql = "SELECT MAX(CTGR_HIRK_ID) FROM %(tableName)s"
        try:
            self.cur.execute(sql % {"tableName": self.tableName})
            item = self.cur.fetchall()
            Max_CTGR_HIRK_ID = item[0]['MAX(CTGR_HIRK_ID)']
            
        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("(STEP 1)최근값 조회 중 오류가 발생했습니다. 프로그램을 종료합니다.")
            sys.exit()

        if not Max_CTGR_HIRK_ID:  # 데이터베이스가 비워져 있음.
            print("INSERT INTO EMPTY TABLE")
            return 10000

        return Max_CTGR_HIRK_ID

    #CTGR_HIRK_ID 카테고리 리스트를 return
    def GET_CTGR_HIRK_ID_LIST(self):
        """
        ONBID_TopCodeInfo 테이블로부터 CTGR_HIRK_ID 리스트를 가져온다.
        :return: [CTGR_HIRK_ID]
        """
        print("CTGR_HIRK_ID_LIST CALCULATING...")
        sql = "SELECT CTGR_ID FROM ONBID_TopCodeInfo"
        try:
            self.cur.execute(sql)
            dict_CTGR_HIRK_ID = self.cur.fetchall()
        except Exception as e:
            print(str(e))
            sys.exit()

        list_CTGR_HIRK_ID = []

        for CTGR_HIRK_ID in dict_CTGR_HIRK_ID:
            list_CTGR_HIRK_ID.append(CTGR_HIRK_ID['CTGR_ID'])

        list_CTGR_HIRK_ID = list(set(list_CTGR_HIRK_ID))
        list_CTGR_HIRK_ID = sorted(list_CTGR_HIRK_ID)
        print("CTGR_HIRK_ID_LIST SUCCESS")
        return list_CTGR_HIRK_ID

    def request_api_and_insert_into_db(self, CTGR_HIRK_ID_LIST,Max_CTGR_HIRK_ID) ->None:
        """
        [CTGR_HIRK_ID] list 을 이용해 pageNo를 증가하며 요청하여 db에 적재한다.
        :param CTGR_HIRK_ID_LIST: [CTGR_HIRK_ID] list
        :param Max_CTGR_HIRK_ID: Max(CTGR_HIRK_ID)
        :return: None
        """
        for CTGR_HIRK_ID in tqdm(CTGR_HIRK_ID_LIST, total = len(CTGR_HIRK_ID_LIST)) :
            if int(CTGR_HIRK_ID) <= int(Max_CTGR_HIRK_ID):
                continue
            pageNo = 1
            while(True):
                print(pageNo)
                self.set_url(CTGR_HIRK_ID,pageNo)
                api_data = self.GET_DATA_FROM_API()

                if(api_data== -1 or api_data == None):
                    print("Nodata")
                    break

                for DATA in api_data:
                    #템플릿과 비교해서 템플릿 형식으로 리턴
                    DATA_FINAL = self.COMPARE_TEMPLATE(DATA, CTGR_HIRK_ID)
                    #템플릿형식 DB저장
                    self.STORE_DATA_INTO_TABLE(DATA_FINAL)

                pageNo= pageNo+1

    def start(self):
        # 작업중인 테이블의 가장큰 CTGR_HIRK_ID값 받아오기
        CTGR_HIRK_ID_LIST = self.GET_CTGR_HIRK_ID_LIST()
        # [CTGR_HIRK_ID] list 가져오기
        Max_CTGR_HIRK_ID = self.get_latest_db_value()
        # api 요청하고 응답값을 database 적재
        self.request_api_and_insert_into_db(CTGR_HIRK_ID_LIST,Max_CTGR_HIRK_ID)
        print("DONE")