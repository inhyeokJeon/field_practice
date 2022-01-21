
from Detail import *

class UnifyUsageCltrEstimationInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "estimationInfo"
        self.tableName = "ONBID_UnifyUsageCltrEstimationInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrEstimationInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'APSL_ASES_AMT' : "",
            'APSL_ASES_DT' : "",
            'APSL_ASES_ORG_NM' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrEstimationInfoDetail (CLTR_NO, PBCT_NO, " \
          "APSL_ASES_AMT, APSL_ASES_DT, APSL_ASES_ORG_NM, hash) " \
          "values (%s,%s,%s,%s,%s,%s)"


