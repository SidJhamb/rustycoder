import random
import time
import json
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
#from celery import Celery
from celery import Celery
from celery.task.control import inspect
import base64
from time import sleep
#import tasks
#from tasks import  run_code_python, run_code_add
from subprocess import *
import re
from flask_cors import CORS, cross_origin
from datetime import timedelta, datetime
from flask import make_response, request, current_app
from functools import update_wrapper
import requests
import os
import runner
from runner import *
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
CORS(app)

# Celery configuration
app.config['DEBUG'] = True
app.config['CELERY_BROKER_URL'] = 'amqp://127.0.0.1'
app.config['CELERY_RESULT_BACKEND'] = 'rpc'
app.config['CELERY_TRACK_STARTED'] = True
app.config['CELERYD_TASK_TIME_LIMIT'] = 300
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False # valid token, but expired
    except BadSignature:
        return None
    return data

@app.route('/my_service')
@crossdomain(origin='*')
def my_service():
    return jsonify(foo='cross domain')

@app.route('/run', methods=['POST'])
@cross_origin()
def run():
    token = request.headers.get('token','')
    authenticated = verify_auth_token(token)

    # print authenticated

    if authenticated == False or authenticated == None:
        return jsonify(authenticated=False), 401

    source_code = base64.b64decode(request.json["code"])
    language = request.json["lang"]
    testInput = base64.b64decode(request.json["stdin"])

    task = run_task.apply_async(args=[source_code, testInput, language])

    if task.state != 'FAILURE':
        # return jsonify({}), 200, {'taskId': task.id, 'message' : 'Job Submitted'}
        return jsonify(taskId=task.id, jobStatus=True), 200

    else:
        # return jsonify({}), 500, {'taskId': task.id, 'message' : 'Job Failed. Please retry.'}
        return jsonify(taskId=task.id, jobStatus=False), 200

@celery.task(bind=True)
def run_task(self, source_code, input1, language):
    directory = os.getcwd()
    directory = directory + "/Code_Files/"

    taskId = self.request.id.__str__()

    if language == 'Python':
        actualOutput,actualError = run_code_python(input1, source_code, directory + 'Python/',taskId)

    elif language == "Cpp":
        actualOutput,actualError = run_code_cpp(input1,source_code, directory + 'Cpp/',taskId)

    elif language == "Ruby":
        actualOutput,actualError = run_code_ruby(input1,source_code, directory + 'Ruby/',taskId)

    elif language == "C":
        actualOutput,actualError = run_code_c(input1,source_code, directory + 'C/',taskId)

    elif language == "Perl":
        actualOutput,actualError = run_code_perl(input1,source_code, directory + 'Perl/',taskId)

    else:
        actualOutput,actualError = run_code_java(input1,source_code, directory + 'Java/',taskId)   
   
    output = {}

    print 'Actual Error'
    # print actualError
    if actualError is None or actualError == "" or actualError == "success":        
        self.update_state(meta = {'message' : "Test Case passed", 'output' : str(actualOutput)})
        return {'message':'Test Case passed', 'output' : base64.b64encode(actualOutput) }
    else:
        self.update_state(meta = {'message' : "Failed", 'output' : base64.b64encode(actualError)})
        return {'message':'Failed', 'output' : base64.b64encode(actualError) }

@app.route('/submit', methods=['POST'])
@cross_origin()
def submit():
    token = request.headers.get('token','')
    authenticated = verify_auth_token(token)

    # print authenticated

    if authenticated == False or authenticated == None:
        return jsonify(authenticated=False), 401

    source_code = base64.b64decode(request.json["code"])
    language = request.json["lang"]
    problemId = request.json["problemId"]
    pairs = request.json["testcases"].values()
    testcaseInputs = []
    expectedOutputs = []
    for pair in pairs:
        testcaseInput = base64.b64decode(pair[0])
        print testcaseInput
        testcaseInputs.append(testcaseInput)
        expectedOutput = base64.b64decode(pair[1])
        print expectedOutput
        expectedOutputs.append(expectedOutput)
    
    task = submit_task.apply_async(args=[source_code, testcaseInputs, expectedOutputs, problemId, language])

    if task.state != 'FAILURE':
        # return jsonify({}), 200, {'taskId': task.id, 'jobStatus' : True}
        return jsonify(taskId=task.id, jobStatus=True), 200
    else:
        # return jsonify({}), 200, {'taskId': task.id, 'jobStatus' : False}
        return jsonify(taskId=task.id, jobStatus=False), 200

