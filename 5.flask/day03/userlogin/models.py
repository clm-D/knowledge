
from flask_sqlalchemy import SQLAlchemy

#获取对象
db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=False, nullable=False)
    s_age = db.Column(db.Integer, default=18)

    __tablename__ = 'students'

    def save(self):
        db.session.add(self)
        db.session.commit()
