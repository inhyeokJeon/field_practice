
from setup import *

dict_summary: dict = {  # 물건 기본정보.
    '물건관리번호': "",
    '물건이름': "",
    '중분류카테고리': "",
    '소분류카테고리': "",
    '소재지': "",
    '태그': "",
    '연식': "",
    '주행거리': "",
    #'연료': "",
    '입찰': "",
    '개찰': "",
    "회차": "",
    "차수": "",
    '최저입찰가': "",
    '최초감정가': "",
    '최저입찰가율': "",
    '물건상태': "",
    '유찰횟수': "",
    '조회수': ""
}

def get_summary_data(index) -> dict:
    """
    물건 요약 정보 dict 형태로 반환.
    :param tds: 물건 열 정보.
    :return: 물건 정보.
    """
    tr = driver.find_element(by=By.CSS_SELECTOR, value=f"#frm > div > div.popup_container > table > tbody > tr:nth-child({index+1})")
    tds = tr.find_elements(by=By.TAG_NAME, value="td")
    dict_summary_copy = dict_summary.copy()
    #tds = tr.find_elements(by=By.TAG_NAME, value="td")
    # 물건정보 선택.

    info = tds[0].find_element(by=By.CLASS_NAME, value="info")
    mulgun = info.find_element(by=By.TAG_NAME, value="dt").text  # 물건관리번호.
    dict_summary_copy["물건관리번호"] = mulgun

    fwb = info.find_element(by=By.CSS_SELECTOR, value="dd:nth-child(2)").text  # 물건 이름.
    dict_summary_copy["물건이름"] = fwb

    tpoint_03 = info.find_element(by=By.CLASS_NAME, value="tpoint_03").text  # 카테고리
    # " / "기준 나누기
    category = re.split("\s.\s", tpoint_03[1:-1])

    dict_summary_copy["중분류카테고리"] = category[0]
    dict_summary_copy["소분류카테고리"] = category[1]
    if category[0] == "토지" or category[0] =="주거용건물" or category[0] =="상가용및업무용건물" or category[0] =='산업용및기타특수용건물' or category[0]=='용도복합용건물' :
        return
    # 소재지
    # try:
    #     sozazi: str = info.find_element(by=By.CSS_SELECTOR, value="dd:nth-child(4) > span").text
    #     dict_summary_copy['소재지'] = sozazi[1:-1]
    # except:
    #     print("소재지없음")


    if (category[0] == '자동차'):
        #frm > div > div.popup_container > table > tbody > tr > td.al.pos_rel > div > dl > span:nth-child(4)
        dict_summary_copy['연식'] = info.find_element(by=By.CSS_SELECTOR,
                                                    value="span:nth-child(4)").text[3:-1]
        #frm > div > div.popup_container > table > tbody > tr > td.al.pos_rel > div > dl > span:nth-child(6)
        dict_summary_copy['주행거리'] = info.find_element(by=By.CSS_SELECTOR,
                                                      value="span:nth-child(6)").text[5:-1]
        # dict_summary_copy['연료'] = info.find_element(by=By.CSS_SELECTOR,
        #                                             value="dd:nth-child(5) > span:nth-child(5)").text[1:-1]

    # 물건정보 -> 매각, 임대 / 경쟁.
    badge_wrap = info.find_element(by=By.CLASS_NAME, value="badge_wrap.mt5")
    badges = badge_wrap.find_elements(by=By.TAG_NAME, value="em")
    badge_list: list = []

    for badge in badges:
        badge_str: str = badge.text
        badge_list.append(badge_str)

    dict_summary_copy['태그'] = badge_list

    # 입찰기간
    bid_dates: str = tds[1].text
    p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
    m = p.findall(bid_dates)
    if len(m) == 2:
        dict_summary_copy['입찰'] = m[0]
        dict_summary_copy['개찰'] = m[1]
    elif len(m) == 1:
        dict_summary_copy['개찰'] = m[0]

    #회차/차수
    hweicha = tds[2].text
    m = re.split('/', hweicha)
    dict_summary_copy['회차'] = m[0]
    dict_summary_copy['차수'] = m[1]

    # 최저입찰가(원), 감정가-최초예정가(원), 최저입찰가율(%)
    bid_rates: str = tds[3].text
    bid_rate: list = bid_rates.split('\n')
    if len(bid_rate) == 3 :
        bid_price_low = re.sub(',', '', bid_rate[0])
        dict_summary_copy['최저입찰가'] = bid_price_low

        bid_price_first = re.sub(',', '', bid_rate[1])
        dict_summary_copy['최초감정가'] = bid_price_first

        dict_summary_copy['최저입찰가율'] = bid_rate[2]
    elif len(bid_rate) == 2:
        bid_price_low = re.sub(',', '', bid_rate[0])
        dict_summary_copy['최저입찰가'] = bid_price_low

        bid_price_first = re.sub(',', '', bid_rate[1])
        dict_summary_copy['최초감정가'] = bid_price_first
    elif len(bid_rate) == 1:
        bid_price_low = re.sub(',', '', bid_rate[0])
        dict_summary_copy['최저입찰가'] = bid_price_low

    # 물건상태, 유찰횟수
    state_count: list = tds[4].text.split('\n')

    state: str = state_count[0]
    dict_summary_copy['물건상태'] = state

    count: str = state_count[1]
    p = re.compile(r'[\d]+')
    m = p.findall(count)
    dict_summary_copy['유찰횟수'] = m[0]

    # 조회수.
    look: str = tds[5].text
    dict_summary_copy['조회수'] = look
    print(dict_summary_copy)

    return dict_summary_copy