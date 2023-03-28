# 1. 环境

~~~python
python --version==3.7.6
tensorflow --version==2.1.0
~~~

# 2. 文件说明

## 2.1 folder: get_data

- whether_scapy.py文件爬取http://www.tianqihoubao.com/中南京市过去10天的最高最低温度
- Temperature_New.csv为所用数据集

## 2.2 folder：images

存放所用报告中所使用的图片

## 2.3 folder：VMD_process_code

- folder：modesdata 存放各个模态预测完的数据
- file：lstm_preds.py 对各个模态的数据进行lstm预测
- file：VMD_data.py用于对预测序列进行变分模态划分
- file：show_data.py、vmd_result.py展示结果