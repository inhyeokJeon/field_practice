import logging
import re
import os
import sys
import time
import json
import requests
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

def element_click_wait(by_type, locator: str) -> None:
    """
    클릭하고 싶은 element에 대한 예외처리.
    :param by_type:
    :param locator:
    :return:
    """
    #print(f"element_click_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver, 5, poll_frequency=0.01).until(EC.element_to_be_clickable((by_type, locator)))
        return

    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        driver.close()
        sys.exit()

def element_locate_wait(by_type, locator: str) -> None:
    """
    가져오고 싶은 element에 대한 예외처리.
    :param by_type:
    :param locator:
    :return:
    """
    #print(f"element_locate_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver, 5, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        # driver.close()
        sys.exit()

def element_visible_wait(by_type, locator: str) -> None:
    """
    가져오고 싶은 element에 대한 예외처리.
    :param by_type:
    :param locator:
    :return:
    """
    #print(f"element_visible_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver, timeout=5, poll_frequency=0.01).until(EC.visibility_of_element_located((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        # driver.close()
        sys.exit()

def is_element_presence(by_type, locator: str) -> bool:
    """
    데이터가 존재하는지 체크.
    :param by_type:
    :param locator:
    :return: 존재 유무
    """
    try:
        WebDriverWait(driver, timeout=3, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        #print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 존재")
        return True
    except selenium.common.exceptions.TimeoutException:
        #print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 비존재")
        return False

def set_newtab_javascript():
    driver.execute_script("""
        up_window = window.open;
            window.open = function openWindow(url, blank){
                up_window(url, "_blank").focus();
            }
        """
    )

def set_open_new_window_to_tap():
    driver.execute_script("""
    
    up_window = window.open;
    window.open = function openWindow(url, blank){
        up_window(url, "_blank").focus();
    }
    
    close_window = window.close;
    window.close = function closeWindow(){
        window.location.reload();
    }
    
""")

def get_total_page():

    try:
        paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")
    except:
        paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging")
    #Contents > div.cm_paging

    # 최대 페이지 번호 계산.
    total_page_text = paging.find_element(by=By.TAG_NAME, value="p").text

    total_number = int(re.sub(r'[^\d]+', "", total_page_text))
    total_page_number = str(int(total_number / 100) + 1)

    return total_page_number

def next_page():
    """
    다음 페이지로 이동.
    :return: 끝에 도달하면 True, 아니면 False
    """
    if not is_element_presence(By.CLASS_NAME, "active"):  # 현재 페이지번호 element가 존재하는지 검사.
        return True

    total_page_number = get_total_page()
    try :
        paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")
    except:
        paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging")
    # 페이지 길이, 현재 페이지 번호 계산.
    pages = paging.find_elements(by=By.TAG_NAME, value="a")
    page_count = len(pages)
    pre_page = paging.find_element(by=By.CLASS_NAME, value="active").text

    # 현재 페이지 번호가 최대 페이지 번호가 되면 True 반환.
    if total_page_number == pre_page:
        return True

    # 다음 페이지로 이동.
    for i in range(page_count):
        if pages[i].text == pre_page:
            pages[i + 1].click()
            return False

def open_gonggo_mulgun_table_tab():
    set_newtab_javascript()

    element_click_wait(By.CSS_SELECTOR,
                       "#Contents > div.top_wrap2.pos_rel > div.top_detail_btns > p > a:nth-child(1)")
    driver.find_element(By.CSS_SELECTOR,
                        "#Contents > div.top_wrap2.pos_rel > div.top_detail_btns > p > a:nth-child(1)").click()

    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[1])
    assert "온비드" in driver.title

def open_mulgun_detail_tab(mulgun_index: int):
    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[1])
    assert "온비드" in driver.title
    set_open_new_window_to_tap()

    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    body = table.find_element(by=By.TAG_NAME, value="tbody")

    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    tds = trs[mulgun_index].find_elements(by=By.TAG_NAME, value="td")

    target: WebElement = tds[0].find_element(by=By.CSS_SELECTOR, value="div > dl > dt > a")

    target.click()

    main = driver.window_handles
    assert len(main) == 2

    driver.switch_to.window(main[0])
    assert "물건검색" in driver.title

def close_mulgun_detail_tab():
    main = driver.window_handles
    assert len(main) == 2
    driver.switch_to.window(main[1])
    assert "온비드" in driver.title

def close_popup() -> None:
    """
    메인창을 제외한 창 닫기
    :param driver:
    :return:
    """
    main: list = driver.window_handles
    for handle in main:
        handle: str
        if handle != main[0]:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(main[0])

def close_gonggo_mulgun_table_tab():
    close_popup()
    assert "공고목록" in driver.title

def set_order_and_click():
    '''
    100줄씩 보기 정렬을 하고 정렬을 누른다.
    :return:
    '''

    element_click_wait(By.CSS_SELECTOR, "#pageUnit > option:nth-child(4)")
    search_btn = driver.find_element(by=By.CSS_SELECTOR, value="#pageUnit > option:nth-child(4)")
    search_btn.click()

    element_click_wait(By.CLASS_NAME, "cm_btn_tnt")
    driver.find_element(by=By.CLASS_NAME, value="cm_btn_tnt").click()

def is_table_end(elem_index: int) -> bool:
    """
    스캔되지 않은 테이블 element 존재하는지 검사.
    :param driver:
    :param elem_index:
    :return:
    """
    # 테이블 선택.
    element_locate_wait(By.CLASS_NAME, "op_tbl_type1")
    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    # 테이블 바디 선택.
    body = table.find_element(by=By.TAG_NAME, value="tbody")

    # 테이블 행 선택.
    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    if elem_index >= len(trs):
        return True

    if "없습니다" in trs[0].text:
        return True

    return False

def is_cancel_gonggo(elem_index: int) -> bool:

    element_locate_wait(By.CSS_SELECTOR,
                        f'#Contents > table > tbody > tr:nth-child({elem_index+1})\
                         > td.al.pos_rel > dl > dd.badge_wrap.mt5')

    badge = driver.find_element(By.CSS_SELECTOR, "#Contents > table > tbody > tr:nth-child(" +
                                f'{elem_index+1}' + ") > td.al.pos_rel > dl > dd.badge_wrap.mt5")

    str_data: str = badge.find_element(By.TAG_NAME, value="em").text

    if "취소공고" in str_data:
        return True

    return False

def handle_alert() -> bool:
    """
    팝업 데이터 유무 판별.
    :return:
    """
    try:
        WebDriverWait(driver, 1, poll_frequency=0.01).until(EC.alert_is_present(), "팝업 대기")
        alert = driver.switch_to.alert
        alert.accept()
        main = driver.window_handles
        driver.switch_to.window(main[0])
        #print("handle_alert 함수 호출 결과 : 데이터 비존재.")
        return False
    except selenium.common.exceptions.TimeoutException:
        #print("handle_alert 함수 호출 결과 : 데이터 존재.")
        return True

def gonggo_detail_click(gonggo_index: int):
    table = driver.find_element(by=By.CLASS_NAME, value="op_tbl_type1")

    body = table.find_element(by=By.TAG_NAME, value="tbody")

    trs = body.find_elements(by=By.TAG_NAME, value="tr")

    tds = trs[gonggo_index].find_elements(by=By.TAG_NAME, value="td")

    tds[0].find_element(by=By.CSS_SELECTOR, value="dl > dt > a").click()
    #Contents > table > tbody > tr:nth-child(1) > td.al.pos_rel > dl > dt > a

