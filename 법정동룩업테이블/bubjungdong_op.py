import pymysql


class main:
    def __init__(self, txtFileName):
        self.fileName = txtFileName
        self.con = pymysql.connect(
            host='1.234.5.16',
            user='dev22',
            password='aimypie111@',
            charset='utf8',
            db='nsdi',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def txtFileToArray(self):
        file = open(self.fileName, 'r', encoding='utf-8')
        try:
            lines = file.readlines()

        except UnicodeDecodeError as e:
            print("Change Encoding 'UTF-8' -> 'EUC-KR'")

            try:
                file = open(self.fileName, 'r', encoding='euc-kr')
                lines = file.readlines()

            except Exception as e:
                print(str(e))

        file.close()
        return lines

    def strListToTupleList(self, lines):
        tupleList = []
        for line in lines:
            column = line.split('\t')
            code = column[0]  # 법정동코드
            name = column[1].split(' ')  # 법정동명
            real = column[2].replace('\n', '')  # 폐지여부

            if '존재' == real:
                flag = 'Y'
            else:
                flag = 'N'

            if len(name) == 1:
                var = (code, name[0], '', '', '', '', flag)
            if len(name) == 2:
                var = (code, name[0], name[1], '', '', '', flag)
            if len(name) == 3:
                var = (code, name[0], name[1], name[2], '', '', flag)
            if len(name) == 4:
                var = (code, name[0], name[1], name[2], name[3], '', flag)
            if len(name) == 5:
                var = (code, name[0], name[1], name[2], name[3], name[4], flag)

            tupleList.append(var)

        return tupleList

    def getTableInstance(self, tableName:str):
        sql = "SELECT * \
                FROM %(table)s"
        try:
            self.cur.execute(sql % {"table": tableName})
            instances = self.cur.fetchall()

        except Exception as e:
            print(str(e))

        return instances

    def insertIntoEmptyTable(self, codeLevelFlags, sql):  # DB에 데이터를 저장.
        try:
            self.cur.executemany(sql, codeLevelFlags)
            self.con.commit()

        except Exception as e:
            print(str(e))

    def strListToDictList(self, lines):
        DictList = []
        for line in lines:
            column = line.split('\t')
            code = column[0]  # 법정동코드
            name = column[1].split(' ')  # 법정동명
            real = column[2].replace('\n', '')  # 폐지여부

            if '존재' == real:
                flag = 'Y'
            else:
                flag = 'N'

            if len(name) == 1:
                dict = {'ldongCd': code,
                        'level1': name[0],
                        'level2': '',
                        'level3': '',
                        'level4': '',
                        'level5': '',
                        'flag': flag}
            if len(name) == 2:
                dict = {'ldongCd': code,
                        'level1': name[0],
                        'level2': name[1],
                        'level3': '',
                        'level4': '',
                        'level5': '',
                        'flag': flag}
            if len(name) == 3:
                dict = {'ldongCd': code,
                        'level1': name[0],
                        'level2': name[1],
                        'level3': name[2],
                        'level4': '',
                        'level5': '',
                        'flag': flag}
            if len(name) == 4:
                dict = {'ldongCd': code,
                        'level1': name[0],
                        'level2': name[1],
                        'level3': name[2],
                        'level4': name[3],
                        'level5': '',
                        'flag': flag}
            if len(name) == 5:
                dict = {'ldongCd': code,
                        'level1': name[0],
                        'level2': name[1],
                        'level3': name[2],
                        'level4': name[3],
                        'level5': name[4],
                        'flag': flag}

            DictList.append(dict)

        return DictList

    def getUpdatedInstances(self, codeLevelFlags, tableInstances):
        updatedInstances = []

        if len(tableInstances) == len(codeLevelFlags):
            print("CALCULATING...")
            for i in range(0, len(codeLevelFlags)):

                if tableInstances[i]['flag'] != codeLevelFlags[i]['flag']:
                    updatedInstances.append(codeLevelFlags[i])

        return updatedInstances

    def updateTable(self, updatedInstances):
        print("UPDATING...")
        query = "UPDATE bubjungdong \
                SET flag = %s \
                WHERE ldongCd = %s"
        for instance in updatedInstances:
            var = (instance['flag'], instance['ldongCd'])
            try:
                self.cur.execute(query, var)
                self.con.commit()
            except Exception as e:
                print(str(e))

            if instance['flag'] == 'Y':
                print("Y")
            else:
                print("N")

    def start(self):

        lines = self.txtFileToArray()  # 텍스트 파일로부터 str List 입력 받음.

        tableInstances = self.getTableInstance('bubjungdong')  # table의 instance를 받아옴.

        # Table이 비어있을 때
        if len(tableInstances) == 0:
            print("bubjungdong Table is Empty")
            codeLevelFlagTupleList = self.strListToTupleList(lines)  # str List -> tuple List.
            print("INSERT INTO bubjungdong")
            self.insertIntoEmptyTable(codeLevelFlagTupleList[1:], "INSERT INTO bubjungdong \
                                                                (ldongCd, level1, level2, level3, level4, level5, flag) \
                                                                VALUES (%s, %s, %s, %s, %s, %s, %s)")
            print("SUCCESS")

        # Table에 instance가 존재할 때
        else:
            print("TABLE bubjungdong  isn't EMPTY")
            codeLevelFlagDictList = self.strListToDictList(lines)  # str List -> Dict List
            print("UPDATE VERIFICATION")  # txt값과 table의 값을 비교하여 다른 값들을 저장함.
            updatedInstances = self.getUpdatedInstances(codeLevelFlagDictList[1:], tableInstances)

            if len(updatedInstances) == 0:
                print("UPDATE IS NOT REQUIRED")  # Update 불필요

            else:
                print("UPDATE IS REQUIRED")  # Update 필요
                self.updateTable(updatedInstances)

            print("SUCCESS")
