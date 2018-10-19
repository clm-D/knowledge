
from flask import Flask
from flask_login import LoginManager
from sqlalchemy.testing.pickleable import User

app = Flask(__name__)

login_manager = LoginManager(app=app)

@login_manager.user_loader
def load_user():
    return User.get(id)

if __name__ == '__main__':
    app.run()