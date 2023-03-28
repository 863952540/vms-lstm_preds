import requests
from bs4 import BeautifulSoup
import pandas as pd
import  time
from fake_useragent import UserAgent

def getresponse(url, headers):
    i = 0
    while i < 4:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            return resp
        except requests.exceptions.RequestException as e:
            print(e)
            i += 1
        time.sleep(1)

def get_data(url):
    headers = {
        'Referer': 'http://www.tianqihoubao.com/',
        'User-Agent': UserAgent().random
    }
    resp = getresponse(url, headers)
    # 对于获取到的 HTML 二进制文件进行 'gbk' 转码成字符串文件
    html = resp.content.decode('gbk')
    soup = BeautifulSoup(html,'html.parser')
    # 获取 HTML 中所有<tr>…</tr>标签
    tr_list = soup.find_all('tr')
    # 初始化日期dates温度temp值
    dates,temp_high, temp_low, windpower_night, windpower_day= [], [], [], [], []

    for data in tr_list[1:]:
        sub_data = data.text.split()
        year = sub_data[0].split("年")[0]
        month = sub_data[0].split("年")[1].split("月")[0]
        day = sub_data[0].split("年")[1].split("月")[1].split("日")[0]
        date = [year, month, day]
        dates.append("/".join(date))
        # 同理采用切片方式获取列表中的最高、最低气温
        temp_low.append(sub_data[3].split("℃")[0])
        temp_high.append(sub_data[5].split("℃")[0])
        windpower_night.append(sub_data[7].split("级")[0])
        windpower_day.append(sub_data[9].split("级")[0])
    # 使用 _data 表存放日期、天气状况、气温表头及其值
    _data = pd.DataFrame()
    _data['Dates'] = dates
    _data['Tem_Low'] = temp_low
    _data['Tem_High'] = temp_high
    _data['WP_Night'] = windpower_night
    _data['WP_Day'] = windpower_day
    return _data

# 爬取目标网页
url = 'http://www.tianqihoubao.com/lishi/nanjing/month/{}{}.html'
# 总数据
data = pd.DataFrame(columns=['Dates', 'Tem_Low', 'Tem_High', 'WP_Night', 'WP_Day'])
for i in range(2013, 2023, 1):
    for j in range(1, 13, 1):
        if j<10:
            temp_url = url.format(i, "0"+str(j))
        else:
            temp_url = url.format(i, j)
        dataPerMonth = get_data(temp_url)
        data = pd.concat([data, dataPerMonth], ignore_index=True)
        print("{}年{}月天气数据已爬取完成.......".format(i, j))
        time.sleep(2)
data['Tem_Low']=data['Tem_Low'].astype(str).astype(int)
data['Tem_High']=data['Tem_High'].astype(str).astype(int)
print(data.head())
# 将 _data 表以 .csv 格式存入指定文件夹中
data.to_csv('./TemperatureData_New.csv', index=False, encoding='utf_8_sig')
