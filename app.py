import os
import goslate
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify ,render_template ,send_file ,redirect ,url_for ,flash
from werkzeug.utils import secure_filename
from ocr import process_image
import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
from pypdf_to_image import convert
from flask_sqlalchemy import SQLAlchemy
import re


_VERSION = 1
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,template_folder = 'template')
gs = goslate.Goslate()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite4'
app.config['SECRET_KEY'] = "user_database"

db = SQLAlchemy(app)



class user(db.Model):
    username = db.Column('username', db.String(30))
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))




def __init__(self,username,name,email,password,book_id,title,author,category):
    self.username = username
    self.email = email
    self.name = name
    self.password = password




@app.route('/')
def inde():
    return render_template('inde.html')

@app.route('/register',methods = ['POST'])
def register():
    E_REG_EX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    P_REG_EX = re.compile(r'[a-z0-9]{4,}')
    if request.method == 'POST':
        if not request.form['username']:
            flash('Please enter the username', 'error')
        elif not P_REG_EX.match(request.form['password']):
            flash('Password does not match our criteria', 'error')
        elif not E_REG_EX.match(request.form['email']):
            flash('Email does not match our criteria', 'error')
        else:
            u = user(username=request.form['username'],email=request.form['email'],name=request.form['name'],password=request.form['password'])
            db.session.add(u)
            db.session.commit()
            print("success")
            return redirect('/info')
    return render_template('inde.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if(db.query.filter_by(request.form['username'] != NULL)):
            if db.query.filter_by(request.form['username'].password) == request.form['password']:
                session['log']='True'
                redirect(url_for('home'))
            else:
                flash('Password does not match','error')
        else:
            flash('Username does not match','error')
    redirect(url_for(up))
@app.route('/info')
def info():
    return render_template("info.html")
@app.route('/up')
def up():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['author']:
            b = user(book_id = 1 , title = request.form['title'] , author = request.form['author'] , category = request.form['category'])
            db.session.add(b)
            db.session.commit()
            return redirect('/up')
        else:
            flash("You cant leave any field blank",'error')
    else:
        return redirect('/register')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['image_url']
        fname = secure_filename(f.filename)
        f.save(os.path.join(DIR_PATH+'/upload/',fname))
        fname1 = os.path.join(DIR_PATH+'/upload/',fname)
        if 'jpg' or 'png' in fname1:
          output = process_image(fname1)
          trans = output.split(' ')
          t=gs.translate(output,'kn')
          write_file(fname1,output)
          write_file("Kn"+fname1,t)
          return output
        elif 'pdf' in fname1:
          output = process_image(convert(fname1))
          out = output.split(' ')
          trans = gs.translate(list(out),'kn')
          return trans.join('')
        else:
          return jsonify({"error": "only .jpg files, please"})

@app.route('/upload/<image_path>')
def image(image_path):
    return send_file(os.path.join('/directory_path/upload/',image_path),mimetype='image/jpg')


@app.route('/ocr', methods=["POST"])
def ocr():
    url = request.form['image_url']
    print(url)
    if 'jpg' in url:
        output = process_image(url)
        print(jsonify({"output": output}))
    elif 'pdf' in url:
        output = process_image(convert(url))
        print(jsonify({"output": output}))
    else:
        return jsonify({"error": "only .jpg files, please"})

def write_file(name,string):
    file_obj = open(name+'.txt','w')
    file_obj.write(string)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=5000)
