## Script for concatenating R1 and R2 reads from different lanes into a single R1 and R2 fastq file in an "output" folder. 
## The unprocessed samples are moved to a separate folder named "unprocessed".

#!/usr/bin/python3
import os,subprocess
import time

## Code for taking files from input folder into an array called rawfiles
rawfiles = []
path_of_input_folder = './samples'
ext = '.gz'
for files in os.listdir(path_of_input_folder):
	if files.endswith(ext):
		rawfiles.append(files)  
	else:
		continue

## Code for reading per line of text file in an array
#filename = input("Enter filename:")
list = []
try:
#	file = open(filename)
	file=open("names1", 'r')
	for line in file:                      
		list.append(line)

	new_list = [x[:-1] for x in list]      
#	print (new_list)

##Code that takes the text file of sample names, then for each sample name, concatenates the RI and R2 reads from different lanes
	filename_array = []
	os.chdir('samples')
	for i in new_list:
		print (i)
		for j in rawfiles:
			if j.startswith(i):
				print (j)
				filename_array = j.split("_L00")
				middlename = filename_array[0]
				index = j.find("R1")
				if index!=-1:
					#print (j)
					cmd1 = "cat  "+str(i)+"*_R1_*.fastq.gz  >  ./../output/"+str(middlename)+"_L001_R1_001.fastq.gz"
					subprocess.call(cmd1, shell=True)
					filename_array = []
				else:
					#print (j)
					cmd2 = "cat  "+str(i)+"*_R2_*.fastq.gz  >  ./../output/"+str(middlename)+"_L001_R2_001.fastq.gz"
					subprocess.call(cmd2, shell=True)
					filename_array = []
		cmd3 = "mv  "+str(i)+"*.fastq.gz  ./../unprocessed"
		subprocess.call(cmd3, shell=True)
		#cmd3 = "echo "+str(i)+"*.fastq.gz"
		#subprocess.call(cmd3, shell=True)

except Exception as e:
	print("Unable to open file: {}".format(filename))
	print ("Reason: {}".format(str(e))) 
