
from setup import *

class gongo_data():
    def __init__(self, index):
        self.index = index
        self.tbody = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > table > tbody")
        self.tr = self.tbody.find_element(by=By.CSS_SELECTOR, value=f"tr:nth-child({index})")
        self.gonggo_basic = {
            'ANNOUNCE_NO': "",  # 공고번호
            'TITLE': "",  # 공고명
            'TAG': [],  # 태그
            'ORGAN_NAME': "",  # 기관명
            'EXE_PART': "",  # 담당부점
            'GONGGO_DATE': "",  # 공고일자(년월일)
            'START_YMD': "",  # 입찰시작일시 (년월일)
            'START_HM': "",  # 입찰시작일시 (시분)
            'END_YMD': "",  # 입찰마감일시 (년월일)
            'END_HM': "",  # 입찰마감일시 (시분)
            'GAECHAL_YMD': "",  # 개찰일시 (년월일)
            'GAECHAL_HM': ""  # 개찰일시 (시분)
        }

    def get_summary_data(self):
        tds: list = self.tr.find_elements(By.TAG_NAME, "td")
        self.gonggo_basic['ANNOUNCE_NO'] = tds[0].find_element(By.TAG_NAME, "dt").text
        self.gonggo_basic['TITLE'] = tds[0].find_element(By.TAG_NAME, "dd").text
        badge: WebElement = tds[0].find_element(By.CSS_SELECTOR, "dl > dd.badge_wrap.mt5")
        self.gonggo_basic['TAG'] = re.split(r'\n', badge.text)

        list_data: list = re.split(r'\n', tds[1].text)
        self.gonggo_basic['ORGAN_NAME'] = list_data[0]
        if len(list_data) == 2:
            self.gonggo_basic['EXE_PART'] = list_data[1][1:-1]

        self.gonggo_basic['GONGGO_DATE'] = tds[2].text

        YMD: list = re.findall(r'[\d]{4}-[\d]{2}-[\d]{2}', tds[3].text)
        HM: list = re.findall(r'[\d]{2}:[\d]{2}', tds[3].text)
        if len(YMD) == 2:
            self.gonggo_basic['START_YMD'] = YMD[0]
            self.gonggo_basic['START_HM'] = HM[0]
            self.gonggo_basic['END_YMD'] = YMD[1]
            self.gonggo_basic['END_HM'] = HM[1]
        elif len(YMD) == 1:
            self.gonggo_basic['END_YMD'] = YMD[0]
            self.gonggo_basic['END_HM'] = HM[0]
        if not tds[4].text == "":
            list_data: list = re.split(r' ', tds[4].text)
            self.gonggo_basic['GAECHAL_YMD'] = list_data[0]
            self.gonggo_basic['GAECHAL_HM'] = list_data[1]

    def get_detail_data(self):
        a = 1

    def open_detail_newtab_and_move(self):
        '''

        :return:
        '''
        target = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(7) > a").get_attribute("onclick")
        driver.execute_script(target)
        driver.switch_to_window(driver.window_handles[1])

    def get_ipchal_number(self):
        '''
        :return: 회차, 차수, 개찰일시를 비교하여 입찰번호를 얻는다.
        '''
        if is_element_presence(By.CSS_SELECTOR, "#Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel > table > tbody"):
            tbody = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel > table > tbody")
            try:
                trs = tbody.find_elements(by=By.TAG_NAME, value="tr")
                for tr in trs:
                    tds = tr.find_elements(by=By.TAG_NAME, value="td")
                    m = re.split(r'/', tds[0].text)
                    if (m[0] == self.dict_ipchal_result_info['회차'] and m[1] == self.dict_ipchal_result_info['차수'] and
                            tds[3].text == self.dict_ipchal_result_info['개찰일시']):
                        self.dict_ipchal_result_info['입찰번호'] = tds[1].text
                        break

            except Exception as e :
                logging.exception(e)

    def open_gonggo_detail(self):
        '''
        물건번호를 클릭해 입찰 이력을 연다.
        :return: None
        '''
        if is_element_presence(By.CSS_SELECTOR, f"#Contents > table > tbody > tr:nth-child({self.index}) > td:nth-child(1) > dl > dt > a"):
            self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(1) > dl > dt > a").click()

    def run(self):
        self.get_summary_data()
        print(self.gonggo_basic)
        # self.open_gonggo_detail()
        # open_gonggo_mulgun_table_tab()