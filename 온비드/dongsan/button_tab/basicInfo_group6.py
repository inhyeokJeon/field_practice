from selenium.webdriver.common.by import By

template_6 = {
    '법인명': "",
    '지분율': "",
    '주식의 종류': "",
    '주당액면가': "",
    '액면총액': "",
    '대표자': "",
    '연락처': "",
    '발행주식총수(주)': "",
    "설립일자": "",
    "결산월": "",
    "업종": "",
    "주요제품": "",
    "본점소재지": "",
    "기타사항": "",
    "증권명": "",
    "수량": ""
}


def tab01_group6_basicInfo(table):
    basic_info_template6 = dict.copy(template_6)
    basicinfo = table.find_element(by=By.TAG_NAME, value="tbody")
    basicinfo_ths = basicinfo.find_elements(by=By.TAG_NAME, value="th")

    basicinfo_tds = basicinfo.find_elements(by=By.TAG_NAME, value="td")
    #기본정보
    for i in range(len(basicinfo_ths)):
        try:
            th_text = basicinfo_ths[i].text
            td_text = basicinfo_tds[i].text
            basic_info_template6[th_text] = td_text

        except Exception as e:
            print(e, "yuga error ")

    return basic_info_template6