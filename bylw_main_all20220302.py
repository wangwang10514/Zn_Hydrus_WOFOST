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
import znuptran
import matplotlib.pyplot as plt

if __name__ == "__main__":
    day_length = 108
    Diffus = 50
    Disp = 10
    Kd = 40
    yita = 0.012
    alpha = 0.5
    croot = 0.005
    Km = 0.002
    file_dir = ".\\hydrus20220228"
    field='2'
    ricetype, soil_zn, sprinkle_zn, sprinkle_das = utils.get_fieldinf(field=field)
    # 叶面肥

    # 锌肥效率

    # 建立一个储存数据的列表
    solute_uptake_list = []
    conc_list = []
    organ_znconc_list = []
    rice_data = wofost.run_wofost(ricetype=ricetype, day_length=108)
    # SELECTOR_IN_data = [100, 150, 15, 0.62, 0.62, 0.5]
    SELECTOR_IN_data = [Diffus, Disp, Kd, yita, alpha, Km]
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    time.sleep(0.5)
    os.mkdir(file_dir)
    zn_rice = znuptran.Zninrice(ricetype=ricetype, ricedata=rice_data, day_length=day_length)

    for i in tqdm.tqdm(range(day_length)):
        # cal_maxZn()
        day = i + 1
        if day in sprinkle_das:
            sprinkle_zn_today = 363*1000/(666.67*10000)
        else:
            sprinkle_zn_today = 0

        zn_rice.run_oneday1()
        croot = zn_rice.cal_croot() / 10e8
        utils.initial_soil(rice_data, croot, day, rice_type=ricetype, soil_zn=soil_zn,
                           SELECTOR_IN_data=SELECTOR_IN_data, filedir=file_dir,sprinkle_zn_today =sprinkle_zn_today)
        utils.run_hydrus(filedir=file_dir, day=day)
        # 运行完毕以后提取结果
        # 需要提取的结果有：每天各土壤深度的溶液、固相、总土壤浓度；每天植物对锌的吸收量3
        out = utils.get_output(filedir=file_dir, day=day)
        solute_uptake = out[0]
        solute_uptake_list.append(solute_uptake)
        conc_array = out[1]
        conc_list.append(conc_array)
        # 分配锌
        zn_rice.update_ZUN(solute_uptake)
        zn_rice.run_oneday2()
        # print(zn_rice.BANLANCE)
        # 收集锌的数据，需要收集的有：各器官锌浓度，各器官锌含量，最小锌含量、最大锌含量、实际吸锌量
        organ_znconc_list.append(
            [zn_rice.day, zn_rice.ZRTC, zn_rice.ZSTC, zn_rice.ZLFC, zn_rice.ZERC, zn_rice.ZART, zn_rice.ZAST,
             zn_rice.ZALF, zn_rice.ZAER, zn_rice.TZDMI, zn_rice.TZDMX, zn_rice.ZU])

    # -----------------收集画图的数据----------------------
    all_solute_uptake_list = []
    all_solute_uptake = 0.
    for solute in solute_uptake_list:
        all_solute_uptake += float(solute)
        all_solute_uptake_list.append(all_solute_uptake)
    # 保存画图的数据
    solute_df = pd.DataFrame({
        'das': np.arange(1, day_length + 1),
        'solute_uptake': solute_uptake_list,
        'all_solute_uptake': all_solute_uptake_list
    })
    solute_df.to_csv("solute_result.csv", index=False)
    all_conc_list = []
    # 获得初始浓度
    initial_conc = utils.get_intial_conc(filedir=file_dir)
    all_conc_list.append(initial_conc[0])  # 水
    all_conc_list.append(initial_conc[1])  # 固相
    all_conc_list.append(initial_conc[2])  # 含水率
    for conc in conc_list:
        all_conc_list.append(conc[0])
        all_conc_list.append(conc[1])
        all_conc_list.append(conc[2])
    all_conc_df_linshi = pd.DataFrame(all_conc_list)
    all_conc_df = pd.DataFrame(all_conc_df_linshi.values.T, index=all_conc_df_linshi.columns,
                               columns=all_conc_df_linshi.index)

    # 重命名
    colname_list = []
    for day in range(day_length + 1):
        conc_name = 'day' + str(day) + "conc"
        sorbconc_name = 'day' + str(day) + "sorbconc"
        moisture_name = 'day' + str(day) + "moisture"
        colname_list.append(conc_name)
        colname_list.append(sorbconc_name)
        colname_list.append(moisture_name)
    all_conc_df.columns = colname_list
    # 计算总浓度
    for i in range(day_length + 1):
        liquid_c = np.array(all_conc_df.iloc[:, i * 3].values).astype(float)
        sorbed_c = np.array(all_conc_df.iloc[:, i * 3 + 1].values).astype(float)
        moisture = np.array(all_conc_df.iloc[:, i * 3 + 2].values).astype(float)
        allconc = utils.cal_massconc(theta=moisture, liquid_c=liquid_c, sorbed_c=sorbed_c)
        name = 'day' + str(i) + "allconc"
        all_conc_df[name] = allconc
    all_conc_df.to_csv("all_conc_result.csv", index=False)
    # -------------------------------------------------------

    # -----------------------收集水稻吸锌的数据-----------------------------
    organ_znconc_df = pd.DataFrame(organ_znconc_list)
    organ_znconc_df.columns = ['day', 'ZRTC', 'ZSTC', 'ZLFC', 'ZERC', 'ZART', 'ZAST', 'ZALF', 'ZAER', 'TZDMI', 'TZDMX',
                               'ZU']
    organ_znconc_df.to_csv("organ_znconc_df.csv", index=False)
