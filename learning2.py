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

# 파인튜닝된 모델 사용
llm = ChatOpenAI(temperature=0.7, openai_api_key="api key", model_name="gpt-3.5-turbo")
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_user_info(user_id, info_type):
    # MySQL 데이터베이스 연결 설정
    conn = mysql.connector.connect(
        host="localhost",
        user="testuser2",
        password="1234",
        database="usertest"
    )
    cursor = conn.cursor()

    if info_type == "email":
        cursor.execute(f"SELECT name, email FROM users WHERE user_id = {user_id}")
    elif info_type == "phone":
        cursor.execute(f"SELECT name, phone FROM users WHERE user_id = {user_id}")
    elif info_type == "membership":
        cursor.execute(f"SELECT name, membership_status FROM users WHERE user_id = {user_id}")
    else:
        cursor.execute(f"SELECT name, email, phone FROM users WHERE user_id = {user_id}")

    result = cursor.fetchone()
    conn.close()

    if result:
        # 데이터베이스에서 가져온 데이터를 딕셔너리로 반환
        columns = cursor.column_names
        return dict(zip(columns, result))
    else:
        return None

@app.route('/data', methods=['POST'])
def get_data():
    data = request.get_json()
    text = data.get('data')
    user_input = text
    user_id = 2  # 예시용 user_id

    try:
        if "내 이메일" in user_input:
            info_type = "email"
        elif "내 전화번호" in user_input:
            info_type = "phone"
        elif "내 멤버십" in user_input:
            info_type = "membership"
        elif "내 정보" in user_input:
            info_type = "all"
        else:
            info_type = None

        if info_type:
            # 사용자 요청에 따라 정보를 딕셔너리로 가져오기
            user_info = get_user_info(user_id, info_type)

            # 가져온 정보를 모델에 전달하여 형식화된 응답 생성
            if user_info:
                prompt = (f"사용자가 요청한 정보는 다음과 같습니다:\n\n{user_info}\n\n"
                          "이를 바탕으로 사용자에게 자연스러운 답변을 생성해 주세요.")
                conversation = ConversationChain(llm=llm, memory=memory)
                final_response = conversation.predict(input=prompt)

                memory.save_context({"input": user_input}, {"output": final_response})
                return jsonify({"response": True, "message": final_response})
            else:
                return jsonify({"response": True, "message": "해당 정보를 찾을 수 없습니다."})

        else:
            # 일반적인 요청 처리
            conversation = ConversationChain(llm=llm, memory=memory)
            output = conversation.predict(input=user_input)
            memory.save_context({"input": user_input}, {"output": output})
            return jsonify({"response": True, "message": output})

    except Exception as e:
        error_message = f'Error: {str(e)}'
        return jsonify({"message": error_message, "response": False})


if __name__ == '__main__':
    app.run()
