
from login import openAndlogin
from mulgun import mulgun_data
from set_search import set_search_table
from gonggo_data import *

def scan_data():
    gonggo_index: int = 0
    while True:
        if is_table_end(gonggo_index):
            break
        if not is_cancel_gonggo(gonggo_index):
            gongo_data(gonggo_index).run()
            mulgun_data()

        gonggo_index = gonggo_index + 1

def start():
    openAndlogin().run()
    sst = set_search_table()
    while True:
        if sst.run():
            break
        while True:
            scan_data()
            if next_page():
                driver.find_element(by=By.CSS_SELECTOR, value="#lnbWrap > div.lnb > ul > li:nth-child(3) > ul > li:nth-child(1) > a").click()
                break
    driver.close()
    driver.quit()

if __name__ == '__main__':
    start()