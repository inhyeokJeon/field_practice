from setup import *

class openAndlogin():
    def __init__(self):
        self.ID = "poiu2389"
        self.PW = "dlsgur4978"
        self.web_page = "https://www.onbid.co.kr/op/bda/bidrslt/moveableResultList.do"

    def handle_alert(self) -> bool:
        """
        팝업 데이터 유무 판별.
        :return:
        """
        try:
            WebDriverWait(driver, 1, poll_frequency=0.01).until(EC.alert_is_present(), "팝업 대기")
            alert = driver.switch_to.alert
            alert.accept()
            main = driver.window_handles
            driver.switch_to.window(main[0])
            print("handle_alert 함수 호출 결과 : 데이터 비존재.")
            return False
        except selenium.common.exceptions.TimeoutException:
            print("handle_alert 함수 호출 결과 : 데이터 존재.")
            return True

    def insert_idpw(self) -> None:
        """
        id와 pw 입력.
        :param driver:
        :param id_param:
        :param pw_param:
        :return:
        """
        element_locate_wait(By.ID, "usrId")
        id_part: WebElement = driver.find_element(By.ID, "usrId")
        pw_part: WebElement = driver.find_element(By.ID, "encpw")

        if id_part == WebElement:
            id_part.click()
        else:
            id_part = driver.find_element(By.ID, "usrId")
            id_part.click()

        time.sleep(1)
        id_part.send_keys(self.ID)
        time.sleep(0.1)
        id_part.clear()
        for word in self.ID:
            id_part.send_keys(word)
            time.sleep(0.1)

        if pw_part == WebElement:
            pw_part.click()
        else:
            pw_part = driver.find_element(by=By.ID, value="encpw")
            pw_part.click()

        time.sleep(1)
        pw_part.clear()
        time.sleep(0.1)
        for word in self.PW:
            pw_part.send_keys(word)
            time.sleep(0.1)
        time.sleep(1)

        element_click_wait(By.CSS_SELECTOR, "#frm > fieldset > a")
        submit_part = driver.find_element(by=By.CSS_SELECTOR, value="#frm > fieldset > a")
        submit_part.click()

        if not self.handle_alert():
            self.insert_idpw()

    def login(self) -> None:
        """
        로그인.
        :param driver:
        :param id_param: 아이디
        :param pw_param: 패스워드
        :return:
        """
        element_click_wait(By.CSS_SELECTOR, "#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)")
        driver.find_element(By.CSS_SELECTOR,
                            "#Wrap > div.headerWrap > div.header > div.util > div > a:nth-child(1)").click()

        self.insert_idpw()
        main: list = driver.window_handles

        if len(main) == 2:
            driver.switch_to.window(main[1])

            if is_element_presence(By.CSS_SELECTOR, "#dplcLoginPop > div.popup_header > h2"):
                title: str = driver.find_element(by=By.CSS_SELECTOR,
                                                 value="#dplcLoginPop > div.popup_header > h2").text
                if "중복 로그인 알림" in title:
                    element_click_wait(By.CLASS_NAME, "cm_btn_b_f.close_pop")
                    driver.find_element(by=By.CLASS_NAME, value="cm_btn_b_f.close_pop").click()

                    """
                    time.sleep() 말고 다른 방법이 있는지 생각.
                    """
                    time.sleep(4)
                    #공동인증서 등록
                    main = driver.window_handles
                    if len(main) == 2:
                        driver.switch_to.window(main[1])
                        driver.close()

            driver.switch_to.window(main[0])

    def run(self):
        driver.get(self.web_page)
        driver.implicitly_wait(5)
        self.login()

