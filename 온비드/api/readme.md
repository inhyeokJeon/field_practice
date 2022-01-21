# 온비드_API
## 1. 실행 방법
>  python Onbid.py -o (1~10)
> 1. 통합조회 , UnifyUsageCltr
> 2. 기본상세조회 , UnifyUsageCltrBasicInfoDetail
> 3. 감정평가서정보 상세조회 , UnifyUsageCltrEstimationInfoDetail
> 4. 임대차정보 상세조회 , UnifyUsageCltrRentalInfoDetail
> 5. 권리종류정보 상세조회 , UnifyUsageCltrRegisteredInfoDetail
> 6. 공매일정 상세조회 , UnifyUsageCltrBidDateInfoDetail
> 7. 입찰이력 상세조회 , UnifyUsageCltrBidHistoryInfoDetail
> 8. 주주정보 상세조회 , UnifyUsageCltrStockholderInfoDetail
> 9. 법인현황정보 상세조회 , UnifyUsageCltrCorporatebodyInfoDetail
> 10. 캠코 기본정보 상세조회(캠코물건조회API) , KamcoPlnmPbctBasicInfoDetail

## 2. 소스코드
> 1. Onbid.py
> > main 실행파일  
> 2. setup.py
> + class => setup
> > + __init__ -> db설정 변수, api key를 설정한다.
> > + set_value -> dictionary를 tuple형태로 return 한다.
> > + STORE_DATA_INTO_TABLE -> dictionary를 tuple로 변환하고 테이블에데이터 에 적재한다.
> > + GET_DATA_FROM_API -> API로 부터 DATA요청하고 응답데이터의 item부분만 추출한 데이터를 return.
> 3. InfoDetail.py
> + class => InfoDetail
> > + setup 클래스를 상속받는다.
> > + set_url -> API요청에 필요한 url을 설정해준다.
> > + get_CLTR_NO_from_self -> 작업중인 테이블의 가장큰 CLTR_NO 를 가져와 리턴한다.
> > + get_number_from_UnifyUsageCltr -> 통합용도별물건목록조회로부터 물건번호 공매번호 가져와 list 형식으로 return.
> > + COMPARE_TEMPLATE -> api요청 template 과 비교하여 data 비교를 저장후 template형태의 dictionary로 리턴. 
> > + start -> 실행.
> 4. Detial.py
> + class => Detail
> > + InfoDetail 를 상속받는다.
> > + request_api_and_insert_into_db -> [CLTR_NO, PBCT_NO]를 이용해 page를 증가하며 요청하여 db에 적재한다.
> > + set_value -> 중복을 없애기 위해 테이블의 모든 column 을 hashing 해 table hash column 에 저장
> > + set_url -> API요청에 필요한 url을 설정해준다.
> 5. UnifyUsageCltr.py
> + class => UnifyUsageCltr
> > + set_url -> API요청에 필요한 url을 설정해준다.
> > + COMPARE_TEMPLATE -> api요청 template 과 비교하여 data 비교를 저장후 template형태의 dictionary로 리턴. 
> > + get_latest_db_value -> 가장큰 CTGR_HIRK_ID를 table로 부터 가져와 리턴
> > + GET_CTGR_HIRK_ID_LIST -> ONBID_TopCodeInfo 테이블로부터 CTGR_HIRK_ID 리스트를 가져온다.
> > + request_api_and_insert_into_db -> [CTGR_HIRK_ID] list 을 이용해 pageNo를 증가하며 요청하여 db에 적재한다.
> > + start -> 실행
> 6. UnifyUsageCltrBasicInfoDetail.py 
> + class -> UnifyUsageCltrBasicInfoDetail
> > + api_to_template_form -> 해당 카테고리의 해당하는 부분(입찰방식 다음것 ~ 입찰시작가 전) 을
>       dict 형식으로 ITEM_INFO key값의 value로 저장한다.
>       api응답값을 template 형식에 맞게 변환하여 return 한다.
> > + request_api_and_insert_into_db -> [CLTR_NO, PBCT_NO]를 이용해 page를 증가하며 요청하여 db에 적재한다.
> > + get_number_from_UnifyUsageCltr -> 통합용도별물건목록조회로부터 물건번호 공매번호 가져오기
> > + start -> 실행
> 7. UnifyUsageCltrEstimationInfoDetail , UnifyUsageCltrRentalInfoDetail
> UnifyUsageCltrRegisteredInfoDetail, UnifyUsageCltrBidDateInfoDetail
> UnifyUsageCltrBidHistoryInfoDetail, UnifyUsageCltrStockholderInfoDetail
> UnifyUsageCltrCorporatebodyInfoDetail
> > + Detail class 를 상속 받는다.
> > + 각 API의 요청 주소와 데이터베이스의 테이블 이름만 지고 상속받은 기능을 사용한다. 
>
> 8. KamcoPlnmPbctBasicInfoDetail.py -> 테스트 해봐야합니다.

## Class 계층구조 ( 대략적 )

![image-20210304181106184](C:\Users\inhyeok_com\AppData\Roaming\Typora\typora-user-images\image-20210304181106184.png)
