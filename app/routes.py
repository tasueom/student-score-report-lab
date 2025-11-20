from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash as gen_pw, check_password_hash as chk_pw
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
        if student and chk_pw(pwd, student[1]):
            session['id'] = id
            session['name'] = student[2]
            return redirect(url_for('index'))
        else:
            flash('학번 또는 비밀번호가 일치하지 않습니다.')
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        id = request.form['id']  # 폼에서 name 필드를 student_id로 사용
        kor = int(request.form['kor'])
        eng = int(request.form['eng'])
        math = int(request.form['math'])
        total, average, grade = service.calculate(kor, eng, math)
        if db.insert_score(id, kor, eng, math, total, average, grade):
            flash('성적이 성공적으로 저장되었습니다.')
        else:
            flash('성적 저장에 실패했습니다.')
        return redirect(url_for('index'))
    return render_template('input.html')

@app.route('/view')
def view():
    scores = db.get_scores()
    subject_averages = db.get_subject_averages()
    chart_data = service.format_chart_data(subject_averages)
    return render_template('view.html', scores=scores, chart_data=chart_data)

@app.route('/export_excel')
def export_excel():
    flash("준비중입니다.")
    return redirect(url_for('view'))

@app.route('/export_pdf')
def export_pdf():
    flash("준비중입니다.")
    return redirect(url_for('view'))