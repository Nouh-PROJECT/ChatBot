from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
import requests,openai,os
from dotenv.main import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
import mysql.connector

llm = ChatOpenAI(temperature=0.7, openai_api_key="my api key", model_name="gpt-3.5-turbo")
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


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

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    text=data.get('data')
    user_input = text
    user_id = 2
    print(1)
    try:
        if "내 정보" in user_input:
            # 사용자 요청을 분석하고 정보 조회가 필요할 때
            response = "내 정보를 조회합니다."
            user_info = get_user_info(user_id)
            final_response = f"{response}\n\n--사용자 정보--\n{user_info}"
            memory.save_context({"input": user_input}, {"output": final_response})
            return jsonify({"response":True,"message":final_response})
        else:
            # OpenAI API를 통해 일반적인 답변 생성
            print(5)
            conversation = ConversationChain(llm=llm,memory=memory)
            output = conversation.predict(input=user_input)
            memory.save_context({"input": user_input}, {"output": output})
            return jsonify({"response":True,"message":output})

    except Exception as e:
        print(e)
        error_message = f'Error: {str(e)}'
        return jsonify({"message":error_message,"response":False})

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


if __name__ == '__main__':
    app.run()
