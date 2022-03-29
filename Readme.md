# 简介

这个程序属刘神舟硕士毕业论文的主要内容，主要功能是使用hydrus1d、WOFOST作物生长模型和自己编写的作物锌转运分配模型模拟锌元素对水稻生长的影响

- 本软件基于hydrus1d和python构建，运行环境为windows 10 

- 将文件下载到本地即可运行

- 其中“final_main20220306.py”用分别模拟1-14号田块，”final_main30220306duoxiancheng.py“用于使用多线程库模拟1-14号田块，加快调参速度

- ”simqingjing20220324.py“用于模拟不同施锌日期下水稻籽粒和精米含锌量的变化情况，“获得不同施锌情景下的锌含量.py”用于统计不同情景下的锌含量并统计

- “计算锌元素流向.py ”用于计算锌元素流向

  

## 模型运行过程

以 final_main20220306.py为例，首先列出field_list，这个是田块编号，然后设置hydrus1d模型文件存放的目录，然后设置hydrus模型溶质参数，不同锌肥的利用效率是指锌元素直接进入叶器官的量占叶面施锌量的比例

## 模型运行结果

模型的运行结果分别是main_result和simreult两个文件夹中

### main_result

其中，main_result如下：

+ extract_data：表示水稻精米、颖壳 的锌含量和土壤中锌元素的流动情况

+ cropdata：作物模型运行的结果。（作物模型使用的pcse5.4.2，并修改了conf文件如下所示）

  ```
  # -*- coding: utf-8 -*-
  # Copyright (c) 2004-2014 Alterra, Wageningen-UR
  # Allard de Wit (allard.dewit@wur.nl), April 2014
  """PCSE configuration file for WOFOST Potential Production simulation
  in PCSE identical to the FORTRAN WOFOST 7.1
  
  This configuration file defines the soil and crop components that
  should be used for potential production simulation.
  """
  
  from pcse.soil.classic_waterbalance import WaterbalancePP
  from pcse.crop.wofost import Wofost
  from pcse.agromanager import AgroManager
  
  # Module to be used for water balance
  SOIL = WaterbalancePP
  
  # Module to be used for the crop simulation itself
  CROP = Wofost
  
  # Module to use for AgroManagement actions
  AGROMANAGEMENT = AgroManager
  
  # variables to save at OUTPUT signals
  # Set to an empty list if you do not want any OUTPUT
  OUTPUT_VARS = ["DVS","LAI","TAGP", "TWSO", "TWLV", "TWST",
                 "TWRT", "TRA", "RD", "SM", "WWLOW","WLV","WST","WRT","DWRT","DWST","DWLV"]
  # interval for OUTPUT signals, either "daily"|"dekadal"|"monthly"|"weekly"
  # For daily output you change the number of days between successive
  # outputs using OUTPUT_INTERVAL_DAYS. For dekadal and monthly
  # output this is ignored.
  OUTPUT_INTERVAL = "daily"
  OUTPUT_INTERVAL_DAYS = 1
  # Weekday: Monday is 0 and Sunday is 6
  OUTPUT_WEEKDAY = 0
  
  # Summary variables to save at CROP_FINISH signals
  # Set to an empty list if you do not want any SUMMARY_OUTPUT
  SUMMARY_OUTPUT_VARS = ["DVS","LAIMAX","TAGP", "TWSO", "TWLV", "TWST",
                         "TWRT", "CTRAT", "RD", "DOS", "DOE", "DOA",
                         "DOM", "DOH", "DOV"]
  
  # Summary variables to save at TERMINATE signals
  # Set to an empty list if you do not want any TERMINAL_OUTPUT
  TERMINAL_OUTPUT_VARS = []
  
  ```

* soildata用于描述不同土层的土壤锌含量、土壤水含锌量、土壤固相含锌量
* solutedata用于描述作物对锌元素的吸收情况
* sumZnbotdata用于描述锌元素从下边界的流出情况
* zn_contentdata用于描述作物对锌元素的需求情况和实际吸收量

### simresult

描述的是不同施锌情景下各数据，其中statricezn.csv是精米和颖壳锌含量的统计

### simlab

本文件夹主要是对模型做敏感性分析的结果

