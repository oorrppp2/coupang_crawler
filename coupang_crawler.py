import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
import sys

"""
    Usage
        - 파이썬 파일이 위치한 경로에 data 폴더를 만들고, coupang_url.txt 파일을 생성합니다.
        - coupang_url.txt 파일의 각 줄에는 담고자하는 상품의 url과 수량을 띄어쓰기로 구분하여 작성합니다. ex) https://coupang.com/robotvision 3
        - python coupang_crawler.py 로 실행하면 data 폴더에 coupang.xlsx 엑셀 파일이 생성됩니다.
"""

headers = {"authority": "www.coupang.com",
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36",
    "sec-ch-ua-platform": "macOS",
    "cookie": "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;"}

# 크롤링할 웹 페이지 URL txt 파일 읽기
file = open("./data/coupang_url.txt", 'r')

xl = openpyxl.Workbook()
ws = xl.active

align_center = Alignment(horizontal='center', vertical='center')
align_right = Alignment(horizontal='right', vertical='center')
subtitle_color = PatternFill('solid', fgColor='C8C8FF')

ws['B2'].value = '제품명'
ws['B2'].alignment = align_center
ws['B2'].fill = subtitle_color
ws['C2'].value = '수량'
ws['C2'].alignment = align_center
ws['C2'].fill = subtitle_color
ws['D2'].value = '링크'
ws['D2'].alignment = align_center
ws['D2'].fill = subtitle_color
ws['E2'].value = '가격'
ws['E2'].alignment = align_center
ws['E2'].fill = subtitle_color

index = 3
total_price = 0

while True:
    # 크롤링할 웹 페이지 URL
    data = file.readline().split()
    if not data: break
    url = data[0]
    ea = data[1]

    # requests 모듈을 사용하여 웹 페이지의 HTML 코드 가져오기
    html = requests.get(url=url, headers=headers).content

    # BeautifulSoup을 사용하여 HTML 코드 파싱
    soup = BeautifulSoup(html, 'html.parser')

    product_name = soup.find(attrs={"class", "prod-buy-header__title"}).get_text()
    price = soup.strong.get_text()

    ws['B{}'.format(index)].value = product_name
    ws['C{}'.format(index)].value = ea
    ws['C{}'.format(index)].alignment = align_center
    ws['D{}'.format(index)].value = url
    ws['E{}'.format(index)].value = price
    ws['E{}'.format(index)].alignment = align_center

    index += 1
    total_price += int(price[:-1].replace(',','')) * int(ea)

ws.column_dimensions['B'].width = 70
ws.column_dimensions['C'].width = 10
ws.column_dimensions['D'].width = 100
ws.column_dimensions['E'].width = 20
ws['D{}'.format(index+1)].value = "총계   "
ws['D{}'.format(index+1)].alignment = align_right
ws['E{}'.format(index+1)].value = format(total_price, ',') + "원"
ws['E{}'.format(index+1)].alignment = align_center
xl.save('./data/coupang.xlsx')