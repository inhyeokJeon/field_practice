from setup import *

dict_detail_temp: dict = {  # 물건 상세정보.
    '물건관리번호': "",
    '중분류카테고리': "",
    '소분류카테고리': "",
    '물건이름': "",
    '태그': [],
    '물건상태': "",
    '공고일자': "",
    '조회수': "",
    '처분방식': "",
    '자산구분': "",
    '용도': "",
    '작품명': "",
    '작가명': "",
    '제조사': "",
    '모델명': "",
    '감정평가금액': "",
    '수량': "",
    '입찰방식': "",
    '입찰': "",
    '개찰': "",
    '회차': "",
    '차수': "",
    '유찰횟수': "",
    '임대기간': "",
    # --------- NPL
    'NPL종류명': "",
    # ---------- 유가증권
    '법인명': "",
    '최초예정가액': "",
    '집행기관': "",
    '담당자정보': "",
    '최저입찰가': ""

}

def get_detail_data() -> dict:
    """
    물건상세정보 dictionary로 반환.
    :return: 물건상세정보
    """
    dict_detail: dict = dict.copy(dict_detail_temp)
    #물건관리번호
    if is_element_presence(By.CSS_SELECTOR, "#Contents > div.tab_wrap.pos_rel > div.finder03 > div"):
        tab_wrap = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.tab_wrap.pos_rel > div.finder03 > div")
    else:
        tab_wrap = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.tab_wrap1.pos_rel > div.finder03 > div")

    mulgun_number: str = tab_wrap.find_element(
        by=By.CSS_SELECTOR, value="div.txt_top > p.fl.fwb > span:nth-child(2)").text

    dict_detail['물건관리번호'] = mulgun_number

    # 물건상태, 공고일자, 조회수
    fr = tab_wrap.find_element(by=By.CSS_SELECTOR, value="div.txt_top > p.fr")

    spans = fr.find_elements(by=By.TAG_NAME, value="span")

    if len(spans) != 3:
        print("물건상태, 공고일자, 조회수 데이터가 없습니다.")
        sys.exit()

    dict_detail['물건상태'] = spans[0].find_element(by=By.TAG_NAME, value="em").text
    dict_detail['공고일자'] = spans[1].find_element(by=By.TAG_NAME, value="em").text
    dict_detail['조회수'] = spans[2].find_element(by=By.TAG_NAME, value="em").text

    # 중분류, 소분류, 물건이름
    cl_mt10 = driver.find_element(by=By.CLASS_NAME, value="cl.mt10")
    category_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="p").text

    category = re.split("\s.\s", category_text[1:-1])

    dict_detail["중분류카테고리"] = category[0]
    dict_detail["소분류카테고리"] = category[1]

    name_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="strong").text
    dict_detail['물건이름'] = name_text

    # 태그
    badge_wrap = driver.find_element(by=By.CLASS_NAME, value="badge_wrap.mt10")
    badges = badge_wrap.find_elements(by=By.TAG_NAME, value="em")
    badge_list: list = []

    for badge in badges:
        badge_list.append(badge.text)

    dict_detail['태그'] = badge_list

    # 처분방식, 자산구분, 용도, 토지면적, 건물면적, 감정평가금액, 입찰방식, 입찰, 개찰, 회차, 차수, 유찰횟수

    body = driver.find_element(by=By.CSS_SELECTOR,
                                    value="#Contents > div.form_wrap.mt20.mb10 > div.check_wrap.fr > table > tbody")

    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    for tr in trs:
        head_line_text: str = tr.find_element(by=By.TAG_NAME, value="th").text
        table_data: str = tr.find_element(by=By.TAG_NAME, value="td").text

        if "처분방식" in head_line_text:
            p = re.compile(r'[\w]+')
            m = p.findall(table_data)

            dict_detail['처분방식'] = m[0]
            dict_detail['자산구분'] = m[1]
            continue

        if "용도" in head_line_text:
            dict_detail['용도'] = table_data
            continue

        if "제조사" in head_line_text:
            try:
                m = re.split("\s.\s", table_data)
                dict_detail['제조사'] = m[0]
                dict_detail['모델명'] = m[1]
            except Exception as e :
                print(e , "no data 제조사 / 모델명")
                continue
            continue
        if "작품명" in head_line_text:
            try:
                p = re.compile(r'[\w]+')
                m = p.findall(table_data)

                dict_detail['작품명'] = m[0]
                dict_detail['작가명'] = m[1]
            except Exception as e :
                print(e , "no data 작품명 / 작가명")
                continue

        if "감정평가금액" in head_line_text:
            p = re.compile(r'[\d]{1,3}')
            m: list = p.findall(table_data)
            gamjung: str = ""
            for text in m:
                gamjung += text
            dict_detail['감정평가금액'] = gamjung
            continue

        if "수량" in head_line_text:
            dict_detail['수량'] = table_data
            continue

        if "입찰방식" in head_line_text:
            dict_detail['입찰방식'] = table_data
            continue

        if "입찰기간" in head_line_text:
            try:
                p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
                m = p.findall(table_data)
                dict_detail['입찰'] = m[0]
                dict_detail['개찰'] = m[1]
                p = re.compile(r'[\d]+/[\d]+')
                m: list = p.findall(table_data)
                data: list = m[0].split('/')
                dict_detail['회차'] = data[0]
                dict_detail['차수'] = data[1]
                continue

            except Exception as e:
                print(e , "no data 입찰기간 (회차/차수)")

                continue

        if "유찰횟수" in head_line_text:
            p = re.compile(r'[\d]+')
            m = p.findall(table_data)
            dict_detail['유찰횟수'] = m[0]
            continue

        if "임대기간" in head_line_text:
            dict_detail['임대기간'] = table_data
            continue

        if "NPL종류명" in head_line_text:
            dict_detail['NPL종류명'] = table_data
            continue

        # if "배분요구종기" in head_line_text:
        #     dict_detail['배분요구종기'] = table_data
        #     continue

        # if "최초공고일자" in head_line_text:
        #     dict_detail['최초공고일자'] = table_data
        #     continue
        #
        # if "공매대행의뢰기관" in head_line_text:
        #     dict_detail['공매대행의뢰기관'] = table_data
        #     continue

        if "집행기관" in head_line_text:
            dict_detail['집행기관'] = table_data
            continue

        if "담당자정보" in head_line_text:
            dict_detail['담당자정보'] = table_data

    # 최저입찰가
    bid_price_text: str = driver.find_element(by=By.CSS_SELECTOR,
                                                   value="#Contents > div.form_wrap.mt20.mb10 > \
                                                          div.check_wrap.fr > dl > dd > em").text
    ipchal_price = re.split(",", bid_price_text)
    bid_price: str = ""
    for ipchal in ipchal_price:
        bid_price += ipchal
    #
    # p = re.compile(r'[\d]{1,3}')
    # m: list = p.findall(bid_price_text)
    # bid_price: str = ""
    # for text in m:
    #     bid_price += text
    dict_detail['최저입찰가'] = bid_price
    print(dict_detail)
    return dict_detail