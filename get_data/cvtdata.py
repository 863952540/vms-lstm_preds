import pandas as pd

df = pd.read_csv("./TemperatureData_New.csv")
df['Dates'] = pd.to_datetime(df['Dates'])

# def process(x):
#     x1 = int(x.split("+")[0])
#     x2 = int(x.split("+")[1])
#     x3 = float((x1+x2)/2)
#     return x3
#
# df['New_Night'] = df['New_Night'].apply(lambda x:process(x))
# df['New_Day'] = df['New_Day'].apply(lambda x:process(x))

# df.to_csv('./TemperatureData_New.csv', index=False, encoding='utf_8_sig')
print(df.head())