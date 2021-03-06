from scipy import interpolate
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class Zninrice():
    def __init__(self, ricetype=None, ricedata=None, day_length=None, field=None):
        # 将锌含量的需求划分为 返青、分蘖、拔节、扬花、灌浆5个阶段
        self.SUMTDZA = 0
        self.SUMZ = 0
        self.SUMTZA = 0
        self.day = 1
        self.ZART = 0
        self.ZAST = 0
        self.ZALF = 0
        self.ZAER = 0
        grow_inf = self.get_para2(field=field)
        self.blossom = grow_inf[0]

        data_name_list = [grow_inf[1], grow_inf[2], grow_inf[3], grow_inf[4],
                          grow_inf[5], grow_inf[6], grow_inf[7], grow_inf[8],
                          grow_inf[9], grow_inf[10], grow_inf[11], grow_inf[12]]
        self.data_list = []
        for i in data_name_list:
            self.data_list.append(self.newtrantable(i))

        # 生长数据表
        hhz_df = ricedata
        # 只取104天的数据表
        hhz_df104 = hhz_df.iloc[0:day_length]
        # hhz_df104['WST'] = hhz_df104.loc[:, 'TWST'] - hhz_df104.loc[:, 'DWST']
        # hhz_df104['WRT'] = hhz_df104.loc[:, 'TWRT'] - hhz_df104.loc[:, 'DWRT']
        # 计算生长速率表
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'TWRT', 'dTWRT', day_length)
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'TWST', 'dTWST', day_length)
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'TWLV', 'dTWLV', day_length)
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'TWSO', 'dTWSO', day_length)
        # 计算死亡速率表
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'DWRT', 'dDWRT', day_length)
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'DWST', 'dDWST', day_length)
        hhz_df104 = self.cal_growth_rate(hhz_df104, 'DWLV', 'dDWLV', day_length)
        # 干物质量表
        self.WRTT = np.array(hhz_df104['WRT'])
        self.WSTT = np.array(hhz_df104['WST'])
        self.WLFT = np.array(hhz_df104['WLV'])
        self.WERT = np.array(hhz_df104['TWSO'])
        # 生长速率表
        self.GRTT = np.array(hhz_df104['dTWRT'])
        self.GSTT = np.array(hhz_df104['dTWST'])
        self.GLFT = np.array(hhz_df104['dTWLV'])
        self.GERT = np.array(hhz_df104['dTWSO'])
        # 死亡速率表
        self.DRTT = np.array(hhz_df104['dDWRT'])
        self.DSTT = np.array(hhz_df104['dDWST'])
        self.DLFT = np.array(hhz_df104['dDWLV'])

    def get_para2(self, field):
        rice_process = {
            'hhz': [1, 8, 29, 70, 75, 108],
            '99-25': [1, 8, 29, 79, 87, 147],
            'NJ9108': [1, 8, 28, 80, 88, 147]
        }
        rice_zn_need = {
            'hhz': [[10, 25, 25, 40, 20, 20],
                    [10, 25, 25, 40, 20, 20],
                    [25, 25, 25, 25, 25, 25],
                    [20, 20, 20, 20, 20, 20],
                    [200, 200, 300, 300, 200, 100],
                    [200, 200, 200, 200, 200, 100],
                    [150, 150, 150, 100, 100, 50],
                    [100, 100, 100, 100, 100, 100],
                    [0.05, 0.05, 0.05, 0.05, 0.05, 0.0],
                    [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                    [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                    [0, 0, 0, 0, 0, 0]],
            '99-25': [[10, 25, 25, 40, 20, 20],
                      [10, 25, 25, 40, 20, 20],
                      [25, 25, 25, 25, 25, 25],
                      [20, 20, 20, 20, 20, 20],
                      [200, 200, 300, 300, 200, 100],
                      [200, 200, 200, 200, 200, 100],
                      [150, 150, 150, 100, 100, 50],
                      [120, 120, 120, 120, 120, 120],
                      [0.05, 0.05, 0.05, 0.05, 0.05, 0.0],
                      [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                      [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                      [0, 0, 0, 0, 0, 0]],
            'NJ9108': [[10, 25, 25, 40, 20, 20],
                       [10, 25, 25, 40, 20, 20],
                       [25, 25, 25, 25, 25, 25],
                       [20, 20, 20, 20, 20, 20],
                       [200, 200, 300, 300, 200, 100],
                       [200, 200, 200, 200, 200, 100],
                       [150, 150, 150, 100, 100, 50],
                       [150, 150, 150, 150, 150, 150],
                       [0.05, 0.05, 0.1, 0.1, 0.05, 0.0],
                       [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                       [0.01, 0.2, 0.1, 0.05, 0.04, 0.0],
                       [0, 0, 0, 0, 0, 0]],
        }

        if field in ['1', '10', '13_1', '13_2', '13_3', '13_4', '14']:
            rice_type = 'NJ9108'
            blossom_date = rice_process[rice_type][3]
            MIZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
            MIZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
            MIZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
            MIZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
            MXZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
            MXZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
            MXZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
            MXZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
            FRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
            FSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
            FLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
            FERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
        if field in ['2', '3', '4', '5', '6']:
            rice_type = 'hhz'
            blossom_date = rice_process[rice_type][3]
            MIZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
            MIZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
            MIZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
            MIZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
            MXZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
            MXZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
            MXZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
            MXZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
            FRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
            FSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
            FLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
            FERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
        if field in ['7', '8', '9', '11', '12']:
            rice_type = '99-25'
            blossom_date = rice_process[rice_type][3]
            MIZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][0])
            MIZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][1])
            MIZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][2])
            MIZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][3])
            MXZRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][4])
            MXZSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][5])
            MXZLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][6])
            MXZERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][7])
            FRTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][8])
            FSTT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][9])
            FLFT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][10])
            FERT = self.cal_table(date=rice_process[rice_type], value=rice_zn_need[rice_type][11])
        return [blossom_date, MIZRTT, MIZSTT, MIZLFT, MIZERT, MXZRTT, MXZSTT, MXZLFT, MXZERT, FRTT, FSTT, FLFT, FERT]

    def cal_table(self, date, value):
        table = []
        datenum = len(date)
        for i in range(datenum):
            table.append([date[i], value[i]])
        return table
        pass

    def run_oneday1(self):
        # ----------------------------状态变量----------------------
        # 第几天

        # 当前器官实际含锌量

        self.TZA = self.ZART + self.ZAST + self.ZALF + self.ZAER

        # ----------------------------速率变量-------------------------
        # 计算最小需求锌浓度mg*kg-1
        self.MIZRT = self.data_list[0][self.day - 1]
        self.MIZST = self.data_list[1][self.day - 1]
        self.MIZLF = self.data_list[2][self.day - 1]
        self.MIZER = self.data_list[3][self.day - 1]

        # 计算最大需求锌浓度mg*kg-1
        self.MXZRT = self.data_list[4][self.day - 1]
        self.MXZST = self.data_list[5][self.day - 1]
        self.MXZLF = self.data_list[6][self.day - 1]
        self.MXZER = self.data_list[7][self.day - 1]
        # 当天死亡器官量
        self.DRT = self.DRTT[self.day - 1]
        self.DST = self.DSTT[self.day - 1]
        self.DLF = self.DLFT[self.day - 1]
        # ----------------------------状态变量----------------------
        # 各器官当前干物质量 kg*ha-1(一天结束后在死亡)
        self.WRT = self.WRTT[self.day - 1] + self.DRT
        self.WST = self.WSTT[self.day - 1] + self.DST
        self.WLF = self.WLFT[self.day - 1] + self.DLF
        self.WER = self.WERT[self.day - 1]

        # 计算锌最小需求量
        self.ZDMIRT, self.ZDMIST, self.ZDMILF, self.ZDMIER = self.cal_ZDMI(self.day, self.blossom, self.MIZRT,
                                                                           self.MIZST, self.MIZLF, self.MIZER,
                                                                           self.WRT, self.WST, self.WLF,
                                                                           self.WER, self.ZART, self.ZAST, self.ZALF,
                                                                           self.ZAER)
        # 认为锌不在第一次吸收阶段获取
        self.TZDMI = self.ZDMIRT + self.ZDMIST + self.ZDMILF + self.ZDMIER
        self.TZDMIdistri1 = self.ZDMIRT + self.ZDMIST + self.ZDMILF
        # 计算锌最大需求量
        self.ZDMXRT = max(0, self.MXZRT * self.WRT - self.ZART)
        self.ZDMXST = max(0, self.MXZST * self.WST - self.ZAST)
        self.ZDMXLF = max(0, self.MXZLF * self.WLF - self.ZALF)
        self.ZDMXER = max(0, self.MXZER * self.WER - self.ZAER)

        self.TZDMX = self.ZDMXRT + self.ZDMXST + self.ZDMXLF + self.ZDMXER
        self.TZDMXdistri2 = self.ZDMXRT + self.ZDMXST + self.ZDMXLF

        # 计算最小锌需求的分配系数Fraction1
        self.FZRT1 = self.cal_massfraction(self.ZDMIRT, self.TZDMIdistri1)
        self.FZST1 = self.cal_massfraction(self.ZDMIST, self.TZDMIdistri1)
        self.FZLF1 = self.cal_massfraction(self.ZDMILF, self.TZDMIdistri1)
        self.FZER1 = 0
        self.TFZ1 = self.FZRT1 + self.FZST1 + self.FZLF1 + self.FZER1
        # 基于最大锌需求量的Fraction2
        self.FZRT4 = self.cal_massfraction(self.ZDMXRT - self.ZDMIRT, self.TZDMX - self.TZDMI)
        self.FZST4 = self.cal_massfraction(self.ZDMXST - self.ZDMIST, self.TZDMX - self.TZDMI)
        self.FZLF4 = self.cal_massfraction(self.ZDMXLF - self.ZDMILF, self.TZDMX - self.TZDMI)
        self.FZER4 = self.cal_massfraction(self.ZDMXER - self.ZDMIER, self.TZDMX - self.TZDMI)
        self.TFZ2 = self.FZRT4 + self.FZST4 + self.FZLF4
        self.FZRT2 = self.cal_massfraction(self.FZRT4, self.TFZ2)
        self.FZST2 = self.cal_massfraction(self.FZST4, self.TFZ2)
        self.FZLF2 = self.cal_massfraction(self.FZLF4, self.TFZ2)

    def cal_croot(self):
        croot = self.TZDMX - self.TZA
        return croot
        pass

    def update_ZUN(self, zn):
        self.ZU = float(zn) * 100000000

    def run_oneday2(self):
        # 开始进行分配
        self.ZU1 = min(self.ZU, self.TZDMIdistri1)
        self.ZURT = self.ZU1 * self.FZRT1
        self.ZUST = self.ZU1 * self.FZST1
        self.ZULF = self.ZU1 * self.FZLF1
        self.ZUER = 0
        # 锌盈余
        self.ZSU = max(0, self.ZU - self.TZDMIdistri1)
        # 二阶段分配
        self.ZSURT = self.ZSU * self.FZRT2
        self.ZSUST = self.ZSU * self.FZST2
        self.ZSULF = self.ZSU * self.FZLF2
        self.ZSUER = 0
        # 通过锌吸收的含量
        self.ZRT = self.ZURT + self.ZSURT
        self.ZST = self.ZUST + self.ZSUST
        self.ZLF = self.ZULF + self.ZSULF
        self.ZER = self.ZUER + self.ZSUER
        # 锌吸收的质量平衡
        self.ZU_BALANCE = self.ZU - self.ZRT - self.ZST - self.ZLF - self.ZER

        self.ZART1 = self.ZART + self.ZRT
        self.ZAST1 = self.ZAST + self.ZST
        self.ZALF1 = self.ZALF + self.ZLF
        self.ZAER1 = self.ZAER + self.ZER

        # 根系吸收后的最小锌含量需求
        # 还需要的锌需要通过转运方式获得
        self.ZDURT, self.ZDUST, self.ZDULF, self.ZDUER = self.cal_ZDU(self.day, self.blossom, self.ZDMIRT,
                                                                      self.ZDMIST, self.ZDMILF,
                                                                      self.ZDMIER, self.ZART1, self.ZAST1, self.ZALF1,
                                                                      self.ZAER1)
        self.TZDU = self.ZDURT + self.ZDUST + self.ZDULF + self.ZDUER

        # 基于转运需求量的Fraction3
        self.FZRT3 = self.cal_massfraction(self.ZDURT, self.TZDU)
        self.FZST3 = self.cal_massfraction(self.ZDUST, self.TZDU)
        self.FZLF3 = self.cal_massfraction(self.ZDULF, self.TZDU)
        self.FZER3 = self.cal_massfraction(self.ZDUER, self.TZDU)

        # 如果信息收之后没有分配的需求
        # 锌的主动吸收分配系数等于0
        # 除去死亡的叶片，总是在死亡时转运一些
        self.FRT = self.data_list[8][self.day - 1]
        self.FST = self.data_list[9][self.day - 1]
        self.FLF = self.data_list[10][self.day - 1]
        self.FER = self.data_list[11][self.day - 1]

        # 开始转运
        # 各器官的可转运锌量
        self.TRZRT = max(0, self.ZART + self.ZRT - self.ZDMIRT) * self.FRT
        self.TRZST = max(0, self.ZAST + self.ZST - self.ZDMIST) * self.FST
        self.TRZLF = max(0, self.ZALF + self.ZLF - self.ZDMILF) * self.FLF
        self.TRZER = 0

        # 总可转运锌量
        self.TTRZ = self.TRZRT + self.TRZST + self.TRZLF
        # 总转运锌量
        self.TTRZ1 = min(self.TTRZ, self.TZDU)
        # 第三阶段的分配
        self.TZPRT = self.FZRT3 * self.TTRZ1
        self.TZPST = self.FZST3 * self.TTRZ1
        self.TZPLF = self.FZLF3 * self.TTRZ1
        self.TZPER = self.FZER3 * self.TTRZ1
        self.TTZP = self.TZPRT + self.TZPST + self.TZPLF + self.TZPER

        # 多余的分配锌
        self.STTRZ = max(0, self.TTRZ - self.TZDU)

        # 多余的分配锌再分配
        self.TSZPRT = self.FZRT4 * self.STTRZ
        self.TSZPST = self.FZST4 * self.STTRZ
        self.TSZPLF = self.FZLF4 * self.STTRZ
        self.TSZPER = self.FZER4 * self.STTRZ
        self.TTSZP = self.TSZPRT + self.TSZPST + self.TSZPLF + self.TSZPER

        # 观测值
        # 更新锌含量
        self.NZURT = self.ZURT + self.ZSURT - self.TRZRT + self.TZPRT + self.TSZPRT
        self.NZUST = self.ZUST + self.ZSUST - self.TRZST + self.TZPST + self.TSZPST
        self.NZULF = self.ZULF + self.ZSULF - self.TRZLF + self.TZPLF + self.TSZPLF
        self.NZUER = self.ZUER + self.ZSUER - self.TRZER + self.TZPER + self.TSZPER

        # 各器官锌含量
        self.ZART += self.NZURT
        self.ZAST += self.NZUST
        self.ZALF += self.NZULF
        self.ZAER += self.NZUER
        self.TZA = self.ZART + self.ZAST + self.ZALF + self.ZAER

        # 总结指标
        # 各器官锌浓度
        self.ZRTC = self.cal_massfraction(self.ZART, self.WRT)
        self.ZSTC = self.cal_massfraction(self.ZAST, self.WST)
        self.ZLFC = self.cal_massfraction(self.ZALF, self.WLF)
        self.ZERC = self.cal_massfraction(self.ZAER, self.WER)

        # 死亡根茎叶的实际锌含量
        self.DZART = self.DRT * self.ZRTC
        self.DZAST = self.DST * self.ZSTC
        self.DZALF = self.DLF * self.ZLFC
        self.TDZA = self.DZART + self.DZAST + self.DZALF
        # 当前各器官锌含量
        # 每个器官减去死亡器官的锌含量
        if self.day != 1:
            self.ZART = self.ZART - self.DRT * self.ZRTC
            self.ZAST = self.ZAST - self.DST * self.ZSTC
            self.ZALF = self.ZALF - self.DLF * self.ZLFC

        self.day += 1

        # 吸收的锌含量
        self.SUMZ += self.ZU
        self.SUMTZA = self.TZA - self.TDZA
        self.SUMTDZA += self.TDZA

        # 质量平衡

        self.BANLANCE = self.SUMZ - self.SUMTZA - self.SUMTDZA
        pass

    def newtrantable(self, df):
        num = len(df)
        x = []
        y = []
        for i in range(num):
            x.append(df[i][0])
            y.append(df[i][1])

        max_day = x[-1]
        xnew = np.arange(1, max_day + 1)
        kind = ["nearest", "zero", "slinear", "quadratic", "cubic"]
        f = interpolate.interp1d(x, y, kind=kind[2])
        ynew = f(xnew)

        # return np.array([xnew,ynew])
        return ynew

    def cal_growth_rate(self, df, target, dtarget, day_length):
        data = []
        da = np.array(df.loc[:, target])
        for i in range(day_length - 1):
            data.append(da[i + 1] - da[i])
        data.append(0)
        df[dtarget] = data
        return df

    def cal_ZDMI(self, j, blossom, MIZRT, MIZST, MIZLF, MIZER, WRT, WST, WLF, WER, ZART, ZAST, ZALF, ZAER):
        if j <= blossom:
            ZDMIRT = max(0, MIZRT * WRT - ZART)
            ZDMIST = max(0, MIZST * WST - ZAST)
            ZDMILF = max(0, MIZLF * WLF - ZALF)
            ZDMIER = max(0, MIZER * WER - ZAER)
        else:
            ZDMIRT = 0
            ZDMIST = 0
            ZDMILF = 0
            ZDMIER = max(0, MIZER * WER - ZAER)

        return ZDMIRT, ZDMIST, ZDMILF, ZDMIER

    def cal_massfraction(self, ZA, W):
        if W != 0:
            ZMA = ZA / W
        else:
            ZMA = 0
        return ZMA

    def cal_ZDU(self, j, blossom, ZDMIRT, ZDMIST, ZDMILF, ZDMIER, ZRT, ZST, ZLF, ZER):
        if j <= blossom:
            ZDURT = max(0, ZDMIRT - ZRT)
            ZDUST = max(0, ZDMIST - ZST)
            ZDULF = max(0, ZDMILF - ZLF)
            ZDUER = max(0, ZDMIER - ZER)
        else:
            ZDURT = 0
            ZDUST = 0
            ZDULF = 0
            ZDUER = max(0, ZDMIER - ZER)
        return ZDURT, ZDUST, ZDULF, ZDUER
