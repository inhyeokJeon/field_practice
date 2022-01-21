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
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select

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
        # self.driver.close()
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
        # self.driver.close()
        sys.exit()

def is_element_presence(by_type, locator: str) -> bool:
    """
    데이터가 존재하는지 체크.
    :param by_type:
    :param locator:
    :return: 존재 유무
    """
    try:
        WebDriverWait(driver, 1, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        #print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 존재")
        return True
    except selenium.common.exceptions.TimeoutException:
        print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 비존재")
        return False

def set_newtab_javascript():
    driver.execute_script("""
        up_window = window.open;
            window.open = function openWindow(url, blank){
                up_window(url, "_blank").focus();
            }
        """
    )


def get_total_page():
    element_locate_wait(By.CLASS_NAME, "active")  # 현재 페이지번호 element가 존재하는지 검사.

    # page column 선택.
    paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")

    # 최대 페이지 번호 계산.
    total_page_text = paging.find_element(by=By.TAG_NAME, value="p").text

    total_number_list = total_page_text.split(' ')
    total_number = int(total_number_list[1])
    total_page_number = str(int(total_number / 100) + 1)

    return total_page_number

def next_page():
    """
    다음 페이지로 이동.
    :return: 끝에 도달하면 True, 아니면 False
    """
    total_page_number = get_total_page()
    paging = driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")
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