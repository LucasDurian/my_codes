#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : app.py
@Time    : 2019/12/17 11:18
@Author  : Yin Zheng
@Email_private   : yinzheng1993@126.com
@Email_company   : yinzheng@mskj.com
@Software: PyCharm
"""
from flask import Flask, request, redirect, url_for, render_template,flash, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db  =SQLAlchemy(app)

class Elient(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    message = db.Column(db.String(300))
    date_time = db.Column(db.DateTime, default=datetime.now)
    # def __repr__(self):
    #     print(self.name,self.email,self.subject,self.message)
    #     return self.name
    def jsonstr(self):
        jsondata = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'date_time':self.date_time
        }
        return jsondata

@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id

        return curr_user


@app.route('/')
@login_required
def index():
    return 'Logged in as: %s' % current_user.get_id()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User()
            curr_user.id = user_id

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            return redirect(url_for('index'))

        flash('Wrong username or password!')

    # GET 请求
    return render_template('login.html')


@app.route('/user')
@login_required
def user():
    return render_template('user_info.html')

@app.route('/user_info')
@login_required
def user_info():


    student = Elient.query.all()

    data = []
    for item in student:
        print(item.jsonstr())
        data.append(item.jsonstr())
    data ={"code": 0, "msg": "", "count": len(student),"data":data}

    return jsonify(data)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'


if __name__ == '__main__':

    app.run(debug=True)
