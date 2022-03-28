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
import matplotlib.pyplot as plt

if __name__ == "__main__":
    day_length = 108
    Diffus = 100
    Disp = 100
    Kd = 4.8
    yita = 0.012
    alpha = 0.52
    croot = 0.005
    Km = 0.005
    file_dir = ".\\hydrus20220228"
    ricetype = 'hhz'
    soil_zn = 1

    # 建立一个储存数据的列表
    solute_uptake_list = []
    conc_list = []
    rice_data = wofost.run_wofost(ricetype=ricetype, day_length=108)
    # SELECTOR_IN_data = [100, 150, 15, 0.62, 0.62, 0.5]
    SELECTOR_IN_data = [Diffus, Disp, Kd, yita, alpha, Km]
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    time.sleep(0.5)
    os.mkdir(file_dir)
    for i in tqdm.tqdm(range(day_length)):
        # cal_maxZn()
        day = i + 1
        # croot = cal_croot(ricetype=,day=,)
        utils.initial_soil(rice_data, croot, day, rice_type=ricetype, soil_zn=soil_zn,
                           SELECTOR_IN_data=SELECTOR_IN_data, filedir=file_dir)
        utils.run_hydrus(filedir=file_dir, day=day)
        pass

        # 运行完毕以后提取结果
        # 需要提取的结果有：每天各土壤深度的溶液、固相、总土壤浓度；每天植物对锌的吸收量3
        out = utils.get_output(filedir=file_dir, day=day)
        solute_uptake = out[0]
        solute_uptake_list.append(solute_uptake)
        conc_array = out[1]
        conc_list.append(conc_array)



    # -----------------收集画图的数据----------------------
    all_solute_uptake_list = []
    all_solute_uptake = 0.
    for solute in solute_uptake_list:
        all_solute_uptake += float(solute)
        all_solute_uptake_list.append(all_solute_uptake)
    # 保存画图的数据
    solute_df = pd.DataFrame({
        'das':np.arange(1,day_length+1),
        'solute_uptake':solute_uptake_list,
        'all_solute_uptake':all_solute_uptake_list
    })
    solute_df.to_csv("solute_result.csv",index=False)
    all_conc_list = []
    # 获得初始浓度
    initial_conc = utils.get_intial_conc(filedir=file_dir)
    all_conc_list.append(initial_conc[0])# 水
    all_conc_list.append(initial_conc[1])# 固相
    all_conc_list.append(initial_conc[2])# 含水率
    for conc in conc_list:
        all_conc_list.append(conc[0])
        all_conc_list.append(conc[1])
        all_conc_list.append(conc[2])
    all_conc_df_linshi = pd.DataFrame(all_conc_list)
    all_conc_df = pd.DataFrame(all_conc_df_linshi.values.T, index=all_conc_df_linshi.columns,
                               columns=all_conc_df_linshi.index)

    # 重命名
    colname_list = []
    for day in range(day_length+1):
        conc_name = 'day'+str(day)+"conc"
        sorbconc_name = 'day' + str(day) + "sorbconc"
        moisture_name = 'day' + str(day) + "moisture"
        colname_list.append(conc_name)
        colname_list.append(sorbconc_name)
        colname_list.append(moisture_name)
    all_conc_df.columns=colname_list
    # 计算总浓度
    for i in range(day_length+1):
        liquid_c = np.array(all_conc_df.iloc[:,i * 3].values).astype(float)
        sorbed_c = np.array(all_conc_df.iloc[:,i * 3 + 1].values).astype(float)
        moisture = np.array(all_conc_df.iloc[:, i * 3 + 2].values).astype(float)
        allconc = utils.cal_massconc(theta = moisture,liquid_c = liquid_c, sorbed_c = sorbed_c)
        name = 'day' + str(i) + "allconc"
        all_conc_df[name] = allconc
    all_conc_df.to_csv("all_conc_result.csv", index=False)
    # -------------------------------------------------------