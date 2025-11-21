import pytesseract
import os
from PIL import Image
import re
from io import BytesIO
import base64

# Tesseract 실행 파일 경로, 아래 구문은 항상 나와야함
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 한국어 또는 다른 나라 언어팩이 들어있는 위치 지정, tessdata 경로 명시
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"

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