from setup import *

ipchal_result = {
    "물건관리번호": "",
    "ipchal_previous" : {},
    "ipchal_result" : []

}

ipchal_previous_temp = {
    "이전입찰결과": "",
    "누적상태_유찰횟수": "",
    "누적상태_취소횟수": "",
    "이전입찰_최저입찰가": ""
}


dict_ipchal_result_info = {
    "회차": "",
    "차수": "",
    "입찰번호": "",
    "처분방식": "",
    "개찰일": "",
    "개찰시": "",
    "개찰종료일": "",
    "개찰종료시": "",
    "최저입찰가": "",
    "입찰결과": "",
    "낙찰가": "",
    "낙찰가율": "",
    "exist": False,
    #-------상세보기
    "물건관리번호": "",
    "물건명": "",
    "기관명": "",
    "공고번호": "",
    "입찰방식": "",
    "경쟁방식": "",
    "입찰시작기간": "",
    "입찰종료기간": "",
    "총액/단가": "",
    "개찰시작일시": "",
    "집행완료일시": "",
    "유효입찰자수": "",
    "무효입찰자수": "",
    "입찰금액": "",
    "개찰결과": "",
    "2인 미만 유찰여부": "",
    "유찰/취소사유": "",
    "감정가": "",
    "낙찰금액": "", # 낙찰가랑 같음
    "낙찰가율(감정가 대비)": "",
    "낙찰가율(최저입찰가 대비)": "",
    "재산구분": "",
    "담당부점": "",
    #-------------------
    '대금납부기한': "",
    '납부여부': "",
    '납부촉구(최고)기한': "",
    '배분기일': "",
}

def ipchal_detail_result(dict_ipchal_result_info):
    '''
    상세보기란의 데이터들을 dict 에 저장
    :return:
    '''
    #----check
    check = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container")
    check_table_count = check.find_elements(by=By.TAG_NAME, value="h4")
    #----check

    element_visible_wait(By.CSS_SELECTOR,"body > div > div.popup_container > table")
    table = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container > table")

    ths = table.find_elements(by=By.TAG_NAME, value="th")
    tds = table.find_elements(by=By.TAG_NAME, value="td")

    for i in range(len(ths)):
        th_text = ths[i].text
        td_text = tds[i].text
        if td_text == '-':
            continue

        if "물건관리번호" in th_text:
            dict_ipchal_result_info['물건관리번호'] = td_text
            continue
        elif "기관명" in th_text:
            dict_ipchal_result_info['기관명'] = td_text
            continue
        elif "믈건명" in th_text:
            dict_ipchal_result_info['기관명'] = td_text
            continue
        elif "공고번호" in th_text:
            dict_ipchal_result_info['기관명'] = td_text
            continue
        elif "회차" in th_text:
            try:
                m = re.split(r'\s/\s', td_text)
                dict_ipchal_result_info['회차'] = m[0]
                dict_ipchal_result_info['차수'] = m[1]
            except Exception as e:
                logging.exception(e)
            continue
        elif "처분방식" in th_text:
            dict_ipchal_result_info['처분방식'] = td_text
            continue
        elif "입찰방식" in th_text:
            try:
                m = re.split(r'\s/\s', td_text)
                dict_ipchal_result_info['입찰방식'] = m[0]
                dict_ipchal_result_info['경쟁방식'] = m[1]
            except Exception as e:
                logging.exception(e)
            continue
        elif "입찰기간" in th_text:
            try:
                m = re.split(r'\s~\s', td_text)
                dict_ipchal_result_info['입찰시작기간'] = m[0]
                dict_ipchal_result_info['입찰종료기간'] = m[1]
            except Exception as e:
                logging.exception(e)
            continue
        elif "총액/단가" in th_text:
            dict_ipchal_result_info['총액/단가'] = td_text
            continue
        elif "개찰시작일시" in th_text:
            dict_ipchal_result_info['개찰시작일시'] = td_text
            continue
        elif "집행완료일시" in th_text:
            dict_ipchal_result_info['집행완료일시'] = td_text
            continue
        elif "입찰자수" in th_text:
            try:
                m = re.findall('\d+', td_text)
                dict_ipchal_result_info['유효입찰자수'] = m[0]
                dict_ipchal_result_info['무효입찰자수'] = m[1]
            except Exception as e:
                logging.exception(e)
            continue
        elif "개찰결과" in th_text:
            dict_ipchal_result_info['개찰결과'] = td_text
            continue
        elif "2인 미만 유찰여부" in th_text:
            dict_ipchal_result_info['2인 미만 유찰여부'] = td_text
            continue
        elif "유찰/취소사유" in th_text:
            dict_ipchal_result_info['유찰/취소사유'] = td_text
            continue
        elif "감정가" in th_text:
            dict_ipchal_result_info['감정가'] = td_text
            continue
        elif "입찰금액" in th_text:
            dict_ipchal_result_info['입찰금액'] = td_text
            continue
        elif "낙찰금액" in th_text:
            dict_ipchal_result_info['낙찰금액'] = td_text
            continue
        elif "최저입찰가" in th_text:
            dict_ipchal_result_info['최저입찰가'] = td_text
            continue
        elif "최저입찰가 대비" in th_text:
            dict_ipchal_result_info['낙찰가율(최저입찰가 대비)'] = td_text
            continue
        elif "감정가 대비" in th_text:
            dict_ipchal_result_info['낙찰가율(감정가 대비)'] = td_text
            continue
        elif "재산구분" in th_text:
            dict_ipchal_result_info["재산구분"] = td_text
            continue
        elif "담당부점" in th_text:
            dict_ipchal_result_info["담당부점"] = td_text
            continue

    dict_ipchal_result_info['exist'] = True
    if "압류" in dict_ipchal_result_info["재산구분"]:
        dict_ipchal_result_info['exist'] = False

    # 상세보기 버튼의 대금납부 및 배분기일 테이블이 있으면
    if len(check_table_count) == 2:
        table = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container > table:nth-child(4)")
        ths = table.find_elements(by=By.TAG_NAME, value="th")
        tds = table.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(ths)):
            th_text = ths[i].text
            td_text = tds[i].text
            if "대금납부기한" in th_text:
                dict_ipchal_result_info['대금납부기한'] = td_text
            elif "납부여부" in th_text:
                dict_ipchal_result_info['납부여부'] = td_text
            elif "납부촉구(최고)기한" in th_text:
                dict_ipchal_result_info['납부촉구(최고)기한'] = td_text
            elif "배분기일" in th_text:
                dict_ipchal_result_info['배분기일'] = td_text

    print(json.dumps(dict_ipchal_result_info, indent=2, ensure_ascii=False))

