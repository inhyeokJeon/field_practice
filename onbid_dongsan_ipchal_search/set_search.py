from setup import *

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
        start_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchBidDateFrom")
        end_text = driver.find_element(by=By.CSS_SELECTOR, value="#searchBidDateTo")
        start_text.clear()
        end_text.clear()

        start_text.send_keys(self.start_date)
        end_text.send_keys(self.end_date)

        driver.find_element(by=By.CSS_SELECTOR, value="#searchBtn").click()

    def set_order_and_click(self):
        '''
        100줄씩 보기 정렬을 하고 정렬을 누른다.
        :return:
        '''
        element_click_wait(By.CSS_SELECTOR, "#pageUnit > option:nth-child(4)")
        search_btn = driver.find_element(by=By.CSS_SELECTOR, value="#pageUnit > option:nth-child(4)")
        search_btn.click()

        element_click_wait(By.CLASS_NAME, "cm_btn_tnt")
        driver.find_element(by=By.CLASS_NAME, value="cm_btn_tnt").click()

    def run(self):

        self.set_date()
        if self.start_date > self.today_date:
            return True

        self.insert_date_and_click()

        self.set_order_and_click()

        return False