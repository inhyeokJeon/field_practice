from selenium.webdriver.common.by import By

dict_jaehan_temp = {
            "자격제한조건": "",
            "지역제한조건": "",
            "기타제한조건": ""
        }

def jaehan(table):
    dict_jaehan = dict.copy(dict_jaehan_temp)
    jaehan_tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    jaehan_trs = jaehan_tbody.find_elements(by=By.TAG_NAME, value="tr")
    for tr in jaehan_trs:
        th_text = tr.find_element(by=By.TAG_NAME, value="th").text
        td_text = tr.find_element(by=By.TAG_NAME, value="td").text
        dict_jaehan[th_text] = td_text

    return dict_jaehan