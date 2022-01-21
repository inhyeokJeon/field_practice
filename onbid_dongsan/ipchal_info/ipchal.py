

#입찰정보 받아오기
from selenium.webdriver.common.by import By

dict_ipchal_info_temp = {
            '전자보증서 사용여부': "",
            '차순위 매수신청 가능여부': "",
            '공동입찰 가능여부': "",
            '2인 미만 유찰여부': "",
            '대리입찰 가능여부': "",
            '2회 이상 입찰 가능여부': "",
        }


def ipchal(table):
    #입찰 방법 및 입찰 제한 정보

    #ipchal_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    ipchal_tbody_ths = table.find_elements(by=By.TAG_NAME, value="th")
    ipchal_tbody_tds = table.find_elements(by=By.TAG_NAME, value="td")

    for i in range(len(ipchal_tbody_ths)):
        th_text = ipchal_tbody_ths[i].text
        td_text = ipchal_tbody_tds[i].text
        dict_ipchal_info_temp[th_text] = td_text

    return dict_ipchal_info_temp

