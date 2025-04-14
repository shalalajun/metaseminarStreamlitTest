from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
from datetime import datetime
from llm import get_ai_response
import langchain_core  # 명시적으로 추가

app = Flask(__name__,
            static_folder='dist',  # 정적 파일 폴더를 dist로 설정
            static_url_path='/dist')  # URL 경로를 /dist로 설정
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('14-chat-list.html')

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    timestamp = datetime.now().strftime('%H:%M')
    
    # LLM 스트리밍 응답
    response_text = ""
    for chunk in get_ai_response(message):
        response_text += chunk
        # 각 청크마다 클라이언트에게 전송
        emit('stream_message', {
            'chunk': chunk,
            'timestamp': timestamp
        })
    
    # 전체 응답 완료 시그널
    emit('stream_complete', {
        'message': response_text,
        'timestamp': timestamp
    })

if __name__ == '__main__':
    socketio.run(app, debug=True) 