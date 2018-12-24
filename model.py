from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

#  retrieve recent directory
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  new version should be setted as True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  sqlite file path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data_register.sqlite')

db = SQLAlchemy(app)
class Questionnaire(db.Model):
    """record the questionnaire result"""
    __tablename__ = 'UserRegisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    Qname = db.Column(db.String(80), unique=False, nullable=False)
    Qdescrib = db.Column(db.String(80), unique=False, nullable=False)
    question1 = db.Column(db.String(10),nullable=False)
    question2 = db.Column(db.String(10),nullable=False)
    question3 = db.Column(db.String(10),nullable=False)
    question4 = db.Column(db.String(10),nullable=False)
    question5 = db.Column(db.String(10),nullable=False)
    question6 = db.Column(db.String(10),nullable=False)
    question7 = db.Column(db.String(10),nullable=False)
    question8 = db.Column(db.String(10),nullable=False)
    question9 = db.Column(db.String(10),nullable=False)
    question10 = db.Column(db.String(10),nullable=False)
    question11 = db.Column(db.String(10),nullable=False)
    question12 = db.Column(db.String(10),nullable=False)

    def __repr__(self):
        ret = "username:{}, ".format(self.username)
        ret += "Qname:{}, ".format(self.Qname)
        ret += "Qdescrib:{}, ".format(self.Qdescrib)
        ret += '{}:{}, '.format('question1',self.question1)
        ret += '{}:{}, '.format('question2',self.question2)
        ret += '{}:{}, '.format('question3',self.question3)
        ret += '{}:{}, '.format('question4',self.question4)
        ret += '{}:{}, '.format('question5',self.question5)
        ret += '{}:{}, '.format('question6',self.question6)
        ret += '{}:{}, '.format('question7',self.question7)
        ret += '{}:{}, '.format('question8',self.question8)
        ret += '{}:{}, '.format('question9',self.question9)
        ret += '{}:{}, '.format('question10',self.question10)
        ret += '{}:{}, '.format('question11',self.question11)
        ret += '{}:{}'.format('question12',self.question12)
        return ret
