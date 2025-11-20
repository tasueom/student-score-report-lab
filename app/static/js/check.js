function validateForm() {
    const kor = document.getElementById('kor').value;
    const eng = document.getElementById('eng').value;
    const math = document.getElementById('math').value;
    
    // 학번 검증
    if (id === '') {
        alert('학번을 입력해주세요.');
        return false;
    }
    
    // 점수가 정수인지 확인
    const korNum = Number(kor);
    const engNum = Number(eng);
    const mathNum = Number(math);
    
    if (isNaN(korNum) || isNaN(engNum) || isNaN(mathNum)) {
        alert('모든 필드를 유효한 숫자로 입력해주세요.');
        return false;
    }
    
    // 정수인지 확인 (소수점 거부)
    if (!Number.isInteger(korNum) || !Number.isInteger(engNum) || !Number.isInteger(mathNum)) {
        alert('점수는 정수만 입력 가능합니다.');
        return false;
    }
    
    // 범위 검증
    if (korNum < 0 || korNum > 100 || engNum < 0 || engNum > 100 || mathNum < 0 || mathNum > 100) {
        alert('국어, 영어, 수학 점수는 0에서 100 사이의 정수여야 합니다.');
        return false;
    }

    // 비밀번호 확인
    if (pwd !== pwd_confirm) {
        alert('비밀번호가 일치하지 않습니다.');
        return false;
    }
    
    return true;
}

function validateSignupForm() {
    const id = document.getElementById('id').value;
    const pwd = document.getElementById('pwd').value;
    const pwd_confirm = document.getElementById('pwd_confirm').value;
    const ban = document.getElementById('ban').value;
    const name = document.getElementById('name').value;
    
    // 학번 검증
    if (id === '') {
        alert('학번을 입력해주세요.');
        return false;
    }
    
    // 비밀번호 검증
    if (pwd === '') {
        alert('비밀번호를 입력해주세요.');
        return false;
    }
    
    // 비밀번호 확인
    if (pwd !== pwd_confirm) {
        alert('비밀번호가 일치하지 않습니다.');
        return false;
    }
    
    // 반 선택 검증
    if (ban === '') {
        alert('반을 선택해주세요.');
        return false;
    }
    
    // 이름 검증
    if (name === '') {
        alert('이름을 입력해주세요.');
        return false;
    }
    
    return true;
}

function validateSigninForm() {
    const id = document.getElementById('id').value;
    const pwd = document.getElementById('pwd').value;
    
    // 학번 검증
    if (id === '') {
        alert('학번을 입력해주세요.');
        return false;
    }
    
    // 비밀번호 검증
    if (pwd === '') {
        alert('비밀번호를 입력해주세요.');
        return false;
    }
    
    return true;
}