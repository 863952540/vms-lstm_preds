#!/usr/bin/env python
# coding: utf-8

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras import utils,losses,layers,Sequential
from tensorflow.keras.callbacks import ModelCheckpoint,TensorBoard



dataset=pd.read_csv("TemperatureData_New.csv",parse_dates=['Dates'],index_col=['Dates'])
data_vmd=pd.read_csv('vmd_data.csv',index_col=0)

days = [0, 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
dataset["day_cos"] = [np.cos((x.day + sum(days[1:x.month])) * (2 * np.pi / 365)) for x in dataset.index]
dataset["day_sin"] = [np.sin((x.day + sum(days[1:x.month])) * (2 * np.pi / 365)) for x in dataset.index]
dataset['month']=dataset.index.month



def multivariate_data(x,y, time_step):
    data = []
    labels = []


    for i in range(len(x)-time_step-6):
        
        data.append(x[i:i+time_step,:])
        labels.append(y[i+time_step+6])

    return np.array(data), np.array(labels)



da=dataset.values
vmd=data_vmd.values
scX = MinMaxScaler(feature_range=(0, 1))
scY = MinMaxScaler(feature_range=(0, 1))
scaledX = scX.fit_transform(da[:,1:])
scaledY = scY.fit_transform(vmd[:,4].reshape(-1,1))

data=np.concatenate((scaledY, scaledX), axis=1)

x=data[:,1:]
y=data[:,0]

#通过2:1划分训练集和测试集，2/3为训练集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33,shuffle=False,random_state=13)

time_step=10
train_x,train_y=multivariate_data(x_train,y_train,time_step)
test_x,test_y=multivariate_data(x_test,y_test,time_step)


#建立神经网络模型-2层LSTM和一个输出层
model= tf.keras.models.Sequential([
    tf.keras.layers.LSTM(128, input_shape=(train_x.shape[1],train_x.shape[2]),return_sequences=True),
#     tf.keras.layers.Dropout(0.4),
#     tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(256),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',loss='mse')

#模型保存的相关设置
utils.plot_model(model)
checkpoint_file='test_model.hdf5'
checkpoint_callback=ModelCheckpoint(filepath=checkpoint_file,monitor='loss',moode='min',save_best_only=True,save_weights_only=True)
#模型训练
history=model.fit(train_x,train_y,batch_size=64,epochs=100,validation_data=(test_x,test_y),verbose=2,shuffle=True)


#最喜欢的绘图环节，通过history获取模型每步训练取得的结果loss和val_loss
plt.figure(figsize=(8,8),dpi=200)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
#plt.ylim(0.005,0.05)
ax=plt.gca()  #gca:get current axis得到当前轴
#设置图片的右边框和上边框为不显示
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.legend(['train','validation'], loc='best')
#plt.savefig("./images/two_layers/result2.jpg")
plt.show()

yhat=model.predict(test_x)

yhat=scY.inverse_transform(yhat)
ytrue=scY.inverse_transform(test_y.reshape(-1,1))

mp=np.concatenate((ytrue,yhat),axis=1)
dp=pd.DataFrame(mp)
dp.to_csv('imf4.csv')

plt.figure(figsize=(16,8))
plt.plot(yhat,label="Pred value")
plt.plot(ytrue,label="true value")
plt.xlabel("Days")
plt.ylabel("Temperature")
plt.legend()

plt.show()
