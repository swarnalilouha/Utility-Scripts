## module load Anaconda3/2019.03
import pandas as pd
import numpy as np
import glob

data = pd.read_csv("./combined_results_project1.txt", sep='\t', low_memory=False)

df2 = data.set_index("sample_name")

files= glob.glob("final_blast/*")

for file in files:
    textfile = open(file,"r")
    linearray = textfile.readlines()
    #print(linearray)
    length = (len(linearray));
    
    for i in range(0, len(linearray)):
        line = linearray[i]
        print(line)
        samples = line.split("\t")
        line1sample1 = samples[0].split(".")
        line1sample2 = samples[1].split(".")
        #print(line1sample1[1], line1sample2[1], sep = '\t')
        x1 = line1sample1[1]         ##name of sample1 on line1
        y1 = line1sample2[1]         ##name of sample2 on line2 
        a1 = line1sample1[0]         ## name of gene
        k = i+1                      ## keeps count of number after .
        
        m = "_".join((str(line1sample1[2]), str(k)))        ## line1sample1[2] contains the closest allele id
        print(x1, y1, a1, k, m, sep = '\t')
              
        if (df2.loc[x1, a1].startswith("closest")):
            #print(x1, m, sep = ' ')
            df2.loc[x1, a1] = m
            
        if (df2.loc[y1, a1].startswith("closest")):
            #print(y1, m, sep = ' ')
            df2.loc[y1, a1] = m
        
        for j in range(i+1, len(linearray)):
            nextline = linearray[j]
            #print(nextline)
            samples1 = nextline.split("\t")
            line2sample1 = samples1[0].split(".")
            line2sample2 = samples1[1].split(".")
            #print(line2sample1[1], line2sample2[1], sep = '\t')
            x2 = line2sample1[1]
            y2 = line2sample2[1]
            #print(x2, y2, sep = '\t')
            
            if (x2 == x1 or y2 == x1 or x2 == y1 or y2 == y1):
                print(x1, y1, x2, y2, sep = ' same ')
                
                if (df2.loc[x2, a1].startswith("closest")):
                    #print(x2, m, sep = ' ')
                    df2.loc[x2, a1] = m
            
                if (df2.loc[y2, a1].startswith("closest")):
                    #print(y2, m, sep = ' ')
                    df2.loc[y2, a1] = m



df2.to_csv('combined_result1.txt', header=True, index=True, sep='\t')
