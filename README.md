# coupang_crawler

로봇비전랩 간식 주문을 위한 쿠팡 크롤러입니다.

## 사용법
- 파이썬 파일이 위치한 경로에 data 폴더를 만들고, coupang_url.txt 파일을 생성합니다.
- coupang_url.txt 파일의 각 줄에는 담고자하는 상품의 url과 수량을 띄어쓰기로 구분하여 작성합니다. ex) https://coupang.com/robotvision 3
- python coupang_crawler.py 로 실행하면 data 폴더에 coupang.xlsx 엑셀 파일이 생성됩니다.
