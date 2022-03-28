from scipy import interpolate
import numpy as np
import pandas as pd
import trantable
import calneed
import matplotlib.pyplot as plt


def cal_growth_rate(df, target, dtarget, day_length):
    data = []
    da = np.array(df.loc[:, target])
    for i in range(day_length - 1):
        data.append(da[i + 1] - da[i])
    data.append(0)
    df[dtarget] = data
    return df


if __name__ == '__main__':

    # 初始化
    # IWRT = 0
    # IWST = 0
    # IWLF = 0

    # IZ
    # IAZ

    # 植物生长指标表
    GRTT = [[1, 0],
            [35, 9.26],
            [50, 10.16],
            [75, 9.33],
            [90, 5.18],
            [105, 3.24]]
    GSTT = [[1, 0],
            [35, 0],
            [50, 0],
            [75, 60.5],
            [90, 0],
            [105, 0]]
    GLFT = [[1, 0],
            [35, 0],
            [50, 0],
            [75, 60.5],
            [90, 0],
            [105, 0]]
    GERT = [[1, 0],
            [35, 0],
            [50, 0],
            [75, 1],
            [90, 1],
            [105, 0]]

    # 锌含量吸收量表kg*ha-1
    ZUT = [[1, 0.005],
           [35, 0.0154],
           [50, 0.0209],
           [75, 0.0148],
           [90, 0.005],
           [105, 0]
           ]
    # 最小锌含量表mg*kg-1
    MIZRTT = [[0, 10],
              [35, 25],
              [50, 25],
              [75, 40],
              [90, 20],
              [105, 20]]
    MIZLFT = [[0, 10],
              [35, 25],
              [50, 25],
              [75, 40],
              [90, 20],
              [105, 20]]
    MIZSTT = [[0, 25],
              [35, 25],
              [50, 25],
              [75, 25],
              [90, 25],
              [105, 25]]
    MIZERT = [[0, 15],
              [35, 15],
              [50, 15],
              [75, 15],
              [90, 15],
              [105, 15]]
    # 最大锌含量表
    MXZRTT = [[0, 500],
              [35, 500],
              [50, 500],
              [75, 500],
              [90, 500],
              [105, 500]]
    MXZLFT = [[0, 200],
              [35, 100],
              [50, 100],
              [75, 200],
              [90, 200],
              [105, 200]]
    MXZSTT = [[0, 200],
              [35, 300],
              [50, 300],
              [75,300],
              [90, 300],
              [105, 200]]
    MXZERT = [[0, 50],
              [35, 50],
              [50, 50],
              [75, 50],
              [90, 50],
              [105, 50]]
    # 活性锌的含量质量分数（可转运）[-]
    FRTT = [[0, 0.1],
            [35, 0.1],
            [50, 0.1],
            [75, 0.2],
            [90, 0.6],
            [105, 0.8]]
    FLFT = [[0, 0.1],
            [35, 0.1],
            [50, 0.1],
            [75, 0.2],
            [90, 0.6],
            [105, 0.8]]
    FSTT = [[0, 0.3],
            [35, 0.3],
            [50, 0.3],
            [75, 0.5],
            [90, 0.6],
            [105, 0.7]]
    FERT = [[0, 0],
            [35, 0],
            [50, 0],
            [75, 0],
            [90, 0],
            [105, 0]]
    # 衰老叶片中的残余锌含量
    RMZLFT = [[0, 0],
              [35, 0],
              [50, 10],
              [75, 10],
              [90, 10],
              [105, 10]]
    # 实测锌含量（我就没写了）

    day_length = 105
    start_time = 1
    finish_time = 105
    blossom = 60
    data_name_list = [ZUT,
                      MIZRTT, MIZSTT, MIZLFT, MIZERT,
                      MXZRTT, MXZSTT, MXZLFT, MXZERT,
                      FRTT, FSTT, FLFT, FERT, RMZLFT]
    data_list = []
    for i in data_name_list:
        data_list.append(trantable.trantable(i))
    # print(data_list)

    path = r'G:\我的研究生\研一下学期\毕业论文\论文\作物模型'
    hhz_df = pd.read_csv(path + "\\黄华占模拟.csv")
    # 只取104天的数据
    hhz_df104 = hhz_df.iloc[0:day_length]
    hhz_df104['WST'] = hhz_df104.loc[:, 'TWST'] - hhz_df104.loc[:, 'DWST']
    hhz_df104['WRT'] = hhz_df104.loc[:, 'TWRT'] - hhz_df104.loc[:, 'DWRT']
    # 计算生长速率
    hhz_df104 = cal_growth_rate(hhz_df104, 'TWRT', 'dTWRT', day_length)
    hhz_df104 = cal_growth_rate(hhz_df104, 'TWST', 'dTWST', day_length)
    hhz_df104 = cal_growth_rate(hhz_df104, 'TWLV', 'dTWLV', day_length)
    hhz_df104 = cal_growth_rate(hhz_df104, 'TWSO', 'dTWSO', day_length)
    # 计算死亡速率
    hhz_df104 = cal_growth_rate(hhz_df104, 'DWRT', 'dDWRT', day_length)
    hhz_df104 = cal_growth_rate(hhz_df104, 'DWST', 'dDWST', day_length)
    hhz_df104 = cal_growth_rate(hhz_df104, 'DWLV', 'dDWLV', day_length)

    # 干物质量
    WRTT = np.array(hhz_df104['WRT'])
    WSTT = np.array(hhz_df104['WST'])
    WLFT = np.array(hhz_df104['WLV'])
    WERT = np.array(hhz_df104['TWSO'])
    # 生长速率
    GRTT = np.array(hhz_df104['dTWRT'])
    GSTT = np.array(hhz_df104['dTWST'])
    GLFT = np.array(hhz_df104['dTWLV'])
    GERT = np.array(hhz_df104['dTWSO'])
    # 死亡速率
    DRTT = np.array(hhz_df104['dDWRT'])
    DSTT = np.array(hhz_df104['dDWST'])
    DLFT = np.array(hhz_df104['dDWLV'])

    # 开始分配
    ZUlist = data_list[0]
    # 初始实际锌含量为0
    ZART = 0
    ZAST = 0
    ZALF = 0
    ZAER = 0
    # 用于收集数据画图
    # 浓度
    ZRTC_list = []
    ZSTC_list = []
    ZLFC_list = []
    ZERC_list = []
    # 含量
    ZART_list = []
    ZAST_list = []
    ZALF_list = []
    ZAER_list = []
    # 潜在需锌量
    TZDMI_list = []
    TXDMX_list = []
    # 计算质量平衡
    SUMZ = 0
    SUMTZA = 0
    SUMTDZA = 0

    for i in range(day_length):
        j = i + 1
        print("开始计算第{0}天".format(j))
        # 计算最小需求量mg*kg-1
        MIZRT = data_list[1][i]
        MIZST = data_list[2][i]
        MIZLF = data_list[3][i]
        MIZER = data_list[4][i]
        # 每天死亡器官量
        DRT = DRTT[i]
        DST = DSTT[i]
        DLF = DLFT[i]
        # 各器官当前干物质量 kg*ha-1(一天结束后在死亡)
        WRT = WRTT[i]+DRT
        WST = WSTT[i]+DST
        WLF = WLFT[i]+DLF
        WER = WERT[i]

        # 锌最小需求量
        ZDMIRT, ZDMIST, ZDMILF, ZDMIER = calneed.cal_ZDMI(j, blossom, MIZRT, MIZST, MIZLF, MIZER, WRT, WST, WLF, WER,
                                                          ZART, ZAST, ZALF, ZAER)
        TZDMI = ZDMIRT + ZDMIST + ZDMILF + ZDMIER

        # 今天的实际锌含量质量分数
        ZMART = calneed.cal_massfraction(ZART, WRT)
        ZMAST = calneed.cal_massfraction(ZAST, WST)
        ZMALF = calneed.cal_massfraction(ZALF, WLF)
        ZMAER = calneed.cal_massfraction(ZAER, WER)

        # 叶片中的净流入（吸取-去转运+来自转运）
        # 此时我认为穗中的锌含量只能通过转运获得

        # 计算最小锌需求的分配系数Fraction1
        FZRT1 = calneed.cal_massfraction(ZDMIRT, TZDMI)
        FZST1 = calneed.cal_massfraction(ZDMIST, TZDMI)
        FZLF1 = calneed.cal_massfraction(ZDMILF, TZDMI)
        FZER1 = calneed.cal_massfraction(ZDMIER, TZDMI)
        TFZ1 = FZRT1 + FZST1 + FZLF1 + FZER1

        # 锌最大需求量表的信息
        MXZRT = data_list[5][i]
        MXZST = data_list[6][i]
        MXZLF = data_list[7][i]
        MXZER = data_list[8][i]

        # 计算日最大锌需求量
        ZDMXRT = max(0, MXZRT * WRT - ZART)
        ZDMXST = max(0, MXZST * WST - ZAST)
        ZDMXLF = max(0, MXZLF * WLF - ZALF)
        ZDMXER = max(0, MXZER * WER - ZAER)
        TZDMX = ZDMXRT + ZDMXST + ZDMXLF + ZDMXER

        # 基于最大锌需求量的Fraction2
        FZRT2 = calneed.cal_massfraction(ZDMXRT - ZDMIRT, TZDMX - TZDMI)
        FZST2 = calneed.cal_massfraction(ZDMXST - ZDMIST, TZDMX - TZDMI)
        FZLF2 = calneed.cal_massfraction(ZDMXLF - ZDMILF, TZDMX - TZDMI)
        FZER2 = calneed.cal_massfraction(ZDMXER - ZDMIER, TZDMX - TZDMI)
        TFZ2 = FZRT2 + FZST2 + FZLF2 + FZER2

        # 开始进行分配

        # 首先锌的吸收先满足最小需求（TZDMI）
        ZU = ZUlist[i] * 1000000  # mg/ha
        ZU1 = min(ZU, TZDMI)
        # 一阶段分配
        ZURT = ZU1 * FZRT1
        ZUST = ZU1 * FZST1
        ZULF = ZU1 * FZLF1
        ZUER = ZU1 * FZER1

        # 锌盈余
        ZSU = max(0, ZU - TZDMI)

        # 二阶段分配
        ZSURT = ZSU * FZRT2
        ZSUST = ZSU * FZST2
        ZSULF = ZSU * FZLF2
        ZSUER = ZSU * FZER2

        # 通过锌吸收的含量
        ZRT = ZURT + ZSURT
        ZST = ZUST + ZSUST
        ZLF = ZULF + ZSULF
        ZER = ZUER + ZSUER
        # 锌吸收的质量平衡
        ZU_BALANCE = ZU-ZRT-ZST-ZLF-ZER

        # 根系吸收后的最小锌含量需求
        # 还需要的锌需要通过转运方式获得
        ZDURT, ZDUST, ZDULF, ZDUER = calneed.cal_ZDU(j, blossom, ZDMIRT, ZDMIST, ZDMILF, ZDMIER, ZRT, ZST, ZLF, ZER)
        TZDU = ZDURT + ZDUST + ZDULF + ZDUER

        # 基于转运需求量的Fraction3
        FZRT3 = calneed.cal_massfraction(ZDURT, TZDU)
        FZST3 = calneed.cal_massfraction(ZDUST, TZDU)
        FZLF3 = calneed.cal_massfraction(ZDULF, TZDU)
        FZER3 = calneed.cal_massfraction(ZDUER, TZDU)

        # 如果信息收之后没有分配的需求
        # 锌的主动吸收分配系数等于0
        # 除去死亡的叶片，总是在死亡时转运一些
        FRT = data_list[9][i]
        FST = data_list[10][i]
        FLF = data_list[11][i]
        FER = data_list[12][i]

        # 开始转运
        # 各器官的可转运锌量
        TRZRT = max(0, ZART + ZRT - ZDMIRT) * FRT
        TRZST = max(0, ZAST + ZST - ZDMIST) * FST
        TRZLF = max(0, ZALF + ZLF - ZDMILF) * FLF
        TRZER = 0

        # 总可转运锌量
        TTRZ = TRZRT + TRZST + TRZLF
        # 总转运锌量
        TTRZ1 = min(TTRZ, TZDU)

        # 第三阶段的分配
        TZPRT = FZRT3 * TTRZ1
        TZPST = FZST3 * TTRZ1
        TZPLF = FZLF3 * TTRZ1
        TZPER = FZER3 * TTRZ1
        TTZP = TZPRT + TZPST + TZPLF + TZPER

        # 多余的分配锌
        STTRZ = max(0, TTRZ - TZDU)

        # 多余的分配锌再分配
        TSZPRT = FZRT2 * STTRZ
        TSZPST = FZST2 * STTRZ
        TSZPLF = FZLF2 * STTRZ
        TSZPER = FZER2 * STTRZ
        TTSZP = TSZPRT + TSZPST + TSZPLF + TSZPER

        # 观测值
        # 更新锌含量
        NZURT = ZURT + ZSURT - TRZRT + TZPRT + TSZPRT
        NZUST = ZUST + ZSUST - TRZST + TZPST + TSZPST
        NZULF = ZULF + ZSULF - TRZLF + TZPLF + TSZPLF
        NZUER = ZUER + ZSUER - TRZER + TZPER + TSZPER

        # 各器官锌含量
        ZART += NZURT
        ZAST += NZUST
        ZALF += NZULF
        ZAER += NZUER
        TZA = ZART + ZAST + ZALF + ZAER

        # 总结指标
        # 各器官锌浓度
        ZRTC = calneed.cal_massfraction(ZART, WRT)
        ZSTC = calneed.cal_massfraction(ZAST, WST)
        ZLFC = calneed.cal_massfraction(ZALF, WLF)
        ZERC = calneed.cal_massfraction(ZAER, WER)

        # 死亡根茎叶的实际锌含量
        DZART = DRT * ZRTC
        DZAST = DST * ZSTC
        DZALF = DLF * ZLFC
        TDZA = DZART + DZAST + DZALF
        # 当前各器官锌含量
        # 每个器官减去死亡器官的锌含量
        if i != 0:
            ZART = ZART - DRT * ZRTC
            ZAST = ZAST - DST * ZSTC
            ZALF = ZALF - DLF * ZLFC

        # 更新living 干物质量
        # WRT -= DRT
        # WST -= DST
        # WLF -= DLF


        # 死亡器官中的锌含量
        # DZA**
        # 吸收的锌含量
        SUMZ += ZU
        SUMTZA = TZA-TDZA
        SUMTDZA += TDZA

        # 质量平衡

        BAMLANCE = SUMZ - SUMTZA - SUMTDZA
        # 收集数据
        ZRTC_list.append(ZRTC)
        ZSTC_list.append(ZSTC)
        ZLFC_list.append(ZLFC)
        ZERC_list.append(ZERC)
        ZART_list.append(ZART)
        ZAST_list.append(ZAST)
        ZALF_list.append(ZALF)
        ZAER_list.append(ZAER)

    # 画图
    x = np.arange(1, 106)
    yZRTC = ZRTC_list
    yZSTC = ZSTC_list
    yZLFC = ZLFC_list
    yZERC = ZERC_list
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax1.plot(x, yZRTC)
    ax1.set_xlabel('DAS')
    ax1.set_ylabel('ZRTC')
    ax2 = fig.add_subplot(222)
    ax2.set_xlabel('DAS')
    ax2.set_ylabel('ZSTC')
    ax2.plot(x, yZSTC)
    ax3 = fig.add_subplot(223)
    ax3.set_xlabel('DAS')
    ax3.set_ylabel('ZLFC')
    ax3.plot(x, yZLFC)
    ax4 = fig.add_subplot(224)
    ax4.set_xlabel('DAS')
    ax4.set_ylabel('ZERC')
    ax4.plot(x, yZERC)
    plt.show()
    # 量
    yZART = ZART_list
    yZAST = ZAST_list
    yZALF = ZALF_list
    yZAER = ZAER_list
    fig2 = plt.figure()
    ax1 = fig2.add_subplot(221)
    ax1.plot(x, yZART)
    ax1.set_xlabel('DAS')
    ax1.set_ylabel('ZART')
    ax2 = fig2.add_subplot(222)
    ax2.set_xlabel('DAS')
    ax2.set_ylabel('ZAST')
    ax2.plot(x, yZAST)
    ax3 = fig2.add_subplot(223)
    ax3.set_xlabel('DAS')
    ax3.set_ylabel('ZALF')
    ax3.plot(x, yZALF)
    ax4 = fig2.add_subplot(224)
    ax4.set_xlabel('DAS')
    ax4.set_ylabel('ZAER')
    ax4.plot(x, yZAER)
    plt.show()
