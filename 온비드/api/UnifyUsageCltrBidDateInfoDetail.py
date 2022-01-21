from Detail import *

class UnifyUsageCltrBidDateInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "bidInfo"
        self.tableName = "ONBID_UnifyUsageCltrBidDateInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrBidDateInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'BID_MNMT_NO' : "",
            'PBCT_SEQ' : "",
            'PBCT_DGR' : "",
            'BID_DVSN_NM' : "",
            'PCMT_PYMT_MTD_CNTN' : "",
            'PCMT_PYMT_EPDT_CNTN' : "",
            'PBCT_BEGN_DTM' : "",
            'PBCT_CLS_DTM' : "",
            'PBCT_EXCT_DTM' : "",
            'OPBD_PLC_CNTN' : "",
            'DPSL_DCSN_DTM' : "",
            'MIN_BID_PRC' : ""
        }

        self.sql = "insert into ONBID_UnifyUsageCltrBidDateInfoDetail (CLTR_NO, PBCT_NO, " \
          "BID_MNMT_NO, PBCT_SEQ, PBCT_DGR, BID_DVSN_NM, PCMT_PYMT_MTD_CNTN, PCMT_PYMT_EPDT_CNTN, " \
          "PBCT_BEGN_DTM, PBCT_CLS_DTM, PBCT_EXCT_DTM, OPBD_PLC_CNTN, DPSL_DCSN_DTM, MIN_BID_PRC,hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


