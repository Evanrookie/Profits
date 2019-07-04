# -*- coding:utf-8 -*-
import time
import pandas as pd
import os
import pyperclip
import tushare as ts
import datetime

#制作浮点数
def make_float(num):
    num = num.replace(' ','').replace(',','.').replace("−", "-")
    return float(num)

#检验是否为合理数字
def is_number(n):
    is_number = True
    try:
        num = float(n)
        # 检查 "nan" 
        is_number = num == num   # 或者使用 `math.isnan(num)`
    except ValueError:
        is_number = False
    return is_number

#检验字符串是否输入
def test(names):
    while True:
        if names:
            break
        else:
            print('请重新输入：')
            names=input()

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(date)

#记录盈利，存储到表格进行分析输出
signal = '1'
if signal == '1':
	name='Cgx'
else:
	name='Jyl'
total = 0
person={}
profits=[]
dates=[]
word=''
id=['846','737','617']
#记录盈利保存为字典
for i in range(0,3):
    current_id=id[i]
    profit = input('资金账号'+current_id+'盈利：\n')
    test(profit)
    
    #检验盈利是否为数字
    while True:
    	if is_number(profit)==False:
    		profit= input('盈利应为数字，请重新输入盈利：')
    	else:
    	    break
    person[current_id]=profit
print('\n\n')

#打印盈利
print(name.upper()+','+date+'盈利:')
for id,profit in person.items():
    if profit != '0':
        word=word+'('+id+'):'+profit+'+'
        profit=make_float(profit) 
        total += profit       
word=word[:-1]
print(word,end='')
end='='+str(total)
print(end+'\n\n')

profits.append(total)
dates.append(date)
save = {
    'name':name,
    'dates':dates,
    '846':person['846'],
    '737':person['737'],
    '617':person['617'],
    'profits':profits,
}
#今天的数据:日期，盈利
dataframe = pd.DataFrame(save)
dataframe.to_csv("日内盈利.csv",index=False,sep=',',mode='a',header=False)
#读取原来的csv
csv_data = pd.read_csv('日内盈利.csv')

#循环删除重复的日期数据
while True:
    #如果今天这个日期在这个csv中
    if date in csv_data.values:
        #删除csv的最后一行
        last_row = len(csv_data) - 1
        csv_data = csv_data.drop(csv_data.index[last_row])  
    #如果不在
    else:
        #写入删除完的csv
        csv_data.to_csv("日内盈利.csv",index=False,sep=',')
        break

#再追加一行今天的数据
dataframe.to_csv("日内盈利.csv",index=False,sep=',',mode='a',header=False)
csv_data_added = pd.read_csv('日内盈利.csv')
total=csv_data_added[['总计']]

#如果最后一天大于2000或者最后三天为负，追加一行下一个工作日的：时间，0，0，0，停盘

alldays = ts.trade_cal()
tradingdays = alldays[alldays['isOpen'] == 1]   # 开盘日
today=datetime.datetime.today().strftime('%Y-%m-%d')
if today in tradingdays['calendarDate'].values:
    tradingdays_list = tradingdays['calendarDate'].tolist()
    today_index  = tradingdays_list.index(today)
    tomorrow = tradingdays_list[int(today_index)+1]

stop = {
    'name':name,
    'dates':tomorrow,
    '846':['停盘'],
    '737':['停盘'],
    '617':['停盘'],
    'profits':[0],
}
#今天的数据:日期，盈利
df_stop = pd.DataFrame(stop)
total=csv_data_added[['总计']]
if float(total.iloc[-1:].sum()) < -2000.0:
    df_stop.to_csv("日内盈利.csv",index=False,sep=',',mode='a',header=False)
    print('明天停盘\n')
    sum=total.tail(20).sum()
elif float(total.iloc[-1:].sum()) < 0 and float(total.iloc[-2:-1].sum()) < 0 and float(total.iloc[-3:-2].sum()) < 0:
    df_stop.to_csv("日内盈利.csv",index=False,sep=',',mode='a',header=False)
    print('明天停盘\n')
    sum=total.tail(20).sum()
else:
    sum=total.tail(19).sum()
csv_data_added = pd.read_csv('日内盈利.csv')
print(csv_data_added.tail(30))

print('19日总盈利为'+str(sum))


pyperclip.copy(name+':'+word+end)

os.system('pause')
