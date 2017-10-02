import os
from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_from_directory
from werkzeug import secure_filename
from utilities import validateUser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import File, Base

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'UploadFiles')

engine = create_engine('sqlite:///files.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
db_session = DBsession()

app = Flask(__name__)
#Read Secret key from text file
app.secret_key = 'randomString'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def login():
  return render_template('login.html', isError = False)


@app.route("/index", methods = ['POST','GET'])
def displayHome():
  if request.method == 'POST':
    userName = request.form['userName']
    pw = request.form['pw']
    if validateUser(userName,pw):
      session['username'] = userName
      return render_template('index.html',name = userName, files = db_session.query(File).all())
    else:
      session.pop('username', None)
      return render_template('login.html', isError = True)
  else:
    if 'username' in session:
      userName = session['username']
      return render_template('index.html',name = userName, files = db_session.query(File).all())
    else:
      return render_template('login.html', isError = False)
    
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    filename = secure_filename(f.filename)
    fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(fullpath)
    newFile = File(name = filename, path = fullpath)
    db_session.add(newFile)
    db_session.commit()
    return redirect('/index')
    
@app.route('/files', methods = ['GET'])
def files_endpoint():
  if 'username' in session:      
    return getAllFilesJson()
  else:
    return render_template('login.html', isError = False)


@app.route('/downloadFile/<id>')
def downloadFile(id):
  file = db_session.query(File).get(id)
  return send_from_directory(app.config['UPLOAD_FOLDER'],file.name, as_attachment=True)

@app.route('/deleteFile/<id>')
def deleteFile(id):
  file = db_session.query(File).get(id)  
  relPath = os.path.join(app.config['UPLOAD_FOLDER'],file.name)
  if os.path.isfile(relPath):
   os.remove(relPath)
   db_session.delete(file)
   db_session.commit()
   return redirect('/index')
  else:
   return "Error"
  

  
def getAllFilesJson():
  files = db_session.query(File).all()
  return jsonify(Files=[i.serialize for i in files])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
