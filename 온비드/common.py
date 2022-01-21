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

def element_locate_wait(self, by_type, locator: str) -> None:
    """
    가져오고 싶은 element에 대한 예외처리.
    :param by_type:
    :param locator:
    :return:
    """
    print(f"element_locate_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(self.driver, 5, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        # self.driver.close()
        sys.exit()

def element_visible_wait(self, by_type, locator: str) -> None:
    """
    가져오고 싶은 element에 대한 예외처리.
    :param by_type:
    :param locator:
    :return:
    """
    print(f"element_locate_wait 함수 호출 ({by_type}, {locator})")
    try:
        WebDriverWait(driver=self.driver, timeout=5, poll_frequency=0.01).until(EC.visibility_of_element_located((by_type, locator)))
        return
    except selenium.common.exceptions.TimeoutException:
        print(str(by_type) + str(locator) + " Timeout Error")
        # self.driver.close()
        sys.exit()

def is_element_presence(self, by_type, locator: str) -> bool:
    """
    데이터가 존재하는지 체크.
    :param by_type:
    :param locator:
    :return: 존재 유무
    """

    try:
        WebDriverWait(self.driver, 1, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
        print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 존재")
        return True
    except selenium.common.exceptions.TimeoutException:
        print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 비존재")
        return False