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
- **성적 조회**: 전체 학생 성적을 테이블로 조회
- **성적 수정**: 기존 성적 수정
- **CSV 업로드**: CSV 파일로 일괄 성적 업로드
- **JSON 업로드**: JSON 파일로 일괄 성적 업로드
- **과목별 평균 시각화**: Chart.js를 사용한 바 차트

#### 학생 기능
- **내 성적 조회**: 로그인한 학생 본인의 성적만 조회

#### 데이터 검증
- 프론트엔드: JavaScript를 통한 실시간 입력 검증 (0-100 정수)
- 백엔드: 데이터베이스 제약 조건 및 에러 처리
- 업로드 파일 검증: CSV/JSON 파일 형식 및 데이터 타입 검증

### 🚧 개발 예정

- **엑셀 내보내기**: 성적 데이터를 엑셀 파일로 다운로드
- **PDF 내보내기**: PDF 성적표 자동 생성

## 기술 스택

- **Backend**: Flask 3.0.0
- **Database**: MySQL (mysql-connector-python)
- **Frontend**: HTML, CSS, JavaScript
- **차트 라이브러리**: Chart.js
- **아이콘**: Font Awesome
- **데이터 처리**: pandas (CSV/JSON 파일 처리)
- **환경 변수**: python-dotenv
- **보안**: Werkzeug (비밀번호 해싱)

## 프로젝트 구조

```
student-score-report-lab/
├── app/
│   ├── __init__.py          # Flask 앱 초기화
│   ├── routes.py            # 라우트 정의
│   ├── db.py                # 데이터베이스 연결 및 쿼리
│   ├── service.py           # 비즈니스 로직 (점수 계산, 차트 데이터 포맷팅)
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
│   └── input_sample.json    # JSON 업로드 샘플 파일
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
```

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

### 6. 테스트 데이터 삽입 (선택사항)

```bash
python insert_test_students.py
```

테스트용 학생 10명(001~010)을 삽입합니다.

### 7. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속하세요.

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

### 성적 조회

1. 네비게이션에서 "성적 조회" 클릭
2. 저장된 모든 성적을 테이블로 확인
   - 학번, 반, 이름, 국어, 영어, 수학, 총점, 평균, 등급
3. 각 행의 "수정" 버튼으로 성적 수정 가능
4. 오른쪽에 과목별 평균 점수 바 차트 확인

### 성적 수정

1. "성적 조회" 페이지에서 수정할 학생의 "수정" 버튼 클릭
2. 국어, 영어, 수학 점수 수정
3. 총점, 평균, 등급은 자동 계산되어 표시 (읽기 전용)
4. "수정" 버튼 클릭하여 저장

### 학생 회원가입 및 로그인

1. 네비게이션에서 "회원가입" 클릭
2. 학번, 비밀번호, 비밀번호 확인, 반, 이름 입력
3. "회원가입" 버튼 클릭
4. 로그인 페이지에서 학번과 비밀번호로 로그인

### 내 성적 조회 (학생)

1. 로그인 후 네비게이션에서 "내 성적 조회" 클릭
2. 본인의 성적만 확인 가능
3. 국어, 영어, 수학, 총점, 평균, 등급 표시

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
| `/upload_csv` | POST | CSV 업로드 | 관리자 |
| `/upload_json` | POST | JSON 업로드 | 관리자 |
| `/my_score` | GET | 내 성적 조회 | 학생 |

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
