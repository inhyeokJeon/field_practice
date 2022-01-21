from operations import *
import argparse


def main():
    args = define_args()

    op = args['operation']
    file = args['file']
    cd = args['add']

    func = {1: 'storeZoneOne()',  # 1. 지정 상권조회
            2: 'storeZoneInRadius(file)',  # 2. 반경내 상권조회
            3: 'storeZoneInRectangle(file)',  # 3. 사각형 내 상권 조회
            4: 'storeZoneInAdmi()',  # 4. 행정구역 단위 상권조회
            5: 'storeOne()',  # 5. 단일 상가업소 조회
            6: 'storeListInBuilding()',  # 6. 건물 단위 상가업소 조회
            7: 'storeListInPnu()',  # 7. 지번 단위 상가업소 조회
            8: 'storeListInDong()',  # 8. 행정동 단위 상가업소 조회
            9: 'storeListInArea()',  # 9 상권내 상가업소 조회
            10: 'storeListInRadius(file)',  # 10 반경내 상가업소 조회
            11: 'storeListInRectangle(file)',  # 11. 사각형내 상가업소 조회
            12: 'storeListInPolygon()',  # 12. 다각형내 상가업소 조회
            13: 'storeListInUpjong()',  # 13. 업종별 상가업소 조회
            14: 'storeListByDate()',  # 14. 수정일자기준 상가업소 조회
            15: 'reqStoreModify()',  # 15. 상가업소정보 변경요청 (필요가 없을것 같아서 구현을 멈추었습니다.)
            16: 'storeStatsUpjongInAdmi(cd)',  # 16. 행정구역내 업종별 상가업소 통계 (ctprvnCd, signguCd, adongCd)
            17: 'storeStatsUpjongInBuilding()',  # 17. 건물내 업종별 상가업소 통계
            18: 'storeStatsUpjongInRadius(file)',  # 18. 반경내 업종별 상가업소 통계
            19: 'storeStatsUpjongInRectangle(file)',  # 19. 사각형내 상가업소 통계 조회
            20: 'storeStatsUpjongInPolygon()',  # 20. 다각형내 상가업소통계 조회
            21: 'largeUpjongList()',  # 21. 상권정보 업종 대분류 조회
            22: 'middleUpjongList()',  # 22. 상권정보 업종 중분류 조회
            23: 'smallUpjongList()',  # 23. 상권정보 업종 소분류 조회
            24: 'siDo()',  # 24. 시도 조회
            25: 'siGnGu()',  # 25. 시군구 조회
            26: 'aDong()',  # 26. 행정동 조회
            27: 'lDong()',  # 27. 법정동 조회
            28: 'bizesId()',  # 28. 상가업소번호 저장
            29: 'lnoCd()',  # 29. PNU코드 저장
            30: 'bldMngNo()',  # 30. 건물관리번호 저장
            31: 'trarNo()'  # 31. 상권번호 and 좌표값 저장
            }
    function = eval(func[op])
    function.start()


def define_args():
    args = argparse.ArgumentParser(description='[-o (0 : siDo),(1 : siGnGu),(2 : aDong),(3 : lDong)] [-h CSV path]')
    args.add_argument("-o", "--operation", help="Operation 설정", required=True, type=int)
    args.add_argument("-f", "--file", help="CSV File 설정", required=False, type=str, default="")
    args.add_argument("-a", "--add", help="Operation 추가 설정", required=False, type=str, default="")
    args = vars(args.parse_args())
    return args


main()