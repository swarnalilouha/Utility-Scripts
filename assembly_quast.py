## Script to run Skesa and Quast for every sample in a given folder
#!/usr/bin/python3
import os,subprocess

list = []
file=open("text", 'r')
for line in file:                      
	list.append(line)
#print (list)
new_list = [x[:-1] for x in list]      ## removing the newline character at the end of every element in list
#print (new_list)

os.chdir('/scicomp/WDPB_pipeline/1_TrimData_analysis/20221110_20220804_20220502/subsampling')

for i in new_list:
	read1=i+"_R1_001_val_1.fq"
	print (read1)
	read2=i+"_R2_001_val_2.fq"
	print (read2)
	skesaInput=read1+","+read2
	print (skesaInput)
	skesaOutput=i+"_skesaContigs.fasta"
	print (skesaOutput)
	subprocess.call(["skesa","--fastq",skesaInput,"--contigs_out",skesaOutput])
	
	quastOutput=i+"_quast"
	print (quastOutput)
	subprocess.call(["quast.py","--eukaryote","-o",quastOutput,"-r","/scicomp/WDPB/Reference_Seqs/CryptoDB-54_CparvumIowaII_Genome.fasta", "--features","/scicomp/WDPB/Reference_Seqs/CryptoDB-54_CparvumIowaII.gff",skesaOutput])

	read1=''
	read2=''
	skesaInput=''
	skesaOutput=''
	quastOutput=''
	#print ("reads=".format(read1))
