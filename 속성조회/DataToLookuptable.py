import pymysql
import csv

def main():
    con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='nsdi',
            cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    
    regstrSeCode(cur)
    
    realLndcgrCode(cur)
    prposArea1(cur)
    prposArea2(cur)
    prposDstrc1(cur)
    prposDstrc2(cur)
    
    ladUseSittn(cur)
    
    tpgrphHgCode(cur)
    tpgrphFrmCode(cur)
    roadSideCode(cur)
    roadDstncCode(cur)
    stdlandPosesnSeCode(cur)
    posesnStle(cur)
    
    con.commit()
    
def regstrSeCode(cur):
    sql = "INSERT INTO regstrSeCode values ('1','일반'),('2','산'),('3','가지번'), \
    ('4','가지번(부번세분)'),('5','블록지번'),('6','블록지번(롯트세분)'),('7','블록지번(지구)'), \
    ('8','블록지번(지구_롯트)'),('9','기타지번')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def realLndcgrCode(cur):
    sql = "INSERT INTO realLndcgrCode values ('0','지정되지않음'),('01','전'),('02','답'),('03','과수원'), \
    ('04','목장용지'),('05','임야'),('06','광천지'),('07','염전'),('08','대'),('09','공장용지'),('10','학교용지'), \
    ('11','주차장'),('12','주유소용지'),('13','창고용지'),('14','도로'),('15','철도용지'),('16','제방'),('17','하천'),('18','구거'),('19','유지'),('20','양어장'), \
    ('21','수도용지'),('22','공원'),('23','체육용지'),('24','유원지'),('25','종교용지'),('26','사적지'),('27','묘지'),('28','잡종지')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def prposArea1(cur):
    sql = "INSERT INTO prposArea1 values ('00','지정되지않음'),('11','제1종전용주거지역'),('12','제2종전용주거지역'),('13','제1종일반주거지역'),('14','제2종일반주거지역'),('15','제3종일반주거지역'),\
    ('16','준주거지역'),('17','일반주거지역'),('21','중심상업지역'),('22','일반상업지역'),('23','근린상업지역'),('24','유통상업지역'),('32','일반공업지역'), \
    ('33','준공업지역'),('41','보전녹지지역'),('42','생산녹지지역'),('43','자연녹지지역'),('44','개발제한구역'),('51','용도미지정'),('61','관리지역'),('62','보전관리지역'),\
    ('63','생산관리지역'),('64','계획관리지역'),('71','농림지역'),('81','자연환경보전지역')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def prposArea2(cur):
    sql = "INSERT INTO prposArea2 values ('00','지정되지않음'),('11','제1종전용주거지역'),('12','제2종전용주거지역'),('13','제1종일반주거지역'),('14','제2종일반주거지역'),('15','제3종일반주거지역'),\
    ('16','준주거지역'),('17','일반주거지역'),('21','중심상업지역'),('22','일반상업지역'),('23','근린상업지역'),('24','유통상업지역'),('32','일반공업지역'), \
    ('33','준공업지역'),('41','보전녹지지역'),('42','생산녹지지역'),('43','자연녹지지역'),('44','개발제한구역'),('51','용도미지정'),('61','관리지역'),('62','보전관리지역'),\
    ('63','생산관리지역'),('64','계획관리지역'),('71','농림지역'),('81','자연환경보전지역')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def prposDstrc1(cur):
    sql = "INSERT INTO prposDstrc1 values ('00','지정되지않음'),('11','역사문화환경보존지구'),('12','중요시설물보존지구'),('13','생태계보존지구'),('14','자연경관지구'),('15','수변경관지구'),\
    ('16','시가지경관지구'),('17','기타경관지구'),('18','학교시설보호지구'),('19','공용시설보호지구'),('20','항만시설보호지구'), \
    ('21','공항시설보호지구'),('22','방재지구'),('23','최고고도지구'),('24','중심지미관지구'),('25','역사문화미관지구'),('26','일반미관지구'),('27','기타미관지구'),\
    ('28','방화지구'),('29','최저고도지구'),('30',''),('31','자연취락지구'),('32','집단취락지구'),('33','특정용도제한지구'),('34','특정용도제한지구'),\
    ('35','기타특정용도제한지구'),('36','주거개발진흥지구'),('37','산업유통개발진흥지구'),('38','유통개발진흥지구'),('39','관광,휴양개발진흥지구'),('40','복합개발진흥지구'), \
    ('41','특정개발진흥지구'),('99','기타지구')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def prposDstrc2(cur):
    sql = "INSERT INTO prposDstrc2 values ('00','지정되지않음'),('11','역사문화환경보존지구'),('12','중요시설물보존지구'),('13','생태계보존지구'),('14','자연경관지구'),('15','수변경관지구'),\
    ('16','시가지경관지구'),('17','기타경관지구'),('18','학교시설보호지구'),('19','공용시설보호지구'),('20','항만시설보호지구'), \
    ('21','공항시설보호지구'),('22','방재지구'),('23','최고고도지구'),('24','중심지미관지구'),('25','역사문화미관지구'),('26','일반미관지구'),('27','기타미관지구'),\
    ('28','방화지구'),('29','최저고도지구'),('30',''),('31','자연취락지구'),('32','집단취락지구'),('33','특정용도제한지구'),('34','특정용도제한지구'),\
    ('35','기타특정용도제한지구'),('36','주거개발진흥지구'),('37','산업유통개발진흥지구'),('38','유통개발진흥지구'),('39','관광,휴양개발진흥지구'),('40','복합개발진흥지구'), \
    ('41','특정개발진흥지구'),('99','기타지구')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def ladUseSittn(cur):
    sql = "INSERT INTO ladUseSittn values (%s,%s)"
    file_name = "ladUseSittn.csv"
    with open(file_name) as file:
        for lines in file:
            lines = lines.replace('\n','')
            line = lines.split(',')
            var = line[0], line[1]
            try:
                cur.execute(sql,var)
            except Exception as e :
                print(e)
            

