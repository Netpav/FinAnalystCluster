#!/usr/bin/perl

for (glob '~/*.arff') {
	print $_, $/;	
	print "\n *********** \n";
	$filename = $_;
	$out1 = ''.$filename. '_J48';
	$out2 = ''.$filename. '_HT';
	$out3 = ''.$filename. '_NaiveBayes';
	$out4 = ''.$filename. '_NaiveBayesMultinomial ';
	print $filename;
	print "\n ///////////////////////////// \n";
	
	
	print $out1;	
	system "java -Xmx8G -XX:-UseGCOverheadLimit -cp ~/weka.jar weka.classifiers.trees.J48 -k -t $filename -split-percentage 66 > $out1 ";	
	print $out2;
	system "java -Xmx8G -XX:-UseGCOverheadLimit -cp ~/weka.jar weka.classifiers.trees.HoeffdingTree -L 2 -S 1 -E 1.0E-7 -H 0.05 -M 0.01 -G 200 -N 0.0 -k -t $filename -split-percentage 66 > $out2 ";	
	print $out3;
	system "java -Xmx8G -XX:-UseGCOverheadLimit -cp ~/weka.jar weka.classifiers.bayes.NaiveBayes -k -t $filename -split-percentage 66 > $out3 ";
	print $out4;
	system "java -Xmx8G -XX:-UseGCOverheadLimit -cp ~/weka.jar weka.classifiers.bayes.NaiveBayesMultinomial  -k -t $filename -split-percentage 66 > $out4 ";
	


}