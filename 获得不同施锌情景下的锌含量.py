import os
import shutil
from shutil import copyfile
import time
import subprocess
import numpy as np
import pandas as pd
from scipy import integrate
import wofost
import utils
import tqdm
import znuptrantwo



dir = 'simresult'

dirlist = os.listdir(dir)
dirlist_path = []
inf_list =[]
for i in range(len(dirlist)):
    print(dirlist[i])
    result_path = dir +'\\'+dirlist[i]+'\\extract_data.csv'
    df = pd.read_csv(result_path)
    print(df)
    field = df.iloc[0,0]
    cmr = df.iloc[0,1]
    cgl = df.iloc[0, 2]
    inf = [dirlist[i],field,cmr,cgl ]
    inf_list.append(inf)

inf_df = pd.DataFrame(inf_list)
inf_df.columns = ['situation','field','cmr','cgl']
print(inf_df)
inf_df.to_csv('simresult\\statricezn.csv')