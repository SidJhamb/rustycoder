use strict;
 
$a=<>;
$b=<>;
my @c=(split / /,$b);
my $out=2;
my $j=0;
our @sum;
my $count=scalar(@c); 
if($count < 3){$count =3;};
 
for (my $z=0;$z<=$out;$z++){
	$sum[$z]=0;
	}
 
for (my $i=0;$i<$count;$i=($i+3)){
	$sum[$j] += $c[$i];
	if(($i + 3) > ($count - 1) ){
		$j++;
		$i=$j - 3;
		if($j > $out){
			print "@sum\n";
			exit;
			}
		}
	}