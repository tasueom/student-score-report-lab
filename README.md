# student-score-report-lab

Flask 기반 학생 성적 관리 웹 애플리케이션으로, MySQL에 데이터를 저장하고 Chart.js로 시각화합니다.

## 주요 기능

### ✅ 구현 완료

#### 인증 및 권한 관리
- **회원가입**: 학번, 비밀번호, 반, 이름으로 회원가입
- **로그인/로그아웃**: 세션 기반 인증
- **권한 분리**: 관리자와 일반 학생 역할 구분

#### 관리자 기능
- **성적 입력**: 개별 학생 성적 입력 (국어, 영어, 수학)
- **성적 조회**: 전체 학생 성적을 테이블로 조회 (페이징 지원)
- **성적 수정**: 기존 성적 수정
- **성적 삭제**: 성적 삭제 기능
- **CSV 업로드**: CSV 파일로 일괄 성적 업로드
- **JSON 업로드**: JSON 파일로 일괄 성적 업로드
- **이미지 업로드**: OCR을 통한 성적표 이미지에서 데이터 추출
- **과목별 평균 시각화**: Chart.js를 사용한 바 차트
- **엑셀 내보내기**: 성적 데이터를 엑셀 파일(.xlsx)로 다운로드
- **PDF 내보내기**: 차트와 성적표를 포함한 PDF 파일 생성 및 다운로드

#### 학생 기능
- **내 성적 조회**: 로그인한 학생 본인의 성적만 조회

#### 데이터 검증
- 프론트엔드: JavaScript를 통한 실시간 입력 검증 (0-100 정수)
- 백엔드: 데이터베이스 제약 조건 및 에러 처리
- 업로드 파일 검증: CSV/JSON 파일 형식 및 데이터 타입 검증

## 기술 스택

- **Backend**: Flask 3.0.0
- **Database**: MySQL (mysql-connector-python)
- **Frontend**: HTML, CSS, JavaScript
- **차트 라이브러리**: Chart.js
- **아이콘**: Font Awesome
- **데이터 처리**: pandas (CSV/JSON 파일 처리)
- **PDF 생성**: reportlab, matplotlib
- **이미지 처리**: PIL (Pillow), pytesseract (OCR)
- **환경 변수**: python-dotenv
- **보안**: Werkzeug (비밀번호 해싱)

## 프로젝트 구조

```
student-score-report-lab/
├── app/
│   ├── __init__.py          # Flask 앱 초기화
│   ├── routes.py            # 라우트 정의
│   ├── db.py                # 데이터베이스 연결 및 쿼리
│   ├── service.py           # 비즈니스 로직 (점수 계산, 차트 데이터 포맷팅, 파일 내보내기)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # 스타일시트
│   │   └── js/
│   │       ├── chart.js     # 차트 렌더링
│   │       └── check.js     # 폼 검증
│   └── templates/
│       ├── layout.html      # 기본 레이아웃
│       ├── index.html        # 홈페이지 (README 표시)
│       ├── signup.html      # 회원가입 페이지
│       ├── signin.html      # 로그인 페이지
│       ├── input.html       # 성적 입력 페이지 (관리자)
│       ├── view.html        # 성적 조회 페이지 (관리자)
│       ├── edit.html        # 성적 수정 페이지 (관리자)
│       └── my_score.html    # 내 성적 조회 페이지 (학생)
├── sample/
│   ├── input_sample.csv     # CSV 업로드 샘플 파일
│   ├── input_sample.json    # JSON 업로드 샘플 파일
│   └── input_sample.png     # 이미지 업로드 샘플 파일
├── app.py                   # 애플리케이션 실행 파일
├── init_db.py              # 데이터베이스 초기화 스크립트
├── insert_test_students.py # 테스트 학생 데이터 삽입 스크립트
├── requirements.txt         # Python 패키지 의존성
├── .env                     # 환경 변수 (gitignore에 포함)
└── README.md               # 프로젝트 문서
```

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd student-score-report-lab
```

### 2. 가상 환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

**주의사항**: OCR 기능을 사용하려면 Tesseract OCR을 별도로 설치해야 합니다.
- Windows: [Tesseract OCR 설치](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-kor` (Ubuntu/Debian)
- Mac: `brew install tesseract tesseract-lang`
- 설치 후 기본 경로가 아닌 경우 `.env` 파일에 경로를 설정하세요.

