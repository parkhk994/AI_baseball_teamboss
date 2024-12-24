import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = "https://gall.dcinside.com/board/lists"

# 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

category = ['KIA', 'SAMSUNG', 'KIWOOM', 'LG', 'LOTTE', 'HANWHA', 'SSG', 'NC', 'KT', 'DOOSAN']
category_url = [
    'tigers_new2',  # 기아 타이거즈
    'samsunglions_new',  # 삼성 라이온즈
    'sh_new',  # 키움 히어로즈
    'lgtwins_new',  # LG 트윈스
    'giants_new3',  # 롯데 자이언츠
    'hanwhaeagles_new',  # 한화 이글스
    'skwyverns_new1',  # SSG 랜더스
    'ncdinos',  # NC 다이노스
    'ktwiz',  # KT 위즈
    'doosanbears_new1'  # 두산 베어스
]

for j in range(0,1):  # 인덱스 0부터 4까지
    # 제목을 저장할 리스트
    titles = []
    # 몇 페이지부터 몇 페이지까지
    for i in range(1, 16):
        # 파라미터 설정
        params = {'id': category_url[j], 'page': i}

        response = requests.get(BASE_URL, params=params, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        # 실질적 글 목록 부분
        article_list = soup.find('tbody').find_all('tr')

        # 한 페이지에 있는 모든 게시물을 긁어오는 코드
        for tr_item in article_list:
            # 제목 추출
            title_tag = tr_item.find('a', href=True)
            if title_tag:
                try:
                    title = title_tag.text.strip()  # 제목 텍스트 가져오기
                    title = re.compile('[^가-힣 ]').sub(' ', title)  # 한글과 띄어쓰기만 남기기
                    # titles.append({'title': title})
                    print(f"{title},{category[j]}")
                except:
                    print(f"Error extracting title from row {i}: {e}")

        time.sleep(1)  # 요청 간 간격을 두기 위해 대기

    # 데이터프레임 생성
    df_titles = pd.DataFrame(titles)

    # 결과 출력
    print(df_titles.head())

    # CSV 파일로 저장
    df_titles.to_csv('./crawling_data/dcinside_{}_titles.csv'.format(category[j]), index=False)  # 현재 날짜로 저장

print("크롤링 완료!")