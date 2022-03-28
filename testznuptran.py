import znuptran
import wofost
day_length = 108
Diffus = 100
Disp = 100
Kd = 4.8
yita = 0.012
alpha = 0.52
croot = 0.005
Km = 0.005
file_dir = ".\\hydrus20220228"
ricetype = 'hhz'
soil_zn = 1

# 建立一个储存数据的列表
solute_uptake_list = []
conc_list = []
rice_data = wofost.run_wofost(ricetype=ricetype, day_length=108)
zn_rice = znuptran.Zninrice(ricetype=ricetype, ricedata=rice_data, day_length=day_length)
croot = zn_rice.cal_croot()/10e8
print(croot)