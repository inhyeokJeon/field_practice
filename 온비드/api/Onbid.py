from UnifyUsageCltr import *
from UnifyUsageCltrBasicInfoDetail import *
from UnifyUsageCltrEstimationInfoDetail import *
from UnifyUsageCltrRentalInfoDetail import *
from UnifyUsageCltrRegisteredInfoDetail import *
from UnifyUsageCltrBidDateInfoDetail import *
from UnifyUsageCltrBidHistoryInfoDetail import *
from UnifyUsageCltrStockholderInfoDetail import *
from UnifyUsageCltrCorporatebodyInfoDetail import *
from KamcoPlnmPbctBasicInfoDetail import *

import argparse

def main():
    args = define_args()

    op = args['operation']

    func = {1: 'UnifyUsageCltr()',  # 1. 통합조회
            #-------------------------------- 통합조회 테이블로부터 공매,물건번호를 통해 조회함
            2: 'UnifyUsageCltrBasicInfoDetail()',  # 2. 기본상세조회
            3: 'UnifyUsageCltrEstimationInfoDetail()',  # 3. 통합용도별물건 감정평가서정보 상세조회
            4: 'UnifyUsageCltrRentalInfoDetail()',  # 4. 통합용도별물건 임대차정보 상세조회
            5: 'UnifyUsageCltrRegisteredInfoDetail()', #5. 통합용도별물건 권리종류정보 상세조회
            6: 'UnifyUsageCltrBidDateInfoDetail()', #6. 통합용도별물건 공매일정 상세조회
            7: 'UnifyUsageCltrBidHistoryInfoDetail()', #7. 통합용도별물건 입찰이력 상세조회
            8: 'UnifyUsageCltrStockholderInfoDetail()', #8. 통합용도별물건 주주정보 상세조회
            9: 'UnifyUsageCltrCorporatebodyInfoDetail()', #9. 통합용도별물건 법인현황정보 상세조회
            10: 'KamcoPlnmPbctBasicInfoDetail()'
            }

    function = eval(func[op])
    function.start()


def define_args():
    args = argparse.ArgumentParser(description='[-o (1 : 통합조회),(2 : 기본상세조회)...] [-h CSV path]')
    args.add_argument("-o", "--operation", help="Operation 설정", required=True, type=int)
    args = vars(args.parse_args())
    return args


main()