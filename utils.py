import os
import shutil
from shutil import copyfile
import time
import subprocess
import numpy as np
import pandas as pd
from scipy import integrate
import wofost
import sympy
import math


def get_fieldinf(field):
    sprinkle_das_dic = {
        '1': [80, 86, 92],
        '2': [73, 79, 87],
        '3': [73, 79, 87],
        '4': [0, 0, 0],
        '5': [74, 79, 87],
        '6': [73, 79, 87],
        '7': [0, 0, 0],
        '8': [74, 81, 91],
        '9': [74, 81, 91],
        '10': [0, 0, 0],
        '11': [75, 82, 91],
        '12': [75, 82, 92],
        '13_1': [0, 0, 0],
        '13_2': [80, 86, 92],
        '13_3': [80, 86, 92],
        '13_4': [80, 86, 92],
        '14': [80, 86, 92],

    }
    sprinkle_zn_dic = {
        '1': True,
        '2': True,
        '3': True,
        '4': False,
        '5': True,
        '6': True,
        '7': False,
        '8': True,
        '9': True,
        '10': False,
        '11': True,
        '12': True,
        '13_1': False,
        '13_2': True,
        '13_3': True,
        '13_4': True,
        '14': True,

    }
    soil_zn_dic = {
        '1': 0,
        '2': 3,
        '3': 2,
        '4': 0,
        '5': 1,
        '6': 0,
        '7': 0,
        '8': 3,
        '9': 2,
        '10': 0,
        '11': 1,
        '12': 0,
        '13_1': 3,
        '13_2': 3,
        '13_3': 3,
        '13_4': 3,
        '14': 3,

    }
    rice_type_dic = {
        '1': 'NJ9108',
        '2': 'hhz',
        '3': 'hhz',
        '4': 'hhz',
        '5': 'hhz',
        '6': 'hhz',
        '7': '99-25',
        '8': '99-25',
        '9': '99-25',
        '10': 'NJ9108',
        '11': '99-25',
        '12': '99-25',
        '13_1': 'NJ9108',
        '13_2': 'NJ9108',
        '13_3': 'NJ9108',
        '13_4': 'NJ9108',
        '14': 'NJ9108',

    }
    sprinkle_das = sprinkle_das_dic[field]
    sprinkle_zn = sprinkle_zn_dic[field]
    soil_zn = soil_zn_dic[field]
    rice_type = rice_type_dic[field]
    return [rice_type,soil_zn ,sprinkle_zn,sprinkle_das]

def get_fieldinf2(field):
    sprinkle_das_dic = {
        '1': [80, 86, 92],
        '2': [73, 79, 87],
        '3': [73, 79, 87],
        '4': [0, 0, 0],
        '5': [74, 79, 87],
        '6': [73, 79, 87],
        '7': [0, 0, 0],
        '8': [74, 81, 91],
        '9': [74, 81, 91],
        '10': [0, 0, 0],
        '11': [75, 82, 91],
        '12': [75, 82, 92],
        '13_1': [0, 0, 0],
        '13_2': [80, 86, 92],
        '13_3': [80, 86, 92],
        '13_4': [80, 86, 92],
        '14': [80, 86, 92],

    }
    sprinkle_zn_dic = {
        '1': True,
        '2': True,
        '3': True,
        '4': False,
        '5': True,
        '6': True,
        '7': False,
        '8': True,
        '9': True,
        '10': False,
        '11': True,
        '12': True,
        '13_1': False,
        '13_2': True,
        '13_3': True,
        '13_4': True,
        '14': True,

    }
    soil_zn_dic = {
        '1': 0,
        '2': 3,
        '3': 2,
        '4': 0,
        '5': 1,
        '6': 0,
        '7': 0,
        '8': 3,
        '9': 2,
        '10': 0,
        '11': 1,
        '12': 0,
        '13_1': 3,
        '13_2': 3,
        '13_3': 3,
        '13_4': 3,
        '14': 3,

    }
    rice_type_dic = {
        '1': 'NJ9108',
        '2': 'hhz',
        '3': 'hhz',
        '4': 'hhz',
        '5': 'hhz',
        '6': 'hhz',
        '7': '99-25',
        '8': '99-25',
        '9': '99-25',
        '10': 'NJ9108',
        '11': '99-25',
        '12': '99-25',
        '13_1': 'NJ9108',
        '13_2': 'NJ9108',
        '13_3': 'NJ9108',
        '13_4': 'NJ9108',
        '14': 'NJ9108',

    }

    sprinkle_das = sprinkle_das_dic[field]
    sprinkle_zn = sprinkle_zn_dic[field]
    soil_zn = soil_zn_dic[field]
    rice_type = rice_type_dic[field]
    return [rice_type,soil_zn ,sprinkle_zn,sprinkle_das]

