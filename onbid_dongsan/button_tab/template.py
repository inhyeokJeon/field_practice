#그룹 1: 물건기본자동차운송장비정보[자동차, 선박, 항공기, 철도, 이륜차] 템플릿
template_1 = {
    "제조사": "",
    "차종": "",
    "모델명": "",
    "수량": "",
    "연식": "",
    "차량번호": "",
    "주행거리": "",
    "배기량": "",
    "변속기": "",
    "연료": "",
    "기타사항": ""
}
#그룹 2: 물건기본기타동산정보[자동차 및 운송장비 부품] 템플릿
template_2 = {
    "제조사": "",
    "물품명": "",
    "모델명": "",
    "수량": "",
    "제조년도": "",
    "생산지/원산지": "",
    "사용기간": "",
    "크기(가로 x 세로 x 너비)": "",
    "무게": "",
    "기타사항": ""
}
#그룹 3: 물건기본기타동산정보[물품] 템플릿
template_3 = {
    "제조사": "",
    "물품명": "",
    "모델명": "",
    "수량": "",
    "제조년도": "",
    "생산지/원산지": "",
    "사용기간": "",
    "크기(가로 x 세로 x 너비)": "",
    "무게": "",
    "기타사항": ""
}
#그룹 4: 물건기본기타동산정보[예술품] 템플릿
template_4 = {
    "작품명": "",
    "작가명": "",
    "제작(추정)년도": "",
    "규격": "",
    "수량": "",
    "기타사항": "",
}
#그룹 5: 물건기본회원권정보[콘도회원권] 템플릿
template_5 = {
    "회원권(증서)명": "",
    "회원권(증서)번호": "",
    "수량": "",
    "기타사항": ""
}
#그룹 6: 물건기본유가증권정보[주식] 템플릿
template_6 = {
    '법인명': "",
    '지분율': "",
    '주식의 종류': "",
    '주당액면가': "",
    '액면총액': "",
    '대표자': "",
    '연락처': "",
    '발행주식총수(주)': "",
    "설립일자": "",
    "결산월": "",
    "업종": "",
    "주요제품": "",
    "본점소재지": "",
    "기타사항": "",

    #----템플릿
    "증권명": "",
    "수량": "",
    "종목명": ""
    #"지분율": "",
    #"주당액면가"
    #"액면총액"
    #기타사항
}

#그룹 7: 기타권리 템플릿
template_7 = {
    "재산명": "",
    "수량": "",
    "기타사항": ""
}
#그룹 8: 회원권 및 유가증권[NPL] 템플릿
template_8 = {
    "매각금융회사": "",
    "NPL종류": "",
    "채권금액": "",
    "양도자산확정일": "",
    "기타사항": ""
}

#이전것들
'''
        self.dict_gamjung: dict = {  # 감정평가정보
            '감정평가기관': "",
            '평가일': "",
            '평가금액(원)': "",
            '감정평가서': ""
        }
        self.basic_info_car: dict = {  # 물건 세부 정보 버튼.
            '제조사': "",
            '차종': "",
            '모델명': "",
            '수량': "",
            '연식': "",
            '차량번호': "",
            '주행거리': "",
            '배기량': "",
            '변속기': "",
            '연료': "",
            # -----22 자동차 그룹에 템플릿 2 번 것들도있네 하
            '물품명': "",
            '수량': "",
            '생산지/원산지': "",
            '사용기간': "",
            '크기': "",
            '무게': "",
            # -----22
            # -----33 템플릿 3 번
            '제조년도': "",
            '기타사항': "",
            # ---------
            '지번': "",
            '도로명': "",
            '보관장소': "",
            # ----------
            '명도이전책임': "",
            '인도장소': "",
            '부대조건': "",
            # ----------
            '감정평가정보': [],
            'file_info': {}
        }
        self.basic_info_gigae: dict = {
            "제조사": "",
            "물품명": "",
            "모델명": "",
            "수량": "",
            "제조년도": "",
            '생산지/원산지': "",
            "사용기간": "",
            "크기": "",
            "무게": "",
            "기타사항": "",
            "지번": "",
            "도로명": "",
            "보관장소": "",
            # ----------
            '명도이전책임': "",
            '인도장소': "",
            '부대조건': "",
            # ----------
            '감정평가정보': [],
            'file_info': {}
        }
        self.basic_info_gita: dict = {  # 용도 = 물품(기계), 물품(기타)
            '제조사': "",
            '물품명': "",
            '모델명': "",
            '수량': "",
            '제조년도': "",
            '생산지/원산지': "",
            '사용기간': "",
            '크기': "",
            '무게': "",
            '기타사항': "",
            # --------- 예술품
            # '제조사': "",
            '작가명': "",
            '제작(추정)년도': "",
            '규격': "",
            # '수량': "", 중복
            # '기타사항': "",
            # ---------
            '지번': "",
            '도로명': "",
            '보관장소': "",
            # ----------
            '명도책임': "",
            '부대조건': "",
            # ----------
            '감정평가정보': []
        }
        self.basic_info_stock: dict = {  # 용도 = 권리 / 증권
            # group6
            # -----물건기본회원권정보
            # -----group7 무형자산
            '재산명': "",
            '수량': "",
            '기타사항': "",
            '감정평가정보': [],
            '명도이전책임': [],
            # -----기본회원권
            '회원권(증서)명': "",
            '회원권(증서)번호': "",
            # '수량': "", 중복
            # '기타사항': "", 중복
            # -----물건기본유가증권정보
            '법인명': "",
            '지분율': "",
            '주식의 종류': "",
            '주당액면가': "",
            '액면총액': "",
            '대표자': "",
            '연락처': "",
            '발행주식총수(주)': "",
            "설립일자": "",
            "결산월": "",
            "업종": "",
            "주요제품": "",
            "본점소재지": "",
            "주요주주현황": [],
            "재무현황정보": [],
            # "기타사항": "" 중복
            # -----기타권리, 회원권, 유가증권
            '매각금융회사': "",
            'NPL종류': "",
            '채권금액': "",
            '양도자산확정일': "",
            "파일정보": [],
            # '기타사항': "", 중복

        }

        self.dict_file_info = {
            "채권내역": "",
            "구비서류": "",
            "기타": ""
        }

        self.dict_mainjuju = {
            "주주명": "",
            "지분율": "",
            "보유주식수": "",
            "비고": ""
        }
        self.dict_jaemu = {
            '재무년도': "",
            '유동자산': "",
            '비유동자산': "",
            '자산총계': "",
            '유동부채': "",
            '비유동부채': "",
            '부채총액': "",
            '자본금': "",
            '자본잉여금': "",
            '자본조정': "",
            '기타포괄손익누계액': "",
            '이익잉여금': "",
            '자본총계': "",
            '매출액': "",
            '매출총이익': "",
            '영업이익': "",
            '영업이익외수익': "",
            '영업외비용': "",
            '당기순이익': "",
            '주당배당율': "",
            '매출액증가율': "",
            '순이익증가율': "",
            '매출액순이익률': "",
            '자기자본순이익률': "",
            '자기자본회전율': "",
            '부채비율': ""
        }
'''