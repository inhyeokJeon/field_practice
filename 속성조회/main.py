from attributes import *
import argparse


def main():
    args = define_args()

    op = args['operation']

    func = {1: 'LandPriceAttribute()',  # 1. 표준지공시지가정보서비스
            2: 'ApartHousingPriceAttribute()',  # 2. 공동주택가격정보서비스
            3: 'getIndvdLandPriceAttr()',  # 3. 개별공시지가정보서비스
            4: 'getIndvdHousingPriceAttr()',  # 4. 개별주택가격정보서비스
            }
    function = eval(func[op])
    function.start()


def define_args():
    args = argparse.ArgumentParser(description='[-o (1 : LandPriceAttribute),(2 : ApartHousingPriceAttribute)...] [-h CSV path]')
    args.add_argument("-o", "--operation", help="Operation 설정", required=True, type=int)
    args = vars(args.parse_args())
    return args


main()