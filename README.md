# Search_everytime

에브리타임 전체글에서 특정 키워드를 검색하고, 날짜별 언급 횟수를 **연도별 상/하반기 그래프**로 시각화하는 도구입니다.

---

## 동작 방식

```
Chrome 디버깅 모드 실행
    → 에브리타임 로그인
    → 스크립트 실행
    → 키워드 검색 결과 수집 (최대 N페이지)
    → 날짜 파싱 및 집계
    → 연도별 상/하반기 막대 그래프 출력
```

---

## 사전 준비

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Chrome 디버깅 모드 실행
```bash
# Windows
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="/tmp/ChromeDebug"
```

### 3. 에브리타임 로그인
열린 Chrome 창에서 [everytime.kr](https://everytime.kr) 에 로그인합니다.

---

## 실행

```bash
python Search_everytime_keyword.py
```

---

## 설정 변경

[Search_everytime_keyword.py](Search_everytime_keyword.py) 하단의 메인 실행부에서 수정합니다.

```python
if __name__ == '__main__':
    posts = collect_posts(driver, '%EC%97%B4%EB%9E%8C%EC%8B%A4', max_pages=50)
    #                              ↑ 검색 키워드 (URL 인코딩)     ↑ 최대 수집 페이지 수
```

| 항목 | 기본값 | 설명 |
|------|--------|------|
| 키워드 | `열람실` | URL 인코딩 필요 ([변환 도구](https://www.urlencoder.org/ko/)) |
| max_pages | `50` | 수집할 최대 페이지 수 |
| current_year | `2025` | 기준 연도 (연도가 바뀌면 수동 업데이트) |

---

## 출력 예시

```
📄 페이지 1 수집 중...
2025-05-01
2025-04-28
📅 페이지 1 수집된 날짜들: ['2025-04-28', '2025-05-01']
...
```

막대 그래프: X축 `연도 H1/H2`, Y축 `언급 횟수`

---

## 주의사항

- 반드시 **디버깅 모드 Chrome**에서 에브리타임에 로그인한 상태로 실행해야 합니다.
- 페이지 수가 많을수록 수집 시간이 길어집니다 (페이지당 약 2초).
- 에브리타임의 HTML 구조가 변경되면 CSS 선택자 수정이 필요할 수 있습니다.
