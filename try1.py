import os
import shutil
from shutil import copyfile
import time
import subprocess
import numpy as np
import pandas as pd
from scipy import integrate


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




hydrus_dir = ".\\hydrus"
if os.path.exists(hydrus_dir):
    shutil.rmtree(hydrus_dir)
time.sleep(0.5)
os.mkdir(hydrus_dir)

day_length = 5
# ATMOSPH.IN数据，即边界条件
boundry_df = pd.read_csv('hydrusnj9108输入.csv')
print(boundry_df)
# SELECTOR.IN数据，即方程参数
# 为 DisperL.(43),DifW(45),Ks,Beta,Alfa(47),KM(60)
SELECTOR_IN_data = [10, 0.6, 0.087, 0.25, 0.62, 0.5]
# 读取根系长度
with open("rootdepth.txt", "r") as f:
    data = f.readlines()
    newdata = []
    for line in data:
        newdata.append(float(line.strip('\n')))
    # print(newdata)
root_depth = []
for new in newdata:
    new = new - new % 3 + 3
    root_depth.append(new)
# print(root_depth)
root_beta_list = []
for depth in root_depth:
    # print(depth)
    node_num = int(depth / 3 - 3)
    input_node_list = [9]
    for i in range(0, node_num):
        input_node_list.append(12 + 3 * i)
    # print(input_node_list)
    i_list = []
    for i in input_node_list:
        v = water_extraction(z=i, lr=depth - 9, lrs=9)
        i_list.append(v)
    # print(i_list)
    newi_list = [0, 0, 0]

    for i in i_list:
        newi_list.append(round(i, 8))
    num = 101 - len(newi_list)
    for i in range(0, num):
        newi_list.append(0)
    max_i = max(newi_list)
    ii_list = []
    for newi in newi_list:
        newi = round(newi * (1 / max_i), 8)
        ii_list.append(newi)

    root_beta_list.append(ii_list)

root_beta_df = pd.DataFrame(root_beta_list)
# print(root_beta_df)



