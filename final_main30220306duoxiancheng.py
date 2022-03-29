import math
import datetime
import multiprocessing as mp
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


def train_on_parameter(name, param):
    result = 0
    for num in param:
        result += math.sqrt(num * math.tanh(num) / math.log2(num) / math.log10(num))
    return {name: result}


def cal_table(date, value):
    table = []
    datenum = len(date)
    for i in range(datenum):
        table.append([date[i], value[i]])
    return table


#
# def get_field_inf(field):
#     rice_process = {
#         'hhz': [1, 8, 29, 70, 75, 108],
#         '99-25': [1, 8, 29, 79, 87, 147],
#         'NJ9108': [1, 8, 28, 80, 88, 147]
#     }
#     rice_zn_need = {
#         'hhz': [[10, 25, 25, 40, 20, 20],
#                 [10, 25, 25, 40, 20, 20],
#                 [25, 25, 25, 25, 25, 25],
#                 [15, 15, 15, 15, 15, 15],
#                 [100, 100, 100, 100, 100, 100],
#                 [100, 100, 100, 200, 200, 200],
#                 [200, 200, 200, 300, 300, 200],
#                 [100, 100, 100, 100, 100, 100],
#                 [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#                 [0.01, 0.04, 0.04, 0.04, 0.04, 0.04],
#                 [0.03, 0.04, 0.05, 0.05, 0.05, 0.05],
#                 [0, 0, 0, 0, 0, ]],
#         '99-25': [[10, 25, 25, 40, 20, 20],
#                   [10, 25, 25, 40, 20, 20],
#                   [25, 25, 25, 25, 25, 25],
#                   [15, 15, 15, 15, 15, 15],
#                   [100, 100, 100, 100, 100, 100],
#                   [100, 100, 100, 200, 200, 200],
#                   [200, 200, 200, 300, 300, 200],
#                   [100, 100, 100, 100, 100, 100],
#                   [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#                   [0.01, 0.04, 0.04, 0.04, 0.04, 0.04],
#                   [0.03, 0.04, 0.05, 0.05, 0.05, 0.05],
#                   [0, 0, 0, 0, 0, ]],
#         'NJ9108': [[10, 25, 25, 40, 20, 20],
#                    [10, 25, 25, 40, 20, 20],
#                    [25, 25, 25, 25, 25, 25],
#                    [15, 15, 15, 15, 15, 15],
#                    [100, 100, 100, 100, 100, 100],
#                    [100, 100, 100, 200, 200, 200],
#                    [200, 200, 200, 300, 300, 200],
#                    [100, 100, 100, 100, 100, 100],
#                    [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#                    [0.01, 0.04, 0.04, 0.04, 0.04, 0.04],
#                    [0.03, 0.04, 0.05, 0.05, 0.05, 0.05],
#                    [0, 0, 0, 0, 0, ]],
#     }
#
#     if field in ['1', '10', '13_1', '13_2', '13_3', '13_4']:
#         rice_type = 'NJ9108'
#         blossom_date = rice_process[rice_type][3]
#         MIZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
#         MIZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
#         MIZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
#         MIZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
#         MXZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
#         MXZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
#         MXZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
#         MXZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
#         FRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
#         FSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
#         FLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
#         FERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
#     if field in ['2', '3', '4', '5', '6']:
#         rice_type = 'hhz'
#         blossom_date = rice_process[rice_type][3]
#         MIZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
#         MIZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
#         MIZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
#         MIZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
#         MXZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
#         MXZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
#         MXZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
#         MXZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
#         FRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
#         FSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
#         FLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
#         FERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
#     if field in ['7', '8', '9', '11', '12']:
#         rice_type = '99-25'
#         blossom_date = rice_process[rice_type][3]
#         MIZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
#         MIZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
#         MIZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
#         MIZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
#         MXZRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
#         MXZSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
#         MXZLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
#         MXZERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
#         FRTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
#         FSTT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
#         FLFT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
#         FERT = cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
#     else:
#         print('Field input wrong.')
#     if field == '1':
#         soil_zn = 0
#         sprinkle_zn = 3
#         sprinkle_das = []
#
#     pass


def get_rice_daylength(ricetype):
    if ricetype == 'hhz':
        day_length = 108
    if ricetype == '99-25':
        day_length = 147
    if ricetype == 'NJ9108':
        day_length = 147
    return day_length


def get_abseff(field, znsofer, edtaznfer, saznfer):
    if field == '13_3':
        abseff = edtaznfer
    if field == '13_4':
        abseff = saznfer
    else:
        abseff = znsofer
    return abseff


def get_km(rice_type):
    if rice_type == 'NJ9108':
        km = 0.008
    if rice_type == 'hhz':
        km = 0.003
    if rice_type == '99-25':
        km = 0.008
    return km