### 4. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=scoredb

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Tesseract OCR Configuration (선택사항)
# Windows에서 기본 경로가 아닌 경우에만 설정하세요
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
# TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
# 
# Linux/Mac의 경우 보통 시스템 PATH에 있으므로 설정 불필요
# TESSERACT_CMD=/usr/bin/tesseract
# TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
```

**환경변수 설명:**
- `TESSERACT_CMD`: Tesseract 실행 파일 경로 (선택사항)
  - Windows 기본값: `C:\Program Files\Tesseract-OCR\tesseract.exe`
  - Linux/Mac: 보통 시스템 PATH에 있어서 설정 불필요
- `TESSDATA_PREFIX`: Tessdata 언어팩 경로 (선택사항)
  - Windows 기본값: `C:\Program Files\Tesseract-OCR\tessdata`
  - Linux/Mac: 보통 시스템 기본 경로 사용
- **참고**: 기본 경로에 Tesseract가 설치되어 있다면 이 설정들을 생략해도 됩니다.

### 5. 데이터베이스 초기화

```bash
python init_db.py
```

이 스크립트는 다음을 수행합니다:
- `scoredb` 데이터베이스 생성
- `students` 테이블 생성 (학번, 비밀번호, 반, 이름)
- `scores` 테이블 생성 (학번, 국어, 영어, 수학, 총점, 평균, 등급)
- 외래키 제약 설정 (`scores.id` → `students.id`)
- 관리자 계정 생성 (id: `admin`, 비밀번호: `admin`)

### 6. 테스트 데이터 삽입

#### 방법 1: 테스트 학생 삽입 스크립트 사용

```bash
python insert_test_students.py
```

이 스크립트는 테스트용 학생 10명(학번: 001~010)을 삽입합니다.
- 모든 학생의 비밀번호: `1234`

#### 방법 2: 샘플 데이터로 성적 업로드

테스트 학생을 삽입한 후, 샘플 데이터를 사용하여 성적을 업로드할 수 있습니다:

1. 관리자로 로그인 (`admin` / `admin`)
2. "성적 입력" 페이지로 이동
3. CSV 또는 JSON 버튼 클릭
4. `sample/input_sample.csv` 또는 `sample/input_sample.json` 파일 업로드

**샘플 데이터 정보:**
- `sample/input_sample.csv`: 30명의 학생 성적 데이터 (학번 001~030)
- `sample/input_sample.json`: 동일한 데이터를 JSON 형식으로 제공

### 7. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속하세요.

## 테스트 시나리오

### 전체 테스트 흐름

#### 1단계: 기본 설정 및 데이터 준비

```bash
# 1. 데이터베이스 초기화
python init_db.py

# 2. 테스트 학생 삽입
python insert_test_students.py

