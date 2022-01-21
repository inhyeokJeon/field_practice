import logging
from urllib.parse import quote_plus, urlencode

from setup import *


class InfoDetail(setup):
    """
    setup 클래스를 상속받는다.
    """
    def __init__(self):
        super().__init__()

    def set_url(self, CLTR_NO: str, PBCT_NO: str) -> None:
        """
        API요청에 필요한 url을 설정해준다.
        :param CTGR_HIRK_ID: CTGR_HIRK_ID를 url parameter에 추가
        :param pageNo: pageNo를 url parameter 에 추가
        :return: None
        """
        queryParams = f'?{quote_plus("serviceKey")}={self.key}&' + urlencode({
                                                                quote_plus('CLTR_NO'):CLTR_NO,
                                                                quote_plus('PBCT_NO'):PBCT_NO
        })
        self.url_result = self.url + queryParams

    def get_CLTR_NO_from_self(self) -> str:
        """
        작업중인 테이블의 가장큰 CLTR_NO 를 가져와 리턴한다.
        :return: 작업중인 테이블의 가장큰 CLTR_NO
        """
        sql = "SELECT MAX(CLTR_NO) FROM %(tableName)s"
        try:
            self.cur.execute(sql % {"tableName": self.tableName})
            item = self.cur.fetchall()
            Max_CLTR_NO = item[0]['MAX(CLTR_NO)']

        except Exception as e:  # 오류발생.
            print(str(e))
            logging.warning("error get_CLTR_NO_from_self")
            sys.exit()

        if not Max_CLTR_NO:  # 데이터베이스가 비워져 있음.
            print("INSERT INTO EMPTY TABLE")
            return '0'

        return Max_CLTR_NO

    def get_number_from_UnifyUsageCltr(self) -> list:
        """
        통합용도별물건목록조회로부터 물건번호 공매번호 가져오기
        :return: [물건번호, 공매번호] list
        """
        sql = "SELECT CLTR_NO ,PBCT_NO FROM onbid.ONBID_UnifyUsageCltr_2 group by CLTR_NO,PBCT_NO order by CLTR_NO"
        try:
            self.cur.execute(sql)
            PB_CL_No = self.cur.fetchall()

        except Exception as e:
            print("Error")
            print(str(e))

        return PB_CL_No

    def COMPARE_TEMPLATE(self, dict_item: dict, CLTR_NO : str, PBCT_NO:str) -> dict:
        """
        api요청 template 과 비교하여 data 비교를 저장.
        :param dict_item: API요청으로부터 받아온 data dictionary
        :param CTGR_HIRK_ID:  요청값으로 주고있는 물건관리번호
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
            dict_template_copy['CLTR_NO'] =CLTR_NO
            dict_template_copy['PBCT_NO'] =PBCT_NO

        except Exception as e:
            print(str(e))
            print("No keys error from COMPARE_TEMPLATE")
        return dict_template_copy

    def start(self):
        # 작업중인 테이블의 가장큰 CLTR_NO값 받아오기
        MAX_CLTR_NO = self.get_CLTR_NO_from_self()
        # [물건번호, 공매번호] list 가져오기
        number_dict_list = self.get_number_from_UnifyUsageCltr()
        # api 요청하고 응답값을 database 적재
        self.request_api_and_insert_into_db(number_dict_list,MAX_CLTR_NO)