def get_fieldinf3(field,sprinkle_date):
    sprinkle_das_dic = {
        '1': [80, 86, 92],
        '2': sprinkle_date,
        '3': [73, 79, 87],
        '4': [0, 0, 0],
        '5': [74, 79, 87],
        '6': [73, 79, 87],
        '7': [0, 0, 0],
        '8': [74, 81, 91],
        '9': [74, 81, 91],
        '10': [0, 0, 0],
        '11': [75, 82, 91],
        '12': [75, 82, 92],
        '13_1': [0, 0, 0],
        '13_2': [80, 86, 92],
        '13_3': [80, 86, 92],
        '13_4': [80, 86, 92],
        '14': [80, 86, 92],

    }
    sprinkle_zn_dic = {
        '1': True,
        '2': True,
        '3': True,
        '4': False,
        '5': True,
        '6': True,
        '7': False,
        '8': True,
        '9': True,
        '10': False,
        '11': True,
        '12': True,
        '13_1': False,
        '13_2': True,
        '13_3': True,
        '13_4': True,
        '14': True,

    }
    soil_zn_dic = {
        '1': 0,
        '2': 3,
        '3': 2,
        '4': 0,
        '5': 1,
        '6': 0,
        '7': 0,
        '8': 3,
        '9': 2,
        '10': 0,
        '11': 1,
        '12': 0,
        '13_1': 3,
        '13_2': 3,
        '13_3': 3,
        '13_4': 3,
        '14': 3,

    }
    rice_type_dic = {
        '1': 'NJ9108',
        '2': 'hhz',
        '3': 'hhz',
        '4': 'hhz',
        '5': 'hhz',
        '6': 'hhz',
        '7': '99-25',
        '8': '99-25',
        '9': '99-25',
        '10': 'NJ9108',
        '11': '99-25',
        '12': '99-25',
        '13_1': 'NJ9108',
        '13_2': 'NJ9108',
        '13_3': 'NJ9108',
        '13_4': 'NJ9108',
        '14': 'NJ9108',

    }

    sprinkle_das = sprinkle_das_dic[field]
    sprinkle_zn = sprinkle_zn_dic[field]
    soil_zn = soil_zn_dic[field]
    rice_type = rice_type_dic[field]
    return [rice_type,soil_zn ,sprinkle_zn,sprinkle_das]

def cal_initial_zn_conc0(soil_zn, theta, Kd, yita):
    mass_conc = 73.33
    v_conc = mass_conc * 1.45 / 1000
    c = sympy.symbols('c')
    liquid_c = sympy.solve(theta * c + 1.45 * Kd * c / (1 + yita * c) - v_conc, c)[1]
    sorbed_c = 1.45 * Kd * liquid_c / (1 + yita * liquid_c)
    liquid_c += soil_zn * 0.0147
    return sorbed_c, liquid_c


def cal_initial_zn_conc1(soil_zn, theta, Kd, yita):
    mass_conc = 73.33 + soil_zn * 5.1724
    v_conc = mass_conc * 1.45 / 1000
    c = sympy.symbols('c')
    liquid_c = sympy.solve(theta * c + 1.45 * Kd * c / (1 + yita * c) - v_conc, c)[1]
    sorbed_c = 1.45 * Kd * liquid_c / (1 + yita * liquid_c)
    return sorbed_c, liquid_c


def cal_massconc(theta, liquid_c, sorbed_c):
    massconc = theta * liquid_c * 1000 / 1.45 + sorbed_c * 1000 / 1.45
    return massconc


