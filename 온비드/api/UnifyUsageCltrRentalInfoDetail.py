
from Detail import *

class UnifyUsageCltrRentalInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "rentalInfo"
        self.tableName = "ONBID_UnifyUsageCltrRentalInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrRentalInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'IRST_DVSN_NM' : "",
            'IRST_IRPS_NM' : "",
            'TDPS_AMT' : "",
            'MTHR_AMT' :"",
            'CONV_GRT_MONY' :"",
            'FIX_DT' :"",
            'MVN_DT' :""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrRentalInfoDetail (CLTR_NO, PBCT_NO, " \
          "IRST_DVSN_NM, IRST_IRPS_NM, TDPS_AMT, MTHR_AMT, CONV_GRT_MONY, FIX_DT, MVN_DT,hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #29