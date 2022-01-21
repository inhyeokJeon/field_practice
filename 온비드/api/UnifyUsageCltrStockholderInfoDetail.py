from Detail import *

class UnifyUsageCltrStockholderInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "stockholderInfo"
        self.tableName = "ONBID_UnifyUsageCltrStockholderInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrStockholderInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'SCRT_STHL_NO' : "",
            'STHL_NM' : "",
            'POSN_STK_CNT' : "",
            'PCOS' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrBidHistoryInfoDetail (CLTR_NO, PBCT_NO, " \
          "SCRT_STHL_NO, STHL_NM, POSN_STK_CNT, PCOS, hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s)"


