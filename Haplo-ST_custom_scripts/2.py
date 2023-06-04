import pandas as pd
import numpy as np

data = pd.read_csv("./combined_result1.txt", sep='\t')

df2 = data.set_index("sample_name")

df2 = df2.astype(object)

for col in df2:
    k = 2001
    for i, row_value in df2[col].iteritems():
        #print(df2[col][i])   ## df2[col][i] contains every row(i) for every col
        if (str(df2[col][i]).startswith("closest")):
            array = df2[col][i].split(" ")
            print(array[2])  ## contains value after closest match:
            m = "_".join((str(array[2]), str(k)))
            df2[col][i] = m
            k = k+1

df2 = df2.fillna("?")

df2.to_csv('combined_result2.txt', header=True, index=True, sep='\t')
