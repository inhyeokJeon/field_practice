

def chumbu(p):
    chumbu_list = []
    for href in p:
        try:
            chumbu_list.append(href.get_attribute("href"))
        except:
            print("첨부파일없음")
    return chumbu_list