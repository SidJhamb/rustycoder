
    # if(language == 'Python'):
    #     # Write the incoming source code to file source_code.py
    #     fpobject = open("source_code.py", "w")
    #     fpobject.write(source_code)
    #     fpobject.close()

    #     p = Popen(["python","source_code.py"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    #     self.update_state(state='PROGRESS', meta = {'message' : "Compiling...", 'output' : ''})
    #     actualOutput,actualError=p.communicate(input1)
    
    # else:
    #     # Write the incoming source code to file source_code.py
    #     fpobject = open("code_reader.cpp", "w")
    #     fpobject.write(source_code)
    #     fpobject.close()

    #     p=Popen(["g++","code_reader.cpp","-o","code_reader"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    #     actualOutput,compilationError=p.communicate() 

    #     if(compilationError != ""):
    #         actualError=compilationError
    #     else:
    #         q=Popen(["./code_reader"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    #         actualOutput,actualError=q.communicate(input1)    
    #         message=find_Error(q.returncode)   
    #         actualError=message 








# @celery.task(bind=True)
# def submit_task(self, source_code, testcaseInputs, expectedOutputs, problemId, language): 

#     self.update_state(state='PROGRESS', meta = {'message' : "Compiling...",
#                                                 'result' : '',
#                                                 'problemId':'5acddc89839cd82cc17269f6',
#                                                 't_status': '',
#                                                 'ratio': ''})

#     result = {}
#     failures = 0
#     testCaseCount = len(testcaseInputs)
#     print 'Testcase count ' + str(len(testcaseInputs))

#     directory = os.getcwd()

#     directory = directory + "/Code_Files/"

#     for index in range(len(testcaseInputs)):
#         if language == 'Python':
#             # Write the incoming source code to file source_code.py
#             # fpobject = open(str(directory) + "source_code.py", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # p = Popen(["python",str(directory) + "source_code.py"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
#             # actualOutput,actualError=p.communicate(testcaseInputs[index])

#             actualOutput,actualError = run_code_python(testcaseInputs[index],source_code, directory)

#         elif language == "Cpp":
#             # Write the incoming source code to file code_reader.cpp
#             # fpobject = open(str(directory) + "code_reader.cpp", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # p=Popen(["g++",str(directory) + "code_reader.cpp", "-o",str(directory) + "code_reader"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             # actualOutput,compilationError=p.communicate() 

#             # if(compilationError != ""):
#             #     actualError=compilationError
#             #     print 'Index ' + str(index)
#             #     print 'In if'
#             #     print 'Actual Output'
#             #     print actualOutput
#             #     print 'Actual Error'
#             #     print actualError  
#             # else:
#             #     q=Popen([str(directory) + "./code_reader"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             #     actualOutput,actualError=q.communicate(testcaseInputs[index]) 
#             #     print 'Index ' + str(index)
#             #     print 'In else'
#             #     print 'Actual Output'
#             #     print actualOutput
#             #     print 'Actual Error'
#             #     print actualError   
#             #     message=find_Error(q.returncode)   
#             #     actualError=message  
#             actualOutput,actualError = run_code_cpp(testcaseInputs[index],source_code, directory)

#         elif language == "Ruby":
#             # Write the incoming source code to file add.rb
#             # fpobject = open(str(directory) + "add.rb", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # print 'File'
#             # print str(directory) + "add.rb"

#             # p=Popen(["ruby",str(directory) + "add.rb"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             # actualOutput,actualError=p.communicate(testcaseInputs[index])
#             actualOutput,actualError = run_code_ruby(testcaseInputs[index],source_code, directory)

#         elif language == "C":
#             # Write the incoming source code to file code_reader.cpp
            
#             # fpobject = open(str(directory) + "/trail.c", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # p=Popen(["gcc","trail.c","-o","trail"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             # p.communicate() 
#             # try:

#             #     q=Popen(["./trail"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
                