def water_extraction(z, lr, lrs):
    """
    Root water absorption distribution function
    :param z:Depth from surface
    :param lr:root length
    :param lrs:The depth at which roots begin to grow
    :return:root uptake water distribution in depth z
    """
    rootdepth1 = lrs + 0.2 * lr
    root_max_depth = lrs + lr

    bz = -9999.
    if z < 0:
        print("z must set >=0")

    elif 0 <= z < lrs:
        bz = 0
    elif lrs <= z <= rootdepth1:
        bz = 5 / (3 * lr)
    elif rootdepth1 < z <= root_max_depth:
        bz = -25 * (z - lrs) / (12 * lr * lr) + 25 / (12 * lr)
    else:
        bz = 0
    return bz


def cal_root_uptake_index(rice_data, day):
    root_depth = rice_data.iloc[day - 1, 9]
    node_num = math.ceil(root_depth / 3) - 3
    root_depth = node_num * 3 + 9
    # 根深有多少个节点
    input_node_list = [9]  # 从9cm开始
    for i in range(node_num):
        input_node_list.append(12 + 3 * i)
    i_list = []
    for i in input_node_list:
        v = water_extraction(z=i, lr=root_depth - 9, lrs=9)
        i_list.append(v)
    newi_list = [0, 0, 0]  # 0,3,6的吸水指数
    for i in i_list:
        newi_list.append(round(i, 8))
    num = 101 - len(newi_list)
    for i in range(0, num):
        newi_list.append(0)

    root_uptake_index = np.array(newi_list)
    root_uptake_index = root_uptake_index / np.max(root_uptake_index)
    return root_uptake_index
    pass


def get_gwl(day):
    with open("gwl.txt", "r") as f:
        data = f.readlines()
        newdata = []
        for line in data:
            newdata.append(float(line.strip('\n')))
    f.close()
    return newdata[day - 1]


def get_lai(rice_data, day):
    lai = rice_data.iloc[day - 1, 2]
    return lai


def get_boundary_con(day, rice_type, rice_data, croot):
    boundary_con = pd.read_csv('边界条件整理-20220228.csv', encoding='gbk')
    if rice_type == 'hhz':
        prec = boundary_con.iloc[day - 1, 24]
        pet = boundary_con.iloc[day - 1, 14]
        hcrita = boundary_con.iloc[day - 1, 6]
        LAI = get_lai(rice_data, day)
        gwl = boundary_con.iloc[day - 1, 7]
        ctop = boundary_con.iloc[day - 1, 8]
        hhz_boundary_con = [prec, pet, hcrita, LAI, gwl, ctop, croot]
        return hhz_boundary_con
    if rice_type == '99-25':
        prec = boundary_con.iloc[day - 1, 25]
        pet = boundary_con.iloc[day - 1, 15]
        hcrita = boundary_con.iloc[day - 1, 6]
        LAI = get_lai(rice_data, day)
        gwl = boundary_con.iloc[day - 1, 7]
        ctop = boundary_con.iloc[day - 1, 9]
        nine25_boundary_con = [prec, pet, hcrita, LAI, gwl, ctop, croot]
        return nine25_boundary_con
    if rice_type == 'NJ9108':
        prec = boundary_con.iloc[day - 1, 26]
        pet = boundary_con.iloc[day - 1, 16]
        hcrita = boundary_con.iloc[day - 1, 6]
        LAI = get_lai(rice_data, day)
        gwl = boundary_con.iloc[day - 1, 7]
        ctop = boundary_con.iloc[day - 1, 10]
        nj9108_boundary_con = [prec, pet, hcrita, LAI, gwl, ctop, croot]
        return nj9108_boundary_con


