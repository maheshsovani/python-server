from flask import Flask,jsonify,request,Response
import json
from settings import *
from settings import app
from book_model import *
from user_model import User
import jwt , datetime
from functools import wraps

app.config['SECRET_KEY'] = 'phoenix'


def token_required(f):
  @wraps(f)
  def wrapper(*args,**kwargs):
    token = request.args.get('token')
    try:
      jwt.decode(token, app.config['SECRET_KEY'])
      return f(*args,**kwargs)
    except:
      return jsonify({'error':'authentication required'}), 401
  return wrapper


@app.route('/login',methods=['POST'])
def get_token():
  request_data = request.get_json()
  username = str(request_data['username'])
  password = str(request_data['password'])
  match = User.username_password_match(username,password)
  if match:
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expire_time},app.config['SECRET_KEY'], algorithm='HS256')
    return token
  else:
    return Response('',401,mimetype='application/json')

def validate_book_object(book_object):
    if ("name" in book_object and "isbn" in book_object and "price" in book_object): 
      return True
    else:
      return False

def valid_put_request_data(book_object):
  if ("name" in book_object and "price" in book_object):
      return True
  else:
      return False

@app.route('/')
def hello_world():
  return "welcome to my application"


@app.route('/books')
@token_required
def get_books():
  return jsonify({'books':Book.get_all_books()})

@app.route('/books' ,methods=['POST'])
def add_book():
  request_data = request.get_json()
  if validate_book_object(request_data):
    Book.add_book(request_data['name'],
                  request_data['price'], request_data['isbn'])
    response = Response("Book has been added successfully" , 201,mimetype='application/json')
    response.headers['Location'] = f"/books/{request_data['isbn']}"
    return response
  else:
    invalidBookObjectErrorMsg = {
      "error":"invalid book object is passed in the request",
      "helpString": "Data passed to add the book should be like{name:'name',isbn:11,price:1998}"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg) ,status=400,mimetype='application/json')
    return response

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = Book.get_book(isbn)
  return jsonify(return_value)

@app.route('/books/<int:isbn>' ,methods=['PUT'])
@token_required
def update_book_by_isbn(isbn):
  request_data = request.get_json()

  if (not valid_put_request_data(request_data)):
    invalid_book_object_error = {'error':'The book supplied for the replcement does not contains all the elements to replace',
    'helpString':"Data should be passed in format '{name:bookName , price:bookPrice}'"}
    response = Response(json.dumps(invalid_book_object_error) , status=400,mimetype='application/json')
    return response

  Book.replace_book(isbn, request_data['name'], request_data['price'])
  return Response("",status=204)

@app.route('/books/<int:isbn>' ,methods=['PATCH'])
@token_required
def update_single_book_property_by_isbn(isbn):
  request_data = request.get_json()

  if "name" in request_data:
    Book.update_book_name(isbn,request_data['name'])

  if "price" in request_data:
    Book.update_book_price(isbn,request_data['price'])

  response = Response("",status=204)
  response.headers['Location'] = f'{isbn}'
  return response

@app.route('/books/<int:isbn>' , methods=['DELETE'])
@token_required
def delete_book_in_store(isbn):
  is_successful = Book.delete_book(isbn)

  if is_successful:
      response = Response("",status=204)
      return response

  book_not_found_error = {error: "Requested book for delete not found in collection"}
  response = Response(json.dumps(book_not_found_error),status=404, mimetype='application/json')

  return response


app.run(port=8080)
