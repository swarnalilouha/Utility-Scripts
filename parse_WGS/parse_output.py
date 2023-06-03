##Script for parsing specific data from output folders of the WGS pipeline and printing to a tab delimited text file.
## This script is used for running Novaseq samples with quast output folders ending with _quast.
 
#!/usr/bin/python3
import os,subprocess

rawfiles = []
path_of_input_folder = '/scicomp//WGS_pipeline/3_Assemble_Skesa_analysis/Data_Run_051723_20230519'
begin  = 'err_'
for files in os.listdir(path_of_input_folder):
	if files.startswith(begin):
		#print(files)
		rawfiles.append(files)
	else:
		continue
#print(rawfiles)

deconfiles = []
path_of_decon_folder = '/scicomp/WGS_pipeline/2_Decon_Kraken_analysis/Data_Run_051723_20230519'
end  = '.txt'
for deconfile in os.listdir(path_of_decon_folder):
        if deconfile.endswith(end):
                deconfiles.append(deconfile)
        else:
                continue
#print(deconfiles)


os.chdir('/scicomp/WGS_pipeline/3_Assemble_Skesa_analysis/Data_Run_051723_20230519')
quast_files = []
begin1 = 'report.txt'
path = '.'
for dirName, subdirList, fileList in os.walk(path):                            
	for filename in fileList:
		#print(filename)                                                       
		#if "__quast" in dirName:  ### used if quast folder ends with __quast
		if "_quast" in dirName:
#			print(dirName)
			#if " report.txt" in filename.lower():
			if filename.startswith(begin1):
				quast_files.append(os.path.join(dirName,filename))


print(quast_files)

for eachfile in rawfiles:
	create_samplename = eachfile.split("err_")
	#create_samplename1 = create_samplename[1].split("_.txt")
	create_samplename1 = create_samplename[1].split(".txt")
	Sample_name = create_samplename1[0]
	print("Samplename =",Sample_name)    ## This variable holds the name of the sample
	os.chdir('/scicomp/WGS_pipeline/3_Assemble_Skesa_analysis/Data_Run_051723_20230519')
	value = open(eachfile, 'r')
	for line in value:
		if line.startswith('Reads Used'):
			array = line.split("\t")
			Num_of_reads = array[1]                    
			print("Num of reads=",Num_of_reads)         ## This variable holds the value for 'Number of reads'
			basepairs_array = array[2].split(" bases")
			basepairs_array1 = basepairs_array[0].split("(")
			Num_of_bases = basepairs_array1[1]         
			print("Num of bases=",Num_of_bases)         ## This variabl holds the value for 'Number of bases'

		elif line.startswith('Average coverage:'):
			cov_array1 = line.split("\t")
			cov_array2 = cov_array1[1].split("\n")
			Average_coverage = cov_array2[0]
			print("Average coverage =", Average_coverage)     ## This variable holds value for 'Average Coverage'
 
	
	for i in quast_files:
		if Sample_name in i:
			print(i)
			value1 = open(i, 'r')
			for line1 in value1:
				if line1.startswith('# contigs (>= 0 bp)'):
					Num_contigs_array = line1.split("         ")
					Num_of_contigs = Num_contigs_array[1]					
					print("Num_of_contigs =", Num_of_contigs)                 ## This variable holds the value for 'Num of contigs'					 
				elif line1.startswith('Total length (>= 0 bp)'):
					Total_length_array = line1.split("      ")
					Total_length = Total_length_array[1]					
#					print("Total length =", Total_length)                     ## This variable holds value for 'Total length'
				elif line1.startswith('N50'):
					N50_array1 = line1.split("                         ")
					N50_array2 = N50_array1[1].split("                ")
					N50 = N50_array2[0]					
#					print("N50 =", N50)                                        ## This variable holds the value for 'N50'
				elif line1.startswith('L50'):
					L50_array1 = line1.split("                         ")
					L50_array2 = L50_array1[1].split("                ")
					L50 = L50_array2[0]
#					print("L50 =", L50)                                        ## This variable holds the value for L50

	os.chdir('/scicomp/WGS_pipeline/2_Decon_Kraken_analysis/Data_Run_051723_20230519')
	for decon in deconfiles:
		if Sample_name in decon:
			value2 = open(decon, 'r')
			for line2 in value2:
				if line2.endswith('     Cryptosporidium\n'):
					decon_array1 = line2.split("\t")
					Percent_match = decon_array1[0]
#					print("Percent match to Cryptosporidium =", decon_array1[0])      ## This variable holds the value for 'Percent match to Cryptosporidium'
	
	os.chdir('/scicomp/home-pure/qxu5/WGSPipeline_conda/script_parse_output')
	try:
		file = open("results.txt", "a")
		file.write(Sample_name+ "\t" +Num_of_reads+ "\t" +Num_of_bases+ "\t" +Average_coverage+ "\t" +Num_of_contigs+ "\t" +Total_length+ "\t" +N50+ "\t" +L50+ "\t" +Percent_match+ "\n")
		Sample_name=''
		Num_of_read=''
		Num_of_bases=''
		Num_of_bases=''
		Average_coverage=''
		Num_of_contigs=''
		Total_length=''
		N50=''
		L50=''
		Percent_match=''
	except Exception as e:
		print ("Unable to open file: {}".format(filename))
		print ("Reason: {}".format(str(e)))
