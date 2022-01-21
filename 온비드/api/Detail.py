import collections
import hashlib

from tqdm import tqdm

from InfoDetail import *


class Detail(InfoDetail):
    """
    InfoDetail 을 상속받음
    """
    def __init__(self):
        super().__init__()
    def request_api_and_insert_into_db(self, number_dict_list : list, MAX_CLTR_NO :str) -> None:
        """
        [CLTR_NO, PBCT_NO]를 이용해 page를 증가하며 요청하여 db에 적재한다.
        :param number_dict_list:  CLTR_NO(물건번호) 와 PBCT_NO(공매번호) 를 값으로 가진 리스트
        :param MAX_CLTR_NO: 작업할 테이블의 가장큰 CLTR_NO 값
        :return: None
        """

        # 물건번호와 공매번호로 이루어진 리스트를 돌면서 실행
        for items in tqdm(number_dict_list, total= len(number_dict_list)):
            # 테이블의 저장된 값중 가장큰 CLTR_NO값과 비교해 이미저장된 값들에대해서는 skip
            if(items['CLTR_NO'] < str(MAX_CLTR_NO)):
                continue
            pageNo = 1
            CLTR_NO: str = items['CLTR_NO']
            PBCT_NO: str = items['PBCT_NO']
            self.total = 0
            # pageNo 를 증가시키면서 반복한다.
            while(True):
                print(pageNo)
                #set url
                self.set_url(CLTR_NO, PBCT_NO, pageNo)
                #API요청 데이터
                api_data = self.GET_DATA_FROM_API()

                # 응답 값이 존재하지 않을 때 break.
                if (api_data == -1 or api_data == None):
                    print("Nodata")
                    break

                # api 응답값이 하나일떄
                if(type(api_data) == collections.OrderedDict):
                    # 템플릿과 비교해서 템플릿 형식으로 리턴
                    DATA_FINAL = self.COMPARE_TEMPLATE(api_data, CLTR_NO, PBCT_NO)
                    #템플릿형식 DB저장
                    self.STORE_DATA_INTO_TABLE(DATA_FINAL)
                    break

                # api 응답값이 여러개일때
                for data in api_data:
                    # 템플릿과 비교해서 템플릿 형식으로 리턴
                    DATA_FINAL = self.COMPARE_TEMPLATE(data, CLTR_NO, PBCT_NO)
                    # 템플릿형식 DB저장
                    self.STORE_DATA_INTO_TABLE(DATA_FINAL)

                if(self.total <= 100*pageNo):
                    break
                pageNo = pageNo + 1

    def set_value(self, test_1: dict) -> tuple:
        """
        중복을 없애기 위해 테이블의 모든 column 을 hashing 해 table hash column 에 저장
        :param test_1: 하나의 dictionary
        :return: dictionary를 tuple형태로 리턴
        """
        h = hashlib.sha1()
        temp_list : list = []
        for item in self.dict_template.keys():
            temp_list.append(test_1[item])
            h.update(test_1[item].encode())
        temp_list.append(h.hexdigest())
        return tuple(temp_list)

    def set_url(self, CLTR_NO: str, PBCT_NO: str, pageNo: int):
        """
        :param CTGR_HIRK_ID: CTGR_HIRK_ID를 url parameter에 추가
        :param pageNo: pageNo를 url parameter 에 추가
        :return: None
        """
        queryParams = f'?{quote_plus("serviceKey")}={self.key}&' + urlencode({
                                                                quote_plus('CLTR_NO'):CLTR_NO,
                                                                quote_plus('PBCT_NO'):PBCT_NO,
                                                                quote_plus('numOfRows'): 100,
                                                                quote_plus('pageNo'): pageNo})
        self.url_result = self.url + queryParams
