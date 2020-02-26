from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/in-maheshsn/project/learnings/learnServer/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
