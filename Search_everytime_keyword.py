# Everystudy Keyword Trend - CSS 선택자 기반 날짜 추출 개선 + 연도별 상/하반기 시각화
# 목적: 사용자가 로그인한 Chrome 창에서 "열람실" 키워드 게시글을 수집하고 연도별 상반기/하반기 언급 횟수를 시각화

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime

# 스타일 설정
style.use('ggplot')  

# 디버깅 포트로 연결
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

# 날짜 연도 처리용 변수
current_year = 2025
prev_month = 12

def parse_date_with_year(month_day_str):
    global current_year, prev_month
    try:
        month, day = map(int, month_day_str.split("/"))
        if month > prev_month:
            current_year -= 1
        prev_month = month
        return f"{current_year}-{month:02d}-{day:02d}"
    except:
        return datetime.today().strftime('%Y-%m-%d')

# 게시글 수집 함수 (URL로 페이지 순회)
def collect_posts(driver, keyword_encoded, max_pages=5):
    posts = []
    base_url = "https://everytime.kr/search/all"

    for page in range(1, max_pages + 1):
        page_url = f"{base_url}/{keyword_encoded}/p/{page}"
        driver.get(page_url)
        time.sleep(2)
        print(f"\n📄 페이지 {page} 수집 중...")

        articles = driver.find_elements(By.CLASS_NAME, 'article')
        page_dates = []

        for article in articles:
            try:
                date_elements = article.find_elements(By.CSS_SELECTOR, 'time.small')
                if date_elements and date_elements[0].text.strip():
                    date = date_elements[0].text.strip()
                    parsed_date = parse_date_with_year(date)
                    content = article.text
                    posts.append({'date': parsed_date, 'content': content})
                    page_dates.append(parsed_date)
                    print(parsed_date)
                else:
                    pass
                    #print("[SKIP] 날짜 정보 없음 또는 비어 있음")
            except Exception as e:
                print(f"[ERROR] 게시글 처리 실패: {e}")
                continue

        if page_dates:
            print(f"📅 페이지 {page} 수집된 날짜들: {sorted(set(page_dates))}")
        else:
            print(f"⚠️ 페이지 {page}에서 날짜 데이터 없음")

    return posts

# 날짜별 언급 수 계산
def count_mentions_by_date(posts):
    valid_posts = [p for p in posts if 'date' in p]
    df = pd.DataFrame(valid_posts)
    if df.empty:
        print("❗ 유효한 날짜 데이터를 가진 게시글이 없습니다.")
        return pd.DataFrame(columns=['date', 'mentions'])
    count_by_date = df.groupby('date').size().reset_index(name='mentions')
    return count_by_date

# 연도별 상/하반기 합산 후 그래프 출력
def plot_mentions(count_by_date):
    if count_by_date.empty:
        print("📉 표시할 데이터가 없습니다.")
        return

    # 날짜 분해
    count_by_date['date'] = pd.to_datetime(count_by_date['date'])
    count_by_date['year'] = count_by_date['date'].dt.year
    count_by_date['month'] = count_by_date['date'].dt.month
    count_by_date['half'] = count_by_date['month'].apply(lambda m: 'H1' if m <= 6 else 'H2')

    # 연도별 상/하반기 그룹화
    summary = count_by_date.groupby(['year', 'half'])['mentions'].sum().reset_index()
    summary['period'] = summary['year'].astype(str) + ' ' + summary['half']

    # 시각화
    plt.figure(figsize=(8,5))
    plt.bar(summary['period'], summary['mentions'],
        color='skyblue', edgecolor='black') 
    plt.title("Keyword Mentions from \"Every time\"", fontsize=14)
    plt.xlabel("Period", fontsize=12)
    plt.ylabel("Mentions", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 메인 실행 함수
if __name__ == '__main__':
    posts = collect_posts(driver, '%EC%97%B4%EB%9E%8C%EC%8B%A4', max_pages=50)
    driver.quit()

    count_by_date = count_mentions_by_date(posts)
    print(count_by_date)
    plot_mentions(count_by_date)
