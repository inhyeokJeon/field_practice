import json
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request
import xmltodict
import sys
from tqdm import tqdm
import pymysql
import logging
from InfoDetail import *

class UnifyUsageCltrBasicInfoDetail(InfoDetail):
    def __init__(self):
        super().__init__()
        self.item_Value = -1
        self.tableName = "ONBID_UnifyUsageCltrBasicInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrBasicInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'CLTR_NM' : "",
            'CTGR_TYPE_NM' : "",
            'DPSL_MTD_NM' : "",
            'PBCT_CLTR_STAT_NM' : "",
            'ORG_NM' : "",
            'RGST_DEPT_NM' : "",
            'PSCG_NM' : "",
            'PSCG_TPNO' : "",
            'LDNM_ADRS' : "",
            'NMRD_ADRS' : "",
            'CLTR_MNMT_NO' : "",
            'PRPT_DVSN_NM' : "",
            'DLGT_ORG_NM' : "",
            'CTGR_FULL_NM' : "",
            'BID_MTD_NM' : "",
            'ITEM_INFO' : "",
            'MIN_BID_PRC' : "",
            'PCMT_PYMT_EPDT_CNTN' : "",
            'BID_PRGN_NFT' : "",
            'DLVR_RSBY' : "",
            'ICDL_CDTN' : "",
            'SHR_RQR_EPRT_DT' : "",
            'totalCountEst' : "",
            'totalCountRental' : "",
            'totalCountRegi' : "",
            'totalCountBid' : "",
            'totalCountBidHis' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrBasicInfoDetail (CLTR_NO, PBCT_NO, " \
          "CLTR_NM, CTGR_TYPE_NM, DPSL_MTD_NM, PBCT_CLTR_STAT_NM, ORG_NM, RGST_DEPT_NM, PSCG_NM, " \
          "PSCG_TPNO, LDNM_ADRS, NMRD_ADRS, CLTR_MNMT_NO, PRPT_DVSN_NM, DLGT_ORG_NM, CTGR_FULL_NM, " \
          "BID_MTD_NM, ITEM_INFO, MIN_BID_PRC, PCMT_PYMT_EPDT_CNTN, BID_PRGN_NFT, DLVR_RSBY, ICDL_CDTN, " \
          "SHR_RQR_EPRT_DT, totalCountEst, totalCountRental, totalCountRegi, totalCountBid, totalCountBidHis) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #29

    def api_to_template_form(self,API_DATA,CLTR_NO,PBCT_NO) -> dict:
        """
        ?????? ??????????????? ???????????? ??????(???????????? ????????? ~ ??????????????? ???) ???
        dict ???????????? ITEM_INFO key?????? value??? ????????????.
        api???????????? template ????????? ?????? ???????????? return ??????.
        :param API_DATA: api ????????? dict
        :param CLTR_NO: ????????????
        :param PBCT_NO: ????????????
        :return: template ????????? dict
        """
        result_dict = dict.copy(self.dict_template)
        temp_dict = dict.copy(API_DATA)
        ITEM_INFO = {}
        #temp_dict ??? ???????????? ???????????? ?????????
        for item in API_DATA.keys() :
            if(temp_dict[item] != None):
                result_dict[item] = temp_dict[item]
            del temp_dict[item]
            if(item=='BID_MTD_NM'):
                break

        #temp2_dict = ?????? ????????? ?????? ????????? ???????????????
        temp2_dict = dict.copy(temp_dict)
        for item in temp_dict.keys():
            if(item=='MIN_BID_PRC'):
                break
            if(temp_dict[item] != None):
                ITEM_INFO[item] = temp_dict[item]
            del temp2_dict[item]

        for item in temp2_dict.keys():
            if(temp2_dict[item] != None):
                result_dict[item] = temp2_dict[item]

        result_dict['CLTR_NO'] = CLTR_NO
        result_dict['PBCT_NO'] = PBCT_NO
        result_dict['ITEM_INFO'] = json.dumps(ITEM_INFO)
        return result_dict

    def request_api_and_insert_into_db(self, number_dict_list) -> None:
        """
        [CLTR_NO, PBCT_NO]??? ????????? page??? ???????????? ???????????? db??? ????????????.
        :param number_dict_list:  CLTR_NO(????????????) ??? PBCT_NO(????????????) ??? ????????? ?????? ?????????
        :param MAX_CLTR_NO: ????????? ???????????? ????????? CLTR_NO ???
        :return: None
        """
        for items in tqdm(number_dict_list, total= len(number_dict_list)):
            CLTR_NO = items['CLTR_NO']
            PBCT_NO = items['PBCT_NO']
            self.set_url(CLTR_NO, PBCT_NO)
            api_data = self.GET_DATA_FROM_API()
            result_template = self.api_to_template_form(api_data,CLTR_NO,PBCT_NO)
            self.STORE_DATA_INTO_TABLE(result_template)

    def get_number_from_UnifyUsageCltr(self) -> list:
        """
        ?????????????????????????????????????????? ???????????? ???????????? ????????????
        :return: [????????????, ????????????] list
        """
        sql = "SELECT u.CLTR_NO, u.PBCT_NO FROM onbid.ONBID_UnifyUsageCltr_2 as u " \
              "where (u.CLTR_NO, u.PBCT_NO) not in (SELECT d.CLTR_NO, d.PBCT_NO from onbid.ONBID_UnifyUsageCltrBasicInfoDetail as d);"
        try:
            self.cur.execute(sql)
            PB_CL_No = self.cur.fetchall()

        except Exception as e:
            print("Error")
            print(str(e))

        return PB_CL_No

    def start(self):
        number_dict_list = self.get_number_from_UnifyUsageCltr()
        self.request_api_and_insert_into_db(number_dict_list)

