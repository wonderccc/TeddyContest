import pandas as pd
import numpy as np
import os
import ways
from pandas import DataFrame
from pandas import Series
from pandas import to_datetime
import webbrowser
import vincent
from folium import plugins
import folium

posi=pd.read_csv("E:\data\csv_file\AA00002.csv")

num=posi.shape[0]    #读取的记录数目；

posi1=posi.drop_duplicates('location_time')        #将location_time列中重复值删除
#posi1.shape

posi1=posi1.reset_index(drop=True)       #去除重复值后重设索引
num1=posi1.shape[0]

lat = np.array(posi1["lat"][0:num1]) # 获取维度之维度值 
lng = np.array(posi1["lng"][0:num1]) # 获取经度值 
location_time=np.array(posi1["location_time"][0:num1])   #获取时间
mile_data=np.array(posi1["mileage"][0:num1])
data1 = [[lat[i],lng[i]] for i in range(num1)] #将数据制作成[lats,lngs]的形式，输入坐标点（注意）folium包要求坐标形式以纬度在前，经度在后
m = folium.Map([lat[0], lng[0]],zoom_start=8)
m.add_child(folium.LatLngPopup()) #在地图上显示经纬度；

posi2=pd.read_csv("E:\\data\\python_file\\bad_driving_exchange_csv_file\\AA00002_bd_ex.csv")
num2=posi2.shape[0]       #读取的记录行数

bad_driving_time = np.array(posi2["bad_driving_time"][0:num2]) # 获取数据采集时间
bad_driving_lat = np.array(posi2["bad_driving_lat"][0:num2]) # 获取维度之维度值 
bad_driving_lng = np.array(posi2["bad_driving_lng"][0:num2]) # 获取经度值 
bad_driving_name = np.array(posi2["bad_driving_name"][0:num2])
bad_driving_info = np.array(posi2["bad_driving_info"][0:num2])
ex_wind_power= np.array(posi2["ex_wind_power"][0:num2]) # 获取数据采集时间
ex_conditions = np.array(posi2["ex_conditions"][0:num2]) # 获取数据采集时间
ex_rain_amount = np.array(posi2["ex_rain_amount"][0:num2]) # 获取数据采集时间

route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
    data1,    #将坐标点连接起来
    weight=3,  #线的大小为3
    color='blue',  #线的颜色为橙色
    opacity=0.8    #线的透明度
).add_to(m)    #将这条线添加到刚才的区域m内

for i in range(num1):
    for k in range(num2):
        if location_time[i]==bad_driving_time[k]:
            str_info='时间：'+bad_driving_time[k]+'；    类型：'+bad_driving_name[k]+'；    详细信息：'+bad_driving_info[k]+';    风力级别：'+ex_wind_power[k]+';    天气状况：'+ex_conditions[k]+';    降水量：'+str(ex_rain_amount[k])
            
            folium.Marker(
                location=[lat[i], lng[i]],
                popup=folium.Popup(str_info, max_width=2650)
            ).add_to(m)
			
html_path=os.path.join('r','E:\\data\\python_file\\bad_driving_exchange_html_file','AA00002_bd_ex.html')
m.save(html_path)      #将结果以HTML形式保存
webbrowser.open(html_path,new = 1)
print('恭喜您，转换成功！','\n')