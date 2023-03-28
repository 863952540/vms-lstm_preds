import numpy as np
import pandas as pd
from vmdpy import VMD

df=pd.read_csv('TemperatureData_New.csv')
# imf=pd.read_csv('out_emd.csv',index_col=0)
# num_data_points = len(df['_time'])
# data_date=df['_time']
# df=df.drop(columns=['_time'])
CPU=df['Tem_Low']


alpha = 7000      # moderate bandwidth constraint
tau = 0.            # noise-tolerance (no strict fidelity enforcement)
K = 5       # 3 modes
DC = 0             # no DC part imposed
init = 1           # initialize omegas uniformly
tol = 1e-7

# """
# alpha、tau、K、DC、init、tol 六个输入参数的无严格要求；
# alpha 带宽限制 经验取值为 抽样点长度 1.5-2.0 倍；
# tau 噪声容限 ；
# K 分解模态（IMF）个数；
# DC 合成信号若无常量，取值为 0；若含常量，则其取值为 1；
# init 初始化 w 值，当初始化为 1 时，均匀分布产生的随机数；
# tol 控制误差大小常量，决定精度与迭代次数
# """

imfs, u_hat, omega = VMD(CPU, alpha, tau, K, DC, init, tol)
imf0=imfs[0].reshape(-1,1)
imf1=imfs[1].reshape(-1,1)
imf2=imfs[2].reshape(-1,1)
imf3=imfs[3].reshape(-1,1)
imf4=imfs[4].reshape(-1,1)


test_hat = np.concatenate([imf0,imf1,imf2,imf3,imf4],axis=1)
df_test = pd.DataFrame(test_hat,columns=['imf0','imf1','imf2','imf3','imf4'])
df_test.to_csv('vmd_data.csv')

print('kf')
