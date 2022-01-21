import re

from selenium.webdriver.common.by import By

dict_hweicha_temp = {
            '입찰번호': "",
            '회차': "",
            '차수': "",
            '구분': "",
            '대금납부': "",
            '납부기한': "",
            '입찰시작기간': "",
            '입찰종료기간': "",
            '개찰일시': "",
            '개찰장소': "",
            '최저입찰가(원)': "",
            '매각결정일시': "",
            'gongmae_link': ""
        }

def hweicha(table):
    """8
    :param table: 셀레니움 WebElement 객체
    :return:
    """
    hweicha_table_thead = table.find_element(by=By.TAG_NAME, value="thead")
    hweicha_table_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    hweicha_table_ths = hweicha_table_thead.find_elements(by=By.TAG_NAME, value="th")
    hweicha_table_trs = hweicha_table_tbody.find_elements(by=By.TAG_NAME, value="tr")

    # 회차별 입찰 정보 리스트
    dict_hewicha_list = []
    for tr in hweicha_table_trs:
        if "없습니다" in tr.text:
            break
        dict_hweicha: dict = dict.copy(dict_hweicha_temp)
        tr_tds = tr.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(hweicha_table_ths)):
            th_text = hweicha_table_ths[i].text
            td_text = tr_tds[i].text
            if "/\n" in th_text:
                dict_key = re.split("/\s", th_text)
                dict_value = re.split("/\s", td_text)
                dict_hweicha[dict_key[0]] = dict_value[0]
                dict_hweicha[dict_key[1]] = dict_value[1]
                continue

            elif th_text == "입찰기간":
                p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
                m = p.findall(td_text)
                dict_hweicha['입찰시작기간'] = m[0]
                dict_hweicha['입찰종료기간'] = m[1]
                continue

            elif "\n" in th_text:
                dict_hweicha['매각결정일시'] = td_text
            # todo 공매재산명세 link 저장해야댐
            # elif th_text == "개찰장소":
            #     try :
            #         # tr_tds[i].find_element(by=By.CLASS_NAME, value="cm_btn_sint7").click()
            #         link = ONBID_Selenium.gongmae_jaesan(tr_tds[i].find_element(by=By.CLASS_NAME, value="cm_btn_sint7"))
            #         dict_hweicha['gongmae_link'] = link
            #         #cltrMakeDate > a
            #     except Exception as e:
            #         print("공매재산명세 없음",e)
            dict_hweicha[th_text] = td_text
        dict_hewicha_list.append(dict_hweicha)
    return dict_hewicha_list