#감정평가정보 템플릿
from selenium.webdriver.common.by import By

template: dict = {  # 감정평가정보
            '감정평가기관': "",
            '평가일': "",
            '평가금액(원)': "",
            '감정평가서': ""
        }

gamjung_list = []

def appraiseInfo(table):
    gamjung_info_thead = table.find_element(by=By.TAG_NAME, value="thead")
    # tbody
    gamjung_info_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    # thead ths
    gamjung_info_thead_ths = gamjung_info_thead.find_elements(by=By.TAG_NAME, value="th")
    # tbody trs
    gamjung_info_tbody_trs = gamjung_info_tbody.find_elements(by=By.TAG_NAME, value="tr")

    for tr in gamjung_info_tbody_trs:
        dict_gamjung: dict = dict.copy(template)
        # tbody trs tds
        gamjung_info_tbody_trs_tds = tr.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(gamjung_info_thead_ths)):
            if "조회된 데이타가 " in gamjung_info_tbody_trs_tds[i].text:
                return gamjung_list
            if (i == 3):
                # todo 느리다
                try:
                    dict_gamjung[gamjung_info_thead_ths[i].text] = \
                        gamjung_info_tbody_trs_tds[i].find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                    # print(gamjung_info_thead_ths[i].text)
                except Exception as e:
                    print("감정평가서 없음")
                break
            try:
                dict_gamjung[gamjung_info_thead_ths[i].text] = gamjung_info_tbody_trs_tds[i].text
                # print(gamjung_info_thead_ths[i].text)
            except Exception as e:
                print(e, "nodata")

        gamjung_list.append(dict_gamjung)

    return gamjung_list