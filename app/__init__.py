from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key1234'

def create_app():
    from app import routes
    
    return app