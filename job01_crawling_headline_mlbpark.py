from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def crawl_mlbpark_kia_posts():
    # Chrome 옵션 설정
    options = ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 웹드라이버 설정
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 페이지 로드
        url = "https://mlbpark.donga.com/mp/b.php?search_select=sct&search_input=&select=spf&m=search&b=kbotown&query=KIA"
        driver.get(url)

        # 페이지 로딩 대기
        time.sleep(5)

        # 게시글 제목 수집
        titles = []

        # 제목 링크 요소 찾기 (제공해주신 HTML 구조에 맞게 선택자 수정)
        title_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "txt")]')

        for element in title_elements:
            try:
                title = element.text.strip()
                titles.append(title)
            except Exception as e:
                print(f"제목 추출 중 오류: {e}")

        # 결과 출력 및 CSV 저장
        print(f"총 {len(titles)}개의 게시글 제목 수집 완료")

        # 데이터프레임 생성 및 CSV 저장
        df = pd.DataFrame({'titles': titles})
        df.to_csv('./crawling_data/mlbpark_kia_titles.csv', index=False, encoding='utf-8-sig')

        # 제목 출력
        for title in titles:
            print(title)

        return df

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

    finally:
        # 브라우저 종료
        driver.quit()


# 크롤링 실행
crawl_mlbpark_kia_posts()