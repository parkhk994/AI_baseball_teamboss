import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://gall.dcinside.com/board/lists"

# 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 제목을 저장할 리스트
titles = []

# 몇 페이지부터 몇 페이지까지
for i in range(1, 10):
    # 파라미터 설정
    params = {'id': 'tigers_new2', 'page': i}

    response = requests.get(BASE_URL, params=params, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # 실질적 글 목록 부분
    article_list = soup.find('tbody').find_all('tr')

    # 한 페이지에 있는 모든 게시물을 긁어오는 코드
    for tr_item in article_list:
        # 제목 추출
        title_tag = tr_item.find('a', href=True)
        if title_tag:
            title = title_tag.text.strip()  # 제목 텍스트 가져오기
            print("제목: ", title)
            # print("주소: ", title_tag['href'])
            titles.append({'title': title})

    time.sleep(1)  # 요청 간 간격을 두기 위해 대기

# 데이터프레임 생성
df_titles = pd.DataFrame(titles)

# 결과 출력
print(df_titles.head())

# CSV 파일로 저장
df_titles.to_csv('./crawling_data/dcinside_tigers_titles.csv', index=False)  # 현재 날짜로 저장
print("크롤링 완료!")