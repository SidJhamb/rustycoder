from subprocess import *
import base64

def run_code_python():
	fobject=open("output.txt","w")
	input=""
	with open("input.txt","r") as file_input:
		for line in file_input:
			input=input+line

	print input
	p=Popen(["python","code_reader.py"],stdout=fobject,stdin=PIPE,stderr=fobject)
	p.communicate(input)

def run_code_cpp():
	fobject=open("output.txt","w")
	input=""
	with open("input.txt","r") as file_input:
		for line in file_input:
			input=input+line

	print input
	p=Popen(["g++","code_reader.cpp","-o","code_reader"],stdout=PIPE,stdin=PIPE,stderr=fobject)
	p.communicate()	
	try:

		q=Popen(["./code_reader"],stdout=fobject,stdin=PIPE,stderr=fobject)
		
		#print "Exception"
		#print q.returncode 
		q.communicate(input)	
		message=find_Error(q.returncode)
		fobject.write(message)
	except Exception:
		message="Compilation failed"
		print message
	

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



def create_file(code,language):
	extension=find_extention(language)
	file_name="code_reader"+"."+extension
	file=open(file_name,"w")
	file.write(base64.b64decode(code))


def find_extention(language):
	if(language=="python"):
		return "py"
	elif(language=="gcc"):
		return "cpp"

# if __name__=="__main__":
# 	code="I051bWJlciBvZiB0ZXN0IGNhc2VzDQpuVGVzdENhc2VzID0gaW5wdXQoKQ0KIA0KI0xvb3AgdGhyb3VnaCBhbGwgdGhlIHRlc3QgY2FzZXMNCmZvciB4IGluIHJhbmdlKDAsIG5UZXN0Q2FzZXMpOg0KIA0KCSNpbnB1dCBmb3IgZWFjaCB0ZXN0IGNhc2UsIG51bU9mTGF5ZXJzKG51bWJlcnMgb2YgbGF5ZXJzLCBpZS4gbnVtYmVyIG9mIG5ldXJvbnMpLCBtaW5YLCBtYXhYDQoJbnVtT2ZMYXllcnMsIG1pblgsIG1heFggPSBtYXAoaW50LCByYXdfaW5wdXQoKS5zcGxpdCgpKQ0KIA0KCSNbaV1bMF0gaXMgV2ksIFtpXVsxXSBpcyBCaQ0KCVdpQmkgPSBbXQ0KIA0KCSN0YWtlIGlucHV0IGZvciBhbGwgdGhlIGxheWVycyhvciBuZXVyb25zIGFzIG5vLl9vZm5ldXJvbnMgPSBuby5fb2ZsYXllcnMpDQoJZm9yIHkgaW4gcmFuZ2UoMCwgbnVtT2ZMYXllcnMpOg0KCQlXaUJpLmFwcGVuZChbMCBmb3IgXyBpbiByYW5nZSgwLDIpXSkNCgkJV2lCaVt5XVswXSwgV2lCaVt5XVsxXSA9IG1hcChpbnQsIHJhd19pbnB1dCgpLnNwbGl0KCkpDQoJDQoJIzIgdmFsdWVzIHRvIHN0b3JlIGZvciBvZGQgb3IgZXZlbg0KCXZhbCA9IFswLDBdDQogDQoJZm9yIHggaW4gcmFuZ2UoMCwyKToNCgkJcmVzID0geA0KCQlmb3IgaSBpbiByYW5nZSgwLCBudW1PZkxheWVycyk6DQoJCQlyZXMgPSAocmVzICogV2lCaVtpXVswXSArIFdpQmlbaV1bMV0pICUgMg0KCQl2YWxbeF0gPSByZXM7DQoJDQoJI2NvdW50IGZvciBldmVuDQoJZXZlbiA9IDANCiANCglpZiB2YWxbbWluWCAlIDJdID09IDA6DQoJCWV2ZW4gKz0gKG1heFggLSBtaW5YKSAvIDIgKyAxOw0KCQ0KCWlmICh2YWxbKG1pblggKyAxKSAlIDJdID09IDApOg0KCQlldmVuICs9IChtYXhYIC0gbWluWCAtIDEpIC8gMiArIDE7DQogDQoJb2RkID0gbWF4WCAtIG1pblggKyAxIC0gZXZlbg0KIA0KCWFucyA9IHN0cihldmVuKSArICcgJyArIHN0cihvZGQpDQogDQoJcHJpbnQoYW5zKSANCg0K"
# 	language="gcc"
# 	create_file(code,language)
# 	run_code()

#run_code_cpp()
run_code_python()

