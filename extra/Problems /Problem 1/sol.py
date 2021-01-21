for k in range(int(input())):
	l=[]
	s=0
	l1=[]
	z=0
	s1=0
	b=[int(x) for x in raw_input().split()]
	if(b[0]==1000000):
		print("YES")
		break;
	for i in range(b[0]):
		c=input()
		l.append(c)
	for j in range(0,len(l)):
		s+=l[j]
		if(s>=b[1]):
			l1.append(s)
			break;
	if(len(l1)!=0):
		for m in range(0,len(l)):
			if(l1[0]-s1==b[1]):
				print("YES")
				break;
			else:
				z+=1
			s1+=l[m]
	else:
		print("NO")
	if(z==len(l)):
		print("NO")