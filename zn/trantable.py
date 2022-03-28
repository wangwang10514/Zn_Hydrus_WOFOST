from scipy import interpolate
import numpy as np
import pandas as pd

def trantable(df):
    num = len(df)
    x = []
    y = []
    for i in range(num):
        x.append(df[i][0])
        y.append(df[i][1])

    max_day = x[-1]
    xnew = np.arange(1,max_day+1)
    kind = ["nearest", "zero", "slinear", "quadratic", "cubic"]
    f = interpolate.interp1d(x, y, kind=kind[2])
    ynew = f(xnew)


    # return np.array([xnew,ynew])
    return ynew
def newtrantable(df):
    num = len(df)
    x = []
    y = []
    for i in range(num):
        x.append(df[i][0])
        y.append(df[i][1])

    max_day = x[-1]
    xnew = np.arange(1,max_day+1)
    kind = ["nearest", "zero", "slinear", "quadratic", "cubic"]
    f = interpolate.interp1d(x, y, kind=kind[2])
    ynew = f(xnew)


    # return np.array([xnew,ynew])
    return ynew

if __name__ == '__main__':
    table = [[1, 0],
             [35, 1.34],
             [50, 3.09],
             [75, 4.8],
             [90, 2.7],
             [105, 0]
             ]
    x = trantable(table)
    print(x)
