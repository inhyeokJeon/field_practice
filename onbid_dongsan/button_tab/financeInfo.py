import re

from selenium.webdriver.common.by import By

dict_jaemu_temp = {
    '재무년도': "",
    '유동자산': "",
    '비유동자산': "",
    '자산총계': "",
    '유동부채': "",
    '비유동부채': "",
    '부채총액': "",
    '자본금': "",
    '자본잉여금': "",
    '자본조정': "",
    '기타포괄손익누계액': "",
    '이익잉여금': "",
    '자본총계': "",
    '매출액': "",
    '매출총이익': "",
    '영업이익': "",
    '영업이익외수익': "",
    '영업외비용': "",
    '당기순이익': "",
    '주당배당율': "",
    '매출액증가율': "",
    '순이익증가율': "",
    '매출액순이익률': "",
    '자기자본순이익률': "",
    '자기자본회전율': "",
    '부채비율': ""
}
# 재무현황 표

def financeInfo(table):
    jaemu_list = []
    jaemu_year_thead = table.find_element(by=By.TAG_NAME, value="thead")
    jaemu_year_class = jaemu_year_thead.find_element(by=By.CLASS_NAME, value="brt")
    jaemu_year_ths = jaemu_year_class.find_elements(by=By.TAG_NAME, value="th")

    jaemu_year_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    jaemu_year_tbody_trs = jaemu_year_tbody.find_elements(by=By.TAG_NAME, value="tr")

    for i in range(len(jaemu_year_ths)):
        dict_jaemu = dict.copy(dict_jaemu_temp)
        dict_jaemu['재무년도'] = jaemu_year_ths[i].text
        for tr in jaemu_year_tbody_trs:
            ths = tr.find_elements(by=By.TAG_NAME, value="th")
            tds = tr.find_elements(by=By.TAG_NAME, value="td")
            if len(ths)==2:
                dict_jaemu[ths[1].text] = tds[i].text
            elif "\n" in ths[0].text:
                m = re.search('[\w]+',ths[0].text)
                dict_jaemu[m[0]] = tds[i].text
            else:
                dict_jaemu[ths[0].text] = tds[i].text
        jaemu_list.append(dict_jaemu)
    return jaemu_list