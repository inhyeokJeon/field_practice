import json
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request
import xmltodict
import sys


key = "HNlRcOgahdKggqJHTRCwyD%2FLGElXLgDlfJ5PGYtafElFJEhUupiPTtdKaXyGhdsodssnEfmW9fJiGywDs1LcNA%3D%3D"
url = "http://openapi.onbid.co.kr/openapi/services/OnbidCodeInfoInquireSvc/getOnbidTopCodeInfo"

queryParams = f'?{quote_plus("serviceKey")}={key}&' + urlencode({quote_plus('numOfRows'): 100,
                                                                 quote_plus('pageNo'): 1})
                                                                                      
try:
    response = Request(url+queryParams)
    response.get_method = lambda: 'GET'
    response_body = urlopen(response).read()
    response_item = xmltodict.parse(response_body)
except Exception as e:
    print(str(e))
    sys.exit()

resultCode = response_item['response']['header']['resultCode']

if resultCode != '00':
    print(response_item['response']['header']['resultMsg'])
    print("resultCode = " + resultCode)
    sys.exit()

items = response_item['response']['body']['items']
#print(items)
if not items:  # 응답 값이 존재하지 않을 때.
    print(items)
    sys.exit()

for item in items["item"]:
    print(item)
    #print(json.dumps(item, indent=2, ensure_ascii=False))