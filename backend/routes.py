
from flask import current_app as app, jsonify, request
from flask_security import auth_required,verify_password

datastore = app.security.datastore

@app.get('/')
def home():
    return '<h1> home </h1>'

@app.get('/proctered')
@auth_required()
def proctered():
    return '<h1> screen </h1>'

@app.get('/login',methods = ['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message" : "invalid inputs"}),400
    
    user = datastore.find_user(email=email) 

    if not user:
        return jsonify({"message" : "invalid email"}),400
    
    if verify_password(password,user.password):
        return jsonify({"token" : user.get_auth_token(),"email":user.email,"role":user.role,"id":user.id})
    return jsonify({"message" : "wrong password"}),400