def tpgrphHgCode(cur):
    sql = "INSERT INTO tpgrphHgCode values ('00','지정되지않음'),('01','저지'),('02','평지'),('03','완경사'),\
        ('04','급경사'),('05','고지')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def tpgrphFrmCode(cur):
    sql = "INSERT INTO tpgrphFrmCode values ('00','지정되지않음'),('01','정방향'),('02','가로장방'),('03','세로장방'), \
    ('04','사다리형'),('05','삼각형'),('06','역삼각형'),('07','부정형'), ('08','자루형')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def roadSideCode(cur):
    sql = "INSERT INTO roadSideCode values ('00','지정되지않음'),('01','광대로한면'),('02','광대소각'),('03','광대세각'), \
    ('04','중로한면'),('05','중로각지'),('06','소로한면'),('07','소로각지'), ('08','세로한면(가)'), ('09','세로각지(가)'),\
    ('10','세로한면(불)'), ('11','세로각지(불)'), ('11','맹지')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)

def roadDstncCode(cur):
    sql = "INSERT INTO roadDstncCode values ('00','지정되지않음'),('01','당해지역'),('02','50M이내'),('03','100M이내'), \
    ('04','500M이내'), ('09','그이상')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)
def stdlandPosesnSeCode(cur):
    sql = "INSERT INTO stdlandPosesnSeCode values ('0','일본인,창씨명'),('1','개인'),('2','국유지'),('3','외국인,외국공공기관'), \
    ('4','시,도유지'),('5','군유지'),('6','법인'),('7','종중'), \
    ('8','종교단체'),('9','기타단체')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)
def posesnStle(cur):
    sql = "INSERT INTO posesnStle values ('0','지정되지않음'),('1','단독소유'),('2','공동소유')"
    try:
        cur.execute(sql)
    except Exception as e :
        print(e)
main()

#('11',''),('12',''),('13',''),('14',''),('15',''),('16',''),('17',''),('18',''),('19',''),('20',''), \
#('21',''),('22',''),('23',''),('24',''),('25',''),('26',''),('27',''),('28',''),('29',''),('30',''), \