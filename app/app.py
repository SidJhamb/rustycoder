from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from flask import Response
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import requests
import datetime
import json

AUTH_API="http://localhost:8000"
DATASTORE_API="http://172.17.9.25:8050"
BROKER_URL="http://172.17.9.106:5000/"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False # valid token, but expired
    except BadSignature:
        return None
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
@app.route('/login/<string:mode>')
def login(mode=None):
    if mode == 'clear':
        return render_template('login.html',mode=mode)
    else:
        return render_template('login.html',mode=5)

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False:
        return redirect(url_for('login',mode='clear'))
    else:
        return render_template('defaultdashboard.html')

@app.route('/dashboard/<string:pid>')
def spl_dashboard(pid):
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False:
        return redirect(url_for('login',mode='clear'))
    else:
        errorMsg=''
        data={}
        data['_id']={'$oid':pid}
        r=requests.post(DATASTORE_API+'/problemsSearchedByUsers',json=data)
        if r.status_code==200:
            resp=r.json()[0]
            problem={}
            problem['name']=resp['name']
            problem['content']=resp['desc']
        else:
            errorMsg='Error loading problem from db'
        return render_template('dashboard.html',problem=problem, errorMsg=errorMsg,probDesc=json.dumps(r.json()[0]),brokerURL=BROKER_URL)

@app.route('/problems')
def problems():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False:
        return redirect(url_for('login',mode='clear'))
    else:
        problems=[]
        errorMsg=''
        r=requests.get(DATASTORE_API+'/fetchProblems')
        if r.status_code == 200:
            for x in r.json():
                problems.append({'name':x['name'],'id':x['_id']['$oid']})
        else:
            errorMsg='Error loading the problems from server'
        return render_template('problems.html', problems=problems,errorMsg=errorMsg)

@app.route('/admin')
def admin():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False or token_status['is_admin'] != 'True':
        return redirect(url_for('login',mode='clear'))
    else:
        return render_template('admin.html')

@app.route('/adminproblems')
def adminproblems():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False or token_status['is_admin'] != 'True':
        return redirect(url_for('login',mode='clear'))
    else:
        problems=[]
        errorMsg=''
        r=requests.get(DATASTORE_API+'/fetchProblems')
        if r.status_code == 200:
            for x in r.json():
                problems.append({'name':x['name'],'id':x['_id']['$oid']})
        else:
            errorMsg='Error loading the problems from server'
        return render_template('adminproblems.html', problems=problems,errorMsg=errorMsg)


@app.route('/api/login',methods=['POST'])
def api_login():
    # print request.json
    # print type(request.json)
    r = requests.post(AUTH_API+'/api/login', json=request.json)
    resp=jsonify(r.json())
    if r.json()['status']:
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=7)
        resp.set_cookie(key='token',value=r.json()['token'],expires=expire_date)
    return resp,200

@app.route('/api/register',methods=['POST'])
def api_register():
    r = requests.post(AUTH_API+'/api/register', json=request.json)
    resp=jsonify(r.json())
    return resp,200

@app.route('/api/addProblem',methods=['POST'])
def api_addProblem():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False or token_status['is_admin'] != 'True':
        return redirect(url_for('login',mode='clear'))
    else:
        # print request.json[0]
        r=requests.post(DATASTORE_API+'/addProblem', json=request.json)
        # print r.text
        return jsonify(r.text), 200

@app.route('/api/queryUserStatus',methods=['POST'])
def api_queryUserStatus():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    else:
        token_status = verify_auth_token(token)
    
    if token_status is None or token_status is False:
        return redirect(url_for('login',mode='clear'))
    else:
        print request.json
        r = requests.post(DATASTORE_API+'/queryUserStatus', json=request.json)
        return jsonify(r.json()), 200




