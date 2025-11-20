from flask import Flask, session
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

def create_app():
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    
    @app.context_processor
    def inject_user():
        return dict(id=session.get('id'), name=session.get('name'))
    
    from app import routes
    
    return app