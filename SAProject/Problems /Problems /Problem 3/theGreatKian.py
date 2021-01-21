n=int(raw_input())
L=map(int,raw_input().split())
sum1=0
sum2=0
sum3=0
for j in range(len(L)):
    if j%3==0:
        sum1+=L[j]
    if j%3==1:
        sum2+=L[j]
    if j%3==2:
        sum3+=L[j]
 
print sum1,sum2,sum3   