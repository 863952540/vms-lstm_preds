import pandas as pd
from matplotlib import pyplot, pyplot as plt
import numpy as np
orgin = pd.read_csv('TemperatureData_New.csv')
imf=pd.read_csv('vmd_data.csv')
tem_low = orgin['Tem_Low'].values
imf0 = imf['imf0'].values
imf1 = imf['imf1'].values
imf2 = imf['imf2'].values
imf3 = imf['imf3'].values
imf4 = imf['imf4'].values
plt.figure(figsize=(16,8))
plt.subplot(611)
plt.plot(tem_low, color='b')
plt.xticks([])
plt.ylabel("Lowest_Temp")
plt.subplot(612)
plt.plot(imf0, color='k')
plt.ylabel("IMF0")
plt.xticks([])
plt.subplot(613)
plt.plot(imf1, color='k')
plt.ylabel("IMF1")
plt.xticks([])
plt.subplot(614)
plt.plot(imf2, color='k')
plt.ylabel("IMF2")
plt.xticks([])
plt.subplot(615)
plt.plot(imf3, color='k')
plt.ylabel("IMF3")
plt.xticks([])
plt.subplot(616)
plt.plot(imf4, color='k')
plt.ylabel("IMF4")
plt.xlabel("Days")
plt.savefig("vmd_result.jpg")
plt.show()
