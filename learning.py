import mysql.connector

# 예제 테이블 생성 및 데이터 삽입 (첫 실행 시에만 필요)
def setup_example_db():
    # users 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(20),
        reservations VARCHAR(255)
    )
    ''')
    
    # 예제 데이터 삽입
    cursor.execute('''
    INSERT INTO users (user_id, name, email, phone, reservations) 
    VALUES 
        (1, 'Alice', 'alice@example.com', '123-456-7890', '2024-11-15, Room 101'),
        (2, 'Bob', 'bob@example.com', '987-654-3210', '2024-11-16, Room 102'),
        (3, 'Charlie', 'charlie@example.com', '555-666-7777', NULL)
    ''')
    
    conn.commit()

# 사용자 정보 조회 함수
def get_user_info(user_id):
    # MySQL 데이터베이스 연결 설정
    print(6)
    conn = mysql.connector.connect(
        host="localhost",         # MySQL 서버 호스트
        user="testuser2",      # MySQL 사용자 이름
        password="1234",  # MySQL 비밀번호
        database="usertest"      # 사용할 데이터베이스 이름
    )
    print(7)
    cursor = conn.cursor()
    # 특정 user_id의 사용자 정보를 조회
    print(8)
    cursor.execute(f"SELECT name, email, phone, reservations FROM users WHERE user_id = {user_id}")
    print(9)
    result = cursor.fetchone()
    print(result)
    if result:
        name, email, phone, reservations = result
        print(result)
        info = f"이름: {name}\n이메일: {email}\n전화번호: {phone}\n예약 정보: {reservations or '예약이 없습니다.'}"
    else:
        info = "해당 사용자를 찾을 수 없습니다."
    conn.close()
    return info

# def chatbot_response(user_input, user_id):
#     if "내 정보" in user_input:
#         # 사용자 요청을 분석하고 정보 조회가 필요할 때
#         response = "정보를 조회 중입니다. 잠시만 기다려 주세요."
#         user_info = get_user_info(user_id)
        
#         # 조회된 사용자 정보로 최종 응답 생성
#         final_response = f"{response}\n\n사용자 정보:\n{user_info}"
#     else:
#         # OpenAI API를 통해 일반적인 답변 생성
#         response = ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": user_input}]
#         )
#         final_response = response['choices'][0]['message']['content']
#     conn.close()
#     return final_response

# 데이터베이스 셋업 (필요할 경우에만 실행)
# setup_example_db()

# Nouh에서 user_id 가져오는 코드
# print(current_user.id)