#             #     print "Exception"
#             #     print q.returncode 
#             #     actualOutput,actualError=q.communicate(testcaseInputs[index])    
#             #     message=find_Error(q.returncode)
#             #     if(message=="success"):
#             #         pass
#             #     else:
#             #         fobject.write(str(message))

#             # except Exception:
#             #     message="Compilation failed"
#             #     print message

#             actualOutput,actualError = run_code_c(testcaseInputs[index],source_code, directory)

#         elif language == "Perl":
#             # Write the incoming source code to file add.rb
#             # fpobject = open(str(directory) + "AddNum.pl", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # print input
#             # p=Popen(["perl","-e",str(directory) + "AddNum.pl"],stdout=PIPE,stdin=PIPE,stderr=PIPE)

#             # p.communicate() 
#             # try:
#             #     os.chmod(str(directory) + "AddNum.pl", 0775)
#             # except Exception:
#             #     print "Exception Occured in python command"

#             # print 'Current Directory' + str(directory) + './AddNum.pl'
#             # q=Popen(["perl",str(directory) + "AddNum.pl"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             # print "Exception"
#             # print q.returncode 
#             # actualOutput,actualError=q.communicate(testcaseInputs[index])    
#             # message=find_Error(q.returncode)
#             # print message
#             # if(message=="success"):
#             #     pass
#             # else:
#             #     # fobject.write(str(message))

#             # except Exception:
#             #     message="Compilation failed"
#             #     print message

#             actualOutput,actualError = run_code_perl(testcaseInputs[index],source_code, directory)

#         else:
#             # Write the incoming source code to file add.rb
#             # fpobject = open(str(directory) + "Addition.java", "w")
#             # fpobject.write(source_code)
#             # fpobject.close()

#             # p=Popen(["javac",str(directory) + "Addition.java"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             # p.communicate() 

#             # # path = os.getcwd()

#             # for File in os.listdir(directory):
#             #     if File.endswith(".class"):
#             #         print "Found a .class file"
#             #         flag=True
#             #     else:
#             #         pass

#             # # print flag==True

#             # if flag==True:
#             #     try:
#             #         q=Popen(["cd Code_Files;java","Addition"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#             #         actualOutput,actualError=q.communicate(testcaseInputs[index])  
#             #         print "Error"+actualOutput,actualError
#             #     except Exception:
#             #         message="Compilation failed"
#             #         print message
#             # else:
#             #     pass

#             # for File in os.listdir(directory):
#             #     if File.endswith(".class"):
#             #         print "Found a .class file"
#             #         print File
#             #         os.remove(directory+File)
#             #         flag=False
#             #     else:
#             #         pass

#             actualOutput,actualError = run_code_java(testcaseInputs[index],source_code, directory)


#         actualOutput = re.sub('[\s+]', '', str(actualOutput))
#         expectedOutputs[index] = re.sub('[\s+]', '', str(expectedOutputs[index]))
#         status = True

#         print 'Actual Output 2'
#         print actualOutput
#         print 'Expected Output 2'
#         print expectedOutputs[index]
#         print 'Actual Error 2'
#         print actualError
#         print 'Actual Error Length 2'
#         print len(str(actualError))


#         if actualError == None or actualError == '':
#             if(actualOutput == expectedOutputs[index]):
#                 print 'I am success'
#                 result[index] = "Passed" 
#             else:
#                 print 'I am failure'
#                 result[index] = "Failed"
#                 status = False
#                 failures = failures + 1
#         else:
#             result[index] = "Failed"
#             status = False
#             failures = failures + 1

#     print 'Failures ' + str(failures)

#     self.update_state(meta = {'message' : "Completed",
#                               'result' : str(result),
#                               'problemId' : '5acddc89839cd82cc17269f6',
#                               't_status' : str(status), 
#                               'ratio' : str(testCaseCount - failures) + '/' + str(testCaseCount) })
#     return {'message' : "Completed",
#             'result' : str(result),
#             'problemId' : '5acddc89839cd82cc17269f6',
#             't_status' : str(status), 
#             'ratio' : str(testCaseCount - failures) + '/' + str(testCaseCount) }