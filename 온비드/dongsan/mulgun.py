
from mulgun_detail_data import *
from detail_data_buttons import *
from bid_type import *
from button_tab_data import *
from mulgun_summary import *

def mulgun_detail(mulgun_index: int):
    open_mulgun_detail_tab(mulgun_index)
    # 물관, 태그 등등 위의 테이블정보
    get_detail_data()
    # 사진, 지적도, 위치도, 감정평가서
    detail_data_buttons()
    # 입찰 유형
    get_bid_type()

    button_tab_data()

    driver.back()
    close_mulgun_detail_tab()

def scan_mulgun_table():
    mulgun_index: int = 0

    while True:
        if is_table_end(mulgun_index):
            break
        get_summary_data(mulgun_index)
        mulgun_detail(mulgun_index)
        mulgun_index = mulgun_index + 1

def gonggo_mulgun_table():
    open_gonggo_mulgun_table_tab()
    set_order_and_click()

    while True:
        scan_mulgun_table()
        if next_page():
            break

    close_gonggo_mulgun_table_tab()

def mulgun_data(gonggo_index):
    gonggo_detail_click(gonggo_index)

    gonggo_mulgun_table()

    driver.back()

