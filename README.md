# coupang_crawler

로봇비전랩 간식 주문을 위한 쿠팡 크롤러입니다.

## 사용법
### Version 1. 23.05.10
- 파이썬 파일이 위치한 경로에 data 폴더를 만들고, coupang_url.txt 파일을 생성합니다.
- coupang_url.txt 파일의 각 줄에는 담고자하는 상품의 url과 수량을 띄어쓰기로 구분하여 작성합니다. ex) https://coupang.com/robotvision 3
- python coupang_crawler_v1.py 로 실행하면 data 폴더에 coupang.xlsx 엑셀 파일이 생성됩니다.


### Version 2. 23.07.04
- 이번 버전에서는 UI를 디자인하여 UI에 직접 입력할 수 있게 구현했습니다.
- 구매할 쿠팡 주소와 수량을 입력하고 "추가" 버튼을 누르면 자동으로 표가 업데이트 됩니다.
- "추가" 버튼을 누르면 자동으로 총액이 업데이트되고, 중간에 표에서 수량을 직접 수정할 수 있습니다. 수정 후 "총액갱신" 버튼을 눌러 총액을 업데이트 할 수 있습니다.
- 수량에 숫자가 아닌 문자를 입력하거나 유효하지 않은 구매링크를 입력할 경우 에러 팝업이 뜹니다.
- 총액 50만원 초과시 빨간색으로 글자색이 변경됩니다.
- 입력을 마친 후 "엑셀로 내보내기" 버튼을 눌러 엑셀 파일을 생성합니다. 엑셀 파일은 data폴더의 coupang.xlsx 라는 이름으로 저장됩니다.
