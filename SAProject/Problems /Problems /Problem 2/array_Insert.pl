=comment
# Sample code to perform I/O:
 
my $name = <STDIN>;             # Reading input from STDIN
print "Hi, $name.\n";           # Writing output to STDOUT
 
# Warning: Printing unwanted or ill-formatted data to output will cause the test cases to fail
=cut
 
# Write your code here
use strict;
use warnings;
 
my ($arr_length, $query_num) = split(/\s/, <>);
my @arr = split(/\s/, <>);
my $count = 0;
for(1..$query_num) {
    my ($query_type, $arg1, $arg2) = split(/\s/, <>);
    if ($query_type == 1) {
        $arr[$arg1] = $arg2;
        $count++;
    } elsif ($query_type == 2) {
        my $sum = 0;
        for($arg1..$arg2) {
            $sum += $arr[$_];
        }
        $count++;
        print $sum . "\n";
    }
}