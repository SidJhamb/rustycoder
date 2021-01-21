from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['TOKEN_EXPIRY'] = 604800 # 7 days
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
migrate=Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.String(5), default='False')

    def verify_password(self,password_hash):
        if self.password_hash == password_hash:
            return True
        else:
            return False

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = app.config['TOKEN_EXPIRY'])
        return s.dumps({ 'id': self.id, 'name':self.name, 'is_admin':self.is_admin})


@app.route('/api/register',methods=['POST'])
def register_user():
    name = request.json.get('name')
    email= request.json.get('email')
    password_hash= request.json.get('password')
    is_admin=request.json.get('is_admin')
    if is_admin is None or is_admin == '':
        is_admin='False'

    if email is None or name is None or password_hash is None:
        return jsonify({ 'status':'false', 'message':'Missing Parameters', 'token':'' }), 200
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({ 'status':'false', 'message':'User already registered', 'token':'' }), 200

    user=User(email=email,name=name,password_hash=password_hash,is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'status':'true', 'message':'User registered', 'token':'' }), 200

@app.route('/api/login',methods=['POST'])
def login():
    email=request.json.get('email')
    password_hash=request.json.get('password')

    if email is None or password_hash is None:
        return jsonify({ 'status':'false', 'message':'Missing Parameters', 'token':'' }), 200

    user=User.query.filter_by(email=email).first()

    if not user:
        return jsonify({ 'status':'false', 'message':'User does not exist', 'token':'' }), 200
    
    if not user.verify_password(password_hash):
        return jsonify({ 'status':'false', 'message':'Password Invalid', 'token':'' }), 200

    token=user.generate_auth_token()

    if user.is_admin == 'True':
        return jsonify({ 'status':'true', 'message':'Login Successful','is_admin':'True','token':token.decode('ascii')}), 200
    else:
        return jsonify({ 'status':'true', 'message':'Login Successful', 'token':token.decode('ascii')}), 200

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8000)

