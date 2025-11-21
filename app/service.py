import pytesseract
import os
from PIL import Image
import re
from io import BytesIO
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 사용 안 함
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# Tesseract 실행 파일 경로 설정 (환경변수에서 읽어오거나 기본값 사용)
tesseract_cmd = os.environ.get('TESSERACT_CMD', r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if tesseract_cmd and os.path.exists(tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# 한국어 또는 다른 나라 언어팩이 들어있는 위치 지정, tessdata 경로 명시
tessdata_prefix = os.environ.get('TESSDATA_PREFIX', r"C:\Program Files\Tesseract-OCR\tessdata")
if tessdata_prefix and os.path.exists(tessdata_prefix):
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

def calculate(kor, eng, math):
    total = kor + eng + math
    average = total / 3
    grade = 'A' if average >= 90 else 'B' if average >= 80 else 'C' if average >= 70 else 'D' if average >= 60 else 'F'
    return total, average, grade

def format_chart_data(subject_averages):
    """과목별 평균 튜플을 Chart.js 바 차트용 데이터 형식으로 변환합니다.
    
    Args:
        subject_averages: (국어평균, 영어평균, 수학평균) 튜플
    
    Returns:
        dict: Chart.js 바 차트 설정 딕셔너리
    """
    avg_kor, avg_eng, avg_math = subject_averages
    
    return {
        'labels': ['국어', '영어', '수학'],
        'datasets': [{
            'label': '과목별 평균 점수',
            'data': [avg_kor, avg_eng, avg_math],
            'backgroundColor': ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(75, 192, 192, 0.6)'],
            'borderColor': ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)', 'rgba(75, 192, 192, 1)'],
            'borderWidth': 1
        }]
    }

def extract_info(file):
    img = Image.open(file)
    
    custom_config = r'-c tessedit_char_blacklist=*=~--"\' --oem 3 --psm 6'
    text_raw = pytesseract.image_to_string(img, lang='kor', config=custom_config)
    
    # 인식된 텍스트를 콘솔에 출력
    print("=== 인식된 텍스트 (원본) ===")
    print(text_raw)
    print("===================")
    
    # 텍스트에서 모든 띄어쓰기 제거 (공백, 탭 등)
    text_no_spaces = re.sub(r'[ \t]+', '', text_raw)
    
    # 줄바꿈은 유지하여 줄 단위로 처리
    lines = text_no_spaces.strip().split('\n')
    
    print("=== 띄어쓰기 제거 후 텍스트 ===")
    print(text_no_spaces)
    print("===================")
    
    # 학번: "학번"로 시작하는 줄에서 학번 이후 내용 추출
    id = ""
    for line in lines:
        if line.strip().startswith('학번'):
            # "학번" 또는 "학번:" 이후의 내용 추출
            id = re.sub(r'^학번:?', '', line.strip())
            break
    
    # 국어: "국어"로 시작하는 줄에서 국어 이후 내용 추출
    kor = ""
    for line in lines:
        if line.strip().startswith('국어'):
            # "국어" 또는 "국어:" 이후의 내용 추출
            kor = re.sub(r'^국어:?', '', line.strip())
            break
    
    # 영어: "영어"로 시작하는 줄에서 영어 이후 내용 추출
    eng = ""
    for line in lines:
        if line.strip().startswith('영어'):
            # "영어" 또는 "영어:" 이후의 내용 추출
            eng = re.sub(r'^영어:?', '', line.strip())
            break
    
    # 수학: "수학"로 시작하는 줄에서 수학 이후 내용 추출
    math = ""
    for line in lines:
        if line.strip().startswith('수학'):
            # "수학" 또는 "수학:" 이후의 내용 추출
            math = re.sub(r'^수학:?', '', line.strip())
            break
    
    # 이미지를 BytesIO로 변환하여 반환
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    return id, kor, eng, math, img_base64

def export_excel(scores):
    """성적 데이터를 엑셀 파일로 내보내는 함수"""
    
    df = pd.DataFrame(scores, columns=['학번', '반', '이름', '국어', '영어', '수학', '총점', '평균', '등급'])
    
    # Excel 파일을 BytesIO에 저장
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    
    return excel_buffer

def create_chart_png(subject_averages):
    """과목별 평균 점수 차트를 PNG 이미지로 생성하는 함수
    
    Args:
        subject_averages: (국어평균, 영어평균, 수학평균) 튜플
    
    Returns:
        BytesIO: PNG 이미지가 저장된 BytesIO 객체
    """
    avg_kor, avg_eng, avg_math = subject_averages
    
    # 한글 폰트 설정 (Windows 기본 폰트 사용)
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
    
    # 차트 크기 설정
    plt.figure(figsize=(8, 4))
    
    # 데이터 준비
    subjects = ['국어', '영어', '수학']
    averages = [avg_kor, avg_eng, avg_math]
    
    # 막대 그래프 생성
    plt.bar(subjects, averages, color=['#3498db', '#e74c3c', '#16a085'])
    plt.title("과목별 평균 점수", fontsize=14, fontweight='bold')
    plt.xlabel("과목", fontsize=12)
    plt.ylabel("평균 점수", fontsize=12)
    plt.ylim(0, 100)  # Y축 범위 설정
    plt.grid(axis="y", alpha=0.3)  # Y축 방향으로만 grid 표시
    
    # 이미지를 BytesIO에 저장
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
    plt.close()
    img_buffer.seek(0)
    
    return img_buffer

def export_pdf(scores, subject_averages):
    """성적 데이터와 차트를 포함한 PDF 파일을 생성하는 함수
    
    Args:
        scores: 성적 데이터 리스트 [(학번, 반, 이름, 국어, 영어, 수학, 총점, 평균, 등급), ...]
        subject_averages: (국어평균, 영어평균, 수학평균) 튜플
    
    Returns:
        BytesIO: PDF 파일이 저장된 BytesIO 객체
    """
    # PDF 파일을 BytesIO에 저장
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    
    # 한글 폰트 설정
    # reportlab은 기본적으로 한글을 지원하지 않으므로 TTF 폰트를 등록해야 함
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    font_name = 'Helvetica'  # 기본값
    # Windows에서 맑은 고딕 폰트 경로 시도
    possible_font_paths = [
        r"C:\Windows\Fonts\malgun.ttf",  # 맑은 고딕
        r"C:\Windows\Fonts\gulim.ttc",   # 굴림
        r"C:\Windows\Fonts\batang.ttc",  # 바탕
    ]
    
    for font_path in possible_font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Korean', font_path))
                font_name = 'Korean'
                break
            except:
                continue
    
    # 1페이지 - 차트 삽입
    c.setFont(font_name, 16)
    c.drawString(50, height - 50, "과목별 평균 점수 차트")
    
    # 차트 이미지 생성 및 삽입
    chart_buffer = create_chart_png(subject_averages)
    # BytesIO를 임시 파일로 저장하여 reportlab에 전달
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        chart_buffer.seek(0)
        tmp_file.write(chart_buffer.read())
        tmp_file_path = tmp_file.name
    
    try:
        c.drawImage(tmp_file_path, 50, height - 350, width=500, height=250)
    finally:
        # 임시 파일 삭제
        try:
            os.unlink(tmp_file_path)
        except:
            pass
    c.showPage()  # 다음 페이지로 이동
    
    # 2페이지 - 성적표 출력
    x = 40  # 표의 시작 X 위치
    y = height - 50  # 표의 시작 Y 위치
    
    # 표 제목
    c.setFont(font_name, 16)
    c.drawString(x, y, "성적표")
    y -= 40  # 줄 내림
    
    # 표 헤더 출력
    headers = ["학번", "반", "이름", "국어", "영어", "수학", "총점", "평균", "등급"]
    c.setFont(font_name, 10)
    col_widths = [60, 40, 60, 50, 50, 50, 50, 50, 40]  # 각 열의 너비
    x_positions = [x]
    for i in range(len(col_widths) - 1):
        x_positions.append(x_positions[-1] + col_widths[i])
    
    for i, h in enumerate(headers):
        c.drawString(x_positions[i], y, str(h))
    y -= 20  # 헤더 아래로 한 줄 내림
    
    # 표 데이터 출력
    c.setFont(font_name, 8)
    for row in scores:
        # 페이지 아래에 공간이 부족하면 페이지 넘김
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont(font_name, 8)
        
        # 한 행 출력
        for i, value in enumerate(row):
            # 숫자는 소수점 둘째 자리까지 표시 (평균)
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)
            c.drawString(x_positions[i], y, value_str)
        y -= 15  # 다음 줄로 이동
    
    # PDF 저장
    c.save()
    pdf_buffer.seek(0)
    
    return pdf_buffer