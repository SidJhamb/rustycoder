import os
import random
import time
import json
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery
import base64
import Worker
from Worker import  long_task


app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'pyamqp://guest@localhost//'

@app.route('/task', methods=['POST'])
def longtask():
    task = long_task.apply_async(base64.encode(request.json["code"]))

    # return jsonify({}), 202, {'Location': url_for('taskstatus',
    #                                               task_id=task.id)}
    print request.json["url"]
    return 0

# @app.route('/status/<task_id>')
# def taskstatus(task_id):
#     task = long_task.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         response = {
#             'state': task.state,
#             'current': 0,
#             'total': 1,
#             'status': 'Pending...'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'current': task.info.get('current', 0),
#             'total': task.info.get('total', 1),
#             'status': task.info.get('status', '')
#         }
#         if 'result' in task.info:
#             response['result'] = task.info['result']
#     else:
#         # something went wrong in the background job
#         response = {
#             'state': task.state,
#             'current': 1,
#             'total': 1,
#             'status': str(task.info),  # this is the exception raised
#         }
#     return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)