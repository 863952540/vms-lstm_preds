import pandas as pd
from matplotlib import pyplot, pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from sklearn.metrics import r2_score

imf0=pd.read_csv('./modesdata/imf0.csv')
imf1=pd.read_csv('./modesdata/imf1.csv')
imf2=pd.read_csv('./modesdata/imf2.csv')
imf3=pd.read_csv('./modesdata/imf3.csv')
imf4=pd.read_csv('./modesdata/imf4.csv')

lstm_re = pd.read_csv('result.csv')['1'].values

y_true=imf0['0']+imf1['0']+imf2['0']+imf3['0']+imf4['0']
y_hat=imf0['1']+imf1['1']+imf2['1']+imf3['1']+imf4['1']
#
lstm_re_smoothed = gaussian_filter1d(lstm_re, sigma=5)
y_true_smoothed = gaussian_filter1d(y_true, sigma=5)
y_hat_smoothed = gaussian_filter1d(y_hat, sigma=5)


yhat = y_hat.values
ytrue = y_true.values
print(yhat.shape)
# 计算MAE
mae = 0
for i in range(1192):
    mae+=abs(yhat[i]-ytrue[i])
print(mae/1192)

#计算MSE
mse = 0;
temp = 0;
for i in range(1192):
    temp = abs(yhat[i]-ytrue[i])
    mse+=pow(temp, 2)
mse/=1192
print(mse)

#计算RMSE
import math
rmse = math.sqrt(mse)
print(rmse)

score=r2_score(yhat,ytrue)
print(score)
# plt.plot(orgin, marker='.', label="orgin")
plt.figure(figsize=(16,8))
plt.plot(y_true_smoothed, label="True value")
plt.plot(y_hat_smoothed, color='r', label="VMD-LSTM")
plt.plot(lstm_re_smoothed, color='g', label="LSTM")
plt.legend(loc='best')
ax=plt.gca()  #gca:get current axis得到当前轴
#设置图片的右边框和上边框为不显示
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.ylabel('Temperature', size=15)
plt.xlabel('Days', size=15)
plt.legend(fontsize=15)
plt.show()