def initial_soil(rice_data, croot, day, rice_type, soil_zn, SELECTOR_IN_data=None, filedir=".\\hydrus20220228",
                 sprinkle_zn_today =None):
    # 获得根系深度
    # if SELECTOR_IN_data is None:
    #     SELECTOR_IN_data = [100, 150, 4.8, 0.62, 0.52, 0.5]
    root_uptake_index = cal_root_uptake_index(rice_data, day)
    # 获得边界条件
    boundary_con = get_boundary_con(day, rice_type, rice_data, croot=croot)
    # 建立文件夹
    hydrus_dir = filedir

    os.mkdir(hydrus_dir + "/" + str(day))
    # 从bylw2中把文件都拷贝过去
    for root, dirs, files in os.walk(".\\bylw2"):
        for file in files:
            source_file = os.path.join(root, file)
            root1 = hydrus_dir + "\\" + str(day)
            destination_file = os.path.join(root1, file)
            copyfile(source_file, destination_file)
    # print("已经转移文件：第{0}天".format(day))
    # 修改每天的LEVEL_01.DIR
    LEVEL_01_DIR = 'H:\\20220217bylw\\' + hydrus_dir[2:] + "\\" + str(day) + "\\LEVEL_01.DIR"
    with open(LEVEL_01_DIR, "w") as f:
        txt = 'H:\\20220217bylw\\' + hydrus_dir[2:] + "\\" + str(day)
        f.write(txt)
    # print("LEVEL_01.DIR修改完毕")
    # 开始修改输入数据
    # 需要修改的参数有ATMOSPH.IN、METEO.IN、SELECTOR.IN
    ATMOSPH_IN = hydrus_dir + "\\" + str(day) + "\\ATMOSPH.IN"
    prec = boundary_con[0]
    pet = boundary_con[1]
    lai = boundary_con[3]
    gwl = boundary_con[4]
    ctop = boundary_con[5]
    cbot = boundary_con[6]
    f = open(ATMOSPH_IN, 'r+')
    flist = f.readlines()
    # tAtm        Prec       rSoil       rRoot      hCritA          rB          hB          ht        tTop
    # tBot        Ampl        cTop        cBot   RootDepth
    # 其中需要修改的是
    flist[11] = '1          {0}         {1}         {2}      100000           0         {3}           0           0 ' \
                '          0           0           {4}       {5} \n'.format(
        str(prec), str(pet), str(lai), str(gwl), str(ctop), str(cbot))
    f.close()
    f = open(ATMOSPH_IN, 'w+')
    f.writelines(flist)
    f.close()
    # print("ATMOSPH_IN修改完毕")
    # 修改SELECTOR.IN
    # 其中需要修改的是
    # DisperL.(43), DifW(45), Ks, yita, Alfa(47), KM(60)
    # SELECTOR_IN_data = [100, 150, 15, 0.62, 0.62, 0.5]
    DisperL = round(SELECTOR_IN_data[0], 3)
    DifW = round(SELECTOR_IN_data[1], 3)
    Ks = round(SELECTOR_IN_data[2], 3)
    yita = round(SELECTOR_IN_data[3], 3)
    Alfa = round(SELECTOR_IN_data[4], 3)
    KM = round(SELECTOR_IN_data[5], 3)
    SELECTOR_IN = hydrus_dir + "\\" + str(day) + "\\SELECTOR.IN"
    f = open(SELECTOR_IN, 'r+')
    flist = f.readlines()
    flist[42] = '       1.45          {0}           0           0 \n'.format(str(DisperL))
    flist[44] = '        {0}           0 \n'.format(str(DifW))
    flist[
        46] = '       {0}           {1}         1          0           0           0           0           0           0           0           0           0           0        {2} \n'.format(
        str(Ks), str(yita), str(Alfa))
    flist[59] = '        1         0       {0}         0         f         1\n'.format(str(KM))
    f.close()
    f = open(SELECTOR_IN, 'w+')
    f.writelines(flist)
    f.close()
    # print("SELECTOR_IN修改完毕")

    if day == 1:
        # 初始化浓度
        # 前三层
        sorbed_c, liquid_c = cal_initial_zn_conc1(soil_zn=soil_zn, theta=0.3713, Kd=Ks, yita=yita)
        # 后面的
        sorbed_c0, liquid_c0 = cal_initial_zn_conc1(soil_zn=0, theta=0.3713, Kd=Ks, yita=yita)
        # 修改PROFILE.DAT
        Conc_list = []
        SorbedConc_list = []
        for i in range(101):
            if i < 7:
                Conc_list.append(liquid_c)
                SorbedConc_list.append(sorbed_c)
            else:
                Conc_list.append(liquid_c0)
                SorbedConc_list.append(sorbed_c0)

        PROFILE_DAT = hydrus_dir + "\\" + str(day) + "\\PROFILE.DAT"
        f = open(PROFILE_DAT, 'r+')
        flist = f.readlines()
        PROFILE_DAT_list = []
        for j in range(5, 106):
            daduan = flist[j].split()
            # print(daduan)
            PROFILE_DAT_list.append(daduan)
        PROFILE_DAT_df = pd.DataFrame(PROFILE_DAT_list)
        f.close()
        for datline in range(101):
            PROFILE_DAT_df.iloc[datline, 5] = root_uptake_index[datline]
            PROFILE_DAT_df.iloc[datline, 10] = Conc_list[datline]
            PROFILE_DAT_df.iloc[datline, 11] = SorbedConc_list[datline]
        # 保存为txt
        PROFILE_DAT_dftxtpath = hydrus_dir + "\\" + str(day) + "\\PROFILE_DAT_df.txt"
        PROFILE_DAT_df.to_csv(PROFILE_DAT_dftxtpath, header=False, index=False, sep='\t')
        time.sleep(0.2)
        ff = open(PROFILE_DAT_dftxtpath, 'r')
        fflist = ff.readlines()
        ff.close()
        f = open(PROFILE_DAT, 'w+')
        for j in range(5, 106):
            # print(j)
            flist[j] = fflist[j - 5]
        f.writelines(flist)
        f.close()
        # print("PROFILE.DAT修改完毕")


    else:
        # 从前一天的数据中获得浓度
        # print("需要修改数据")
        # 需要更新的是 水势、根系、Conc、SConc
        # print("读取Nod_Inf.out")
        Nod_Inf_out = hydrus_dir + "\\" + str(day - 1) + "\\Nod_Inf.out"
        f = open(Nod_Inf_out, 'r+')
        flist = f.readlines()
        nod_inf = []
        for j in range(123, 224):
            daduan = flist[j].split()
            nod_inf.append(daduan)
        f.close()
        nodes_out_df = pd.DataFrame(nod_inf)
        # print(nodes_out_df)
        Moisture = nodes_out_df.iloc[:, 3]
        h = nodes_out_df.iloc[:, [2]]
        Conc = nodes_out_df.iloc[:, [11]]
        SConc = nodes_out_df.iloc[:, [12]]
        # 检查是否需要增加锌含量
        if sprinkle_zn_today != 0:
            # 假设增加的锌均匀分布于前3cm土壤水中
            # 增加的量为mg/3cm3*含水率
            # 获得的量为
            Moisture_avg = (float(nodes_out_df.iloc[0, 3])+float(nodes_out_df.iloc[1, 3]))/2
            add_c = sprinkle_zn_today/(3*Moisture_avg)
            Conc.iloc[0,0] = float(Conc.iloc[0,0])+add_c
            Conc.iloc[1, 0] = float(Conc.iloc[1, 0]) + add_c
            pass
        else:
            pass


        # 修改PROFILE.DAT
        PROFILE_DAT = hydrus_dir + "\\" + str(day) + "\\PROFILE.DAT"
        f = open(PROFILE_DAT, 'r+')
        flist = f.readlines()
        PROFILE_DAT_list = []
        for j in range(5, 106):
            daduan = flist[j].split()
            # print(daduan)
            PROFILE_DAT_list.append(daduan)
        PROFILE_DAT_df = pd.DataFrame(PROFILE_DAT_list)
        f.close()
        for datline in range(101):
            PROFILE_DAT_df.iloc[datline, 2] = h.iloc[datline, 0]
            PROFILE_DAT_df.iloc[datline, 5] = root_uptake_index[datline]
            PROFILE_DAT_df.iloc[datline, 10] = Conc.iloc[datline, 0]
            PROFILE_DAT_df.iloc[datline, 11] = SConc.iloc[datline, 0]
        # 保存为txt
        PROFILE_DAT_dftxtpath = hydrus_dir + "\\" + str(day) + "\\PROFILE_DAT_df.txt"
        PROFILE_DAT_df.to_csv(PROFILE_DAT_dftxtpath, header=False, index=False, sep='\t')
        time.sleep(0.2)
        ff = open(PROFILE_DAT_dftxtpath, 'r')
        fflist = ff.readlines()
        ff.close()
        f = open(PROFILE_DAT, 'w+')
        for j in range(5, 106):
            # print(j)
            flist[j] = fflist[j - 5]
        f.writelines(flist)
        f.close()
        # print("PROFILE.DAT修改完毕")


