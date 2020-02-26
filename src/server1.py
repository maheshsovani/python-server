from flask import Flask
from requests import get
app = Flask(__name__)

@app.route('/')
def helloWorld():
    res = get('http://localhost:5000/home').content
    return res

@app.route('/home')
def homePage():
    return '<h1>Welcome to the server 1"s home</h1>'