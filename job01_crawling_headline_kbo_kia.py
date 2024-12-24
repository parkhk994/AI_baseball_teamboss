import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://gall.dcinside.com/board/lists"

# 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 카테고리와 크롤링할 URL 매핑
categories = ['KIA', 'SAMSUNG', 'KIWOOM', 'LG', 'LOTTE', 'HANWHA', 'SSG', 'NC', 'KT', 'DOOSAN']
ids = [
    'tigers_new2', 'samsunglions_new', 'sh_new', 'lgtwins_new', 'giants_new3',
    'hanwhaeagles_new', 'skwyverns_new1', 'ncdinos', 'ktwiz', 'doosanbears_new1'
]

# 전체 데이터 저장
all_titles = []

# 카테고리별로 크롤링
for category, gall_id in zip(categories, ids):
    print(f"크롤링 중: {category} 갤러리")
    for i in range(1, 15):  # 1페이지부터 14페이지까지
        # 파라미터 설정
        params = {'id': gall_id, 'page': i}

        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 실질적 글 목록 부분
            article_list = soup.find('tbody').find_all('tr')

            # 한 페이지에 있는 모든 게시물을 긁어오기
            for tr_item in article_list:
                # 제목 추출
                title_tag = tr_item.find('a', href=True)
                if title_tag:
                    title = title_tag.text.strip()  # 제목 텍스트 가져오기
                    print(f"{title}, {category}")
                    all_titles.append({'Title': title, 'Category': category})
        else:
            print(f"페이지 {i} 요청 실패 (상태 코드: {response.status_code})")

        time.sleep(1)  # 요청 간 간격을 두기 위해 대기

# 데이터프레임 생성
df_titles = pd.DataFrame(all_titles)

# 결과 출력
print(df_titles.head())

# CSV 파일로 저장
df_titles.to_csv('./crawling_data/dcinside_titles_with_categories.csv', index=False, encoding='utf-8-sig')
print("크롤링 완료!")
