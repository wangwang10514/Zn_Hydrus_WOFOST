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
import utils

# 目标：不同参数变化对结果的影响
# 结果：土壤剖面锌浓度含量，根系吸收锌含量。不同初始条件下的土壤锌浓度。


if __name__ == "__main__":
    sorbed_c, liquid_c = utils.cal_initial_zn_conc(soil_zn=1, theta=0.3713, Kd=15, yita=0.62)
    print(sorbed_c)
    print(liquid_c)
