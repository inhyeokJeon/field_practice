from Detail import *

class UnifyUsageCltrCorporatebodyInfoDetail(Detail):
    def __init__(self):
        super().__init__()
        self.item_Value = "corporatebodyInfo"
        self.tableName = "ONBID_UnifyUsageCltrCorporatebodyInfoDetail"
        self.url_result = ""
        self.url = "http://openapi.onbid.co.kr/openapi/services/ThingInfoInquireSvc/getUnifyUsageCltrCorporatebodyInfoDetail"
        self.dict_template = {
            'CLTR_NO' : "",
            'PBCT_NO' : "",
            'FNCL_YR' : "",
            'IVTR_AST_AMT' : "",
            'IVSM_AST_AMT' : "",
            'TYPE_AST_AMT' : "",
            'ITGB_AST_AMT' : "",
            'DFD_AST_AMT' : "",
            'LQDY_LBT_AMT' : "",
            'FIXD_LBT_AMT' : "",
            'CPTL_AMT' : "",
            'CPTL_SPLS_AMT' : "",
            'GAIN_SPLS_AMT' : "",
            'CPTL_AJST_AMT' : "",
            'SALS_AMT' : "",
            'SALS_COST_AMT' : "",
            'TOT_SALS_AMT' : "",
            'SALE_AMT_MNMT_AMT' : "",
            'BIZ_GAIN_AMT' : "",
            'NOPT_GAIN_AMT' : "",
            'NOPT_EPNS_AMT' : "",
            'RGLR_GAIN_AMT' : "",
            'SPCL_GAIN_AMT' : "",
            'SPCL_LOS_AMT' : "",
            'CPRX_DCTN_BEF_NET_LSNG_AMT' : "",
            'CPRX_AMT' : "",
            'TSTR_NPRF_AMT' : "",
            'PRSH_NPRF_AMT' : "",
            'DVRT' : "",
            'DVNS' : "",
            'SALS_AMT_NPRF_RT' : "",
            'TOT_CPTL_BIZ_GAIN_RT' : "",
            'SELF_CPTL_NPRF_RT' : "",
            'TOT_CPTL_NPRF_RT' : "",
            'SALS_AMT_INCRT' : "",
            'NPRF_INCRT' : "",
            'LQDY_RT' : "",
            'LBT_RT' : "",
            'TOT_AST_ROTN_RT' : "",
            'ETC_ICLS_LSNG_CMLT_AMT' : ""

        }
        #41 with hash
        self.sql = "insert into ONBID_UnifyUsageCltrBidHistoryInfoDetail (CLTR_NO, PBCT_NO, " \
          "FNCL_YR, CRCT_AST_AMT, IVTR_AST_AMT, IVSM_AST_AMT, TYPE_AST_AMT, ITGB_AST_AMT, DFD_AST_AMT, " \
          "LQDY_LBT_AMT, FIXD_LBT_AMT, CPTL_AMT, CPTL_SPLS_AMT, GAIN_SPLS_AMT, CPTL_AJST_AMT, SALS_AMT, " \
          "SALS_COST_AMT, TOT_SALS_AMT, SALE_AMT_MNMT_AMT, BIZ_GAIN_AMT, NOPT_GAIN_AMT, NOPT_EPNS_AMT, " \
          "RGLR_GAIN_AMT, SPCL_GAIN_AMT, SPCL_LOS_AMT, CPRX_DCTN_BEF_NET_LSNG_AMT, CPRX_AMT, TSTR_NPRF_AMT, " \
          "PRSH_NPRF_AMT, DVRT, DVNS, SALS_AMT_NPRF_RT, TOT_CPTL_BIZ_GAIN_RT, SELF_CPTL_NPRF_RT, TOT_CPTL_NPRF_RT, " \
          "SALS_AMT_INCRT, NPRF_INCRT, LQDY_RT, LBT_RT, TOT_AST_ROTN_RT, ETC_ICLS_LSNG_CMLT_AMT, hash) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


