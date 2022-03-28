import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pcse
import os
from pcse.fileinput import CABOFileReader
from pcse.util import WOFOST71SiteDataProvider
from pcse.base import ParameterProvider
from pcse.fileinput import YAMLAgroManagementReader
from pcse.models import Wofost71_PP
from pcse.fileinput import ExcelWeatherDataProvider
from pcse.fileinput import YAMLCropDataProvider

def run_wofost(ricetype,day_length):
    if ricetype == 'hhz':
        data_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\pcse'
        cropfile_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\WOFOST_crop_parameters-master'
        cropdata = YAMLCropDataProvider(fpath=cropfile_dir)
        cropdata.set_active_crop('rice', 'huanghuazhan')
        soilfile = os.path.join(data_dir, 'ec3.soil')
        soildata = CABOFileReader(soilfile)
        sitedata = WOFOST71SiteDataProvider(WAV=50, CO2=360)
        parameters = ParameterProvider(cropdata=cropdata, soildata=soildata, sitedata=sitedata)
        agromanagement_file = os.path.join(data_dir, 'Rice_huanghuazhan_calendar.agro')
        agromanagement = YAMLAgroManagementReader(agromanagement_file)
        wdp = ExcelWeatherDataProvider(os.path.join(data_dir, 'ycweather.xlsx'))
        wofsim = Wofost71_PP(parameters, wdp, agromanagement)
        wofsim.run_till_terminate()
        output = wofsim.get_output()
        df = pd.DataFrame(output)
        if df.shape[0]==day_length:
            return df
        else:
            print("day length wrong!")
    if ricetype == '99-25':
        data_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\pcse'
        cropfile_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\WOFOST_crop_parameters-master'
        cropdata = YAMLCropDataProvider(fpath=cropfile_dir)
        cropdata.set_active_crop('rice', 'Rice99_25')
        soilfile = os.path.join(data_dir, 'ec3.soil')
        soildata = CABOFileReader(soilfile)
        sitedata = WOFOST71SiteDataProvider(WAV=50, CO2=360)
        parameters = ParameterProvider(cropdata=cropdata, soildata=soildata, sitedata=sitedata)
        agromanagement_file = os.path.join(data_dir, 'Rice_99_25.agro')
        agromanagement = YAMLAgroManagementReader(agromanagement_file)
        wdp = ExcelWeatherDataProvider(os.path.join(data_dir, 'ycweather.xlsx'))
        wofsim = Wofost71_PP(parameters, wdp, agromanagement)
        wofsim.run_till_terminate()
        output = wofsim.get_output()
        df = pd.DataFrame(output)
        if df.shape[0]==day_length:
            return df
        else:
            print("day length wrong!")
    if ricetype == 'NJ9108':
        data_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\pcse'
        cropfile_dir = r'G:\我的研究生\研一下学期\毕业论文\作物模型\WOFOST_crop_parameters-master'
        cropdata = YAMLCropDataProvider(fpath=cropfile_dir)
        cropdata.set_active_crop('rice', 'NJ_9108')
        soilfile = os.path.join(data_dir, 'ec3.soil')
        soildata = CABOFileReader(soilfile)
        sitedata = WOFOST71SiteDataProvider(WAV=50, CO2=360)
        parameters = ParameterProvider(cropdata=cropdata, soildata=soildata, sitedata=sitedata)
        agromanagement_file = os.path.join(data_dir, 'Rice_NJ9108_calendar.agro')
        agromanagement = YAMLAgroManagementReader(agromanagement_file)
        wdp = ExcelWeatherDataProvider(os.path.join(data_dir, 'ycweather.xlsx'))
        wofsim = Wofost71_PP(parameters, wdp, agromanagement)
        wofsim.run_till_terminate()
        output = wofsim.get_output()
        df = pd.DataFrame(output)
        if df.shape[0] == day_length:
            return df
        else:
            print("day length wrong!")

    pass

if __name__ == "__main__":
    df = run_wofost(ricetype='hhz',day_length=108)
    print(df)