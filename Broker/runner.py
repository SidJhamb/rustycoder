from subprocess import *
import base64
import os

def run_code_python(input, source_code, directory, taskId):
	# Write the incoming source code to file source_code.py
    filename = taskId + "_source_code.py"
    fpobject = open(str(directory) + filename, "w")
    fpobject.write(source_code)
    fpobject.close()

    p = Popen(["python",str(directory) + filename], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    actualOutput,actualError=p.communicate(input)

    return actualOutput,actualError

def run_code_c(input, source_code, directory, taskId):
	# Write the incoming source code to file code_reader.cpp
    print 'Directory'
    print directory
    filename = taskId + "_trail.c" 
    filename2 = taskId + "trail"            
    fpobject = open(str(directory) + "/" + filename, "w")
    fpobject.write(source_code)
    fpobject.close()

    p=Popen(["gcc",str(directory) + filename,"-o",str(directory) + filename2],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    actualOutput, actualError = p.communicate() 

    try:
        q=Popen([str(directory) + "./" + filename2],stdout=PIPE,stdin=PIPE,stderr=PIPE)
        
        print "Exception"
        print q.returncode 
        actualOutput,actualError=q.communicate(input) 
        print 'Actual Output'
        print actualOutput
        print 'Actual Error'
        print actualError   
        message=find_Error(q.returncode)
        if(message=="success"):
            pass
        else:
        	print 'Fail'
            # fobject.write(str(message))
    except Exception:
        message="Compilation failed"
        print message
        return actualOutput,actualError

    return actualOutput,actualError

def run_code_ruby(input,source_code, directory, taskId):
	# Write the incoming source code to file add.rb
    filename = taskId + "_add.rb"
    fpobject = open(str(directory) + filename, "w")
    fpobject.write(source_code)
    fpobject.close()

    print 'File'
    print str(directory) + "add.rb"

    p=Popen(["ruby",str(directory) + filename],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    actualOutput,actualError=p.communicate(input)

    return actualOutput,actualError

def run_code_java(input,source_code, directory, taskId):
	# Write the incoming source code to file add.rb
    filename = taskId + "_Addition.java"
    filename2 = taskId + "_Addition"
    # fpobject = open(str(directory) + filename, "w")
    fpobject = open(filename, "w")
    fpobject.write(source_code)
    fpobject.close()
    flag=False
    print 'Directory'
    print directory
    # p=Popen(["javac",str(directory) + "Addition.java"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    p=Popen(["javac",filename],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    actualOutput,actualError = p.communicate() 

    path = os.getcwd()

    for File in os.listdir(path):
        if File.endswith(".class"):
            print "Found a .class file"
            flag=True
        else:
            pass

    # print flag==True

    if flag==True:
        # try:
        q=Popen(["java","main"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
        actualOutput,actualError=q.communicate(input)  
        print "Error"+actualOutput,actualError
        # except Exception:
        #     message="Compilation failed"
        #     print message
    else:
        pass

    for File in os.listdir(path):
        if File.endswith(".class"):
            print "Found a .class file"
            print File
            os.remove(path+'/'+File)
            flag=False
        else:
            pass

    return actualOutput,actualError

def run_code_perl(input,source_code, directory, taskId):
	# Write the incoming source code to file add.rb
    filename = taskId + "AddNum.pl"
    fpobject = open(str(directory) + filename, "w")
    fpobject.write(source_code)
    fpobject.close()

    print input
    p=Popen(["perl","-e",str(directory) + filename],stdout=PIPE,stdin=PIPE,stderr=PIPE)

    p.communicate() 
    try:
        os.chmod(str(directory) + filename, 0775)
    except Exception:
        print "Exception Occured in python command"

    print 'Current Directory' + str(directory) + './AddNum.pl'
    q=Popen(["perl",str(directory) + filename],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    print "Exception"
    print q.returncode 
    actualOutput,actualError=q.communicate(input)    
    message=find_Error(q.returncode)
    print message

    return actualOutput,actualError
	
def run_code_cpp(input,source_code, directory, taskId):
	# Write the incoming source code to file code_reader.cpp
    filename = taskId + "code_reader.cpp"
    filename2 = taskId + "code_reader" 
    fpobject = open(str(directory) + filename, "w")
    fpobject.write(source_code)
    fpobject.close()

    p=Popen(["g++",str(directory) + filename, "-o",str(directory) + filename2],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    actualOutput,compilationError=p.communicate() 

    if(compilationError != ""):
        actualError=compilationError
        # print 'Index ' + str(index)
        # print 'In if'
        # print 'Actual Output'
        # print actualOutput
        # print 'Actual Error'
        # print actualError  
    else:
        q=Popen([str(directory) + "./" + filename2],stdout=PIPE,stdin=PIPE,stderr=PIPE)
        actualOutput,actualError=q.communicate(input) 
        # print 'Index ' + str(index)
        # print 'In else'
        # print 'Actual Output'
        # print actualOutput
        # print 'Actual Error'
        # print actualError   
        message=find_Error(q.returncode)   
        actualError=message  
        # print 'here'
        # print actualOutput
        # print actualError

    return actualOutput,actualError
	

def find_Error(returncode):
	if(abs(returncode)==1):
		return "SIGHUP:Hangup detected on controlling terminal or death of controlling process(core-dumped)"
	elif(abs(returncode)==2):
		return "SIGINT: Interrupt from keyboard(core-dumped)"
	elif(abs(returncode)==3):
		return "SIGQUIT:Quit from keyboard(core-dumped)"
	elif(abs(returncode)==4):
		return "SIGILL:Illegal Instruction(core-dumped)"
	elif(abs(returncode)==6):
		return "SIGABRT:Abort signal(core-dumped)"
	elif(abs(returncode)==8):
		return "SIGFPE: Floating-point exception(core-dumped)"
	elif(abs(returncode)==9):
		return "SIGKILL:Kill signal(core-dumped)"
	elif(abs(returncode)==11):
		return "SIGSEGV:Invalid memory reference(core-dumped)"
	elif(abs(returncode)==13):
		return "SIGPIPE:Broken pipe: write to pipe with no readers(core-dumped)"
	elif(abs(returncode)==14):
		return "SIGALRM:Timer signal from alarm(core-dumped)"
	else:
		return "success"



def create_file(code,language):
	extension=find_extention(language)
	file_name="code_reader"+"."+extension
	file=open(file_name,"w")
	file.write(base64.b64decode(code))


def find_extention(language):
	if(language=="python"):
		return "py"
	elif(language=="C"):
		return "c"
	elif(language=="C++"):
		return "cpp"


if __name__=="__main__":
	# code=""
	# language="gcc"
	# create_file(code,language)
	run_code_java()

#run_code_cpp()

