
#주요주주현황
from selenium.webdriver.common.by import By

dict_mainjuju_temp = {
    "주주명": "",
    "지분율": "",
    "보유주식수": "",
    "비고": ""
}

def stockholderInfo(table):
    mainjuju_thead = table.find_element(by=By.TAG_NAME, value="thead")
    mainjuju_tbody = table.find_element(by=By.TAG_NAME, value="tbody")

    mainjuju_ths = mainjuju_thead.find_elements(by=By.TAG_NAME, value="th")

    mainjuju_trs = mainjuju_tbody.find_elements(by=By.TAG_NAME, value="tr")

    mainjuju_list = []

    for tr in mainjuju_trs:
        dict_mainjuju = dict.copy(dict_mainjuju_temp)
        tds = tr.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(mainjuju_ths)):
            if "입력된 데이터가" in tds[i].text:
                break
            try:
                dict_mainjuju[mainjuju_ths[i].text] = tds[i].text
            except Exception as e:
                print(e)
        mainjuju_list.append(dict_mainjuju)

    return mainjuju_list