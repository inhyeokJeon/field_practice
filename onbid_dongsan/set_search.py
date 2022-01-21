from setup import *
from datetime import datetime, timedelta


class set_search_table():
    def __init__(self):
        #oldest_date = 2003-04-21
        #self.oldest_date = "2003-10-29" # 가장 오래된
        self.oldest_date = "2002-10-29"
        self.today_date = datetime.today().strftime("%Y-%m-%d")
        self.start_date = (datetime.strptime(self.oldest_date, "%Y-%m-%d")).strftime("%Y-%m-%d")
        self.end_date = (datetime.strptime(self.start_date, "%Y-%m-%d") + timedelta(365)).strftime("%Y-%m-%d")
        #test
        #self.end_date = (datetime.strptime(self.start_date, "%Y-%m-%d")).strftime("%Y-%m-%d")

    def set_date(self):
        '''
        시작과 끝의 날짜를 1년씩 더해준다.
        '''
        self.start_date = (datetime.strptime(self.start_date, "%Y-%m-%d")
                           + timedelta(365)).strftime("%Y-%m-%d")
        self.end_date = (datetime.strptime(self.end_date, "%Y-%m-%d")
                         + timedelta(365)).strftime("%Y-%m-%d")

    def insert_date_and_click(self):
        '''
        시작시간 종료시간을 입력하고 검색을 누른다.
        :return:
        '''
        ipchal_start_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchPbctBegnDtm")
        gonggo_start_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchBegnPlnmDt")

        ipchal_end_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchPbctClsDtm")
        gonggo_end_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchClsPlnmDt")

        ipchal_start_text.clear()
        ipchal_end_text.clear()
        gonggo_start_text.clear()
        gonggo_end_text.clear()

        gonggo_start_text.send_keys(self.start_date)
        gonggo_end_text.send_keys(self.end_date)

        element_click_wait(By.CSS_SELECTOR,
                       "#Contents > div.tab_wrap2.pos_re.mt20 > div.op_detail_show2 > div > a.cm_btn_w_o.ml3")
        driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.tab_wrap2.pos_re.mt20 > div.op_detail_show2 > div > a.cm_btn_w_o.ml3").click()

    def run(self):
        self.set_date()
        if self.start_date > self.today_date:
            return True

        self.insert_date_and_click()

        set_order_and_click()

        return False