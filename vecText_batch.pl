#!/usr/bin/perl
my $i;


for(my $i = 1;glob '~/*.txt';$i++) {
   print "$i";
# 	print $_, $/;
print $i
	/(.*)\.txt/;

system qq!perl ~/VecText/vectext-cmdline.pl --input=$_ --output_dir=. --output_file=$i --local_weights="Term Frequency (TF)" --output_format="cluto (sparse)" --encoding=utf8 --processed_classes="pokles,rust" --class_position=2 --remove_URIs!;	
}