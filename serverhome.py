from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')

#Make an app.route() decorator here
@app.route("/Test", methods = ['GET'])
def puppiesFunction():
  if request.method == 'GET':
  	#Call the method to Get all of the puppies
  	return "Hello World"
  

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
