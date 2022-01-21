import logging

from setup import *

class ipchal_result_data():
    def __init__(self, index):
        self.index = index
        self.tbody = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > table > tbody")
        self.tr = self.tbody.find_element(by=By.CSS_SELECTOR, value=f"tr:nth-child({index})")
        self.dict_ipchal_result_info = {
            "물건관리번호": "",
            "물건명": "",
            "최저입찰가": "",
            "낙찰가": "",
            "낙찰가율": "",
            "입찰결과": "",
            "개찰일시": "",
            #-------상세보기
            "기관명": "",
            #"물건명": "",
            "공고번호": "",
            "회차": "",
            "차수": "",
            "처분방식": "",
            "입찰방식": "",
            "경쟁방식": "",
            "입찰시작기간": "",
            "입찰종료기간": "",
            "총액/단가": "",
            "개찰시작일시": "",
            "집행완료일시": "",
            "유효입찰자수": "",
            "무효입찰자수": "",
            "개찰결과": "",
            "2인 미만 유찰여부": "",
            "유찰/취소사유": "",
            "감정가": "",
            "입찰금액": "",
            "낙찰금액": "",
            "낙찰가율(감정가 대비)": "",
            "낙찰가율(최저입찰가 대비)": "",
            "입찰번호": "",
            "재산구분": "",
            "담당부점": "",
            #-------------------
            '대금납부기한': "",
            '납부여부': "",
            '납부촉구(최고)기한': "",
            '배분기일': "",
            'button_exist' : False
        }

    def get_summary_data(self):
        self.dict_ipchal_result_info['물건관리번호'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(1) > div > dl > dt > a").text
        self.dict_ipchal_result_info['물건명'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(1) > div > dl > dt > em").text
        self.dict_ipchal_result_info['최저입찰가'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(2)").text
        self.dict_ipchal_result_info['낙찰가'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(3)").text
        self.dict_ipchal_result_info['낙찰가율'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(4)").text
        self.dict_ipchal_result_info['입찰결과'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(5)").text
        self.dict_ipchal_result_info['개찰일시'] = self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(6)").text

    def get_detail_data(self):
        '''
        상세보기란의 데이터들을 dict 에 저장
        :return:
        '''
        #----check
        check = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container")
        check_table_count = check.find_elements(by=By.TAG_NAME, value="h4")
        #----check
        element_visible_wait(By.CSS_SELECTOR,"body > div > div.popup_container > table")
        table = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container > table")

        ths = table.find_elements(by=By.TAG_NAME, value="th")
        tds = table.find_elements(by=By.TAG_NAME, value="td")
        for i in range(len(ths)):
            th_text = ths[i].text
            td_text = tds[i].text
            if td_text == '-':
                continue

            if "물건관리번호" in th_text:
                self.dict_ipchal_result_info['물건관리번호'] = td_text
                continue
            elif "기관명" in th_text:
                self.dict_ipchal_result_info['기관명'] = td_text
                continue
            elif "믈건명" in th_text:
                self.dict_ipchal_result_info['기관명'] = td_text
                continue
            elif "공고번호" in th_text:
                self.dict_ipchal_result_info['기관명'] = td_text
                continue
            elif "회차" in th_text:
                try:
                    m = re.split(r'\s/\s', td_text)
                    self.dict_ipchal_result_info['회차'] = m[0]
                    self.dict_ipchal_result_info['차수'] = m[1]
                except Exception as e:
                    logging.exception(e)
                continue
            elif "처분방식" in th_text:
                self.dict_ipchal_result_info['처분방식'] = td_text
                continue
            elif "입찰방식" in th_text:
                try:
                    m = re.split(r'\s/\s', td_text)
                    self.dict_ipchal_result_info['입찰방식'] = m[0]
                    self.dict_ipchal_result_info['경쟁방식'] = m[1]
                except Exception as e:
                    logging.exception(e)
                continue
            elif "입찰기간" in th_text:
                try:
                    m = re.split(r'\s~\s', td_text)
                    self.dict_ipchal_result_info['입찰시작기간'] = m[0]
                    self.dict_ipchal_result_info['입찰종료기간'] = m[1]
                except Exception as e:
                    logging.exception(e)
                continue
            elif "총액/단가" in th_text:
                self.dict_ipchal_result_info['총액/단가'] = td_text
                continue
            elif "개찰시작일시" in th_text:
                self.dict_ipchal_result_info['개찰시작일시'] = td_text
                continue
            elif "집행완료일시" in th_text:
                self.dict_ipchal_result_info['집행완료일시'] = td_text
                continue
            elif "입찰자수" in th_text:
                try:
                    m = re.findall('\d+', td_text)
                    self.dict_ipchal_result_info['유효입찰자수'] = m[0]
                    self.dict_ipchal_result_info['무효입찰자수'] = m[1]
                except Exception as e:
                    logging.exception(e)
                continue
            elif "개찰결과" in th_text:
                self.dict_ipchal_result_info['개찰결과'] = td_text
                continue
            elif "2인 미만 유찰여부" in th_text:
                self.dict_ipchal_result_info['2인 미만 유찰여부'] = td_text
                continue
            elif "유찰/취소사유" in th_text:
                self.dict_ipchal_result_info['유찰/취소사유'] = td_text
                continue
            elif "감정가" in th_text:
                self.dict_ipchal_result_info['감정가'] = td_text
                continue
            elif "입찰금액" in th_text:
                self.dict_ipchal_result_info['입찰금액'] = td_text
                continue
            elif "낙찰금액" in th_text:
                self.dict_ipchal_result_info['낙찰금액'] = td_text
                continue
            elif "최저입찰가" in th_text:
                self.dict_ipchal_result_info['최저입찰가'] = td_text
                continue
            elif "최저입찰가 대비" in th_text:
                self.dict_ipchal_result_info['낙찰가율(최저입찰가 대비)'] = td_text
                continue
            elif "감정가 대비" in th_text:
                self.dict_ipchal_result_info['낙찰가율(감정가 대비)'] = td_text
                continue
            elif "재산구분" in th_text:
                self.dict_ipchal_result_info["재산구분"] = td_text
                continue
            elif "담당부점" in th_text:
                self.dict_ipchal_result_info["담당부점"] = td_text
                continue

        self.dict_ipchal_result_info['button_exist'] = True
        if "압류" in self.dict_ipchal_result_info["재산구분"]:
            self.dict_ipchal_result_info['button_exist'] = False

        # 상세보기 버튼의 대금납부 및 배분기일 테이블이 있으면
        if len(check_table_count) == 2:
            table = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container > table:nth-child(4)")
            ths = table.find_elements(by=By.TAG_NAME, value="th")
            tds = table.find_elements(by=By.TAG_NAME, value="td")
            for i in range(len(ths)):
                th_text = ths[i].text
                td_text = tds[i].text
                if "대금납부기한" in th_text:
                    self.dict_ipchal_result_info['대금납부기한'] = td_text
                elif "납부여부" in th_text:
                    self.dict_ipchal_result_info['납부여부'] = td_text
                elif "납부촉구(최고)기한" in th_text:
                    self.dict_ipchal_result_info['납부촉구(최고)기한'] = td_text
                elif "배분기일" in th_text:
                    self.dict_ipchal_result_info['배분기일'] = td_text

        driver.close()
        driver.switch_to_window(driver.window_handles[0])

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

    def open_ipchal_history(self):
        '''
        물건번호를 클릭해 입찰 이력을 연다.
        :return: None
        '''
        self.tr.find_element(by=By.CSS_SELECTOR, value="td:nth-child(1) > div > dl > dt > a").click()
        self.get_ipchal_number()
        driver.back()

    def run(self):
        self.get_summary_data()

        # 상세보기 버튼 존재하면 상세보기
        if is_element_presence(By.CSS_SELECTOR, f"#Contents > table > tbody > tr:nth-child({self.index}) > td:nth-child(7) > a"):
            self.open_detail_newtab_and_move()
            self.get_detail_data()

        # 상세보기 버튼 존재하고 압류자산이 아니면 입찰이력열고 입찰번호받는다
        if self.dict_ipchal_result_info['button_exist']:
            self.open_ipchal_history()

        print(self.dict_ipchal_result_info)


# ------------------- 템플릿 테스트용
    #입찰 상세에 상세입찰결과의 어떤 칼럼이 있는지 확인하기위해

    # def test(self):
    #     if is_element_presence(By.CSS_SELECTOR, f"#Contents > table > tbody > tr:nth-child({self.index}) > td:nth-child(7) > a"):
    #         self.open_detail_newtab_and_move()
    #         self.test_newtab_template()
    #
    # def test_newtab_template(self):
    #     table = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div.popup_container > table")
    #     ths = table.find_elements(by=By.TAG_NAME, value="th")
    #     temp_list = []
    #     for th in ths:
    #         temp_list.append(th.text)
    #     print(temp_list)
    #     driver.close()
    #     driver.switch_to_window(driver.window_handles[0])

