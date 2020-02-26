from flask import Flask
app = Flask(__name__)

@app.route('/')
def getSecondServerResponse():
    return '<h1>This response is coming from second server</h1>'


@app.route('/home')
def getSecondServersecondHome():
    return '<h1>Welcome to the server 2"s home</h1>'