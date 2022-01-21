
from setup import *

class gongo_data():
    def __init__(self, index):
        self.index = index
        self.tbody = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > table > tbody")
        self.tr = self.tbody.find_element(by=By.CSS_SELECTOR, value=f"tr:nth-child({index+1})")
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
        self.dict_gonggo: dict = {  # 공고 상세
            '공고명': "",
            '공고종류': "",
            '공고일자': "",
            '공고회차': "",
            '공고번호': "",
            '처분방식': "",
            '자산구분': "",
            '공고기관': "",
            '담당자': "",
            '공고문 전문': "",
            '첨부파일': [],
            '입찰구분': "",
            '입찰방식': "",
            '경쟁방식': "",
            '총액/단가구분': "",
            '입찰가공개여부': "",
            '참가수수료': "",
            '참가자격': "",
            '입찰일시및장소': []
        }
        self.dict_gonggo_table: dict = {  # 입찰일시 및 장소
            '회차': "",
            '차수': "",
            '입찰보증금율': "",
            '현장입찰시작년도': "",
            '현장입찰시작시간': "",
            '입찰시작년도': "",
            '입찰시작시간': "",
            '입찰마감년도': "",
            '입찰마감시간': "",
            '개찰년도': "",
            '개찰시간': "",
            '매각결정년도': "",
            '매각결정시간': "",
            '개찰장소': ""
        }

    def get_summary_data(self):
        tds: list = self.tr.find_elements(By.TAG_NAME, "td")
        self.gonggo_basic['ANNOUNCE_NO'] = tds[0].find_element(By.TAG_NAME, "dt").text
        self.gonggo_basic['TITLE'] = tds[0].find_element(By.TAG_NAME, "dd").text
        badge: WebElement = tds[0].find_element(By.CSS_SELECTOR, "dl > dd.badge_wrap.mt5")
        self.gonggo_basic['TAG'] = re.split(r'\n', badge.text)

        list_data: list = re.split(r'\n', tds[1].text)
        #기관명
        self.gonggo_basic['ORGAN_NAME'] = list_data[0]
        if len(list_data) == 2:
            self.gonggo_basic['EXE_PART'] = list_data[1][1:-1]

        self.gonggo_basic['GONGGO_DATE'] = tds[2].text

        #입찰기간
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

    def open_detail_newtab_and_move(self):
        '''

        :return:
        '''
        target = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(7) > a").get_attribute("onclick")
        driver.execute_script(target)
        driver.switch_to_window(driver.window_handles[1])

    def open_gonggo_detail(self):
        '''
        물건번호를 클릭해 입찰 이력을 연다.
        :return: None
        '''
        if is_element_presence(By.CSS_SELECTOR, f"#Contents > table > tbody > tr:nth-child({self.index+1}) > td:nth-child(1) > dl > dt > a"):
            self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(1) > dl > dt > a").click()

    def scan_gonggo_data(self) -> None:
        """
        공고 상세 페이지.
        :return:
        """
        dict_gonggo: dict = self.dict_gonggo.copy()
        dict_gonggo['공고명'] = driver.find_element(by=By.CSS_SELECTOR,
                                                      value="#Contents > div.top_wrap2.pos_rel >\
                                                      div.op_top_head_wrap.pos_rel > h4 > strong").text

        # 공고 테이블
        if is_element_presence(By.CSS_SELECTOR, "#Contents > div.top_wrap2.pos_rel > table > tbody > tr"):
            table: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                         value="#Contents > div.top_wrap2.pos_rel > table")
            tbody: WebElement = table.find_element(by=By.TAG_NAME, value="tbody")
            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")

            for tr in trs:
                tr: WebElement
                ths: list = tr.find_elements(by=By.TAG_NAME, value="th")
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")

                for i in range(len(tds)):
                    header: str = ths[i].text
                    body: str = tds[i].text

                    if '공고종류' in header:
                        dict_gonggo['공고종류'] = body

                    if '공고일자' in header:
                        dict_gonggo['공고일자'] = body

                    if '공고회차' in header:
                        dict_gonggo['공고회차'] = body

                    if '공고번호' in header:
                        dict_gonggo['공고번호'] = body

                    if '처분방식' in header:
                        dict_gonggo['처분방식'] = body

                    if '자산구분' in header:
                        dict_gonggo['자산구분'] = body

                    if '공고기관' in header:
                        dict_gonggo['공고기관'] = body

                    if '경쟁방식' in header:
                        dict_gonggo['경쟁방식'] = body

                    if '담당자정보' in header:
                        dict_gonggo['담당자정보'] = body

        # 공고문 전문
        if is_element_presence(By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt10 > div > div > div"):
            gonggo_text: str = driver.find_element(by=By.CSS_SELECTOR,
                                                        value="#tab_01 > div.op_bid_twrap.mt10 > div > div > div").text
            dict_gonggo['공고문 전문'] = gonggo_text

        # 첨부파일
        if is_element_presence(By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt15 > div"):
            file_body: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                             value="#tab_01 > div.op_bid_twrap.mt15 > div")
            file_list: list = file_body.find_elements(by=By.TAG_NAME, value="a")
            chumbu_list: list = []
            for file in file_list:
                file: WebElement
                dict_chumbu: dict = self.dict_ipchal_chumbu.copy()

                text: str = file.text
                href: str = file.get_attribute('href')
                dict_chumbu['파일명'] = text
                dict_chumbu['href'] = href
                chumbu_list.append(dict_chumbu)

            dict_gonggo['첨부파일'] = chumbu_list

        # 입찰이력
        if is_element_presence(By.CSS_SELECTOR, "#Contents > ul > li:nth-child(2) > a"):
            ipchal_info_button: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                                      value="#Contents > ul > li:nth-child(2) > a")
            try:
                ipchal_info_button.click()
            except selenium.common.exceptions.ElementClickInterceptedException:
                ipchal_info_button.click()

            tbody: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                         value="#tab_02 > div:nth-child(1) > table > tbody")
            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")

            for tr in trs:
                tr: WebElement
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                ths: list = tr.find_elements(by=By.TAG_NAME, value="th")

                for i in range(len(ths)):
                    head: str = ths[i].text
                    main: str = tds[i].text

                    if '입찰구분' in head:
                        dict_gonggo['입찰구분'] = main

                    if '입찰방식/경쟁방식' in head:
                        index: int = main.find('(')
                        dict_gonggo['경쟁방식'] = main[:index]
                        dict_gonggo['입찰방식'] = main[index+1:-1]

                    if '총액/단가구분' in head:
                        dict_gonggo['총액/단가구분'] = main

                    if '입찰가공개여부' in head:
                        dict_gonggo['입찰가공개여부'] = main

                    if '참가수수료' in head:
                        dict_gonggo['참가수수료'] = main

                    if '참가자격' in head:
                        dict_gonggo['참가자격'] = main

        # 입찰일시 및 장소
        if is_element_presence(By.CSS_SELECTOR, "#tab_02 > div:nth-child(2) > div > table > tbody"):
            element_locate_wait(By.CSS_SELECTOR, "#tab_02 > div:nth-child(2) > div > table > thead")
            thead: WebElement = driver.find_element(by=By.CSS_SELECTOR, value="#tab_02 > div:nth-child(2) > div > table > thead")
            ths = thead.find_elements(by=By.TAG_NAME, value="th")
            tbody: WebElement = driver.find_element(by=By.CSS_SELECTOR,
                                                         value="#tab_02 > div:nth-child(2) > div > table > tbody")
            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")
            gonggo_table_list: list = []
            for tr in trs:
                tr: WebElement
                if '없습니다' in tr.text:
                    break
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                dict_gonggo_table: dict = self.dict_gonggo_table.copy()
                for i in range(len(ths)):
                    if tds[i].text == "~" or tds[i].text == "" or tds[i].text == "-":
                        continue

                    if '/' in ths[i].text:
                        th_split = re.split('/',ths[i].text)
                        td_split = re.split('/',tds[i].text)
                        dict_gonggo_table[th_split[0]] = td_split[0]
                        dict_gonggo_table[th_split[1]] = td_split[1]

                    elif "보증금" in ths[i].text:
                        dict_gonggo_table['입찰보증금율'] = tds[i].text

                    elif ths[i].text == '입찰기간':
                        text_data: str = tds[i].text
                        p: re.Pattern = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
                        list_data: list = p.findall(text_data)
                        dict_gonggo_table['입찰시작년도'] = list_data[0]
                        dict_gonggo_table['입찰마감년도'] = list_data[1]
                        p: re.Pattern = re.compile(r'[\d]{2}:[\d]{2}')
                        list_data: list = p.findall(text_data)
                        dict_gonggo_table['입찰시작시간'] = list_data[0]
                        dict_gonggo_table['입찰마감시간'] = list_data[1]


                    elif ths[i].text == "현장입찰기간":
                        text_data = tds[i].text
                        hyunjang_start_YMD = re.findall('[\d]{4}-[\d]{2}-[\d]{2}',text_data)
                        dict_gonggo_table['현장입찰시작년도'] = hyunjang_start_YMD[0]
                        hyunjang_start_HM = re.findall('[\d]{2}:[\d]{2}',text_data)
                        dict_gonggo_table['현장입찰시작시간'] = hyunjang_start_HM[0]

                    elif ths[i].text == "현장입찰장소":
                        dict_gonggo_table['현장입찰장소'] = tds[i].text

                    elif ths[i].text == "개찰일시":
                        text_data: str = tds[i].text
                        p: re.Pattern = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
                        list_data: list = p.findall(text_data)
                        dict_gonggo_table['개찰년도'] = list_data[0]
                        p: re.Pattern = re.compile(r'[\d]{2}:[\d]{2}')
                        list_data: list = p.findall(text_data)
                        dict_gonggo_table['개찰시간'] = list_data[0]

                    elif "개찰장소" in ths[i].text:
                        text_data: str = tds[i].text
                        dict_gonggo_table['개찰장소'] = text_data

                # todo 매각결정년도
                #dict_gonggo_table['매각결정년도'] = list_data[1]


                #dict_gonggo_table['매각결정시간'] = list_data[1]

                gonggo_table_list.append(dict_gonggo_table)

            dict_gonggo['입찰일시및장소'] = gonggo_table_list

        return dict_gonggo

    def run(self):
        self.get_summary_data()

        self.open_gonggo_detail()
        print(json.dumps(self.gonggo_basic, indent=2, ensure_ascii=False))
        gonggo_data = self.scan_gonggo_data()
        print(json.dumps(gonggo_data, indent=2, ensure_ascii=False))
        # self.open_gonggo_detail()
        # open_gonggo_mulgun_table_tab()