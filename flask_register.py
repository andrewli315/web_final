from flask import Flask, render_template,g,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import sqlite3
import json
from form import FormRegister
from modell import UserReister
import os

#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
app.config['SECRET_KEY']='abcd0392'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data_register.sqlite')
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db
@app.route('/DELETE/api/user/<id>', methods=['GET', 'POST'])
def delete(id):
    #from modell import UserReister
    from modell import db

    users=UserReister.query.filter_by(id=id).first()
    db.session.delete(users)
    db.session.commit()
    return 'Success Thank You'
@app.route('/GET/api/user', methods=['GET', 'POST'])
def user():
    class UserEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, UserReister):
                return obj.id,obj.username,obj.email,obj.password
            return json.JSONEncoder.default(self, obj)

    from modell import UserReister
    #db = get_db()
    #cursor = db.cursor()
    #cursor.execute("SELECT * FROM UserRegisters")
    users=UserReister.query.all()
    #ret = cursor.fetchall()

    print (users)
    print (type(json.dumps(users,cls=UserEncoder)))
    #print (json.dumps(users))
    #return jsonify(users)
    #return jsonify({'username':'wang123123'})
    #j2={'user':UserReister('username':'wang123123')}
    return json.dumps(users,cls=UserEncoder)
    #return 'thing'

@app.route('/register', methods=['GET', 'POST'])
def register():
    from form import FormRegister
    from modell import UserReister
    form =FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            #username = '1111111111111111111',
            #email = '1111@11111111111111',
            #password = '111111111111111111'
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
