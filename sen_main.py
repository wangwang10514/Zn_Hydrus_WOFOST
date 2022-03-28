import os
import shutil
from shutil import copyfile
import time
import subprocess
import numpy as np
import pandas as pd
from SALib.sample import saltelli
from SALib.analyze import sobol
import tqdm

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





def change_croot(croot,df):
    df[6] = croot
    return df



def change_root_depth2beta(filepath="rootdepth.txt"):
    with open(filepath, "r") as f:
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
    return root_beta_list




# print(root_beta_df)


def run_hydrus_sensitive(day_length=1 , goaldir_name='hydrus_sensi', fromdir=".\\bylw2",
               boundry_df = None, SELECTOR_IN_data=None):
    hydrus_dir = ".\\" + goaldir_name
    try:
        if os.path.exists(hydrus_dir):
            shutil.rmtree(hydrus_dir)
        time.sleep(0.6)
        os.mkdir(hydrus_dir)
    except:
        time.sleep(10)
        if os.path.exists(hydrus_dir):
            shutil.rmtree(hydrus_dir)
        time.sleep(0.6)
        os.mkdir(hydrus_dir)


    for i in range(1, day_length + 1):
        os.mkdir(hydrus_dir + "/" + str(i))
        # 从bylw2中把文件都拷贝过去
        for root, dirs, files in os.walk(fromdir):
            for file in files:
                source_file = os.path.join(root, file)
                root1 = hydrus_dir + "\\" + str(i)
                destination_file = os.path.join(root1, file)
                copyfile(source_file, destination_file)
        print("已经转移文件：第{0}天".format(i))
        # 修改每天的LEVEL_01.DIR
        LEVEL_01_DIR = r"H:\20220217bylw\\" + goaldir_name + "\\" + str(i) + "\\LEVEL_01.DIR"
        with open(LEVEL_01_DIR, "w") as f:
            txt = r"H:\20220217bylw\\"+goaldir_name + "\\" + str(i)
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
        ATMOSPH_IN = r"H:\20220217bylw\\"+goaldir_name + "\\" + str(i) + "\\ATMOSPH.IN"
        f = open(ATMOSPH_IN, 'r+')
        flist = f.readlines()
        # tAtm        Prec       rSoil       rRoot      hCritA          rB          hB          ht        tTop
        # tBot        Ampl        cTop        cBot   RootDepth
        # 其中需要修改的是
        flist[
            11] = '1          {0}         {1}         {2}      100000           0         {3}           0           0 ' \
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
        SELECTOR_IN = r"H:\20220217bylw\\"+goaldir_name + "\\" + str(i) + "\\SELECTOR.IN"
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



    # 运行主程序
    h1ddir = "H:\\20220217bylw\\"+goaldir_name + "\\" + str(i)
    current_dir = os.getcwd()
    print('current_dir:', current_dir)
    print('h1ddir:', h1ddir)
    os.chdir(h1ddir)
    # return_value = os.system(h1ddir+"\\H1D_CALC.EXE")
    rc, out = subprocess.getstatusoutput(h1ddir + "\\H1D_CALC.EXE")
    time.sleep(0.4)
    os.chdir(current_dir)


def get_putput(dir):
    # 需要获得20cm处的溶质溶度	40cm处的溶质溶度	60cm处的溶质溶度	100cm处的溶质溶度	根系吸收溶质的速率	根系吸收溶质的量
    # ---------获得溶质浓度------------
    solut_path=  dir+"\\Nod_Inf.out"
    f = open(solut_path, 'r+')
    flist = f.readlines()
    f.close()
    result = []
    for j in range(123,224):
        result.append(flist[j].split())
    result = pd.DataFrame(result)
    solute_result = []
    for step in range(0,7):
        solute_result.append(result.iloc[step,11])
        solute_result.append(result.iloc[step, 12])

    root_uptake_path =  dir+"\\solute1.out"
    f = open(root_uptake_path, 'r+')
    flist = f.readlines()
    f.close()
    root_uptake_result = flist[-2].split()
    solute_result.append(root_uptake_result[10])
    solute_result.append(root_uptake_result[11])
    return solute_result


if __name__ == "__main__":
    problem = {'num_vars': 7,
               'names': ['disp', 'diffus', 'kd', 'beta', 'alpha', 'km', 'croot'],
               'bounds': [[0.1, 0.5],
                          [0.1, 0.2],
                          [0.7, 0.9],
                          [0.2, 0.3],
                          [0.3, 0.7],
                          [0.005, 0.5],
                          [0.0005, 0.005]]
               }
    # problem = {'num_vars': 3,
    #            'names': ['disp', 'diffus', 'kd', 'beta', 'alpha', 'km', 'croot'],
    #            'bounds': [
    #                       [0.7, 0.9],
    #                       [0.2, 0.3],
    #                       [0.3, 0.7]]
    #            }
    # problem = {'num_vars': 4,
    #            'names': ['disp', 'diffus',  'croot', 'km'],
    #            'bounds': [[0.1, 0.5],
    #                       [0.1, 0.2],
    #                       [0.0005, 0.005],
    #                       [0.005, 0.5]]
    #            }
    param_values = saltelli.sample(problem, 70)
    shouji = []
    for num_list in tqdm.tqdm(range(len(param_values))):
        iii = param_values[num_list]
        print(iii)

        # ----------只运行1天-------------
        day_length = 1
        goaldir_name = 'hydrus_sensi'
        # ATMOSPH.IN数据，即边界条件
        boundry_df = [0.74, 0.500060016, 100000, 0.091017526, 61.6177092, 0, 0.001]
        # SELECTOR.IN数据，即方程参数
        # 为 DisperL.(43),DifW(45),Ks,Beta,Alfa(47),KM(60)
        SELECTOR_IN_data = [0.5, 0.1, 0.87, 0.25, 0.62, 0.5]

        SELECTOR_IN_data = [float(iii[0]),float(iii[1]), float(iii[2]),float(iii[3]),float(iii[4]), float(iii[5])]
        croot = float(iii[6])

        # SELECTOR_IN_data = [0.5, 0.1,float(iii[0]),float(iii[1]), float(iii[2]), 0.5]
        # croot = 0.001

        boundry_df = change_croot(croot, boundry_df)
        # Prec, pET, hCritA, LAI, GWL, cTop, croot
        boundry_df = pd.DataFrame({'Prec': [ boundry_df[0]],
                                   'pET': [boundry_df[1]],
                                   'hCritA': [boundry_df[2]],
                                   'LAI': [boundry_df[3]],
                                   "GWL": [boundry_df[4]],
                                   "cTop": [boundry_df[5]],
                                   "croot": [boundry_df[6]]
                                   })
        # root_beta_df = pd.DataFrame(change_root_depth2beta(filepath="rootdepth.txt"))
        run_hydrus_sensitive(day_length=1, goaldir_name=goaldir_name, fromdir=".\\bylw2",
                             boundry_df=boundry_df, SELECTOR_IN_data=SELECTOR_IN_data)
        time.sleep(0.5)
        dir = goaldir_name+"\\"+str(day_length)
        try:
            result = get_putput(dir)
            print(result)
            shouji.append(result)
            shouji_df = pd.DataFrame(shouji)
            shouji_df.to_csv("shouji_dfd100h-100.csv",index=False)
        except:
            # dir = goaldir_name + "\\" + str(day_length)
            # result = get_putput(dir)
            # print(result)
            # shouji.append(result)
            # shouji_df = pd.DataFrame(shouji)
            # shouji_df.to_csv("shouji_dfd100h0.csv", index=False)
            print('IndexError: list index out of range')