for i in range(1, day_length + 1):
    os.mkdir(hydrus_dir + "/" + str(i))
    # 从bylw2中把文件都拷贝过去
    for root, dirs, files in os.walk(".\\bylw2"):
        for file in files:
            source_file = os.path.join(root, file)
            root1 = ".\\hydrus" + "\\" + str(i)
            destination_file = os.path.join(root1, file)
            copyfile(source_file, destination_file)
    print("已经转移文件：第{0}天".format(i))
    # 修改每天的LEVEL_01.DIR
    LEVEL_01_DIR = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\LEVEL_01.DIR"
    with open(LEVEL_01_DIR, "w") as f:
        txt = r"H:\20220217bylw\hydrus" + "\\" + str(i)
        f.write(txt)
    print("LEVEL_01.DIR修改完毕")
    # 开始修改数据
    # 需要修改的参数有ATMOSPH.IN、METEO.IN、SELECTOR.IN
    # 修改ATMOSPH.IN
    ATMOSPH_IN_data = boundry_df.loc[i - 1]
    # print(ATMOSPH_IN_data)
    # Prec, pET, hcrita, rRoot, hB, cTop, cBot
    # 要改的参数：Prec;rSoil;rRoot;hB;cTop;cBot
    # 实际对应：  Prec;pET;  LAI;  GWL;cTop;cRoot
    prec = round(ATMOSPH_IN_data[0], 3)
    pet = round(ATMOSPH_IN_data[1], 3)
    lai = round(ATMOSPH_IN_data[3], 3)
    gwl = round(ATMOSPH_IN_data[4], 3)
    ctop = round(ATMOSPH_IN_data[5], 3)
    cbot = round(ATMOSPH_IN_data[6], 3)
    ATMOSPH_IN = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\ATMOSPH.IN"
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
    print("ATMOSPH_IN修改完毕")

    # 修改SELECTOR.IN
    # 其中需要修改的是
    # DisperL.(43), DifW(45), Ks, Beta, Alfa(47), KM(60)
    # SELECTOR_IN_data = [10, 0.5, 0.87, 0.25, 0.62, 0.5]
    DisperL = round(SELECTOR_IN_data[0], 3)
    DifW = round(SELECTOR_IN_data[1], 3)
    Ks = round(SELECTOR_IN_data[2], 3)
    Beta = round(SELECTOR_IN_data[3], 3)
    Alfa = round(SELECTOR_IN_data[4], 3)
    KM = round(SELECTOR_IN_data[5], 3)
    SELECTOR_IN = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\SELECTOR.IN"
    f = open(SELECTOR_IN, 'r+')
    flist = f.readlines()
    flist[42] = '       1.45          {0}           0           0 \n'.format(str(DisperL))
    flist[44] = '        {0}           0 \n'.format(str(DifW))
    flist[
        46] = '       {0}           0        {1}           0           0           0           0           0           0           0           0           0           0        {2} \n'.format(
        str(Ks), str(Beta), str(Alfa))
    flist[59] = '        1         0       {0}         0         f         1\n'.format(str(KM))
    f.close()
    f = open(SELECTOR_IN, 'w+')
    f.writelines(flist)
    f.close()
    print("SELECTOR_IN修改完毕")

    # 更新数据
    if i != 1:
        print("需要修改数据")
        # 需要更新的是 水势、根系、Conc、SConc
        # 运行完毕，获得输出
        # 水势是124-224
        print("读取Nod_Inf.out")
        Nod_Inf_out = r"H:\20220217bylw\hydrus" + "\\" + str(i-1) + "\\Nod_Inf.out"
        f = open(Nod_Inf_out, 'r+')
        flist = f.readlines()
        nod_inf = []
        for j in range(123, 224):
            daduan = flist[j].split()
            nod_inf.append(daduan)
        f.close()
        # print(daduan)
        nodes_out = nod_inf
        nodes_out_df = pd.DataFrame(nodes_out)
        print(nodes_out_df)
        h = nodes_out_df.iloc[:, [2]]
        Conc = nodes_out_df.iloc[:, [11]]
        root_beta = list(root_beta_df.iloc[i - 1])
        SConc = nodes_out_df.iloc[:, [12]]
        # 修改PROFILE.DAT
        PROFILE_DAT = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\PROFILE.DAT"
        f = open(PROFILE_DAT, 'r+')
        flist = f.readlines()
        PROFILE_DAT_list = []
        for j in range(5, 106):
            daduan = flist[j].split()
            # print(daduan)
            PROFILE_DAT_list.append(daduan)
        PROFILE_DAT_df = pd.DataFrame(PROFILE_DAT_list)
        f.close()
        # print(h.iloc[0, 0])
        # print(h.iloc[2, 0])
        for datline in range(101):
            PROFILE_DAT_df.iloc[datline, 2] = h.iloc[datline, 0]
            PROFILE_DAT_df.iloc[datline, 5] = root_beta[datline]
            PROFILE_DAT_df.iloc[datline, 10] = Conc.iloc[datline, 0]
            PROFILE_DAT_df.iloc[datline, 11] = SConc.iloc[datline, 0]

        PROFILE_DAT_dftxtpath = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\PROFILE_DAT_df.txt"

        PROFILE_DAT_df.to_csv(PROFILE_DAT_dftxtpath, header=False, index=False, sep='\t')
        time.sleep(0.2)
        PROFILE_DAT_dftxtpath = r"H:\20220217bylw\hydrus" + "\\" + str(i) + "\\PROFILE_DAT_df.txt"
        ff = open(PROFILE_DAT_dftxtpath, 'r')
        fflist = ff.readlines()
        ff.close()
        f = open(PROFILE_DAT, 'w+')
        for j in range(5, 106):
            # print(j)
            flist[j] = fflist[j - 5]

        f.writelines(flist)
        f.close()
        print("PROFILE.DAT修改完毕")

    # 运行主程序
    h1ddir = "H:\\20220217bylw\hydrus" + "\\" + str(i)
    current_dir = os.getcwd()
    print('current_dir:', current_dir)
    print('h1ddir:', h1ddir)
    os.chdir(h1ddir)
    # return_value = os.system(h1ddir+"\\H1D_CALC.EXE")
    rc, out = subprocess.getstatusoutput(h1ddir + "\\H1D_CALC.EXE")
    time.sleep(0.4)
    os.chdir(current_dir)