# 3. 애플리케이션 실행
python app.py
```

#### 2단계: 관리자 기능 테스트

1. **관리자 로그인**
   - 학번: `admin`
   - 비밀번호: `admin`

2. **성적 입력 테스트**
   - 방법 A: 개별 입력
     - "성적 입력" → 학번 선택 → 점수 입력 → 저장
   - 방법 B: CSV 업로드
     - "성적 입력" → CSV 버튼 → `sample/input_sample.csv` 업로드
   - 방법 C: JSON 업로드
     - "성적 입력" → JSON 버튼 → `sample/input_sample.json` 업로드

3. **성적 조회 테스트**
   - "성적 조회" 클릭
   - 테이블에서 입력된 성적 확인
   - 오른쪽 차트에서 과목별 평균 확인
   - 페이징 기능 확인 (10개씩 표시)

4. **성적 수정 테스트**
   - "성적 조회"에서 특정 학생의 "수정" 버튼 클릭
   - 점수 수정 후 저장
   - 자동 계산된 총점, 평균, 등급 확인

5. **성적 삭제 테스트**
   - "성적 조회"에서 특정 학생의 "삭제" 버튼 클릭
   - 확인 후 삭제

6. **파일 내보내기 테스트**
   - "성적 조회" 페이지에서:
     - 엑셀 아이콘 클릭 → 엑셀 파일 다운로드 확인
     - PDF 아이콘 클릭 → PDF 파일 다운로드 확인
       - PDF 1페이지: 과목별 평균 점수 차트
       - PDF 2페이지 이후: 전체 성적표

#### 3단계: 학생 기능 테스트

1. **회원가입**
   - "회원가입" 클릭
   - 학번: `011` (새로운 학번)
   - 비밀번호: `student123`
   - 반: `2`
   - 이름: `테스트학생`
   - 회원가입 완료

2. **학생 로그인**
   - 학번: `011`
   - 비밀번호: `student123`
   - 로그인

3. **내 성적 조회**
   - "내 성적 조회" 클릭
   - 성적이 없으면 "입력된 성적이 없습니다" 메시지 확인

4. **관리자로 성적 입력 후 재확인**
   - 관리자로 다시 로그인
   - 학번 `011`의 성적 입력
   - 학생으로 다시 로그인하여 "내 성적 조회"에서 성적 확인

#### 4단계: 에러 처리 테스트

1. **중복 성적 입력**
   - 이미 성적이 있는 학생의 성적을 다시 입력 시도
   - 에러 메시지 확인

2. **존재하지 않는 학번으로 성적 입력**
   - 가입되지 않은 학번으로 성적 입력 시도
   - 에러 메시지 확인

3. **잘못된 파일 형식 업로드**
   - CSV/JSON 형식이 아닌 파일 업로드 시도
   - 에러 처리 확인

## 사용 방법

### 관리자 로그인

1. 기본 관리자 계정으로 로그인:
   - 학번: `admin`
   - 비밀번호: `admin`

### 성적 입력

#### 개별 입력
1. 네비게이션에서 "성적 입력" 클릭
2. 성적이 없는 학생 목록에서 학번 선택
3. 국어, 영어, 수학 점수 입력 (0-100 정수)
4. "입력" 버튼 클릭
5. 자동으로 총점, 평균, 등급 계산 및 저장

#### 파일 업로드
1. "성적 입력" 페이지에서 CSV 또는 JSON 버튼 클릭
2. 업로드 폼이 나타나면 파일 선택
3. CSV 또는 JSON 파일 업로드
4. 파일 형식:
   - **CSV**: `id,kor,eng,math` 헤더 필요
   - **JSON**: `[{"id": "001", "kor": 85, "eng": 90, "math": 88}, ...]` 형식

#### 이미지 업로드 (OCR)
1. "성적 입력" 페이지에서 이미지 버튼 클릭
2. 성적표 이미지 파일 선택
3. OCR을 통해 학번, 국어, 영어, 수학 점수 자동 추출
4. 추출된 데이터 확인 후 입력

### 성적 조회

1. 네비게이션에서 "성적 조회" 클릭
2. 저장된 모든 성적을 테이블로 확인
   - 학번, 반, 이름, 국어, 영어, 수학, 총점, 평균, 등급
3. 페이징: 페이지당 10개씩 표시, 하단에서 페이지 이동
4. 각 행의 "수정" 버튼으로 성적 수정 가능
5. 각 행의 "삭제" 버튼으로 성적 삭제 가능
6. 오른쪽에 과목별 평균 점수 바 차트 확인
7. 엑셀/PDF 다운로드 버튼으로 파일 내보내기

### 성적 수정

1. "성적 조회" 페이지에서 수정할 학생의 "수정" 버튼 클릭
2. 국어, 영어, 수학 점수 수정
3. 총점, 평균, 등급은 자동 계산되어 표시 (읽기 전용)
4. "수정" 버튼 클릭하여 저장

### 성적 삭제

1. "성적 조회" 페이지에서 삭제할 학생의 "삭제" 버튼 클릭
2. 확인 대화상자에서 확인 클릭
3. 성적이 삭제되고 목록에서 제거됨

### 파일 내보내기

#### 엑셀 내보내기
1. "성적 조회" 페이지에서 엑셀 아이콘 클릭
2. `성적표.xlsx` 파일이 다운로드됨
3. 엑셀에서 열어서 데이터 확인

#### PDF 내보내기
1. "성적 조회" 페이지에서 PDF 아이콘 클릭
2. `성적표.pdf` 파일이 다운로드됨
3. PDF 내용:
   - **1페이지**: 과목별 평균 점수 막대 차트
   - **2페이지 이후**: 전체 성적표 (학번, 반, 이름, 국어, 영어, 수학, 총점, 평균, 등급)

### 학생 회원가입 및 로그인

1. 네비게이션에서 "회원가입" 클릭
2. 학번, 비밀번호, 비밀번호 확인, 반, 이름 입력
3. "회원가입" 버튼 클릭
4. 로그인 페이지에서 학번과 비밀번호로 로그인

### 내 성적 조회 (학생)

1. 로그인 후 네비게이션에서 "내 성적 조회" 클릭
2. 본인의 성적만 확인 가능
3. 국어, 영어, 수학, 총점, 평균, 등급 표시
4. 성적이 없으면 "입력된 성적이 없습니다" 메시지 표시

## 데이터베이스 스키마

### students 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | VARCHAR(50) | 학번 (기본 키) |
| pwd | TEXT | 비밀번호 (해시) |
| ban | INT | 반 |
| name | VARCHAR(50) | 이름 |

### scores 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | VARCHAR(50) | 학번 (기본 키, 외래키 → students.id) |
| kor | INT | 국어 점수 |
| eng | INT | 영어 점수 |
| math | INT | 수학 점수 |
| total | INT | 총점 |
| average | DECIMAL(5,2) | 평균 |
| grade | CHAR(1) | 등급 (A-F) |

### 외래키 관계

- `scores.id` → `students.id` (외래키 제약)
- 학생이 먼저 가입되어야 성적을 입력할 수 있음

## 등급 기준

- **A**: 평균 90점 이상
- **B**: 평균 80점 이상
- **C**: 평균 70점 이상
- **D**: 평균 60점 이상
- **F**: 평균 60점 미만

## 파일 업로드 형식

### CSV 파일 형식

```csv
id,kor,eng,math
001,85,90,88
002,92,87,95
003,78,82,80
```

### JSON 파일 형식

```json
[
  {"id": "001", "kor": 85, "eng": 90, "math": 88},
  {"id": "002", "kor": 92, "eng": 87, "math": 95},
  {"id": "003", "kor": 78, "eng": 82, "math": 80}
]
```

**주의사항:**
- `id`는 문자열로 저장되어야 함 (앞자리 0 유지)
- 점수는 0-100 사이의 정수
- 업로드 시 에러 처리:
  - 이미 성적이 있는 학번: "이미 성적이 입력된 학번입니다" 메시지
  - 가입되지 않은 학번: "가입된 학번이 아닙니다" 메시지
  - 성공한 개수만큼 "N명의 성적이 성공적으로 업로드되었습니다" 메시지

## 개발 특징

- **역할 분리**: routes, service, db 모듈로 명확한 책임 분리
- **환경 변수 관리**: 하드코딩 없이 `.env` 파일로 설정 관리
- **에러 처리**: 데이터베이스 연결 및 쿼리 예외 처리
- **보안**: 비밀번호 해싱, 세션 관리, 관리자 권한 체크
- **프론트엔드 검증**: JavaScript를 통한 실시간 입력 검증
- **반응형 디자인**: 모바일과 데스크톱 환경 모두 지원
- **사용자 경험**: Flash 메시지를 통한 피드백 제공
- **페이징**: 대량의 데이터를 효율적으로 표시
- **파일 내보내기**: 엑셀, PDF 형식으로 데이터 내보내기 지원

## 주요 라우트

| 경로 | 메서드 | 설명 | 권한 |
|------|--------|------|------|
| `/` | GET | 홈페이지 (README 표시) | 모두 |
| `/signup` | GET, POST | 회원가입 | 모두 |
| `/signin` | GET, POST | 로그인 | 모두 |
| `/signout` | GET | 로그아웃 | 로그인 필요 |
| `/input` | GET, POST | 성적 입력 | 관리자 |
| `/view` | GET | 성적 조회 | 관리자 |
| `/edit/<id>` | GET, POST | 성적 수정 | 관리자 |
| `/delete/<id>` | GET | 성적 삭제 | 관리자 |
| `/upload_csv` | POST | CSV 업로드 | 관리자 |
| `/upload_json` | POST | JSON 업로드 | 관리자 |
| `/upload_img` | POST | 이미지 업로드 (OCR) | 관리자 |
| `/export_excel` | GET | 엑셀 내보내기 | 관리자 |
| `/export_pdf` | GET | PDF 내보내기 | 관리자 |
| `/my_score` | GET | 내 성적 조회 | 학생 |

## 문제 해결

### Tesseract OCR 오류
- OCR 기능 사용 시 Tesseract 설치 필요
- Windows 기본 경로: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- 기본 경로가 아닌 경우 `.env` 파일에 `TESSERACT_CMD`와 `TESSDATA_PREFIX` 설정
- Linux/Mac은 보통 시스템 PATH에 있어서 별도 설정 불필요

### 한글 폰트 문제 (PDF)
- PDF 생성 시 한글이 깨질 경우:
  - Windows: 맑은 고딕 폰트가 자동으로 감지됨
  - Linux/Mac: 한글 폰트 파일 경로를 `app/service.py`에서 수정 필요

### 데이터베이스 연결 오류
- `.env` 파일의 데이터베이스 설정 확인
- MySQL 서버가 실행 중인지 확인
- 데이터베이스 사용자 권한 확인
