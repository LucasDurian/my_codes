#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2019/12/13 15:51
@Author  : Yin Zheng
@Email_private   : yinzheng1993@126.com
@Email_company   : yinzheng@mskj.com
@Software: PyCharm
"""
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__,template_folder='../templates/',static_folder='../static/')
# 连接数据库
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db  =SQLAlchemy(app)

# 建Client表
class Client(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    message = db.Column(db.String(300))
    date_time = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return self.name,self.email,self.subject,self.message

db.create_all()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=["POST"])
def register_info():
    if request.method=='POST':
# 获取前端form数据
        client_name=request.form['name']
        client_email = request.form['email']
        client_subject = request.form['subject']
        client_message = request.form['message']
# 插入数据
        new_client_message = Client(name=client_name,email=client_email,subject=client_subject,message=client_message)
        db.session.add(new_client_message)
        db.session.commit()
        return "已经收到您的信息，感谢您的反馈！"
if __name__ == '__main__':
    app.run(debug=True)
