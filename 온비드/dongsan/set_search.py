from setup import *
from datetime import datetime, timedelta


class set_search_table():
    def __init__(self):
        self.oldest_date = "2001-10-29" # 가장 오래된 물건
        self.today_date = datetime.today().strftime("%Y-%m-%d")
        self.start_date = (datetime.strptime(self.oldest_date, "%Y-%m-%d")
                           + timedelta(365)).strftime("%Y-%m-%d")
        self.end_date = (datetime.strptime(self.start_date, "%Y-%m-%d")
                         + timedelta(365)).strftime("%Y-%m-%d")

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
        start_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchPbctBegnDtm")
        end_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchPbctClsDtm")
        start_text.clear()
        end_text.clear()

        start_text.send_keys(self.start_date)
        end_text.send_keys(self.end_date)
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