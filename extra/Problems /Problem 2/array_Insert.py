'''
# Sample code to perform I/O:
 
name = raw_input()          # Reading input from STDIN
print 'Hi, %s.' % name      # Writing output to STDOUT
 
# Warning: Printing unwanted or ill-formatted data to output will cause the test cases to fail
'''
 
# Write your code here
num_queries = int(raw_input().split(' ')[1])
my_array = map(int, raw_input().split(' '))
for i in range(num_queries):
    query = map(int, raw_input().split(' '))
    if query[0] == 1:
        index = query[1]
        new_num = query[2]
        my_array[index] = new_num
    if query[0] == 2:
        sum = 0
        for j in range(query[1], query[2]+1):
            sum += my_array[j]
        print sum