def run_hydrus(filedir, day):
    h1ddir = 'H:\\20220217bylw\\' + filedir[2:] + "\\" + str(day)
    current_dir = os.getcwd()
    # print('current_dir:', current_dir)
    # print('h1ddir:', h1ddir)
    os.chdir(h1ddir)
    rc, out = subprocess.getstatusoutput(h1ddir + "\\H1D_CALC.EXE")
    time.sleep(0.1)
    os.chdir(current_dir)
    pass


def get_output(filedir, day):
    # 需要提取的结果有：每天各土壤深度的溶液、固相、总土壤浓度；每天植物对锌的吸收量
    # print("读取Nod_Inf.out的数据")
    Nod_Inf_out = filedir + "\\" + str(day) + "\\Nod_Inf.out"
    f = open(Nod_Inf_out, 'r+')
    flist = f.readlines()
    nod_inf = []
    for j in range(123, 224):
        daduan = flist[j].split()
        nod_inf.append(daduan)
    f.close()
    nodes_out_df = pd.DataFrame(nod_inf)
    # print(nodes_out_df)
    h = nodes_out_df.iloc[:, [2]]
    Moisture = nodes_out_df.iloc[:, 3].tolist()
    Conc = nodes_out_df.iloc[:, 11].tolist()
    SConc = nodes_out_df.iloc[:, 12].tolist()
    conc_array = [Conc, SConc, Moisture]
    # 读取溶质吸收的量
    solute1_out = filedir + "\\" + str(day) + "\\solute1.out"
    f = open(solute1_out, 'r+')
    flist = f.readlines()
    f.close()
    solute_uptake = flist[-2].split()[11]
    return [solute_uptake, conc_array]
    pass


