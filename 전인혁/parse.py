from Operations import *
import argparse

def main():
    operation_name = parser()
    operation = eval(operation_name +'()')
    operation.data_load()
    print(operation)

def parser():
    parser = argparse.ArgumentParser(description='실행할 오퍼레이션명을 적으세요 string type으로')
    parser.add_argument('string', type=str , help='give me a string')
    args = parser.parse_args()
    return args.string

main()