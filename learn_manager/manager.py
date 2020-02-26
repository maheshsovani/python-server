from flask_script import Command
import os

from flask import Flask, jsonify
from flask_script import Manager


class Hello(Command):
    "prints hello world"

    def run(self):
        print("hello world")



app = Flask(__name__)
manager = Manager(app)
manager.add_command('hello', Hello())

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to TECH_TENALIRAM_API'

def create_app():
    return app

if __name__ == "__main__":
    manager.run()
