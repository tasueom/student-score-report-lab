import mysql.connector

base_config = {
    "host": "localhost",   # MySQL 서버 주소 (로컬)
    "user": "root",        # MySQL 계정
    "password": "1234"     # MySQL 비밀번호
}

DB_NAME = "scoredb"

table_name = "scores"

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

def create_table():
    """테이블을 생성하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"""
                        CREATE TABLE scores (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(50),
                            kor INT,
                            eng INT,
                            math INT,
                            total INT,
                            average DECIMAL(5,2),
                            grade CHAR(1)
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

def insert_score(name, kor, eng, math, total, average, grade):
    """성적을 삽입하고 성공 여부를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"""
                        INSERT INTO scores (name, kor, eng, math, total, average, grade)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (name, kor, eng, math, total, average, grade))
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
    """성적을 조회하고 리스트를 반환합니다."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Score retrieval failed: {err}")
        return []  # 빈 리스트 반환
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()