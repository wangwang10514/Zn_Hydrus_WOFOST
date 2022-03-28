import numpy as np
from scipy import interpolate

def cal_massconc(theta,liquid_c, sorbed_c):
    massconc = theta * liquid_c * 1000 / 1.45 + sorbed_c * 1000 / 1.45
    return massconc




d = cal_massconc(0.3713,0.01391,0.0968)
print(d)


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
MXZSTT = [[1, 200],
                      [35, 200],
                      [50, 200],
                      [75, 300],
                      [90, 300],
                      [108, 200]]

print(len(newtrantable(self=None, df = MXZSTT)))