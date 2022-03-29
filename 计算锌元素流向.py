import pandas as pd
import numpy as np

def cal_addzn(field_name):
    soil3 = ['2','8','13_1','13_2','13_3','13_4']
    soil2 = ['3','9','14']
    soil1 = ['5','11']
    soil0 = ['1','4','6','7','10','12']
    sprinkle0 =['4','7','10','13_1']

    # 不同锌肥种类的利用效率
    znsofer = 0.13
    edtaznfer = 0.05
    saznfer = 0.23

    if field_name in soil0:
        zn = 0
        soilzn = 0
    elif field_name in soil1:
        zn = 1*1000000/(666.67*10000)
        soilzn = 1
    elif field_name in soil2:
        zn = 2*1000000/(666.67*10000)
        soilzn = 2
    elif field_name in soil3:
        zn = 3*1000000/(666.67*10000)
        soilzn = 3

    if field_name in sprinkle0:
        szn = 0
        sprinkle = 0
    elif field_name == '13_3':
        szn = 210*1000*(1-edtaznfer)/(666.67*10000)
        sprinkle = 3
    elif field_name == '13_4':
        szn = 210*1000*(1-saznfer)/(666.67*10000)
        sprinkle = 3
    else:
        szn = 210*1000*(1-znsofer)/(666.67*10000)
        sprinkle = 3


    return zn+szn,soilzn,sprinkle



if __name__ == '__main__':
    field_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13_1', '13_2', '13_3', '13_4',
                  '14']
    result_list = []
    for field in field_list:

        field_name = field
        zn_initial = 73.33

        soil_init_zn = zn_initial * 300 * 1.45 / 1000  # mg
        # print('原始土壤锌含量{}'.format(soil_init_zn))
        # 计算下边界流出量
        # 读取文件
        sumbot = pd.read_csv('main_result/field' + field_name + '_sumZnbotdata.csv')
        sumbot_flow = sumbot.iloc[-1, 2]

        # print('下边界流出锌含量{}'.format(sumbot_flow))

        # 读取土壤锌含量文件
        soil = pd.read_csv('main_result/field' + field_name + '_soildata.csv')
        soilznlist = soil.iloc[:, -1].tolist()
        # print(soil)
        # print(soilznlist)
        # 计算锌含量
        soilzncontent = 0
        # print(len(soilznlist))
        for i in range(len(soilznlist) - 1):
            soilzncontent += (soilznlist[i]+soilznlist[i+1]) * 3 * 1.45 / (2*1000)
        # print('土壤锌含量为{}'.format(soilzncontent))

        # 计算植株的锌含量
        znplant = pd.read_csv('main_result/field' + field_name + '_zndata.csv')
        # print(znplant)
        # 提取两部分的量，穗、总吸收
        allplantzn = znplant.iloc[:, 11].tolist()
        allplantzn = sum(allplantzn) / 100000000
        # print('植物吸收的锌含量{}'.format(allplantzn))

        allricezn = znplant.iloc[-1, 8]
        allricezn = allricezn / 100000000
        # print('穗的锌含量{}'.format(allricezn))

        addzn,soilzn,sprinklezn = cal_addzn(field_name)
        # print('施锌量{}'.format(addzn))

        mass_balance = soil_init_zn + addzn + sumbot_flow - allplantzn - soilzncontent
        # print(mass_balance)

        result = [field_name,soil_init_zn,sumbot_flow,soilzncontent,allplantzn,allricezn,addzn,mass_balance,soilzn,sprinklezn]
        result_list.append(result)
    result_df = pd.DataFrame(result_list)
    result_df.columns = ['field_name','soil_init_zn','sumbot_flow','soilzncontent','allplantzn','allricezn',
                         'addzn','mass_balance','soilzn','sprinklezn']
    print(result_df)
    result_df.to_csv('main_result/mass_balance.csv',index=False)