from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from SALib.plotting.bar import plot as barplot
import matplotlib.pyplot as plot

result_df = pd.read_csv('shouji_dfd100h0.csv')
result_df.columns = ('node1conc','node1Sconc','node2conc','node2Sconc','node3conc','node3Sconc',
                     'node4conc','node4Sconc','node5conc','node5Sconc','node6conc','node6Sconc',
                     'node7conc','node7Sconc','root_uptake_solute_v','root_uptake_solute_sum')

# result_array = np.array(result_df)
# problem = {'num_vars': 4,
#            'names': ['disp', 'diffus', 'croot', 'km'],
#            'bounds': [[0.1, 0.5],
#                       [0.1, 0.2],
#                       [0.0005, 0.005],
#                       [0.005, 0.5]]
#            }
# problem = {'num_vars': 3,
#            'names': [ 'kd', 'beta', 'alpha'],
#            'bounds': [
#                [0.7, 0.9],
#                [0.2, 0.3],
#                [0.3, 0.7]]
#            }
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
target = "node7Sconc"
result_array  = np.array(result_df[target])
Si = sobol.analyze(problem, result_array, calc_second_order=True,print_to_console=True)
Si_df = Si.to_df()
barplot(Si_df[0])
# barplot(Si_df[1])
# barplot(Si_df[2])
plot.show()