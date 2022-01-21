from login import *
from set_search import *
from ipchal_result_data import *

def scan_data():
    mulgun_index: int = 1
    while True:
        element_locate_wait(By.CSS_SELECTOR, "#Contents > table > tbody")
        body = driver.find_element(by=By.CSS_SELECTOR, value="#Contents > table > tbody")
        trs = body.find_elements(by=By.TAG_NAME, value="tr")
        if mulgun_index > len(trs):
            break

        if "없습니다" in trs[0].text:
            break
        ipchal_result_data(mulgun_index).run()
        #ipchal_result_data(mulgun_index).test()

        mulgun_index = mulgun_index + 1

def start():

    openAndlogin().run()
    sst = set_search_table()
    # todo 데이터읽기
    while True:
        if sst.run():
            break
        while True:
            set_newtab_javascript()
            scan_data()
            if next_page():
                driver.find_element(by=By.CSS_SELECTOR, value="#lnbWrap > div.lnb > ul > li:nth-child(5) > ul > li:nth-child(1) > a").click()
                break
    driver.close()
    driver.quit()
start()


'''창고
driver.execute_script("""
                function fn_openDetailView(cltrNo, pbctNo, pbctCdtnNo) {
                    if(!gfn_checkLogin()) {
                        return;
                    }
                    window.name="moveable";
                    var url = "/op/bda/bidrslt/bidResultPopup.do?cltrNo=" +cltrNo+ "&pbctCdtnNo=" + pbctCdtnNo+ "&pbctNo=" + pbctNo;
                    window.open(url, "_blank");
                }
                %s;

            """ % target)
'''