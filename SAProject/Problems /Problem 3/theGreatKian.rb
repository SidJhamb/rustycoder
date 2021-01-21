=begin
# Read input from stdin and provide input before running code
 
print "Please enter your name: "
name = gets.chomp
print "Hi #{name}\n"
=end
 
n = gets.chomp.to_i
 
int = gets.chomp
#puts int
int = int.split(' ')
 
a1=0
a2=1
a3=2
sum1 = 0
sum2 = 0
sum3 = 0
for i in 0..n-1
	if i == a1
		a1 = a1+ 3
		#puts a1
		sum1 += int[i].to_i
		#puts sum1
	elsif i == a2
		a2= a2 + 3
		sum2 +=int[i].to_i
	elsif i==a3
		a3 = a3 + 3
		sum3 += int[i].to_i
	end
end
puts "#{sum1} #{sum2} #{sum3}"