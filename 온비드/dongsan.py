import selenium.common.exceptions
from dongsan.ipchal_info import *
from dongsan.button_tab import *


class ONBID_Selenium:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.web_page = "https://www.onbid.co.kr/op/cta/cltrdtl/collateralDetailMoveableAssetsList.do"

        self.dict_template: dict = {
            '기본정보': {},
            '상세정보': {},
            '첨부파일': {},
            '입찰유형': {},
            '세부정보버튼': {}
        }
        self.dict_summary: dict = {  # 물건 기본정보.
            '물건관리번호': "",
            '물건이름': "",
            '중분류카테고리': "",
            '소분류카테고리': "",
            '소재지': "",
            '태그': "",
            '연식': "",
            '주행거리': "",
            '연료': "",
            '입찰': "",
            '개찰': "",
            '최저입찰가': "",
            '최초감정가': "",
            '최저입찰가율': "",
            '물건상태': "",
            '유찰횟수': "",
            '조회수': ""
        }
        self.dict_detail: dict = {  # 물건 상세정보.
            '물건관리번호': "",
            '중분류카테고리': "",
            '소분류카테고리': "",
            '물건이름': "",
            '태그': [],
            '물건상태': "",
            '공고일자': "",
            '조회수': "",
            '처분방식': "",
            '자산구분': "",
            '용도': "",
            '작품명': "",
            '작가명': "",
            '제조사': "",
            '모델명': "",
            '감정평가금액': "",
            '수량': "",
            '입찰방식': "",
            '입찰': "",
            '개찰': "",
            '회차': "",
            '차수': "",
            '유찰횟수': "",
            '임대기간': "",
            # --------- NPL
            'NPL종류명': "",
            # ---------- 유가증권
            '법인명': "",
            '최초예정가액': "",
            '집행기관': "",
            '담당자정보': "",
            '최저입찰가': ""

        }
        self.dict_chumbu: dict = {  # 첨부파일 갯수.
            '사진': "0",
            '감정평가서': {}
            # '사고이력': {}
        }
        self.dict_bid_type: dict = {  # 입찰 유형.
            '전자보증서가능': 'N',
            '공동입찰가능': 'N',
            '2회이상입찰가능': 'N',
            '대리입찰가능': 'N',
            '2인미만유찰여부': 'N',
            '공유자여부': 'N',
            '차순위매수신청가능': 'N'
        }
        self.dict_chumbu: dict = {  # 첨부파일 갯수.
            '사진': "0",
            '지적도': {},
            '위치도': {},
            '감정평가서': {}
        }
        self.dict_bid_type: dict = {  # 입찰 유형.
            '전자보증서가능': 'N',
            '공동입찰가능': 'N',
            '2회이상입찰가능': 'N',
            '대리입찰가능': 'N',
            '2인미만유찰여부': 'N',
            '공유자여부': 'N',
            '차순위매수신청가능': 'N'
        }
        self.dict_gamjung: dict = {  # 감정평가정보
            '감정평가기관': "",
            '평가일': "",
            '평가금액': "",
            '감정평가서': ""
        }
        self.dict_area: dict = {
            '종별': "",
            '지목': "",
            '면적': "",
            '평수': "",
            '지분': "",
            '비고': ""
        }
        self.dict_detail_info: dict = {  # 물건 세부 정보 버튼.
            '토지면적': "",
            '건물면적': "",
            '면적정보': [],
            '지번': "",
            '도로명': "",
            '위치및부근현황': "",
            '이용현황': "",
            '기타사항': "",
            '명도책임': "",
            '부대조건': "",
            '감정평가정보': []
        }

        self.dict_hweicha: dict = {  # 회차별 입찰 정보
            '입찰번호': "",
            '회차': "",
            '차수': "",
            '구분': "",
            '대금납부': "",
            '납부기한': "",
            '입찰시작기간': "",
            '입찰종료기간': "",
            '개찰일시': "",
            '개찰장소': "",
            '최저입찰가': ""
        }

        self.dict_ipchal_chumbu: dict = {  # 입찰 정보 첨부파일
            '파일명': "",
            'href': ""
        }

        self.dict_ipchal_info: dict = {  # 입찰 정보 버튼.
            '전자보증서사용여부': "",
            '차순위매수신청가능여부': "",
            '공동입찰가능여부': "",
            '2인미만유찰여부': "",
            '대리입찰가능여부': "",
            '2회이상입찰가능여부': "",
            '자격제한조건': "",
            '지역제한조건': "",
            '기타제한조건': "",
            '회차별입찰정보': [],
            '첨부파일': []
        }

        self.dict_imdae: dict = {  # 임대차 정보
            '임대차내용': "",
            '성명': "",
            '보증금': "",
            '차임(월세)': "",
            '환산보증금': "",
            '확정(설정)일': "",
            '전입일': ""
        }

        self.dict_deunggi: dict = {  # 등기사항증명서 주요정보
            '권리종류': "",
            '권리자명': "",
            '설정일자': "",
            '설정금액': ""
        }

        self.dict_apryu: dict = {  # 압류재산 정보
            '임대차정보': [],
            '등기사항증명서주요정보': []
        }

        self.dict_gonggo_table: dict = {  # 입찰일시 및 장소
            '회차': "",
            '차수': "",
            '입찰보증금율': "",
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

        self.dict_history: dict = {  # 입찰이력정보
            # '물건관리번호': "",
            # '공고번호': "",
            '회차': "",
            '차수': "",
            '입찰번호': "",
            '처분방식': "",
            '개찰년도': "",
            '개찰시간': "",
            '최저입찰가': "",
            '입찰결과': "",
            '낙찰가': "",
            '낙찰가율': ""
            # '재산구분': "",
            # '담당부점': "",
            # '입찰방식': "",
            # '경쟁방식': "",
            # '유효입찰자수': "",
            # '무효입찰자수': "",
            # '유찰/취소사유': "",
            # '감정가': ""
        }
    def element_click_wait(self, by_type, locator: str) -> None:
        """
        클릭하고 싶은 element에 대한 예외처리.
        :param by_type:
        :param locator:
        :return:
        """
        #print(f"element_click_wait 함수 호출 ({by_type}, {locator})")
        try:
            WebDriverWait(self.driver, 10, poll_frequency=0.01).until(EC.element_to_be_clickable((by_type, locator)))
            return

        except selenium.common.exceptions.TimeoutException:
            print(str(by_type) + str(locator) + " Timeout Error")
            self.driver.close()
            sys.exit()

    def element_locate_wait(self, by_type, locator: str) -> None:
        """
        가져오고 싶은 element에 대한 예외처리.
        :param by_type:
        :param locator:
        :return:
        """
        #print(f"element_locate_wait 함수 호출 ({by_type}, {locator})")
        try:
            WebDriverWait(self.driver, 10, poll_frequency=0.01).until(EC.presence_of_element_located((by_type, locator)))
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
        #print(f"element_visible_wait 함수 호출 ({by_type}, {locator})")
        try:
            WebDriverWait(driver=self.driver, timeout=10, poll_frequency=0.01).until(EC.visibility_of_element_located((by_type, locator)))
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
            #print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 존재")
            return True
        except selenium.common.exceptions.TimeoutException:
            print(f"is_element_presence 함수 호출 ({by_type}, {locator}) 결과 : 비존재")
            return False

    def handle_alert(self) -> bool:
        """
        팝업 데이터 유무 판별.
        :return:
        """
        try:
            WebDriverWait(self.driver, 1, poll_frequency=0.01).until(EC.alert_is_present(), "팝업 대기")
            alert = self.driver.switch_to.alert
            alert.accept()
            main = self.driver.window_handles
            self.driver.switch_to.window(main[0])
            print("handle_alert 함수 호출 결과 : 데이터 비존재.")
            return False
        except selenium.common.exceptions.TimeoutException:
            print("handle_alert 함수 호출 결과 : 데이터 존재.")
            return True

    def login(self) -> None:
        """
        로그인
        :return:
        """
        self.element_click_wait(By.CSS_SELECTOR,
                                "#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)")
        self.driver.find_element(by=By.CSS_SELECTOR,
                                 value="#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)").click()

        self.element_locate_wait(By.ID, "usrId")

        id_part = self.driver.find_element(by=By.ID, value="usrId")
        pw_part = self.driver.find_element(by=By.ID, value="encpw")

        id_part.click()
        time.sleep(1)
        id_part.send_keys('5')
        time.sleep(1)
        id_part.send_keys(Keys.DELETE)
        id_part.clear()
        for word in self.ID:
            id_part.send_keys(word)

        time.sleep(1)
        pw_part.click()
        id_part.send_keys(Keys.HOME)
        for word in self.PW:
            pw_part.send_keys(word)
        time.sleep(1)

        self.element_click_wait(By.CSS_SELECTOR, "#frm > fieldset > a")
        submit_part = self.driver.find_element(by=By.CSS_SELECTOR, value="#frm > fieldset > a")
        submit_part.click()
        time.sleep(1)
        if not self.handle_alert():
            self.login()

    def main_page(self) -> None:
        """
        1. 웹페이지 접속
        2. 팝업창 닫기
        3. 로그인
        :return: None
        """
        self.driver.get(self.web_page)
        assert "온비드" in self.driver.title

        main = self.driver.window_handles
        for handle in main:
            if handle != main[0]:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(main[0])

        self.login()

        main = self.driver.window_handles

        if len(main) == 2:
            self.driver.switch_to.window(main[1])

            if self.is_element_presence(By.CSS_SELECTOR, "#dplcLoginPop > div.popup_header > h2"):
                title = self.driver.find_element(by=By.CSS_SELECTOR, value="#dplcLoginPop > div.popup_header > h2").text
                if "중복 로그인 알림" in title:
                    self.element_click_wait(By.CLASS_NAME, "cm_btn_b_f.close_pop")
                    self.driver.find_element(by=By.CLASS_NAME, value="cm_btn_b_f.close_pop").click()

                    """
                    time.sleep() 말고 다른 방법이 있는지 생각.
                    """
                    time.sleep(7)
                    main = self.driver.window_handles
                    if len(main) == 2:
                        self.driver.switch_to.window(main[1])

            self.driver.close()
            self.driver.switch_to.window(main[0])

    def next_page(self) -> bool:
        """
        다음 페이지로 이동.
        :return: 끝에 도달하면 True, 아니면 False
        """
        self.element_locate_wait(By.CLASS_NAME, "active")  # 현재 페이지번호 element가 존재하는지 검사.

        # page column 선택.
        paging = self.driver.find_element(by=By.CLASS_NAME, value="cm_paging.cl")

        # 최대 페이지 번호 계산.
        total_page_text = paging.find_element(by=By.TAG_NAME, value="p").text
        total_number_list = total_page_text.split(' ')
        total_number = int(total_number_list[1])
        total_number = str(int(total_number / 100) + 1)

        # 페이지 길이, 현재 페이지 번호 계산.
        pages = paging.find_elements(by=By.TAG_NAME, value="a")
        page_count = len(pages)
        pre_page = paging.find_element(by=By.CLASS_NAME, value="active").text

        # 현재 페이지 번호가 최대 페이지 번호가 되면 True 반환.
        if total_number == pre_page:
            return True

        # 다음 페이지로 이동.
        for i in range(page_count):
            if pages[i].text == pre_page:
                pages[i + 1].click()
                return False

    def change_file_name(self, old_file_name: str, new_file_name: str, file_type: str) -> None:
        """
        최근 다운받은 파일 이름 변경.
        :param old_file_name:
        :param new_file_name:
        :param file_type:
        :return:
        """
        old = f"{self.download_location}/{old_file_name}.{file_type}"
        new = f"{self.download_location}/{new_file_name}.{file_type}"
        try:
            os.rename(src=old, dst=new)
        except FileNotFoundError:
            print("Waiting Download...")
            time.sleep(5)
            os.rename(src=old, dst=new)

    @staticmethod
    def split_file_text(file_text: str) -> list:
        """
        파일이름, 파일타입으로 분할.
        :param file_text: str
        :return: list
        """
        index: int = file_text.rfind('.')
        return [file_text[0:index], file_text[index + 1:]]

    def gongmae_jaesan(self, element):
        element.click()
        main = self.driver.window_handles
        self.driver.switch_to.window(main[1])
        attr = self.driver.find_element(by=By.CSS_SELECTOR, value="#cltrMakeDate > a")
        link = attr.get_attribute("href")
        self.driver.close()
        self.driver.switch_to.window(main[0])

        return link

    def handle_photo(self, photo, mulgun_number: str) -> int:
        """
        사진 데이터 다운로드.
        저장형식 : 물건번호_번호.JPG
        저장위치 : ./img
        :param mulgun_number:
        :param photo:
        :return: 사진 갯수.
        """
        try:
            photo.click()
            self.handle_alert()
        except selenium.common.exceptions.ElementClickInterceptedException:
            photo.click()
            self.handle_alert()

        main = self.driver.window_handles
        count = 0
        if len(main) == 1:
            self.driver.back()
            return count

        self.driver.switch_to.window(main[1])

        # 사진 갯수
        self.element_locate_wait(By.CLASS_NAME, "conList")
        conList = self.driver.find_element(by=By.CLASS_NAME, value="conList")
        photo_list = conList.find_elements(by=By.TAG_NAME, value="li")
        length = len(photo_list)
        current = 1
        for elem in photo_list:
            count = count + 1
            elem.find_element(by=By.TAG_NAME, value="a").click()
            self.element_click_wait(By.CSS_SELECTOR,
                                    "#frm > div > div.popup_container > div > div.pop_viewer > a > img")
            self.driver.find_element(by=By.CSS_SELECTOR,
                                     value="#frm > div > div.popup_container > div > div.pop_viewer > a > img").click()
            sub = self.driver.window_handles
            self.driver.switch_to.window(sub[2])
            self.element_locate_wait(By.TAG_NAME, "img")
            photo_url = self.driver.find_element(by=By.TAG_NAME, value="img").get_attribute("src")

            try:
                response = requests.get(url=photo_url, stream=True)
            except requests.exceptions.SSLError:
                response = requests.get(url=photo_url, stream=True)
            except requests.exceptions.ConnectionError:
                response = requests.get(url=photo_url, stream=True)

            if response.status_code == 200:
                with open(f"./img/{mulgun_number}_photo_{str(current)}.JPG", 'wb') as f:
                    f.write(response.content)
            else:
                try:
                    response = requests.get(url=photo_url, stream=True)
                except requests.exceptions.SSLError:
                    response = requests.get(url=photo_url, stream=True)
                except requests.exceptions.ConnectionError:
                    response = requests.get(url=photo_url, stream=True)

                if response.status_code == 200:
                    with open(f"./img/{mulgun_number}_photo_{str(current)}.JPG", 'wb') as f:
                        f.write(response.content)
                else:
                    print("IMAGE DOWNLOAD ERROR")
                    sys.exit()

            self.driver.close()
            self.driver.switch_to.window(sub[1])
            if current > 3 and current != length:
                self.element_click_wait(By.CLASS_NAME, "btn_down")
                self.driver.find_element(by=By.CLASS_NAME, value="btn_down").click()
            current = current + 1

        self.driver.close()
        self.driver.switch_to.window(main[0])
        self.driver.back()
        return count

    def handle_registration_map(self, registration_map) -> dict:
        """
        지적도 데이터 처리.
        :param registration_map:
        :return: 지적도 첨부파일.
        """
        dict_registration_map: dict = {
            "첨부파일갯수": "0",
            "href": []
        }
        href_list: list = []
        registration_map.click()
        self.handle_alert()
        main = self.driver.window_handles

        if len(main) == 1:
            self.driver.back()
            return dict_registration_map

        self.driver.switch_to.window(main[1])

        # 지적도 데이터.
        self.element_click_wait(By.CLASS_NAME, "fwu.cm_txt_bu_01")
        elems = self.driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")

        count: int = len(elems)
        for elem in elems:
            href: str = elem.get_attribute("href")
            href_list.append(href)

        self.driver.close()
        self.driver.switch_to.window(main[0])
        self.driver.back()

        dict_registration_map["첨부파일갯수"] = count
        dict_registration_map["href"] = href_list

        return dict_registration_map

    def handle_location_map(self, location_map) -> dict:
        """
        위치도 데이터 처리.
        :param location_map:
        :return: 위치도 첨부파일 수
        """
        dict_location_map: dict = {
            "첨부파일갯수": "0",
            "href": []
        }
        href_list: list = []
        location_map.click()

        if not self.handle_alert():
            self.driver.back()
            return dict_location_map

        main = self.driver.window_handles
        self.driver.switch_to.window(main[1])

        # 위치도 다운로드.
        self.element_click_wait(By.CLASS_NAME, "fwu.cm_txt_bu_01")
        elems = self.driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")

        count: int = len(elems)
        for elem in elems:
            href: str = elem.get_attribute("href")
            href_list.append(href)

        self.driver.close()
        self.driver.switch_to.window(main[0])
        self.driver.back()
        dict_location_map["첨부파일갯수"] = count
        dict_location_map["href"] = href_list

        return dict_location_map

    def detail_data_buttons(self) -> dict:
        """
        사진, 지적도, 감정평가서, 사고이력조회 버튼을 클릭하여 데이터 얻기.
        :return: 첨부파일 갯수
        """
        self.element_locate_wait(By.CLASS_NAME, "visual_inner")
        visual_inner = self.driver.find_element(by=By.CLASS_NAME, value="visual_inner")

        btn_vway = visual_inner.find_element(by=By.CLASS_NAME, value="btn_vway")  # 첫번째 행.

        first_rows = btn_vway.find_elements(by=By.TAG_NAME, value="a")  # 첫번째 행 버튼들.

        # 물건관리번호
        if self.is_element_presence(By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        # 버튼들 선택.
        photo = first_rows[0]  # 사진

        # 사진 데이터 팝업창.
        photo_count = self.handle_photo(photo, mulgun_number)

        # 감정 평가서 데이터.
        dict_gamjung: dict = {
            "첨부파일갯수": "0",
            "href": []
        }
        href_list: list = []
        gamjung_count: int = 0

        self.element_click_wait(By.ID, "btn_downview")
        self.driver.find_element(by=By.ID, value="btn_downview").click()

        if self.handle_alert():
            files = self.driver.find_elements(by=By.CLASS_NAME, value="fwu.cm_txt_bu_01")
            gamjung_count = len(files)

            for file in files:
                href: str = file.get_attribute("href")
                href_list.append(href)

        dict_gamjung["첨부파일갯수"] = gamjung_count
        dict_gamjung["href"] = href_list

        dict_chumbu: dict = self.dict_chumbu.copy()
        dict_chumbu['사진'] = photo_count
        dict_chumbu['감정평가서'] = dict_gamjung
        return dict_chumbu

    def get_detail_data(self) -> dict:
        """
        물건상세정보 dictionary로 반환.
        :return: 물건상세정보
        """
        dict_detail: dict = self.dict_detail.copy()

        # 물건관리번호
        if self.is_element_presence(By.CLASS_NAME, "tab_wrap1.pos_rel"):
            tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        else:
            tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")

        mulgun_number: str = tab_wrap.find_element(
            by=By.CSS_SELECTOR, value="div.finder03 >div > div.txt_top > p.fl.fwb > span:nth-child(2)").text

        dict_detail['물건관리번호'] = mulgun_number

        # 물건상태, 공고일자, 조회수
        fr = tab_wrap.find_element(by=By.CSS_SELECTOR, value="div.finder03 > div > div.txt_top > p.fr")

        spans = fr.find_elements(by=By.TAG_NAME, value="span")

        if len(spans) != 3:
            print("물건상태, 공고일자, 조회수 데이터가 없습니다.")
            sys.exit()

        dict_detail['물건상태'] = spans[0].find_element(by=By.TAG_NAME, value="em").text
        dict_detail['공고일자'] = spans[1].find_element(by=By.TAG_NAME, value="em").text
        dict_detail['조회수'] = spans[2].find_element(by=By.TAG_NAME, value="em").text

        # 중분류, 소분류, 물건이름
        cl_mt10 = self.driver.find_element(by=By.CLASS_NAME, value="cl.mt10")
        category_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="p").text

        category = re.split("\s.\s", category_text[1:-1])

        dict_detail["중분류카테고리"] = category[0]
        dict_detail["소분류카테고리"] = category[1]

        name_text: str = cl_mt10.find_element(by=By.TAG_NAME, value="strong").text
        dict_detail['물건이름'] = name_text

        # 태그
        badge_wrap = self.driver.find_element(by=By.CLASS_NAME, value="badge_wrap.mt10")
        badges = badge_wrap.find_elements(by=By.TAG_NAME, value="em")
        badge_list: list = []

        for badge in badges:
            badge_list.append(badge.text)

        dict_detail['태그'] = badge_list

        # 처분방식, 자산구분, 용도, 토지면적, 건물면적, 감정평가금액, 입찰방식, 입찰, 개찰, 회차, 차수, 유찰횟수

        body = self.driver.find_element(by=By.CSS_SELECTOR,
                                        value="#Contents > div.form_wrap.mt20.mb10 > div.check_wrap.fr > table > tbody")

        trs = body.find_elements(by=By.TAG_NAME, value="tr")

        for tr in trs:
            head_line_text: str = tr.find_element(by=By.TAG_NAME, value="th").text
            table_data: str = tr.find_element(by=By.TAG_NAME, value="td").text

            if "처분방식" in head_line_text:
                p = re.compile(r'[\w]+')
                m = p.findall(table_data)

                dict_detail['처분방식'] = m[0]
                dict_detail['자산구분'] = m[1]
                continue

            if "용도" in head_line_text:
                dict_detail['용도'] = table_data
                continue

            if "제조사" in head_line_text:
                try:
                    m = re.split("\s.\s", table_data)
                    dict_detail['제조사'] = m[0]
                    dict_detail['모델명'] = m[1]
                except:
                    print("no data 제조사 / 모델명")
                    continue
                continue
            if "작품명" in head_line_text:
                try:
                    p = re.compile(r'[\w]+')
                    m = p.findall(table_data)

                    dict_detail['작품명'] = m[0]
                    dict_detail['작가명'] = m[1]
                except:
                    print("no data 작품명 / 작가명")
                    continue

            if "감정평가금액" in head_line_text:
                p = re.compile(r'[\d]{1,3}')
                m: list = p.findall(table_data)
                gamjung: str = ""
                for text in m:
                    gamjung += text
                dict_detail['감정평가금액'] = gamjung
                continue

            if "수량" in head_line_text:
                dict_detail['수량'] = table_data
                continue

            if "입찰방식" in head_line_text:
                dict_detail['입찰방식'] = table_data
                continue

            if "입찰기간" in head_line_text:
                p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
                m = p.findall(table_data)
                dict_detail['입찰'] = m[0]
                dict_detail['개찰'] = m[1]

                p = re.compile(r'[\d]+/[\d]+')
                m: list = p.findall(table_data)
                data: list = m[0].split('/')
                dict_detail['회차'] = data[0]
                dict_detail['차수'] = data[1]
                continue

            if "유찰횟수" in head_line_text:
                p = re.compile(r'[\d]+')
                m = p.findall(table_data)
                dict_detail['유찰횟수'] = m[0]
                continue

            if "임대기간" in head_line_text:
                dict_detail['임대기간'] = table_data
                continue

            if "NPL종류명" in head_line_text:
                dict_detail['NPL종류명'] = table_data
                continue

            # if "배분요구종기" in head_line_text:
            #     dict_detail['배분요구종기'] = table_data
            #     continue

            # if "최초공고일자" in head_line_text:
            #     dict_detail['최초공고일자'] = table_data
            #     continue
            #
            # if "공매대행의뢰기관" in head_line_text:
            #     dict_detail['공매대행의뢰기관'] = table_data
            #     continue

            if "집행기관" in head_line_text:
                dict_detail['집행기관'] = table_data
                continue

            if "담당자정보" in head_line_text:
                dict_detail['담당자정보'] = table_data

        # 최저입찰가
        bid_price_text: str = self.driver.find_element(by=By.CSS_SELECTOR,
                                                       value="#Contents > div.form_wrap.mt20.mb10 > \
                                                              div.check_wrap.fr > dl > dd > em").text
        ipchal_price = re.split(",", bid_price_text)
        bid_price: str = ""
        for ipchal in ipchal_price:
            bid_price += ipchal
        #
        # p = re.compile(r'[\d]{1,3}')
        # m: list = p.findall(bid_price_text)
        # bid_price: str = ""
        # for text in m:
        #     bid_price += text
        dict_detail['최저입찰가'] = bid_price

        return dict_detail

    def get_button_tab_data(self, yongdo_index):
        """
        물건 세부 정보, 입찰 정보, 시세 및 낙찰 통계, 부가정보, 일괄입찰물건 Tab
        :return:
        """
        if (yongdo_index == 0): # 자동차만 template 1번이고 나머지는 3번임 바꿀까 말까
            self.group_mulgun_info(self.basic_info_car)
            self.group_ipchal_info(self.dict_ipchal_info)

        if (yongdo_index == 1):  # 물품(기계)
            self.group_mulgun_info(self.basic_info_gigae)
            self.group_ipchal_info(self.dict_ipchal_info)

        if (yongdo_index == 2): # 기타
            self.group_mulgun_info(self.basic_info_gita)
            self.group_ipchal_info(self.dict_ipchal_info)

        if(yongdo_index==3): # 유가증권
            #self.yuga_mulgun_info(self.basic_info_stock)
            ipchal.group_ipchal_info(self.driver)
            #self.group_ipchal_info(self.dict_ipchal_info)

    def get_bid_type(self) -> dict:
        """
        입찰유형 dict 반환.
        :return: dict
        """
        dict_bid_type = self.dict_bid_type.copy()

        self.element_locate_wait(By.CLASS_NAME, "check_inner")

        ul = self.driver.find_element(by=By.CLASS_NAME, value="check_inner")

        table = ul.find_elements(by=By.TAG_NAME, value="li")

        for box in table:
            text_head: str = box.text.replace(" ", "")
            text_condition: str = box.find_element(by=By.TAG_NAME, value="img").get_attribute("alt")
            if "yes" in text_condition:
                dict_bid_type[text_head] = 'Y'
        return dict_bid_type

    def scan_detail_data(self, mulgun) -> tuple:
        """
        물건 상세 정보 파싱.
        :param mulgun:
        :return: 물건 상세 정보 tuple(dict)로 반환.
        """
        # 물건 상세 페이지로 이동.
        mulgun.click()

        # 페이지 잘 불러졌는지 체크.
        self.element_locate_wait(By.CLASS_NAME, "txt_top")

        # 상세 정보.
        dict_detail: dict = self.get_detail_data()

        # 사진, 지적도, 위치도, 감정평가서
        dict_chumbu: dict = self.detail_data_buttons()

        # 입찰 유형
        dict_bid_type: dict = self.get_bid_type()

        #self.button_tab_test()

        #나눈것들 테스트
        mulgun_sebu , ipchal_info = self.button_tab_test()
        print(json.dumps(dict_detail,indent=2, ensure_ascii=False))
        print(json.dumps(dict_chumbu,indent=2, ensure_ascii=False))
        print(json.dumps(dict_bid_type,indent=2, ensure_ascii=False))
        print(json.dumps(mulgun_sebu,indent=2, ensure_ascii=False))
        print(json.dumps(ipchal_info,indent=2, ensure_ascii=False))
        #print(json.dumps(self.button_tab_test(),indent=2, ensure_ascii=False))

        #dict_detail_info: dict = self.get_button_tab_data(yongdo_index)  # todo tuple로 바꿔야함.

        # 공고이동
        # if self.is_element_presence(By.CLASS_NAME, "tab_wrap1.pos_rel"):
        #     tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap1.pos_rel")
        # else:
        #     tab_wrap = self.driver.find_element(by=By.CLASS_NAME, value="tab_wrap.pos_rel")
        #
        # gonggo_button = tab_wrap.find_element(by=By.CSS_SELECTOR,
        #                                       value="div.sch_txt > p > a:nth-child(1) > span")
        # self.scan_gonggo_data(gonggo_button)
        #
        # # 입찰이력
        # if self.is_element_presence(By.CLASS_NAME, "tab_wrap1.pos_rel"):
        #     ipchal_button: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
        #                                                          value="#Contents > div.tab_wrap1.pos_rel > \
        #                                                          ul > li:nth-child(2) > a")
        # else:
        #     ipchal_button: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
        #                                                          value="#Contents > div.tab_wrap.pos_rel > \
        #                                                          ul > li:nth-child(2) > a")
        #
        # self.scan_ipchal_data(ipchal_button)


        # 물건 목록 페이지로 이동.
        self.driver.back()

        # return dict_chumbu, dict_bid_type, dict_detail, dict_detail_info  # todo button 데이터들 추가.

    def button_tab_test(self) :

        mulgun_sebu_all = {}
        ipchal_info_all = {}

        self.element_locate_wait(By.CSS_SELECTOR, "#Contents > ul")
        button_tab_table = self.driver.find_element(by=By.CSS_SELECTOR, value="#Contents > ul")
        self.element_click_wait(By.CSS_SELECTOR, "#dtbuttontab")
        button_tabs = button_tab_table.find_elements(by=By.CSS_SELECTOR, value="#dtbuttontab")
        for button_tab in button_tabs:
            if button_tab.get_attribute("value") == '001':
                mulgun_button = button_tab
            elif button_tab.get_attribute("value") == '002':
                ipchal_button = button_tab
        mulgun_button.click()
        # 물건세부정보
        self.element_visible_wait(By.ID, "tab01")
        mulgun_element = self.driver.find_element(by=By.ID, value="tab01")
        # 기본정보
        if self.is_element_presence(By.ID, "basicInfo"):
            basicinfo = mulgun_element.find_element(by=By.ID, value="basicInfo")
            group = basicinfo.find_element(by=By.TAG_NAME, value="div").get_attribute("id")
            basicinfo_table: WebElement = basicinfo.find_element(by=By.TAG_NAME, value="table")

            if group == "tab01_group1_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_1)
            elif group == "tab01_group2_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_2)
            elif group == "tab01_group3_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_3)
            elif group == "tab01_group4_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_4)
            elif group == "tab01_group5_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_5)
            elif group == "tab01_group6_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_6)
                #print(tab01_group6_basicInfo(basicinfo_table))
                # 주요주주현황
                if self.is_element_presence(By.ID, "tab01_group6_stockholderInfo"):
                    try:
                        mainjuju = basicinfo.find_element(by=By.ID, value="tab01_group6_stockholderInfo")
                        mainjuju_table = mainjuju.find_element(by=By.TAG_NAME, value="table")
                        basicinfo_all["stockholderinfo"] = stockholderInfo(mainjuju_table)
                    except:
                        print("주요주주현황 없음")
                if self.is_element_presence(By.ID, "financeInfo"):
                    try :
                        jaemu = basicinfo.find_element(by=By.ID, value="financeInfo")
                        jaemu_table = jaemu.find_element(by=By.TAG_NAME, value="table")
                        basicinfo_all["financeinfo"] = financeInfo(jaemu_table)
                    except:
                        print("재무현황정보없음")

            elif group == "tab01_group7_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_7)
            elif group == "tab01_group8_basicInfo":
                basicinfo_all = tab01_group_basicInfo(basicinfo_table, template_8)
            #물건세부정보 전부다
            mulgun_sebu_all['basicinfo'] = basicinfo_all

            # todo 수정 지번 도로명 보관장소
            if self.is_element_presence(By.CSS_SELECTOR,"#tab01 > div:nth-child(2) > table"):
                sub_table = mulgun_element.find_element(by=By.CSS_SELECTOR, value="#tab01 > div:nth-child(2) > table")
                mulgun_sebu_all['subinfo'] = basicInfo_address(sub_table)

        # 감정평가정보
        if self.is_element_presence(By.ID, "tab01_appraiseInfo"):
            tab01_appraiseInfo = mulgun_element.find_element(by=By.ID, value="tab01_appraiseInfo")
            appraiseInfo_table = tab01_appraiseInfo.find_element(by=By.TAG_NAME, value="table")
            mulgun_sebu_all['appraiseinfo'] = appraiseInfo(appraiseInfo_table)

        # 명도이전책임
        if self.is_element_presence(By.ID, "tab01_nominalTransferInfo"):
            tab01_nominalTransferInfo = mulgun_element.find_element(by=By.ID, value="tab01_nominalTransferInfo")
            nominalTransferInfo_table = tab01_nominalTransferInfo.find_element(by=By.TAG_NAME, value="table")
            mulgun_sebu_all['nominaltransferinfo'] = nominalTransferInfo(nominalTransferInfo_table)


        # 입찰정보
        ipchal_button.click()
        self.element_visible_wait(By.ID, "tab02")

        tab02 = self.driver.find_element(by=By.ID, value="tab02")


        '''
        try:
            jaehan_table_class = tab02.find_element(by=By.CSS_SELECTOR, value="div.op_bid_twrap.mt15")
            jaehan_table = jaehan_table_class.find_element(by=By.TAG_NAME, value="table")
            print(jaehan(jaehan_table))
        except:
            print("제한 조건 없음")

        
        # todo ss
        if self.is_element_presence(By.CSS_SELECTOR, "#tab02 > div.op_bid_twrap.mt15"):
            try:
                jaehan_table_class = tab02.find_element(by=By.CSS_SELECTOR, value="div.op_bid_twrap.mt15")
                jaehan_table = jaehan_table_class.find_element(by=By.TAG_NAME, value="table")
                print(jaehan(jaehan_table))

            except:
                print("제한 조건 없음")
        '''
        #입찰 방법 및 입찰 제한 정보
        if self.is_element_presence(By.CSS_SELECTOR, "#tab02 > div.op_bid_twrap.cl.mt15 > table"):
            try :
                #ipchal_table_class = tab02.find_element(by=By.CSS_SELECTOR, value="#tab02 > div > table")
                ipchal_table = tab02.find_element(by=By.CSS_SELECTOR, value="#tab02 > div.op_bid_twrap.cl.mt15 > table")
                ipchal_info_all['ipchal'] = ipchal(ipchal_table)
            except :
                print("no ipchal info")

        #회차별 입찰정보
        if self.is_element_presence(By.CSS_SELECTOR, "#tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table"):
            try :
                hweicha_table_class = tab02.find_element(by=By.CLASS_NAME, value="finder.pos_rel")
                hweicha_table = hweicha_table_class.find_element(by=By.TAG_NAME, value="table")
                # 증권 #tab02 > div.op_bid_twrap.cl.mt15 > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
                # 자동차 #tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
                #tab02 > div > div.op_bid_twrap.mt10 > div.finder.pos_rel > table
                ipchal_info_all['hweicha'] = hweicha(hweicha_table)
            except :
                print("no hweicha info")

        try:
            file_p_id = tab02.find_element(by=By.ID, value="resultFileList")
            file_p_a = file_p_id.find_elements(by=By.TAG_NAME, value="a")
            ipchal_info_all['chumbu'] = chumbu(file_p_a)
        except:
            print("no chumbu file")


        '''
        if self.is_element_presence(By.CSS_SELECTOR, "#tab02 > #rec_file > div"):
            try:
                file_p_id = tab02.find_element(by=By.ID, value="resultFileList")
                file_p_a = file_p_id.find_elements(by=By.TAG_NAME, value="a")
                print(chumbu(file_p_a))
            except:
                print("no chumbu file")
        '''

        return mulgun_sebu_all , ipchal_info_all

    def merge_dict(self, *dict_args):
        result ={}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def get_summary_data(self, tds) -> dict:
        """
        물건 정보 dict 형태로 반환.
        :param tds: 물건 열 정보.
        :return: 물건 정보.
        """
        dict_summary_copy = self.dict_summary.copy()

        # 물건정보 선택.
        info = tds[0].find_element(by=By.CLASS_NAME, value="info")
        mulgun = info.find_element(by=By.TAG_NAME, value="dt").text  # 물건관리번호.
        dict_summary_copy["물건관리번호"] = mulgun
        info_list = info.find_elements(by=By.TAG_NAME, value='dd')

        fwb = info.find_element(by=By.CLASS_NAME, value="fwb").text  # 물건 이름.
        dict_summary_copy["물건이름"] = fwb

        tpoint_03 = info.find_element(by=By.CLASS_NAME, value="tpoint_03").text  # 카테고리
        # " / "기준 나누기
        category = re.split("\s.\s", tpoint_03[1:-1])

        dict_summary_copy["중분류카테고리"] = category[0]
        dict_summary_copy["소분류카테고리"] = category[1]

        # 소재지
        try:
            sozazi: str = info.find_element(by=By.CSS_SELECTOR, value="dd:nth-child(4) > span").text
            dict_summary_copy['소재지'] = sozazi[1:-1]
        except:
            print("소재지없음")


        if (category[0] == '자동차'):
            dict_summary_copy['연식'] = info.find_element(by=By.CSS_SELECTOR,
                                                        value="dd:nth-child(5) > span:nth-child(1)").text[1:-1]
            dict_summary_copy['주행거리'] = info.find_element(by=By.CSS_SELECTOR,
                                                          value="dd:nth-child(5) > span:nth-child(3)").text[1:-1]
            dict_summary_copy['연료'] = info.find_element(by=By.CSS_SELECTOR,
                                                        value="dd:nth-child(5) > span:nth-child(5)").text[1:-1]

        # 물건정보 -> 매각, 임대 / 경쟁.
        badge_wrap = info.find_element(by=By.CLASS_NAME, value="badge_wrap.mt5")
        badges = badge_wrap.find_elements(by=By.TAG_NAME, value="em")
        badge_list: list = []

        for badge in badges:
            badge_str: str = badge.text
            badge_list.append(badge_str)

        dict_summary_copy['태그'] = badge_list

        # 입찰기간
        bid_dates: str = tds[1].find_element(by=By.TAG_NAME, value="font").text
        p = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}')
        m = p.findall(bid_dates)
        dict_summary_copy['입찰'] = m[0]
        dict_summary_copy['개찰'] = m[1]

        # 최저입찰가(원), 감정가-최초예정가(원), 최저입찰가율(%)
        bid_rates: str = tds[2].text
        bid_rate: list = bid_rates.split('\n')

        bid_price: list = bid_rate[0].split(',')
        bid_price_low: str = ""
        for s in bid_price:
            bid_price_low += s
        dict_summary_copy['최저입찰가'] = bid_price_low  # 최저입찰가

        bid_price: list = bid_rate[1].split(',')
        bid_price_first: str = ""
        for s in bid_price:
            bid_price_first += s
        dict_summary_copy['최초감정가'] = bid_price_first  # 최초감정가

        # 최저입찰가율
        dict_summary_copy['최저입찰가율'] = bid_rate[2]

        # 물건상태, 유찰횟수
        state_count: list = tds[3].text.split('\n')

        state: str = state_count[0]
        dict_summary_copy['물건상태'] = state

        count: str = state_count[1]
        p = re.compile(r'[\d]+')
        m = p.findall(count)
        dict_summary_copy['유찰횟수'] = m[0]

        # 조회수.
        look: str = tds[4].text
        dict_summary_copy['조회수'] = look
        print(dict_summary_copy)
        return dict_summary_copy


    def scan_ipchal_data(self, ipchal_button: WebElement):
        ipchal_button.click()
        if self.is_element_presence(By.CSS_SELECTOR, "#Contents > div.tab_wrap1.pos_rel"):
            tab_wrap: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
                                                            value="#Contents > div.tab_wrap1.pos_rel")
        else:
            tab_wrap: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
                                                            value="#Contents > div.tab_wrap.pos_rel")

        #Contents > div.tab_wrap.pos_rel > div.finder04 > div > div.txt_top > p.fr > em
        # todo finder03 에서 04로 바꿈
        try:
            gonggo_date = tab_wrap.find_element(by=By.CSS_SELECTOR, value="div.finder04 > div.op_top_head_wrap.pos_rel > div.txt_top > p.fr > em")
            print(gonggo_date)
        except selenium.common.exceptions.StaleElementReferenceException:
            print('공고일자 x')

        # todo 입찰이력정보
        # todo finder01 에서 finder 로 바꿈
        ipchal_text: str = self.driver.find_element(by=By.CSS_SELECTOR,
                                                    value="#Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel \
                                                    > table > tbody > tr > td").text
        dict_history: dict = self.dict_history.copy()
        if '없습니다' not in ipchal_text:
            tbody: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value="#Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel > table > tbody")
            #Contents > div.op_bid_twrap.mt10 > div.finder.pos_rel > table > tbody

            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")
            for tr in trs:
                tr: WebElement
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                dict_history: dict = self.dict_history.copy()

                list_data: list = re.split(r'/', tds[0].text)
                dict_history['회차'] = list_data[0]
                dict_history['차수'] = list_data[1]

                dict_history['입찰번호'] = tds[1].text

                dict_history['처분방식'] = tds[2].text

                list_data = re.split(r' ', tds[3].text)
                dict_history['개찰년도'] = list_data[0]
                dict_history['개찰시간'] = list_data[1]

                str_data: str = re.sub(r'[,원]', "", tds[4].text)
                dict_history['최저입찰가'] = str_data

                dict_history['입찰결과'] = tds[5].text
                m = re.split("\s", tds[6].text)
                price = re.sub(r'[,원]', "", m[0])
                dict_history['낙찰가'] = price
                dict_history['낙찰가율'] = m[1]
        print(json.dumps(dict_history, indent=2, ensure_ascii=False))
        self.driver.back()

    def scan_gonggo_data(self, gonggo_button) -> None:
        """
        공고 상세 페이지.
        :return:
        """
        dict_gonggo: dict = self.dict_gonggo.copy()
        try:
            gonggo_button.click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            gonggo_button.click()

        self.element_locate_wait(By.CSS_SELECTOR,
                                 "#Contents > div.top_wrap2.pos_rel > div.op_top_head_wrap.pos_rel > h4 > strong")

        # 공고명
        dict_gonggo['공고명'] = self.driver.find_element(by=By.CSS_SELECTOR,
                                                      value="#Contents > div.top_wrap2.pos_rel >\
                                                      div.op_top_head_wrap.pos_rel > h4 > strong").text

        # 공고 테이블
        if self.is_element_presence(By.CSS_SELECTOR, "#Contents > div.top_wrap2.pos_rel > table > tbody > tr"):
            table: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
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
        if self.is_element_presence(By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt10 > div > div > div"):
            gonggo_text: str = self.driver.find_element(by=By.CSS_SELECTOR,
                                                        value="#tab_01 > div.op_bid_twrap.mt10 > div > div > div").text
            dict_gonggo['공고문 전문'] = gonggo_text

        # 첨부파일
        if self.is_element_presence(By.CSS_SELECTOR, "#tab_01 > div.op_bid_twrap.mt15 > div"):
            file_body: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
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
        if self.is_element_presence(By.CSS_SELECTOR, "#Contents > ul > li:nth-child(2) > a"):
            ipchal_info_button: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                      value="#Contents > ul > li:nth-child(2) > a")
            try:
                ipchal_info_button.click()
            except selenium.common.exceptions.ElementClickInterceptedException:
                ipchal_info_button.click()

            tbody: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
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
        if self.is_element_presence(By.CSS_SELECTOR, "#tab_02 > div:nth-child(2) > div > table > tbody"):
            tbody: WebElement = self.driver.find_element(by=By.CSS_SELECTOR,
                                                         value="#tab_02 > div:nth-child(2) > div > table > tbody")
            trs: list = tbody.find_elements(by=By.TAG_NAME, value="tr")
            gonggo_table_list: list = []
            for tr in trs:
                tr: WebElement
                if '없습니다' in tr.text:
                    break
                tds: list = tr.find_elements(by=By.TAG_NAME, value="td")
                dict_gonggo_table: dict = self.dict_gonggo_table.copy()

                text_data: str = tds[0].text
                list_data: list = text_data.split('/')
                dict_gonggo_table['회차'] = list_data[0]
                dict_gonggo_table['차수'] = list_data[1]

                text_data: str = tds[1].text
                dict_gonggo_table['입찰보증금율'] = text_data

                text_data: str = tds[2].text
                p: re.Pattern = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
                list_data: list = p.findall(text_data)
                dict_gonggo_table['입찰시작년도'] = list_data[0]
                dict_gonggo_table['입찰마감년도'] = list_data[1]

                p: re.Pattern = re.compile(r'[\d]{2}:[\d]{2}')
                list_data: list = p.findall(text_data)
                dict_gonggo_table['입찰시작시간'] = list_data[0]
                dict_gonggo_table['입찰마감시간'] = list_data[1]

                text_data: str = tds[3].text
                p: re.Pattern = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
                list_data: list = p.findall(text_data)
                dict_gonggo_table['개찰년도'] = list_data[0]
                # todo 매각결정년도
                #dict_gonggo_table['매각결정년도'] = list_data[1]

                p: re.Pattern = re.compile(r'[\d]{2}:[\d]{2}')
                list_data: list = p.findall(text_data)
                dict_gonggo_table['개찰시간'] = list_data[0]
                #dict_gonggo_table['매각결정시간'] = list_data[1]

                text_data: str = tds[4].text
                dict_gonggo_table['개찰장소'] = text_data

                gonggo_table_list.append(dict_gonggo_table)

            dict_gonggo['입찰일시및장소'] = gonggo_table_list

        print(json.dumps(dict_gonggo, indent=2, ensure_ascii=False))

        self.driver.back()



    # def ipchal_info(self, mulgun):
    #     mulgun.click()
    #
    #     self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[3]/ul/li[2]/a").click()
    #     time.sleep(1)
    #     self.element_locate_wait(By.CLASS_NAME, "op_tbl_type7")
    #     table = self.driver.find_element(by=By.CLASS_NAME, value="op_tbl_type7")
    #
    #     # 테이블 바디 선택.
    #     body = table.find_element(by=By.TAG_NAME, value="tbody")
    #     # 테이블 행 선택.
    #     # tr = body.find_elements(by=By.TAG_NAME, value="tr")
    #     # print(tr)
    #
    #     tds = body.find_elements(by=By.TAG_NAME, value="td")
    #     print(tds)
    #
    #     print(tds[0].text)
    #     print(tds[1].text)
    #     print(tds[2].text)
    #     print(tds[3].text)
    #     print(tds[4].text)
    #     print(tds[5].text)


    # 수정
    def scan_table_data(self, yongdo_index) -> None:
        """
        물건 목록 테이블의 데이터들을 훑으며
        데이터베이스에 저장되어 있으면 skip
        데이터베이스에 저장되어 있지 않으면 상세페이지로 이동한다.
        :return:
        """
        mulgun_index: int = 0  # todo

        while True:
            # 테이블 선택.
            self.element_locate_wait(By.CLASS_NAME, "op_tbl_type6")
            table = self.driver.find_element(by=By.CLASS_NAME, value="op_tbl_type6")

            # 테이블 바디 선택.
            body = table.find_element(by=By.TAG_NAME, value="tbody")

            # 테이블 행 선택.
            trs = body.find_elements(by=By.TAG_NAME, value="tr")

            if mulgun_index >= len(trs):
                break

            if "없습니다" in trs[0].text:
                break
            # 테이블 열 선택.
            tds = trs[mulgun_index].find_elements(by=By.TAG_NAME, value="td")

            # 물건관리번호 선택.
            mulgun = tds[0].find_element(by=By.CSS_SELECTOR, value="div > dl > dt > a")

            mulgun_text = mulgun.text

            # todo 수정 물건 요약 정보.
            self.dict_summary: dict = self.get_summary_data(tds)

            self.element_click_wait(By.CSS_SELECTOR, f"#collateralSearchForm > table > tbody > tr:nth-child({mulgun_index+1}) > td.al.pos_rel > div > dl > dt > a")
            # todo 수정중
            self.scan_detail_data(mulgun)

            # 상세이동.
            # tuple_data: tuple = self.scan_detail_data(mulgun)
            mulgun_index = mulgun_index + 1

        '''
            # dict 저장.
            dict_template: dict = self.dict_template.copy()
            dict_template['기본정보'] = dict_summary
            dict_template['첨부파일'] = tuple_data[0]
            dict_template['입찰유형'] = tuple_data[1]
            dict_template['상세정보'] = tuple_data[2]
            dict_template['세부정보버튼'] = tuple_data[3]

            dict_mulgun[mulgun_text] = dict_template
            print(json.dumps(dict_mulgun, indent=2, ensure_ascii=False))

            # 다음 물건 선택.
            mulgun_index = mulgun_index + 1
        '''

    # 수정
    def set_home_page(self, begin_date, end_date, yongdo_index):
        self.element_locate_wait(By.ID, "searchBegnDtm")
        begin = self.driver.find_element(by=By.ID, value="searchBegnDtm")
        end = self.driver.find_element(by=By.ID, value="searchClsDtm")
        begin.clear()
        end.clear()

        begin.send_keys(begin_date)
        end.send_keys(end_date)

        self.element_click_wait(By.ID, "businessTypeAll")
        asset_check = self.driver.find_element(by=By.ID, value="businessTypeAll")
        asset_check.click()

        yongdo_ul = self.driver.find_element(by=By.CSS_SELECTOR,
                                             value="#moveableAssetsFormDiv > div:nth-child(1) > table > tbody > tr:nth-child(3) > td > ul")
        yongdo_lis = yongdo_ul.find_elements(by=By.TAG_NAME, value='li')

        yongdo_lis[yongdo_index].click()

        self.element_click_wait(By.ID, "searchBtn")
        search_btn = self.driver.find_element(by=By.ID, value="searchBtn")
        search_btn.click()

        # 100줄씩 설정.
        self.element_click_wait(By.CSS_SELECTOR, "#pageUnit > option:nth-child(4)")
        self.driver.find_element(by=By.CSS_SELECTOR, value="#pageUnit > option:nth-child(4)").click()

        # 정렬.
        self.element_click_wait(By.CLASS_NAME, "cm_btn_tnt")
        self.driver.find_element(by=By.CLASS_NAME, value="cm_btn_tnt").click()

        while True:
            self.scan_table_data(yongdo_index)
            if self.next_page():
                break

        self.driver.find_element(by=By.CSS_SELECTOR,
                                 value='#lnbWrap > div.lnb > ul > li:nth-child(2) > ul > li:nth-child(1) > a').click()

    def home_page(self) -> None:
        self.driver.get(self.web_page)
        today_date = datetime.today().strftime("%Y-%m-%d")
        one_year_ago = (datetime.today() - timedelta(365)).strftime("%Y-%m-%d")
        one_year_later = (datetime.today() + timedelta(366)).strftime("%Y-%m-%d")
        tomorrow_date = (datetime.today() + timedelta(1)).strftime("%Y-%m-%d")
        print(one_year_ago)
        print(today_date)
        print(one_year_later)

        for i in range(4):
            self.set_home_page(one_year_ago, today_date, i)
            self.set_home_page(tomorrow_date, one_year_later, i)

        print("Done")

    def start(self):
        # self.main_page()

        self.home_page()

        # self.driver.close()


run = ONBID_Selenium()

run.start()
