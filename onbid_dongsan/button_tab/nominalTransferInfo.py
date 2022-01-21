#nominalTransferInfo 명도 및 부대조건 템플릿
#div id nominalTransferInfo 값 받아오기
from selenium.webdriver.common.by import By

myungdo_template = {
    "명도이전책임": "",
    "인도장소": "",
    "부대조건": ""
}

# todo 왜 " " : " " 가 생기지
def nominalTransferInfo(table):
    dict_myungdo = dict.copy(myungdo_template)
    myungdo_table_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    myungdo_table_tbody_trs = myungdo_table_tbody.find_elements(by=By.TAG_NAME, value="tr")

    for tr in myungdo_table_tbody_trs:
        if tr.get_attribute("id") == "placeDelivery":
            continue
        dict_myungdo[tr.find_element(by=By.TAG_NAME, value="th").text] = tr.find_element(by=By.TAG_NAME,
                                                                                               value="td").text
    return dict_myungdo