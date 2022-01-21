from tqdm import tqdm
import csv
import mmap
import time
import pymysql
file_path ='zzzz.csv'

con = pymysql.connect(
    host='1.234.5.16',
    user='dev22',
    password='aimypie111@',
    charset='utf8',
    db='nsdi',
    cursorclass=pymysql.cursors.DictCursor)

cur = con.cursor()
sql = "INSERT INTO region_code values (%s,%s)"
with open("zzzz.csv") as file:
    for lines in file:
        line = lines.replace('\n','')
        line = lines.split(',') 
        x = line[0]
        y = line[1]
        var = (x,y)
        cur.execute(sql,var)
con.commit()