def run(i):
    field_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13_1', '13_2', '13_3', '13_4',
                  '14']

    files_dir = []
    for sada in field_list:
        files_dir.append('.\\hydrus20220327' + '_' + sada)
    field = field_list[i]
    file_dir = files_dir[i]
    # hydrus模型参数
    Diffus = 100
    Disp = 10
    Kd = 120
    yita = 0.012
    alpha = 0.62
    croot = 0.002
    # Km = 0.035
    # 不同锌肥种类的利用效率
    znsofer = 0.13
    edtaznfer = 0.05
    saznfer = 0.23
    # 收集数据
    # 每块田的作物数据、土壤锌浓度、作物锌浓度

    # 获得水稻种类、土壤施锌量、喷施锌肥量、喷施日期
    ricetype, soil_zn, sprinkle_zn, sprinkle_das = utils.get_fieldinf2(field=field)
    day_length = get_rice_daylength(ricetype)
    # Km
    Km = get_km(ricetype)
    # 锌肥效率
    abseff = get_abseff(field, znsofer, edtaznfer, saznfer)
    # 水稻作物数据
    rice_data = wofost.run_wofost(ricetype=ricetype, day_length=day_length)
    # hydrus参数
    SELECTOR_IN_data = [Diffus, Disp, Kd, yita, alpha, Km]
    # 创建hydrus文件夹
    time.sleep(0.5)
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    time.sleep(0.2)
    os.mkdir(file_dir)
    # 建立锌吸收的类
    zn_rice = znuptrantwo.Zninrice(ricetype=ricetype, ricedata=rice_data, day_length=day_length, field=field)
    # 建立收集数据的列表
    solute_uptake_list = []
    conc_list = []
    organ_znconc_list = []
    zn_content = []
    sumZnbot_list = []
    # 开始运行
    for i in range(day_length):
        # cal_maxZn()
        day = i + 1
        # 判断此天是否有锌肥喷入
        if day in sprinkle_das:
            sprinkle_zn_today = 70 * (1 - abseff) * 1000 / (666.67 * 10000)
        else:
            sprinkle_zn_today = 0

        zn_rice.run_oneday1()
        croot = zn_rice.cal_croot() / 10e8
        utils.initial_soil(rice_data, croot, day, rice_type=ricetype, soil_zn=soil_zn,
                           SELECTOR_IN_data=SELECTOR_IN_data, filedir=file_dir,
                           sprinkle_zn_today=sprinkle_zn_today)
        utils.run_hydrus(filedir=file_dir, day=day)
        # 运行完毕以后提取结果
        # 需要提取的结果有：每天各土壤深度的溶液、固相、总土壤浓度；每天植物对锌的吸收量3
        out = utils.get_output(filedir=file_dir, day=day)
        if day in sprinkle_das:
            solute_uptake = float(out[0])
            zn_rice.ZALF = zn_rice.ZALF + 70 * abseff * 1000 * 15
        else:
            solute_uptake = float(out[0])
        solute_uptake_list.append(solute_uptake)
        conc_array = out[1]
        conc_list.append(conc_array)
        # 分配锌
        zn_rice.update_ZUN(solute_uptake)
        zn_rice.run_oneday2()
        organ_znconc_list.append(
            [zn_rice.day, zn_rice.ZRTC, zn_rice.ZSTC, zn_rice.ZLFC, zn_rice.ZERC, zn_rice.ZART, zn_rice.ZAST,
             zn_rice.ZALF, zn_rice.ZAER, zn_rice.TZDMI, zn_rice.TZDMX, zn_rice.ZU])
        # -------------锌-------------------
        # 锌最小需求量
        min_zn_inrice = zn_rice.MIZRT * rice_data.loc[i, 'WRT'] + zn_rice.MIZST * rice_data.loc[i, 'WST'] + \
                        zn_rice.MIZLF * rice_data.loc[i, 'WLV'] + zn_rice.MIZER * rice_data.loc[i, 'TWSO']
        # 锌最大需求量
        max_zn_inrice = zn_rice.MXZRT * rice_data.loc[i, 'WRT'] + zn_rice.MXZST * rice_data.loc[i, 'WST'] + \
                        zn_rice.MXZLF * rice_data.loc[i, 'WLV'] + zn_rice.MXZER * rice_data.loc[i, 'TWSO']
        # 锌实际量
        zn_actual = zn_rice.ZART + zn_rice.ZAST + zn_rice.ZALF + zn_rice.ZAER
        zn_content.append([day, min_zn_inrice, max_zn_inrice, zn_actual])
        # 下边界的流出锌量
        sumZnbot = utils.read_sumZnbot(file_dir, day)
        if day == 1:
            sumZnbotsum = sumZnbot
        else:
            sumZnbotsum += sumZnbot
        sumZnbot_list.append([day, sumZnbot, sumZnbotsum])

    rice_data.to_csv('main_result\\field' + field + '_cropdata.csv', index=False)
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
    solute_df.to_csv('main_result\\field' + field + '_solutedata.csv', index=False)
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
    all_conc_df.to_csv('main_result\\field' + field + '_soildata.csv', index=False)
    # -------------------------------------------------------

    # -----------------------收集水稻吸锌的数据-----------------------------
    zn_content_df = pd.DataFrame(zn_content)
    zn_content_df.columns = ['day', 'min_zn_inrice', 'max_zn_inrice', 'zn_actual']
    zn_content_df.to_csv('main_result\\field' + field + '_zn_contentdata.csv', index=False)
    organ_znconc_df = pd.DataFrame(organ_znconc_list)
    organ_znconc_df.columns = ['day', 'ZRTC', 'ZSTC', 'ZLFC', 'ZERC', 'ZART', 'ZAST', 'ZALF', 'ZAER', 'TZDMI',
                               'TZDMX',
                               'ZU']
    organ_znconc_df.to_csv('main_result\\field' + field + '_zndata.csv', index=False)

    # -----------------------锌流出的数据----------------------------------

    sumZnbot_df = pd.DataFrame(sumZnbot_list)
    sumZnbot_df.columns = ['day', 'sumZnbot', 'sumZnbotsum']
    sumZnbot_df.to_csv('main_result\\field' + field + '_sumZnbotdata.csv', index=False)
    pass


import multiprocessing

if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    xs = range(17)

    pool.map(run, xs)
    import calricezn

    calricezn.main()
    import winsound

    duration = 2500  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)