def get_intial_conc(filedir):
    # print("读取Nod_Inf.out的数据")
    Nod_Inf_out = filedir + "\\" + str(1) + "\\Nod_Inf.out"
    f = open(Nod_Inf_out, 'r+')
    flist = f.readlines()
    nod_inf = []
    for j in range(13, 114):
        daduan = flist[j].split()
        nod_inf.append(daduan)
    f.close()
    nodes_out_df = pd.DataFrame(nod_inf)
    # print(nodes_out_df)
    h = nodes_out_df.iloc[:, [2]]
    Moisture = nodes_out_df.iloc[:, 3].tolist()
    Conc = nodes_out_df.iloc[:, 11].tolist()
    SConc = nodes_out_df.iloc[:, 12].tolist()
    conc_array = [Conc, SConc, Moisture]
    return conc_array


# if __name__ == "__main__":
#     ricetype = 'hhz'
#     # 测试根系吸水
#     # rice_data = wofost.run_wofost(ricetype='hhz', day_length=108)
#     # print(rice_data.iloc[0,9])
#     # root_uptake_index = cal_root_uptake_index(rice_data, day=30)
#     # print(root_uptake_index)
#     # 测试边界条件
#     # get_boundary_con(day=1, rice_type='hhz', rice_data=rice_data, croot=0.001)
#     SELECTOR_IN_data = [100, 150, 4.8, 0.62, 0.52, 0.5]
#     # initial_soil(rice_data, croot=0.001, day=1, rice_type='hhz', soil_zn=1,SELECTOR_IN_data=None, filedir=".\\hydrus20220228")
#     mass = cal_massconc(0.0287227818248161, 0.0967573411084458)
#
#     mass = cal_massconc(0.02861, 0.0968)
#     print(mass)
#
#     pass

def read_sumZnbot(file_dir , day):
    solute1_out = file_dir + "\\" + str(day) + "\\solute1.out"
    f = open(solute1_out, 'r+')
    flist = f.readlines()
    sumZnbot = flist[-2].split()[4]
    return float(sumZnbot)


if __name__ == '__main__':
    file_dir = ".\\hydrus20220306"
    day = 1
    read_sumZnbot(file_dir, day)