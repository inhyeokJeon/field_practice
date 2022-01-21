from selenium.webdriver.remote.webelement import WebElement

from button_tab import *
from ipchal_info import *
from setup import *
def mulgun_sebu(mulgun_button):
    mulgun_sebu_all = {}

    mulgun_button.click()
    # 물건세부정보
    element_visible_wait(By.ID, "tab01")
    mulgun_element = driver.find_element(by=By.ID, value="tab01")
    # 기본정보
    if is_element_presence(By.ID, "basicInfo"):
        basicinfo = mulgun_element.find_element(by=By.ID, value="basicInfo")
        group = basicinfo.find_element(by=By.TAG_NAME, value="div").get_attribute("id")
        basicinfo_table: WebElement = basicinfo.find_element(by=By.TAG_NAME, value="table")

        if group == "tab01_group1_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_1)
        elif group == "tab01_group2_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_2)
        elif group == "tab01_group3_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_3)
        elif group == "tab01_group4_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_4)
        elif group == "tab01_group5_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_5)
        elif group == "tab01_group6_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_6)
            #print(tab01_group6_basicInfo(basicinfo_table))
            # 주요주주현황
            if is_element_presence(By.ID, "tab01_group6_stockholderInfo"):
                try:
                    mainjuju = basicinfo.find_element(by=By.ID, value="tab01_group6_stockholderInfo")
                    mainjuju_table = mainjuju.find_element(by=By.TAG_NAME, value="table")
                    basicinfo_all["stockholderinfo"] = stockholderInfo(mainjuju_table)
                except:
                    print("주요주주현황 없음")
            if is_element_presence(By.ID, "financeInfo"):
                try :
                    jaemu = basicinfo.find_element(by=By.ID, value="financeInfo")
                    jaemu_table = jaemu.find_element(by=By.TAG_NAME, value="table")
                    basicinfo_all["financeinfo"] = financeInfo(jaemu_table)
                except:
                    print("재무현황정보없음")

        elif group == "tab01_group7_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_7)
        elif group == "tab01_group8_basicInfo":
            basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_8)
        #물건세부정보 전부다
        mulgun_sebu_all['basicinfo'] = basicinfo_all

        # todo 수정 지번 도로명 보관장소
        if is_element_presence(By.CSS_SELECTOR,"#tab01 > div:nth-child(2) > table"):
            sub_table = mulgun_element.find_element(by=By.CSS_SELECTOR, value="#tab01 > div:nth-child(2) > table")
            mulgun_sebu_all['subinfo'] = basicInfo_address(sub_table)

    # 감정평가정보
    if is_element_presence(By.ID, "tab01_appraiseInfo"):
        tab01_appraiseInfo = mulgun_element.find_element(by=By.ID, value="tab01_appraiseInfo")
        appraiseInfo_table = tab01_appraiseInfo.find_element(by=By.TAG_NAME, value="table")
        mulgun_sebu_all['appraiseinfo'] = appraiseInfo(appraiseInfo_table)

    # 명도이전책임
    if is_element_presence(By.ID, "tab01_nominalTransferInfo"):
        tab01_nominalTransferInfo = mulgun_element.find_element(by=By.ID, value="tab01_nominalTransferInfo")
        nominalTransferInfo_table = tab01_nominalTransferInfo.find_element(by=By.TAG_NAME, value="table")
        mulgun_sebu_all['nominaltransferinfo'] = nominalTransferInfo(nominalTransferInfo_table)

    return mulgun_sebu_all

def ipchal_info(ipchal_button):
    ipchal_info_all = {}
    # 입찰정보
    ipchal_button.click()
    element_visible_wait(By.ID, "tab02")

    tab02 = driver.find_element(by=By.ID, value="tab02")

    try:
        jaehan_table_class = tab02.find_element(by=By.CSS_SELECTOR, value="div.op_bid_twrap.mt15 >table.op_tbl_type2.mt10")
        jaehan_table = jaehan_table_class.find_element(by=By.TAG_NAME, value="table")
        print(jaehan(jaehan_table))
    except:
        print("제한 조건 없음")

    #입찰 방법 및 입찰 제한 정보
    if is_element_presence(By.CSS_SELECTOR, "#tab02 > div.op_bid_twrap.cl.mt15 > table"):
        try :
            #ipchal_table_class = tab02.find_element(by=By.CSS_SELECTOR, value="#tab02 > div > table")
            ipchal_table = tab02.find_element(by=By.CSS_SELECTOR, value="#tab02 > div.op_bid_twrap.cl.mt15 > table")
            ipchal_info_all['ipchal'] = ipchal(ipchal_table)
        except :
            print("no ipchal info")

    #회차별 입찰정보
    if is_element_presence(By.CSS_SELECTOR, "#tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table"):
        try :
            hweicha_table_class = tab02.find_element(by=By.CLASS_NAME, value="finder.pos_rel")
            hweicha_table = hweicha_table_class.find_element(by=By.TAG_NAME, value="table")
            # 증권 #tab02 > div.op_bid_twrap.cl.mt15 > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
            # 자동차 #tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
            #tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
            ipchal_info_all['hweicha'] = hweicha(hweicha_table)
        except :
            print("no hweicha info")

    try:
        file_p_id = tab02.find_element(by=By.ID, value="resultFileList")
        file_p_a = file_p_id.find_elements(by=By.TAG_NAME, value="a")
        ipchal_info_all['chumbu'] = chumbu(file_p_a)
    except:
        print("no chumbu file")

    '''
    if is_element_presence(By.CSS_SELECTOR, "#tab02 > #rec_file > div"):
        try:
            file_p_id = tab02.find_element(by=By.ID, value="resultFileList")
            file_p_a = file_p_id.find_elements(by=By.TAG_NAME, value="a")
            print(chumbu(file_p_a))
        except:
            print("no chumbu file")
    '''
    return ipchal_info_all

def button_tab_data() :
    element_locate_wait(By.CSS_SELECTOR, "#Contents > ul")
    button_tab_table = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
    element_click_wait(By.CSS_SELECTOR, "#dtbuttontab")
    button_tabs = button_tab_table.find_elements(by=By.CSS_SELECTOR, value="#dtbuttontab")
    for button_tab in button_tabs:
        if button_tab.get_attribute("value") == '001':
            mulgun_button = button_tab
        elif button_tab.get_attribute("value") == '002':
            ipchal_button = button_tab
    mulgun_info_all = mulgun_sebu(mulgun_button)
    ipchal_info_all = ipchal_info(ipchal_button)
    print(json.dumps(mulgun_info_all,indent=2 ,ensure_ascii=False))

    print(json.dumps(ipchal_info_all,indent=2 ,ensure_ascii=False))