def move_to_detail(td, dict_result):
    td.find_element(by=By.TAG_NAME, value ="a").click()
    main = driver.window_handles
    driver.switch_to.window(main[2])

    ipchal_detail_result(dict_result)

    driver.close()
    driver.switch_to_window(main[0])
    driver.back()
    time.sleep(10)

def ipchal_table_data():
    set_order_and_click()
    set_newtab_javascript()

    table = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel > table")
    ths = table.find_elements(by=By.TAG_NAME, value="th")
    tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    trs = tbody.find_elements(by=By.TAG_NAME, value="tr")
    ipchal_result = []
    for tr in trs:
        dict_summary = dict_ipchal_result_info.copy()
        tds = tr.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(ths)):
            th_text = ths[i].text
            td_text = tds[i].text
            if td_text == '-' or td_text == '' or td_text == '~':
                continue

            if "회차" in th_text:
                m = re.split('/',td_text)
                dict_summary['회차'] = m[0]
                dict_summary['차수'] = m[1]
                continue
            elif "개찰일시" in th_text:
                YMD = re.findall('[\d]{4}-[\d]{2}-[\d]{2}', td_text)
                HM = re.findall('[\d]{2}:[\d]{2}', td_text)
                dict_summary['개찰일'] = YMD[0]
                dict_summary['개찰시'] = HM[0]
                continue

            elif "낙찰가" in th_text:
                m = re.split('\s', td_text)
                dict_summary['낙찰가'] = m[0]
                dict_summary['낙찰가율'] = m[1]
                continue

            elif "상세입찰결과" in th_text:
                move_to_detail(tds[i], dict_summary)
                continue

            dict_summary[th_text] = td_text
        ipchal_result.append(dict_summary)

def ipchal_previous():
    dict_ipchal_prev = dict.copy(ipchal_previous_temp)
    dict_ipchal_prev['이전입찰결과'] = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_box_sch_bg.mt10 > div > div.op_top_info4.fl.bg_img09 > dl > dd")
    dict_ipchal_prev['누적상태_유찰횟수'] = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_box_sch_bg.mt10 > div > div.op_top_info5.fl.bg_img10 > dl > dd > em:nth-child(2)")
    dict_ipchal_prev['누적상태_취소횟수'] = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_box_sch_bg.mt10 > div > div.op_top_info5.fl.bg_img10 > dl > dd > em:nth-child(4)")
    dict_ipchal_prev['이전입찰_최저입찰가'] = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_box_sch_bg.mt10 > div > div.op_top_info6.fr.bg_img11 > dl > dd > em")

def is_presence_ipchal_previous():
    element_visible_wait(By.CSS_SELECTOR, "#Contents > div.tab_wrap.pos_rel > ul > li:nth-child(2) > a")
    driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.tab_wrap.pos_rel > ul > li:nth-child(2) > a").click()
    element_visible_wait(By.CLASS_NAME, "fs14.ac.op_txt_serch")
    main_text = driver.find_element(by=By.CLASS_NAME, value="fs14.ac.op_txt_serch").text
    print(main_text)
    if "없습니다" in main_text:
        return False
    else:
        return True

def ipchal_history():
    if not is_presence_ipchal_previous():
        driver.back()
        return
    else:
        ipchal_previous()
        ipchal_table_data()

    driver.back()



'''
ipchal_history_summary_temp = {
    "회차": "",
    "차수": "",
    "입찰번호": "",
    "처분방식": "",
    "개찰일": "",
    "개찰시": "",
    "개찰종료일": "",
    "개찰종료시": "",
    "최저입찰가": "",
    "입찰결과": "",
    "낙찰가": "",
    "낙찰가율": "",
    "exist": False
}
'''