import mysql.connector
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

base_config = {
    "host": os.environ.get('DB_HOST', 'localhost'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD'),
}

DB_NAME = os.environ.get('DB_NAME', 'scoredb')

TABLE_NAME = "scores"

def get_conn():
    """커넥션과 커서 반환하는 함수"""
    return mysql.connector.connect(**base_config, database=DB_NAME)

def create_database():
    """데이터베이스를 생성하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**base_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        # 리소스 정리: 예외 발생 여부와 관계없이 항상 실행
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def drop_table():
    """테이블을 삭제하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # 외래키 제약 때문에 scores를 먼저 삭제
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        cursor.execute("DROP TABLE IF EXISTS students")
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Table drop failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_table():
    """테이블을 생성하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        # students 테이블 생성 (먼저 생성해야 외래키 참조 가능)
        cursor.execute("""
            CREATE TABLE students (
                id VARCHAR(50) PRIMARY KEY,
                pwd TEXT,
                ban INT,
                name VARCHAR(50)
            );
        """)
        
        # scores 테이블 생성 (students.id를 참조하는 외래키)
        cursor.execute(f"""
            CREATE TABLE {TABLE_NAME} (
                id VARCHAR(50) PRIMARY KEY,
                kor INT,
                eng INT,
                math INT,
                total INT,
                average DECIMAL(5,2),
                grade CHAR(1),
                FOREIGN KEY (id) REFERENCES students(id)
            );
        """)
        
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        # 리소스 정리: 예외 발생 여부와 관계없이 항상 실행
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def check_id(id):
    """학번이 존재하는지 확인합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM students WHERE id = %s", (id,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"ID check failed: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_student(id, pwd_hash, ban, name):
    """학생을 삽입하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO students (id, pwd, ban, name) VALUES (%s, %s, %s, %s)", (id, pwd_hash, ban, name))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Student insertion failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_student(id):
    """학생을 조회하고 튜플을 반환합니다. (id, pwd, ban, name)"""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, pwd, ban, name FROM students WHERE id = %s", (id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Student retrieval failed: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_no_score_students():
    """성적을 입력하지 않은 학생을 조회하고 리스트를 반환합니다. (admin 제외)"""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students WHERE id != 'admin' AND id NOT IN (SELECT id FROM scores)")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"No score students retrieval failed: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_score(id, kor, eng, math, total, average, grade):
    """성적을 삽입하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"""
                        INSERT INTO {TABLE_NAME} (id, kor, eng, math, total, average, grade)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (id, kor, eng, math, total, average, grade))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Score insertion failed: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        # 리소스 정리: 예외 발생 여부와 관계없이 항상 실행
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_scores():
    """성적을 조회하고 리스트를 반환합니다. (학생 이름 포함)"""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT s.id, st.ban, st.name, s.kor, s.eng, s.math, s.total, s.average, s.grade
            FROM {TABLE_NAME} s
            JOIN students st ON s.id = st.id
            ORDER BY s.id
        """)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Score retrieval failed: {err}")
        return []  # 빈 리스트 반환
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_subject_averages():
    """과목별 평균 점수를 조회하고 튜플로 반환합니다. (국어, 영어, 수학)"""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 
                AVG(kor) as avg_kor,
                AVG(eng) as avg_eng,
                AVG(math) as avg_math
            FROM {TABLE_NAME}
        """)
        result = cursor.fetchone()
        if result and result[0] is not None:
            # 평균을 소수점 둘째 자리까지 반올림
            avg_kor = round(float(result[0]), 2)
            avg_eng = round(float(result[1]), 2)
            avg_math = round(float(result[2]), 2)
            return (avg_kor, avg_eng, avg_math)
        return (0, 0, 0)  # 데이터가 없을 경우
    except mysql.connector.Error as err:
        print(f"Subject average retrieval failed: {err}")
        return (0, 0, 0)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_score(id):
    """학생의 성적을 조회하고 리스트를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT kor, eng, math, total, average, grade FROM {TABLE_NAME} WHERE id = %s", (id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Score retrieval failed: {err}")
        return []