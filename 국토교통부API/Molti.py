from RTMS_DataSvcAptRent import *
from RTMS_DataSvcAptTrade import *
from RTMS_DataSvcAptTradeDev import *
from RTMS_DataSvcLandTrade import *
from RTMS_DataSvcNrgTrade import *
from RTMS_DataSvcOffiRent import *
from RTMS_DataSvcOffiTrade import *
from RTMS_DataSvcRHRent import *
from RTMS_DataSvcRhTrade import *
from RTMS_DataSvcShTrade import *
from RTMS_DataSvcSHRent import *
from RTMS_DataSvcSilvTrade import *
from TradePrcIndex import *
from molitBaseClass import *
import argparse


def main():
    args = define_args()

    op = args['operation']
    
    func = {1: 'RTMS_DataSvcAptRent()',  # 1. 아파트 전월세 
            2: 'RTMS_DataSvcAptTrade()',  # 2. 아파트매매 실거래 
            3: 'RTMS_DataSvcAptTradeDev()',  # 3. 아파트매매 실거래 상세
            4: 'RTMS_DataSvcLandTrade()',  # 4. 토지 매매 신고 조회
            5: 'RTMS_DataSvcNrgTrade()',  # 5. 상업업무용 부동산 매매
            6: 'RTMS_DataSvcOffiRent()',  # 6. 오피스텔 전월세 신고 
            7: 'RTMS_DataSvcOffiTrade()',  # 7. 오피스텔 매매 신고
            8: 'RTMS_DataSvcRHRent()',  # 8. 연립다세대 전월세 
            9: 'RTMS_DataSvcRhTrade()',  # 9. 연립다세대 매매
            10: 'RTMS_DataSvcSHRent()',  # 10. 단독/다가구 전월세 
            11: 'RTMS_DataSvcShTrade()',  # 11. 단독/다가구 매매
            12: 'RTMS_DataSvcSilvTrade()',  # 12. 부동산 매매 신고
            13: 'TradePrcIndex()' # 13. 한국부동산원_ 부동산 매매가격지수
            }
    
    function = eval(func[op])
    function.start()
    
def define_args():
    args = argparse.ArgumentParser(description='[-o ...] ')
    args.add_argument("-o", "--operation", help="Operation 설정", required=True, type=int)
    args = vars(args.parse_args())
    return args


main()