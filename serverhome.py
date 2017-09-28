from flask import Flask, request, render_template, redirect, url_for, session
from utilities import validateUser
app = Flask(__name__)
app.secret_key = 'randomString'

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
      return render_template('index.html',name = userName)
    else:
      return render_template('login.html', isError = True)
  else:
    if 'username' in session:
      userName = session['username']
      return render_template('index.html',name = userName)
    else:
      return render_template('login.html', isError = False)
    
    
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
