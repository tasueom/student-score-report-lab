from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash as gen_pw, check_password_hash as chk_pw
import pandas as pd
from app import app, service, db
import os

@app.route('/')
def index():
    # README.md 파일 읽기
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    readme_content = ''
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        readme_content = 'README.md 파일을 찾을 수 없습니다.'
    
    return render_template('index.html', readme_content=readme_content)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form['id']
        if db.check_id(id):
            flash('이미 존재하는 학번입니다.')
            return redirect(url_for('signup'))
        pwd = request.form['pwd']
        pwd_hash = gen_pw(pwd)
        ban = request.form['ban']
        name = request.form['name']
        if db.insert_student(id, pwd_hash, ban, name):
            flash('회원가입이 성공적으로 완료되었습니다.')
            return redirect(url_for('signin'))
        else:
            flash('회원가입에 실패했습니다.')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        student = db.get_student(id)
        
        if student and chk_pw(student[1], pwd):
            session['id'] = id
            session['name'] = student[3]  # name은 인덱스 3 (id=0, pwd=1, ban=2, name=3)
            return redirect(url_for('index'))
        else:
            flash('학번 또는 비밀번호가 일치하지 않습니다.')
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))

@app.route('/input', methods=['GET', 'POST'])
def input():
    # admin 체크를 먼저 수행 (GET/POST 모두)
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        id = request.form['id']  # 폼에서 name 필드를 student_id로 사용
        kor = int(request.form['kor'])
        eng = int(request.form['eng'])
        math = int(request.form['math'])
        total, average, grade = service.calculate(kor, eng, math)
        result = db.insert_score(id, kor, eng, math, total, average, grade)
        if result == True:
            flash('성적이 성공적으로 저장되었습니다.')
        elif result == 'duplicate':
            flash('성적 저장에 실패했습니다. 이미 성적이 입력된 학번입니다.')
        elif result == 'foreign_key':
            flash('성적 저장에 실패했습니다. 가입된 학번이 아닙니다.')
        else:
            flash('성적 저장에 실패했습니다.')
        return redirect(url_for('view'))
    
    no_score_students = db.get_no_score_students()
    return render_template('input.html', no_score_students=no_score_students)

@app.route('/view')
def view():
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    scores = db.get_scores()
    subject_averages = db.get_subject_averages()
    chart_data = service.format_chart_data(subject_averages)
    return render_template('view.html', scores=scores, chart_data=chart_data)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        kor = int(request.form['kor'])
        eng = int(request.form['eng'])
        math = int(request.form['math'])
        total, average, grade = service.calculate(kor, eng, math)
        if db.update_score(id, kor, eng, math, total, average, grade):
            flash('성적이 성공적으로 수정되었습니다.')
        else:
            flash('성적 수정에 실패했습니다.')
        return redirect(url_for('view'))
    score = db.get_score(id)
    return render_template('edit.html', score=score, id=id)

@app.route('/delete/<id>')
def delete(id):
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    if db.delete_score(id):
        flash('삭제되었습니다.')
    else:
        flash('삭제에 실패했습니다.')
    return redirect(url_for('view'))

@app.route('/export_excel')
def export_excel():
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    flash("준비중입니다.")
    return redirect(url_for('view'))

@app.route('/export_pdf')
def export_pdf():
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    flash("준비중입니다.")
    return redirect(url_for('view'))

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    file = request.files['file']
    df = pd.read_csv(file, dtype={'id': str})
    success_count = 0
    for _, row in df.iterrows():
        id = str(row['id']).strip()
        print(f"[CSV] 읽은 학번: '{id}' (타입: {type(id)}, 길이: {len(id)})")
        kor = int(row['kor'])
        eng = int(row['eng'])
        math = int(row['math'])
        total, average, grade = service.calculate(kor, eng, math)
        result = db.insert_score(id, kor, eng, math, total, average, grade)
        print(f"[CSV] 학번 '{id}' 삽입 결과: {result}")
        if result == True:
            success_count += 1
        elif result == 'duplicate':
            flash(f'({id}) 성적 저장에 실패했습니다. 이미 성적이 입력된 학번입니다.')
        elif result == 'foreign_key':
            flash(f'({id}) 성적 저장에 실패했습니다. 가입된 학번이 아닙니다.')
        else:
            flash(f'({id}) 성적 저장에 실패했습니다.')
    if success_count > 0:
        flash(f'{success_count}명의 성적이 성공적으로 업로드되었습니다.')
    return redirect(url_for('input'))

@app.route('/upload_json', methods=['POST'])
def upload_json():
    if session.get('id') != 'admin':
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('index'))
    file = request.files['file']
    # JSON을 읽을 때 id를 문자열로 유지하도록 dtype 지정
    df = pd.read_json(file, dtype={'id': str})
    success_count = 0
    for _, row in df.iterrows():
        id = str(row['id']).strip()
        kor = int(row['kor'])
        eng = int(row['eng'])
        math = int(row['math'])
        total, average, grade = service.calculate(kor, eng, math)
        result = db.insert_score(id, kor, eng, math, total, average, grade)
        if result == True:
            success_count += 1
        elif result == 'duplicate':
            flash(f'({id}) 성적 저장에 실패했습니다. 이미 성적이 입력된 학번입니다.')
        elif result == 'foreign_key':
            flash(f'({id}) 성적 저장에 실패했습니다. 가입된 학번이 아닙니다.')
        else:
            flash(f'({id}) 성적 저장에 실패했습니다.')
    if success_count > 0:
        flash(f'{success_count}명의 성적이 성공적으로 업로드되었습니다.')
    return redirect(url_for('input'))

@app.route('/my_score')
def my_score():
    if not session.get('id'):
        flash('로그인이 필요합니다.')
        return redirect(url_for('signin'))
    if session.get('id') == 'admin':
        flash('일반 학생 전용 페이지입니다.')
        return redirect(url_for('index'))
    scores = db.get_score(session.get('id'))
    return render_template('my_score.html', scores=scores)