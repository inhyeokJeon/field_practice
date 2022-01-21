import collections
from urllib.parse import quote_plus, urlencode

from tqdm import tqdm
from setup import *

class KamcoPlnmPbctBasicInfoDetail(setup):
    def __init__(self):
        super().__init__()
        self.tableName = "KamcoPlnmPbctBasicInfoDetail"
        self.url_result = ""
        self.item_Value = -1
        self.url = "http://openapi.onbid.co.kr/openapi/services/KamcoPblsalThingInquireSvc/getKamcoPlnmPbctBasicInfoDetail"
        self.dict_template = {
            'PLNM_NO' : "",
            'PBCT_NO' : "",
            'PLNM_NM' : "",
            'ORG_NM' : "",
            'RSBY_DEPT' : "",
            'PSCG_NM' : "",
            'PSCG_TPNO' : "",
            'PSCG_EMAL_ADRS' : "",
            'PLNM_KIND_NM' : "",
            'PLNM_DT' : "",
            'PLNM_YR' : "",
            'PLNM_SEQ' : "",
            'PRPT_DVSN_NM' : "",
            'AST_DVSN_CD' : "",
            'PLNM_MNMT_NO' : "",
            'ORG_PLNM_NO' : "",
            'RLTN_PLNM_NO' : "",
            'RLTN_PLNM_TITL' : "",
            'BID_MTD_NM' : "",
            'DPSL_MTD_NM' : "",
            'CPTN_MTD_NM' : "",
            'TOT_AMT_UNPC_DVSN_NM' : "",
            'PTCT_QLFC' : "",
            'RBD_YN' : "",
            'COMN_BID_PMSN_YN' : "",
            'SUBT_BID_PMSN_YN' : "",
            'PLNM_DOC' : "",
            'bidDateInfosTotalCount' : "",
            'filesTotalCount' : ""
        }
        # 2 7 7 6 7
        self.sql = "insert into KamcoPlnmPbctBasicInfoDetail (PLNM_NO, PBCT_NO, " \
                   "PLNM_NM, ORG_NM, RSBY_DEPT, PSCG_NM, PSCG_TPNO, PSCG_EMAL_ADRS, PLNM_KIND_NM, " \
                   "PLNM_DT, PLNM_YR, PLNM_SEQ, PRPT_DVSN_NM, AST_DVSN_CD, PLNM_MNMT_NO, ORG_PLNM_NO, " \
                   "RLTN_PLNM_NO, RLTN_PLNM_TITL, BID_MTD_NM, DPSL_MTD_NM, CPTN_MTD_NM, TOT_AMT_UNPC_DVSN_NM, " \
                   "PTCT_QLFC, RBD_YN, COMN_BID_PMSN_YN, SUBT_BID_PMSN_YN, PLNM_DOC, bidDateInfosTotalCount, filesTotalCount) " \
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def request_api_and_insert_into_db(self, number_dict_list) -> None:
        for items in tqdm(number_dict_list, total= len(number_dict_list)):
            PLNM_NO = items['PLNM_NO']
            PBCT_NO = items['PBCT_NO']
            self.set_url(PLNM_NO, PBCT_NO)
            api_data = self.GET_DATA_FROM_API()
            if(api_data == -1):
                continue
            result_template = self.COMPARE_TEMPLATE(api_data,PLNM_NO,PBCT_NO)
            self.STORE_DATA_INTO_TABLE(result_template)

    def COMPARE_TEMPLATE(self, dict_item: dict, PLNM_NO : str, PBCT_NO:str) -> dict:

        dict_template_copy: dict = self.dict_template.copy()

        try:
            for key in dict_item.keys():
                #api 로 받은 key 값에 대해서
                if dict_item[str(key)] == None:
                    continue
                if dict_item[str(key)] == 'RNUM':
                    continue
                dict_template_copy[str(key)] = dict_item[str(key)]
            dict_template_copy['PLNM_NO'] =PLNM_NO
            dict_template_copy['PBCT_NO'] =PBCT_NO

        except Exception as e:
            print(str(e))
            print("No keys error from COMPARE_TEMPLATE")
        return dict_template_copy

    def set_url(self, PLNM_NO: str, PBCT_NO: str):
        """
        :param CTGR_HIRK_ID: CTGR_HIRK_ID를 url parameter에 추가
        :param pageNo: pageNo를 url parameter 에 추가
        :return: None
        """
        queryParams = f'?{quote_plus("serviceKey")}={self.key}&' + urlencode({
                                                                quote_plus('PLNM_NO'):PLNM_NO,
                                                                quote_plus('PBCT_NO'):PBCT_NO})
        self.url_result = self.url + queryParams

    def set_value(self, test_1):
        """
        :param test_1: 하나의 dictionary
        :return: dictionary를 tuple형태로 리턴
        """
        temp_list = []
        for i in self.dict_template.keys():
            temp_list.append(test_1[i])
        return tuple(temp_list)

    def get_number_from_UnifyUsageCltr(self) -> list:
        """
        통합용도별물건목록조회로부터 물건번호 공매번호 가져오기
        :return: [PLNM_NO, 공매번호] list
        """
        sql = "SELECT PLNM_NO ,PBCT_NO FROM onbid.ONBID_UnifyUsageCltr_2 group by PLNM_NO,PBCT_NO order by PLNM_NO"

        try:
            self.cur.execute(sql)
            PL_PB_No = self.cur.fetchall()

        except Exception as e:
            print("Error")
            print(str(e))

        return PL_PB_No

    def GET_DATA_FROM_API(self):
        """
        :return: API로 부터 DATA요청하고 응답데이터의 item부분만 추출한 데이터
        """
        try:
            response = Request(self.url_result)
            response.get_method = lambda: 'GET'
            response_body = urlopen(response).read()
            response_item = xmltodict.parse(response_body)

        except Exception as e:
            print(str(e))
            sys.exit("response error")

        resultCode = response_item['response']['header']['resultCode']

        if resultCode != '00': # API에러가 발생할 때
            print(response_item['response']['header']['resultMsg'])
            print()
            sys.exit("API ERROR resultCode = " + resultCode)

        if self.item_Value == -1 :
            items = response_item['response']['body']['item']
            if not items:  # 응답 값이 존재하지 않을 때.
                return -1
            return items

        #더이상 API응답값이 없을때.
        totalCount = response_item['response']['body']['totalCount']
        if totalCount == 0:
            print("no data")
            return -1

        #items 안에 값이 있을떄
        items = response_item['response']['body']['items']
        if not items:  # 응답 값이 존재하지 않을 때.
            print("no data")
            return -1

        return items[self.item_Value]

    def start(self):
        # [PLNM_NO, 공매번호] list 가져오기
        print("list 가져오기")
        number_dict_list = self.get_number_from_UnifyUsageCltr()
        print("list 가져오기끝")
        # api 요청하고 응답값을 database 적재
        print("db 적재")
        self.request_api_and_insert_into_db(number_dict_list)
        print("db적재끝")

