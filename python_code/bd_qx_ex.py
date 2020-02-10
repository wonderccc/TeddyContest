import pandas as pd
import numpy as np
from pandas import DataFrame
from pandas import Series

posi=pd.read_csv("E:\\data\\python_file\\bad_driving_exchange_csv_file\\AA00002_bd.csv")

num=posi.shape[0]       #读取的记录行数

bad_driving_time = np.array(posi["bad_driving_time"][0:num]) # 获取不良驾驶发生的时间
bad_driving_lat = np.array(posi["bad_driving_lat"][0:num]) # 获取纬度值
bad_driving_lng = np.array(posi["bad_driving_lng"][0:num]) # 获取经度值 
bad_driving_name = np.array(posi["bad_driving_name"][0:num]) #获取不良驾驶的类型
bad_driving_info = np.array(posi["bad_driving_info"][0:num])  #获取不良驾驶的详细信息

from urllib.request import urlopen, quote
import json

#定义一个将wgs84坐标系转化为百度坐标系的函数
def wgs84tobaidu(x,y):
	data=str(x)+','+str(y);
	output = 'json'
	url='http://api.map.baidu.com/geoconv/v1/?coords='+data+'&from=1&to=5&output=' +output+'&ak=S2HzBb9CHpFRM55s8H8bjkkrUGBmGhIY'  #ak为百度api的密钥
	req = urlopen(url)
	res = req.read().decode() 
	temp = json.loads(res)
	baidu_x=0
	baidu_y=0
	if temp['status']==0:
		baidu_x=temp['result'][0]['x']
		baidu_y=temp['result'][0]['y']

	return baidu_x,baidu_y
	
ex_lng=[]
ex_lat=[]
ex_location=[]

for i in range(num):
	x,y=wgs84tobaidu(bad_driving_lng[i],bad_driving_lat[i])
	ex_lng.append(x)
	ex_lat.append(y)
for i in range(num):
	location_str=str(ex_lat[i])+','+str(ex_lng[i])     #将转化成功的坐标合并在一起
	ex_location.append(location_str)
	
import requests
import json

ex_district=[]
ex_city=[]
ex_province=[]

#利用百度api，根据经纬度得出具体的地理位置（省、市、县）
for i in range(num):
	r = requests.get(url='http://api.map.baidu.com/geocoder/v2/', params={'location':ex_location[i],'ak':'S2HzBb9CHpFRM55s8H8bjkkrUGBmGhIY','output':'json'})
	result = r.json()
	district = result['result']['addressComponent']['district']
	city = result['result']['addressComponent']['city']
	province = result['result']['addressComponent']['province']

	ex_district.append(district)     #获取县
	ex_city.append(city)     #获取市
	ex_province.append(province)     #获取省份
	
#df=DataFrame({'ex_province':Series(ex_province),'ex_city':Series(ex_city),'ex_district':Series(ex_district)})
#df.to_csv('E:\\data\\AA00002_bd_ex1.csv',index=False,encoding="utf_8_sig")

posi1=pd.read_csv("E:\\data\\python_file\\bad_driving_exchange_csv_file\\qx_data.csv")     #读取气象数据的csv文件

num1=posi1.shape[0]       #读取气象数据的记录行数

qx_province = np.array(posi1["province"][0:num1]) # 获取省份
qx_city = np.array(posi1["prefecture_city"][0:num1]) # 获取市
qx_district = np.array(posi1["county"][0:num1]) # 获取县
qx_wind_power = np.array(posi1["wind_power"][0:num1])   #获取风力级别
qx_conditions = np.array(posi1["conditions"][0:num1])     #获取天气信息
qx_rain_amount = np.array(posi1["precipitation"][0:num1])   #获取降雨量
qx_date = np.array(posi1["record_date"][0:num1])      #获取时间

from pandas import to_datetime

posi_dt=to_datetime(posi.bad_driving_time,format='%Y/%m/%d %H:%M:%S')

posi_day=posi_dt.dt.day
posi_month=posi_dt.dt.month
posi_year=posi_dt.dt.year

ex_date=[]
for i in range(num):
	ex_date.append(str(posi_day[i])+'/'+str(posi_month[i])+'/'+str(posi_year[i]))    #将日期数据转化为日/月/年的字符串格式，方便后续与气象数据中的日期相比较

for i in range(num):
	ex_province[i]=ex_province[i][:2]    #去除“省”字样
	ex_city[i]=ex_city[i][:2]     #去除“市”
	l=len(ex_district[i])
	ex_district[i]=ex_district[i][:l-1]     #去除“县/区”字样
	
ex_wind_power=[]
ex_conditions=[]
ex_rain_amount=[]

for i in range(num):
	ex_wind_power.append('')
	ex_conditions.append('')
	ex_rain_amount.append('')

#通过省、市、县、日期与气象数据中的相应属性列进行匹配，获取某天、某地区的具体天气情况
for i in range(num):
	for k in range(num1):
		if ex_province[i]==qx_province[k] and ex_city[i]==qx_city[k] and ex_district[i]==qx_district[k] and ex_date[i]==qx_date[k]: 
			ex_wind_power[i]=qx_wind_power[k]
			ex_conditions[i]=qx_conditions[k]
			ex_rain_amount[i]=qx_rain_amount[k]

for i in range(num):
	if ex_conditions[i]=='':
		for k in range(num1):
			if ex_province[i]==qx_province[k] and ex_city[i]==qx_city[k] and ex_date[i]==qx_date[k]:
				ex_wind_power[i]=qx_wind_power[k]
				ex_conditions[i]=qx_conditions[k]
				ex_rain_amount[i]=qx_rain_amount[k]

#存储多行与多列的数据集合
df=DataFrame({'bad_driving_time':Series(bad_driving_time),'bad_driving_lng':Series(bad_driving_lng),'bad_driving_lat':Series(bad_driving_lat),'bad_driving_name':Series(bad_driving_name),'bad_driving_info':Series(bad_driving_info),'ex_province':Series(ex_province),'ex_city':Series(ex_city),'ex_district':Series(ex_district),'ex_wind_power':Series(ex_wind_power),'ex_conditions':Series(ex_conditions),'ex_rain_amount':Series(ex_rain_amount)})
#存储为csv文件，并保存至相应文件夹
df.to_csv('E:\\data\\python_file\\bad_driving_exchange_csv_file\\AA00002_bd_ex.csv',index=False,encoding="utf_8_sig")