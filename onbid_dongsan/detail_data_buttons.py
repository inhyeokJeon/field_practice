from setup import *

dict_chumbu_temp: dict = {  # 첨부파일 갯수.
            '사진': "0",
            '감정평가서': {}
            # '사고이력': {}
        }

def detail_data_buttons() -> dict:
    """
    사진, 감정평가서, 클릭하여 데이터 얻기.
    :return: 첨부파일 갯수
    """
    element_locate_wait(By.CLASS_NAME, "visual_inner")
    visual_inner = driver.find_element(by=By.CLASS_NAME, value="visual_inner")

    btn_vway = visual_inner.find_element(by=By.CLASS_NAME, value="btn_vway")  # 첫번째 행.

    first_rows = btn_vway.find_elements(by=By.TAG_NAME, value="a")  # 첫번째 행 버튼들.

    # 물건관리번호
    try:
        if is_element_presence(By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")
    except Exception as e:
        logging.exception(e, "물건관리번호못받음")

    mulgun_number: str = tab_wrap.find_element(
        by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text
    # 버튼들 선택.
    photo = first_rows[0]  # 사진

    # 사진 데이터 팝업창.
    photo_count = handle_photo(photo, mulgun_number)

    # 감정 평가서 데이터.
    dict_gamjung: dict = {
        "첨부파일갯수": "0",
        "href": []
    }
    href_list: list = []
    gamjung_count: int = 0

    element_click_wait(By.ID, "btn_downview")
    driver.find_element(by=By.ID, value="btn_downview").click()

    if handle_alert():
        files = driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")
        gamjung_count = len(files)

        for file in files:
            href: str = file.get_attribute("href")
            href_list.append(href)

    dict_gamjung["첨부파일갯수"] = gamjung_count
    dict_gamjung["href"] = href_list

    dict_chumbu: dict = dict_chumbu_temp.copy()
    dict_chumbu['사진'] = photo_count
    dict_chumbu['감정평가서'] = dict_gamjung
    print(dict_chumbu)
    return dict_chumbu

def handle_photo(photo, mulgun_number: str) -> int:
    """
    사진 데이터 다운로드.
    저장형식 : 물건번호_번호.JPG
    저장위치 : ./img
    :param mulgun_number:
    :param photo:
    :return: 사진 갯수.
    """
    set_newtab_javascript()
    try:
        photo.click()
        handle_alert()
    except selenium.common.exceptions.ElementClickInterceptedException:
        photo.click()
        handle_alert()

    main = driver.window_handles
    count = 0
    if len(main) == 2:
        driver.back()
        return count

    driver.switch_to.window(main[2])

    # 사진 갯수
    set_newtab_javascript()

    element_visible_wait(By.CLASS_NAME, "conList")
    conList = driver.find_element(by=By.CLASS_NAME, value="conList")
    photo_list = conList.find_elements(by=By.TAG_NAME, value="li")
    length = len(photo_list)
    current = 1
    for elem in photo_list:
        count = count + 1
        elem.find_element(by=By.TAG_NAME, value="a").click()
        element_click_wait(By.CSS_SELECTOR,
                                "#frm > div > div.popup_container > div > div.pop_viewer > a > img")

        driver.find_element(by=By.CSS_SELECTOR,
                                 value="#frm > div > div.popup_container > div > div.pop_viewer > a > img").click()
        sub = driver.window_handles
        driver.switch_to.window(sub[3])
        element_locate_wait(By.TAG_NAME, "img")
        photo_url = driver.find_element(by=By.TAG_NAME, value="img").get_attribute("src")

        try:
            response = requests.get(url=photo_url, stream=True)
        except requests.exceptions.SSLError:
            response = requests.get(url=photo_url, stream=True)
        except requests.exceptions.ConnectionError:
            response = requests.get(url=photo_url, stream=True)

        if response.status_code == 200:
            with open(f"./img/{mulgun_number}_photo_{str(current)}.JPG", 'wb') as f:
                f.write(response.content)
        else:
            try:
                response = requests.get(url=photo_url, stream=True)
            except requests.exceptions.SSLError:
                response = requests.get(url=photo_url, stream=True)
            except requests.exceptions.ConnectionError:
                response = requests.get(url=photo_url, stream=True)

            if response.status_code == 200:
                with open(f"./img/{mulgun_number}_photo_{str(current)}.JPG", 'wb') as f:
                    f.write(response.content)
            else:
                print("IMAGE DOWNLOAD ERROR")
                sys.exit()

        driver.close()
        driver.switch_to.window(sub[2])
        if current > 3 and current != length:
            element_click_wait(By.CLASS_NAME, "btn_down")
            driver.find_element(by=By.CLASS_NAME, value="btn_down").click()
        current = current + 1

    driver.close()
    driver.switch_to.window(main[0])
    driver.back()
    return count