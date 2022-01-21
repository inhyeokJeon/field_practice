from Detail import *

class UnifyUsageCltrBidHistoryInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "bidHistoryInfo"
        self.tableName = "ONBID_UnifyUsageCltrBidHistoryInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrBidHistoryInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'PBCT_SEQ' : "",
            'PBCT_DGR' : "",
            'BID_MNMT_NO' : "",
            'DPSL_MTD_NM' : "",
            'PBCT_EXCT_DTM' : "",
            'MIN_BID_PRC' : "",
            'PBCT_STAT_NM' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrBidHistoryInfoDetail (CLTR_NO, PBCT_NO, " \
          "PBCT_SEQ, PBCT_DGR, BID_MNMT_NO, DPSL_MTD_NM, PBCT_EXCT_DTM, MIN_BID_PRC, PBCT_STAT_NM, hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


