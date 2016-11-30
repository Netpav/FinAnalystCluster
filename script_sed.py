#!/usr/bin/python
import glob
import subprocess
import os
import sys


for fileName in glob.glob('~/*.text'):
	print fileName
# for line in fileinput.input("www.txt", inplace=True):
    # print "\n *********** \n"     
    # print "\n *********** \n"
    # print line.replace("[1-9]", ""),
    # #subprocess.call(["sed -i -e 's/[1-9]//g' fileName"], shell=True)
    # print "\n *********** OK **************** \n"
