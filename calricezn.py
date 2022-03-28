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
from sympy import *
import mycalet0

def cal_zn_conn_in_rice(allconc, field):
    x = symbols('x')
    allconc = float(allconc)
    if field in ['1', '10', '13_1', '13_2', '13_3', '13_4','14']:
        cmr = solve(0.45 * x + 0.55 * (3.11 * x - 37.06) - allconc, x)
        cmr = float(cmr[0])
        cgl = 3.11 * cmr - 37.06
    if field in ['2', '3', '4', '5', '6']:
        cmr = solve(0.45 * x + 0.55 * (5.36 * x - 46.34) - allconc, x)
        cmr = float(cmr[0])
        cgl = 5.36 * cmr - 46.34
    if field in ['7', '8', '9', '11', '12']:
        cmr = solve(0.45 * x + 0.55 * (0.85 * x + 28.74) - allconc, x)
        cmr = float(cmr[0])
        cgl = 0.85 * cmr + 28.74
    return cmr, cgl



def main(dir='main_result\\'):
    field_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13_1', '13_2', '13_3', '13_4',
                  '14']
    extract_list = []
    for i in field_list:
        zndata_name = dir + 'field' + i + '_zndata.csv'
        soildata_name = dir + 'field' + i + '_soildata.csv'
        solutedata_name = dir + 'field' + i + '_solutedata.csv'
        zn_df = pd.read_csv(zndata_name)
        soil_df = pd.read_csv(soildata_name)
        solutedata_df = pd.read_csv(solutedata_name)
        erc = float(zn_df.iloc[-1, 4])
        cmr, cgl = cal_zn_conn_in_rice(allconc=erc, field=i)
        print('精米的锌含量为：', cmr)
        print('颖壳的锌含量为：', cgl)
        # 提取土壤锌浓度
        depth10conc = float(soil_df.iloc[2, -1])
        depth20conc = float(soil_df.iloc[7, -1])
        extract_list.append([i, cmr, cgl, depth10conc, depth20conc])
        extract_df = pd.DataFrame(extract_list)
        extract_df.columns = ['field', 'cmr', 'cgl', 'depth10conc', 'depth20conc']
        extract_df.to_csv(dir + 'extract_data.csv', index=False)

def main11(dir='main_result\\'):
    field_list = ['2']

    extract_list = []
    i = '2'
    zndata_name = dir + 'field' + i + '_zndata.csv'
    soildata_name = dir + 'field' + i + '_soildata.csv'
    solutedata_name = dir + 'field' + i + '_solutedata.csv'
    zn_df = pd.read_csv(zndata_name)
    soil_df = pd.read_csv(soildata_name)
    solutedata_df = pd.read_csv(solutedata_name)
    erc = float(zn_df.iloc[-1, 4])
    cmr, cgl = cal_zn_conn_in_rice(allconc=erc, field=i)
    print('精米的锌含量为：', cmr)
    print('颖壳的锌含量为：', cgl)
    # 提取土壤锌浓度
    depth10conc = float(soil_df.iloc[2, -1])
    depth20conc = float(soil_df.iloc[7, -1])
    extract_list.append([i, cmr, cgl, depth10conc, depth20conc])
    extract_df = pd.DataFrame(extract_list)
    extract_df.columns = ['field', 'cmr', 'cgl', 'depth10conc', 'depth20conc']
    extract_df.to_csv(dir + 'extract_data.csv', index=False)
if __name__ == "__main__":
    main()

