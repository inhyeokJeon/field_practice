from setup import *

dict_bid_type_temp: dict = {  # 입찰 유형.
            '전자보증서가능': 'N',
            '공동입찰가능': 'N',
            '2회이상입찰가능': 'N',
            '대리입찰가능': 'N',
            '2인미만유찰여부': 'N',
            '공유자여부': 'N',
            '차순위매수신청가능': 'N'
        }

def get_bid_type() -> dict:
        """
        입찰유형 dict 반환.
        :return: dict
        """
        dict_bid_type = dict_bid_type_temp.copy()

        element_locate_wait(By.CLASS_NAME, "check_inner")

        ul = driver.find_element(by=By.CLASS_NAME, value="check_inner")

        table = ul.find_elements(by=By.TAG_NAME, value="li")

        for box in table:
            text_head: str = box.text.replace(" ", "")
            text_condition: str = box.find_element(by=By.TAG_NAME, value="img").get_attribute("alt")
            if "yes" in text_condition:
                dict_bid_type[text_head] = 'Y'
        print(dict_bid_type)
        return dict_bid_type