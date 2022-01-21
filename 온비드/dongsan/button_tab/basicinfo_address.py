from selenium.webdriver.common.by import By

template = {
    "지번": "",
    "도로명": "",
    "보관장소": ""
}

def basicInfo_address(table):
    subinfo = table.find_element(by=By.TAG_NAME, value="tbody")
    subinfo_ths = subinfo.find_elements(by=By.TAG_NAME, value="th")
    subinfo_tds = subinfo.find_elements(by=By.TAG_NAME, value="td")

    del subinfo_ths[0]

    template_address = dict.copy(template)

    for i in range(len(subinfo_ths)):
        try:
            template_address[subinfo_ths[i].text] = subinfo_tds[i].text
        except Exception as e:
            print(e)

    return template_address