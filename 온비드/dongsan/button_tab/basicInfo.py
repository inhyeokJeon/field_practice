from selenium.webdriver.common.by import By

template = {
    "제조사": "",
    "차종": "",
    "모델명": "",
    "수량": "",
    "연식": "",
    "차량번호": "",
    "주행거리": "",
    "배기량": "",
    "변속기": "",
    "연료": "",
    "기타사항": ""
}



def tab01_group_basicInfo(table,template):
    basicinfo = table.find_element(by=By.TAG_NAME, value="tbody")
    basicinfo_ths = basicinfo.find_elements(by=By.TAG_NAME, value="th")

    basicinfo_tds = basicinfo.find_elements(by=By.TAG_NAME, value="td")

    basic_info_template: dict = template

    for i in range(len(basicinfo_ths)):
        try:
            th_text = basicinfo_ths[i].text
            td_text = basicinfo_tds[i].text
            basic_info_template[th_text] = td_text
        except Exception as e:
            print(e)

    return basic_info_template
