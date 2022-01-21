
import sys
from urllib.request import Request, urlopen

import pymysql
import xmltodict


class setup:
    """

    """
    def __init__(self):
        self.key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
        self.con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='onbid',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.url_result = ""
        self.total = 0

    def set_value(self, test_1):
        """
        :param test_1: 하나의 dictionary
        :return: dictionary를 tuple형태로 리턴
        """
        temp_list = []
        for i in self.dict_template.keys():
            temp_list.append(test_1[i])
        return tuple(temp_list)

    def STORE_DATA_INTO_TABLE (self, DATA):
        """
        dictionary를 tuple로 변환하고 테이블에데이터 에 적재한다.
        :param DATA: dictionary
        :return: NONE
        """
        var = self.set_value(DATA)
        try:
            self.cur.execute(self.sql, var)
            self.con.commit()
        except Exception as e:
            print("Error from STORE_DATA_INTO_TABLE")
            print(str(e))

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

        #item 안에 값이 있을떄
        if self.item_Value == -1 :
            items = response_item['response']['body']['item']
            if not items:  # 응답 값이 존재하지 않을 때.
                return -1
            return items

        #더이상 API응답값이 없을때.
        totalCount = int(response_item['response']['body']['totalCount'])
        if totalCount == 0:
            return -1
        #API요청 총 건수
        self.total = totalCount

        #item 안에 값이 있을떄
        if self.item_Value == -1 :
            items = response_item['response']['body']['item']
            if not items:  # 응답 값이 존재하지 않을 때.
                return -1
            return items



        #items 안에 값이 있을떄
        items = response_item['response']['body']['items']
        if not items:  # 응답 값이 존재하지 않을 때.
            return -1

        return items[self.item_Value]
