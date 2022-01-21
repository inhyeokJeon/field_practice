### 1. 표준지공시지가정보 적재
    main.py -o 1 실행시키면 표준지공시지가정보서비스 API로부터 nsdi DB의 LandPriceAttribute 테이블에 데이터적재

### 2. 공동주택가격정보 적재
    main.py -o 2 실행시키면 공동주택가격정보서비스 API로부터 nsdi DB의 ApartHousingPriceAttribute 테이블에 데이터적재

### 3. 개별공시지가정보 적재
    main.py -o 3 실행시키면 개별공시지가정보서비스 API로부터 nsdi DB의 getIndvdLandPriceAttr 테이블에 데이터적재

### 4. 개별주택가격정보 적재
    main.py -o 4 실행시키면 개별주택가격정보서비스 API로부터 nsdi DB의 getIndvdHousingPriceAttr 테이블에 데이터적재

### 참고폴더
    개별공시지가정보서비스 : 개별공시지가정보서비스 명세
    공동주택가격정보서비스 : 공동주택가격정보서비스 명세
    개별공시지가정보서비스 : 개별공시지가정보서비스 명세
    개별주택가격정보서비스 : 개별주택가격정보서비스 명세   

### 사용소스코드
    DataToLookuptable.py : 속성조회에 필요한 특수지구분코드 치계(regstrSeCode), 지목코드 체계(lndcgrCode), 실제지목코드 체계(realLndcgrCode), 용도지역코드1 체계(prposArea1), 용도지역코드2 체계(prposArea2), 용도지구코드1 체계(prposDstrc1), 용도지구코드2 체계(prposDstrc2), 토지이용상황코드 체계(ladUseSittn), 지형높이코드 체계(tpgrphHgCode), 지형형상코드 체계(tpgrphFrmCode), 도로측면코드 체계(roadSideCode), 도로거리코드 체계(roadDstncCode), 표준지소유구분코드 체계 (stdlandPosesnSeCode),소유형태코드 체계(posesnStle) 정보들을 각테이블에 적재한다.

### 개발일지
    2021-01-12 : 현재 완료 모든 기능 동작 확인했으나, 
                방대한 데이터로 인해 API문제 발생 -> 현재 해결방안 모색중
