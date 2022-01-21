
from Detail import *

class UnifyUsageCltrRegisteredInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "registered"
        self.tableName = "ONBID_UnifyUsageCltrRegisteredInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrRegisteredInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'IRST_DVSN_NM' : "",
            'IRST_IRPS_NM' : "",
            'RGST_DT' : "",
            'STUP_AMT' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrRegisteredInfoDetail (CLTR_NO, PBCT_NO, " \
          "IRST_DVSN_NM, IRST_IRPS_NM, RGST_DT, STUP_AMT, hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s)"


