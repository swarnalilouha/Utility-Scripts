#!/usr/bin/python3
import os,subprocess

path_of_input_folder = './files'
outfile = open("DevwgCrypto_20230620_alleles_renamed.fasta", "a")
for file in os.listdir(path_of_input_folder):
	os.chdir('./files')
	filecontent = open(file, 'r')
	for line in filecontent:
		if line.startswith('>'):
			array1 = line.split("|")
			#print(array1[0],"\t",array1[1])
			array2 = array1[0].split("_")
			#print(array2[0],"\t",array2[1],"\t",array2[2])
			new_header = array2[0]+array2[1]+"_"+array2[2]+"\n"
			outfile.write(new_header)
		else:
			outfile.write(line)
