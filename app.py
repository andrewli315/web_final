import sys
from io import BytesIO
from flask import Flask,request,render_template,jsonify,redirect, url_for, session
import json
import requests
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from model import Questionnaire
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'development'
bootstrap = Bootstrap(app)
CORS(app)
oauth = OAuth(app)
github = oauth.remote_app(
    'github',
    consumer_key='0cdeffb69f3d3eff1983',
    consumer_secret='7cb62738faa5796546221c3bae2f0b4d34777be6',
    request_token_params={'scope':'user:email'},
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


recent_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+\
                                    os.path.join(recent_dir,'data_register.sqlite')
app.config['SECRET_KEY'] = 'abcd0392'

db = SQLAlchemy(app)

def process_data(datas):
    ret = '['
    for i in datas:
        tmp = {
                "id" : i.id,
            "username" : i.username,
            "Qname" : i.Qname,
            "Qdescrib" : i.Qdescrib,
            "question1" : i.question1,
            "question2" : i.question2,
            "question3" : i.question3,
            "question4" : i.question4,
            "question5" : i.question5,
            "question6" : i.question6,
            "question7" : i.question7,
            "question8" : i.question8,
            "question9" : i.question9,
            "question10" : i.question10,
            "question11" : i.question11,
            "question12" : i.question12,
        }
        ret += json.dumps(tmp)
        ret += ','
    ret = ret[:-1]
    ret += ']'
    return ret


@app.route('/')
def index():
    if 'github_token' in session:
        me = github.get('user')
        return jsonify(me.data)
#    return 
    return render_template('index.html')
@app.route('/login')
def login():
    return github.authorize(callback='http://andrewli315.nctu.me/authorized')

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
#    print(me.data)
    
    print(me.data['name'])
    return redirect('http://web.andrewli315.nctu.me/tabs/(home:home)?token={}'.format(me.data['name']))
#return redirect('https://web.andrewli315.nctu.me/tabs/(home:home/1)')



@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@app.route('/statistic',methods=['GET'])
def statistic():
    from model import Questionnaire
    datas = Questionnaire.query.all()    
    ret = process_data(datas)
    json_obj = jsonify(ret)
    print(json_obj.data[0])

    return ret

@app.route('/questions', methods=['GET'])
def query(): 
    from model import Questionnaire
    datas = Questionnaire.query.all()
    ret = process_data(datas)
    return ret
@app.route('/analyze/<string:user>',methods=['GET'])
def analyze(user):
    print(user)
    from model import Questionnaire
    datas = Questionnaire.query.all()
    ret = process_data(datas)
    json_data = json.loads(ret)
    for i in json_data:
        if user == i['username']:
            userdata = i
    print(userdata)
    r = requests.post(url='http://192.168.2.132:5000/calculate',data=json.dumps(userdata))
    print(r.status_code)
    print(r.text)
    return r.text

@app.route('/finish',methods=['GET','POST'])
def finish_form():
    req = request.get_json(force=True)
    print(req['Qname'])
    from model import Questionnaire
    
    
    data = Questionnaire(           
        username = req['username'],
        Qname = req['Qname'],
        Qdescrib = req['Qdescrib'],
        question1 = req['question1'],
        question2 = req['question2'],
        question3 = req['question3'],
        question4 = req['question4'],
        question5 = req['question5'],
        question6 = req['question6'],
        question7 = req['question7'],
        question8 = req['question8'],
        question9 = req['question9'],
        question10 = req['question10'],
        question11 = req['question11'],
        question12 = req['question12']
    )
    print(data)
    try:
        db.session.add(data)
        db.session.commit()
    except:
        return 'failed'
    
    return 'sucess' 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=False)


