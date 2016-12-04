#!/usr/bin/perl

for (glob './~/*.arff') {
	
	print "\n *********** \n";
	$filename = $_;
	$out1 = ''.$filename. '_J48_EvaluateInterleavedTestThenTrain';
	$out2 = ''.$filename. '_J48_learnModel';
	$out3 = ''.$filename. '_HT_EvaluateInterleavedTestThenTrain';
	$out4 = ''.$filename. '_HT_learnModel';	
	$out5 = ''.$filename. '_HTopt_EvaluateInterleavedTestThenTrain';
	$out6 = ''.$filename. '_HTopt_learnModel';
	$out7 = ''.$filename. '_HTadapt_EvaluateInterleavedTestThenTrain';
	$out8 = ''.$filename. '_HTadapt_learnModel';
	
	print "\n ///////////////////////////// \n";
	print $filename;
	print "\n ///////////////////////////// \n";
	
	
system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask EvaluateInterleavedTestThenTrain -l (moa.classifiers.meta.WEKAClassifier -l (weka.classifiers.trees.J48 -C 0.25 -M 2)) -s (ArffFileStream -f $filename ) > $out1 ";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask LearnModel -l (moa.classifiers.meta.WEKAClassifier -l (weka.classifiers.trees.J48 -C 0.25 -M 2)) -s (ArffFileStream -f $filename ) > $out2";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask EvaluateInterleavedTestThenTrain -l (moa.classifiers.trees.HoeffdingTree ) -s (ArffFileStream -f $filename)  > $out3";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask LearnModel -l (moa.classifiers.trees.HoeffdingTree ) -s (ArffFileStream -f $filename ) > $out4";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask EvaluateInterleavedTestThenTrain -l (moa.classifiers.trees.HoeffdingOptionTree ) -s (ArffFileStream -f $filename)  > $out5";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask LearnModel -l (moa.classifiers.trees.HoeffdingOptionTree ) -s (ArffFileStream -f $filename)  > $out6";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask EvaluateInterleavedTestThenTrain -l (moa.classifiers.trees.HoeffdingAdaptiveTree ) -s (ArffFileStream -f $filename)  >$out7";

system "java -Xmx8g -XX:-UseGCOverheadLimit -cp ~/moa.jar;weka.jar moa.DoTask LearnModel -l (moa.classifiers.trees.HoeffdingAdaptiveTree ) -s (ArffFileStream -f $filename)  > $out8";
}