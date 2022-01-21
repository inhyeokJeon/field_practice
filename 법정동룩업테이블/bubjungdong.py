from bubjungdong_op import *
import argparse


def define_args():
    args = argparse.ArgumentParser(description='행정표준코드관리시스템 법정동 코드 목록 업데이트')
    args.add_argument("-f", "--file", help="txt file path 설정", required=True, type=str, default="")
    args = vars(args.parse_args())
    return args


args = define_args()

func = main(args['file'])

func.start()
