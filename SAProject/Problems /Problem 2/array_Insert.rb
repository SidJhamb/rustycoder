=begin
# Read input from stdin and provide input before running code
 
print "Please enter your name: "
name = gets.chomp
print "Hi #{name}\n"
=end
 
N, Q = gets.split.map { |n| n.to_i }
A = gets.split.map { |n| n.to_i }
(1..Q).each do
    c, i1, i2 = gets.split.map { |n| n.to_i }
    if (c==1)
        A[i1] = i2
    else
        puts A[i1, i2-i1+1].inject(0, :+)
    end
end