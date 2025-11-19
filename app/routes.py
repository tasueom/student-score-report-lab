from flask import render_template, request, redirect, url_for, flash
from app import app, service, db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        name = request.form['name']
        kor = int(request.form['kor'])
        eng = int(request.form['eng'])
        math = int(request.form['math'])
        total, average, grade = service.calculate(kor, eng, math)
        if db.insert_score(name, kor, eng, math, total, average, grade):
            flash('성적이 성공적으로 저장되었습니다.')
        else:
            flash('성적 저장에 실패했습니다.')
        return redirect(url_for('index'))
    return render_template('input.html')