@celery.task(bind=True)
def submit_task(self, source_code, testcaseInputs, expectedOutputs, problemId, language): 

    self.update_state(state='PROGRESS', meta = {'message' : "Compiling...",
                                                'result' : '',
                                                'problemId': str(problemId),
                                                't_status': '',
                                                'ratio': ''})

    result = []
    failures = 0
    taskId = self.request.id.__str__()
    testCaseCount = len(testcaseInputs)
    print 'Testcase count ' + str(len(testcaseInputs))

    directory = os.getcwd()

    directory = directory + "/Code_Files/"

    for index in range(len(testcaseInputs)):
        if language == 'Python':
            actualOutput,actualError = run_code_python(testcaseInputs[index],source_code, directory + 'Python/', taskId)

        elif language == "Cpp":
            actualOutput,actualError = run_code_cpp(testcaseInputs[index],source_code, directory + 'Cpp/', taskId)

        elif language == "Ruby":
            actualOutput,actualError = run_code_ruby(testcaseInputs[index],source_code, directory + 'Ruby/', taskId)

        elif language == "C":
            actualOutput,actualError = run_code_c(testcaseInputs[index],source_code, directory + 'C/', taskId)

        elif language == "Perl":
            actualOutput,actualError = run_code_perl(testcaseInputs[index],source_code, directory + 'Perl/', taskId)

        else:
            actualOutput,actualError = run_code_java(testcaseInputs[index],source_code, directory + 'Java/', taskId)


        actualOutput = re.sub('[\s+]', '', str(actualOutput))
        expectedOutputs[index] = re.sub('[\s+]', '', str(expectedOutputs[index]))
        status = 'Pass'

        print 'Actual Output 2'
        print actualOutput
        print 'Expected Output 2'
        print expectedOutputs[index]
        print 'Actual Error 2'
        print actualError
        print 'Actual Error Length 2'
        print len(str(actualError))



        if actualError == None or actualError == '' or actualError == "success":
            if(actualOutput == expectedOutputs[index]):
                print 'I am success'
                result.append("Passed") 
            else:
                print 'I am failure'
                result.append("Failed")
                status = 'Fail'
                failures = failures + 1
        else:
            result.append("Failed")
            status = 'Fail'
            failures = failures + 1

    print 'Failures ' + str(failures)

    self.update_state(meta = {'message' : "Completed",
                              'result' : result,
                              'problemId' : str(problemId),
                              't_status' : str(status), 
                              'ratio' : str(testCaseCount - failures) + '/' + str(testCaseCount),
                              'actualError' : str(actualError) })
    return {'message' : "Completed",
            'result' : result,
            'problemId' : str(problemId),
            't_status' : str(status), 
            'ratio' : str(testCaseCount - failures) + '/' + str(testCaseCount),
            'actualError' : str(actualError) }


# Return status of a single Task Id : Custom Input case
@app.route('/runStatus/<task_id>', methods=['GET'])
@cross_origin()
def runStatus(task_id):
    token = request.headers.get('token','')
    authenticated = verify_auth_token(token)

    # print authenticated

    if authenticated == False or authenticated == None:
        return jsonify(authenticated=False), 401

    task = run_task.AsyncResult(task_id)
    print str(task.info)
    dict={}
    return jsonify(status=task.state, message=str(task.info.get('message','')),
            output=str(base64.b64decode(task.info.get('output',''))))

# #Return status of multiple Task Ids : System Test Cases case
@app.route('/submitStatus/<task_id>', methods=['GET'])
@cross_origin()
def submitStatus(task_id):
    print request
    token = request.headers.get('token','')
    authenticated = verify_auth_token(token)

    #print authenticated

    if authenticated == False or authenticated == None:
        return jsonify(authenticated=False), 401

   

    task = submit_task.AsyncResult(task_id)    
    print 'Task info printing here: '+str(task.info)

    request_data = {}
    request_data['jobId'] = task.id
    request_data['status'] = task.state
    request_data['message'] = str(task.info.get('message',''))
    request_data['username'] = authenticated['name']
    # request_data['username'] = 'abc'
    request_data['timestamp'] = str(datetime.now().isoformat())
    request_data['userId'] = authenticated['id']
    # request_data['userId'] = '1'
    request_data['testCaseStatus'] = str((task.info.get('ratio','')))
    request_data['problemId'] = str((task.info.get('problemId','')))
    request_data['result'] = task.info.get('result','')
    # request_data['actualError'] = task.info.get('actualError','')
    # if(str((task.info.get('t_status',''))) == 'False'):
    #     request_data['overallStatus'] = 'Fail'
    # else:
    #     request_data['overallStatus'] = 'Pass'
    request_data['overallStatus'] = str((task.info.get('t_status','')))


    requestList = []
    requestList.append(request_data)

    print 'Task info printing here data: '+ str(requestList)
    
    if(task.state == 'SUCCESS'):
        headers = {"Accept": "application/json"}
        response = requests.post("http://10.42.0.1:8050/saveStatus", json = requestList, headers= headers)


    return jsonify(request_data)

def find_Error(returncode):
    if(abs(returncode)==1):
        return "SIGHUP:Hangup detected on controlling terminal or death of controlling process"
    elif(abs(returncode)==2):
        return "SIGINT: Interrupt from keyboard"
    elif(abs(returncode)==3):
        return "SIGQUIT:Quit from keyboard"
    elif(abs(returncode)==4):
        return "SIGILL:Illegal Instruction"
    elif(abs(returncode)==6):
        return "SIGABRT:Abort signal"
    elif(abs(returncode)==8):
        return "SIGFPE: Floating-point exception"
    elif(abs(returncode)==9):
        return "SIGKILL:Kill signal"
    elif(abs(returncode)==11):
        return "SIGSEGV:Invalid memory reference"
    elif(abs(returncode)==13):
        return "SIGPIPE:Broken pipe: write to pipe with no readers"
    elif(abs(returncode)==14):
        return "SIGALRM:Timer signal from alarm"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

    # {
    #     "username": "Pranjal Priyadarshi",
    #     "timestamp": "Now",
    #     "userId": "1",
    #     "testCaseStatus": "3/3",
    #     "problemId": "5acddc89839cd82cc17269f6",
    #     "_id": {
    #         "$oid": "5ace1cfc839cd82cc17269f7"
    #     },
    #     "overallStatus": "Pass"
    # },



