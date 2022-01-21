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

if self.is_element_presence(By.CSS_SELECTOR, "tbody#resultPbctlList"):
    tbody: WebElement = main_element.find_element(by=By.ID, value="resultPbctlList")

    if tbody.is_displayed():
        try:
            WebDriverWait(driver=self.driver, timeout=2, poll_frequency=0.1).\
                until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody#resultPbctlList > tr")))
        except selenium.common.exceptions.TimeoutException:
            print("회차별 입찰 정보 Time Out...")
            self.driver.close()
            self.driver.quit()
            sys.exit()

        trs = tbody.find_elements(by=By.TAG_NAME, value="tr")
        hweicha_list: list = []
        for tr in trs:
            if "없습니다" in tr.text:
                break
            dict_hweicha: dict = self.dict_hweicha.copy()
            tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
            dict_hweicha['입찰번호'] = tds[0].text
            p = re.compile(r'[\d]+')
            m = p.findall(tds[1].text)
            dict_hweicha['회차'] = m[0]
            dict_hweicha['차수'] = m[1]
            dict_hweicha['구분'] = tds[2].text
            dict_hweicha['대금납부'] = tds[3].text.split('\n')[0][:-1]
            dict_hweicha['납부기한'] = tds[3].text.split('\n')[1]
            p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
            m = p.findall(tds[4].text)
            dict_hweicha['입찰시작기간'] = m[0]
            dict_hweicha['입찰종료기간'] = m[1]
            dict_hweicha['개찰일시'] = tds[5].text
            dict_hweicha['개찰장소'] = tds[6].text
            dict_hweicha['최저입찰가'] = tds[7].text
            hweicha_list.append(dict_hweicha)

        dict_ipchal_info['회차별입찰정보'] = hweicha_list