from flask import Flask,jsonify
from flask_pymongo import PyMongo 
from flask import render_template, json, request
from bson.json_util import dumps,ObjectId
import json

app=Flask(__name__)
with app.app_context():
	app.config['MONGO_DBNAME']='mydb'
	app.config['MONGO_URI']='mongodb://127.0.0.1:27017/'
	mongo =PyMongo(app)
	problemset = mongo.db.problems
	userhistory = mongo.db.userhistory



@app.route('/fetchProblems',methods=['GET','POST'])
def fetch_problems():
	
	allproblems=[]
	if request.method=='GET':
		allproblems=problemset.find();
		allproblems= dumps(allproblems)

	
	return allproblems
	#problemset.insert()
	#return "Problems Added ! "

@app.route('/addProblem',methods=['POST'])
def add_problems():
	
	list=request.get_json()
	for data in list:
		problemset.insert(data)
	#print list

	return 'done'


@app.route('/problemsSearchedByUsers',methods=['POST'])
def find_problems():
	query={}
	problemId=request.data
	problemId_dict=json.loads(problemId)
	value=problemId_dict['_id']['$oid']
	value=ObjectId(value)
	query={"_id":value}
	#print query
	returned_problem=problemset.find(query)
	returned_problem=dumps(returned_problem)
	#print returned_problem
	return returned_problem
	#return "Hello"


@app.route('/queryUserStatus',methods=['POST'])
def queryUserStatus():
	query={}
	problemId=request.data
	#print problemId
	problemId_dict=json.loads(problemId)
	value=problemId_dict['problemId']
	print value
	# value=ObjectId(value
	query={"problemId":value}
	print query

	returned_problem=userhistory.find(query)
	returned_problem=dumps(returned_problem)
	#print returned_problem
	return returned_problem
	#return "Hello"

@app.route('/fetchUserStatus',methods=['GET','POST'])
def fetchUserStatus():
	
	userstatus=[]
	if request.method=='GET':
		userstatus=userhistory.find();
		userstatus= dumps(userstatus)

	
	return userstatus
	#problemset.insert()
	#return "Problems Added ! "




@app.route('/saveStatus',methods=['POST'])
def saveStatus():
	list=request.get_json()
	#print list
	for data in list:
		#print "Printing data"+data[jobId]
		print data["jobId"]
	query={}
	query={"jobId":data["jobId"]}
	retval=userhistory.find(query)
	retval=dumps(retval)
	print "Printing retval",len(retval)
	if len(retval)<>2:
	 	pass
	else:
		userhistory.insert(list)
	
	return "Data Inserted"

@app.route('/deleteallProblems',methods=['GET'])
def deleteallProblems():
	
	returnval=problemset.drop()
	return "Problems Deleted"

@app.route('/deleteUserHistory',methods=['GET'])
def deleteUserHistory():
	
	userhistory.drop()
	return "User History Deleted"

if __name__=='__main__':
		app.run(debug='TRUE')

