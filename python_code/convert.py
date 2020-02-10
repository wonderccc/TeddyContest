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

def execute(file_path,file_name):
	section=input("请选择您想要进行的操作：")
	section=int(section)
	
	csv_path=os.path.join('r',file_path,file_name+'.csv')
	posi=pd.read_csv(csv_path)

	#posi=pd.read_csv("E:\data\AA00002.csv") 

	num=posi.shape[0]       #读取的记录行数
	
	posi1=posi.drop_duplicates('location_time')        #将location_time列中重复值删除
	posi1=posi1.reset_index(drop=True)       #去除重复值后重设索引
	num1=posi1.shape[0]     #读取去掉重复值后的记录数目

	lat = np.array(posi1["lat"][0:num1]) # 获取维度之维度值 
	lng = np.array(posi1["lng"][0:num1]) # 获取经度值 
	gps_speed = np.array(posi1["gps_speed"][0:num1]) #获取每一秒的速度，转换为数值
	acceleration_data = []
	for i in range(num1):
		if i==0:
			acceleration_data.append(0)    #第一秒的加速度设为0
		else:
			d=(gps_speed[i]-gps_speed[i-1])/3.6
			d=round(d,2)
			acceleration_data.append(d)      #获取每一秒的加速度
	mileage = np.array(posi1["mileage"][0:num1]) # 获取里程数
	direction_angle = np.array(posi1["direction_angle"][0:num1])       # 获取方向角，方向角指从定位点的正北方向起，以顺时针方向至行驶方向间的水平夹角
	direction_angle_v=[]
	for i in range(num1):
		if i==0:
			direction_angle_v.append(0)   #第一秒的方向角变化数设为0
		else:
			d2=direction_angle[i]-direction_angle[i-1]
			if d2>180 or d2<-180:
				if d2>180:
					direction_angle_v.append(360-d2)
				else:
					direction_angle_v.append(360+d2)
			else:
				if d2<0:
					direction_angle_v.append(-d2)
				else:
					direction_angle_v.append(d2)   #获取每一秒的方向角变化数
	acc_state = np.array(posi1["acc_state"][0:num1])     #获取acc状态，点火1/熄火0
	right_turn_signals = np.array(posi1["right_turn_signals"][0:num1]) # 获取右转向灯数据，灭0/开1 
	left_turn_signals = np.array(posi1["left_turn_signals"][0:num1]) # 获取左转向灯数据，灭0/开1
	hand_brake = np.array(posi1["hand_brake"][0:num1]) # 获取手刹数据，灭0/开1
	foot_brake = np.array(posi1["foot_brake"][0:num1]) # 获取脚刹数据，灭0/开1
	location_time = np.array(posi1["location_time"][0:num1]) # 获取数据采集时间
	vehicleplatenumber = np.array(posi1["vehicleplatenumber"][0:num1])
	vehicleplate_number=vehicleplatenumber[0]   #获取车辆车牌号码
	device_num = np.array(posi1["device_num"][0:num1])
	device_number=device_num[0]    #获取设备号

	map_data = [[lat[i],lng[i]] for i in range(num1)] #将数据制作成[lats,lngs]的形式，输入坐标点（注意）folium包要求坐标形式以纬度在前，经度在后
	
	posi1_dt=to_datetime(posi1.location_time,format='%Y/%m/%d %H:%M:%S')       #日期格式的转化
	posi1_second=posi1_dt.dt.second    #获取秒数
	posi1_minute=posi1_dt.dt.minute     #获取分钟数
	posi1_hour=posi1_dt.dt.hour      #获取小时数
	posi1_day=posi1_dt.dt.day       #获取天数

	if section==1:
		sum_speed=0
		count_speed=0
		for i in range(num1):
			if acc_state[i]==1:
				sum_speed+=gps_speed[i]
				count_speed+=1
		ave_speed=sum_speed/count_speed
		ave_speed=round(ave_speed,2)
		print(file_name+"的平均行车速度为："+str(ave_speed)+"km/h")      #计算车辆的平均行车速度
	if section==2:
		total_mile=mileage[num1-1]-mileage[0]
		print(file_name+"的行车里程为："+str(total_mile)+"km")
	if section==3:
		file_out_path=input("请输入转换后的html文件存储的位置（例如：E:\data\python_file\html_file）：")
		print("正在转换中，请稍等……")
		ways.show_route(map_data,lat[0],lng[0],vehicleplate_number,file_out_path)      #绘制车辆的行驶路线图，并保存为html文件
		print("恭喜您，转换成功！","\n")
	if section==4:
		file_out_path=input("请输入转换后的html文件存储的位置（例如：E:\data\python_file\html_file）：")
		print("正在转换中，请稍等……")
		ways.show_speed(map_data,lat[0],lng[0],vehicleplate_number,num1,gps_speed,lat,lng,location_time,file_out_path)   #在路线图上每60条记录处加一个标记点，点击标记点显示该时段内的速度变化折线图
		print("恭喜您，转换成功！","\n")
	if section==5:
		file_out_path=input("请输入转换后的html文件存储的位置（例如：E:\data\python_file\html_file）：")
		print("正在转换中，请稍等……")
		ways.show_acce(map_data,lat[0],lng[0],vehicleplate_number,num1,acceleration_data,lat,lng,location_time,file_out_path)   #在路线图上每60条记录处添加一个标记点，点击标记点显示该时段内的加速度变化折线图
		print("恭喜您，转换成功！","\n")
	if section==6:
		file_out_path=input("请输入转换后的csv文件存储的位置（例如：E:\data\python_file\bad_driving_csv_file）：")
		file_out2_path=input("请输入转换后的html文件存储的位置（例如：E:\data\python_file\bad_driving_html_file）：")
		print("正在转换中，请稍等……")
		
		bad_driving_time=[]
		bad_driving_lng=[]
		bad_driving_lat=[]
		bad_driving_name=[]
		bad_driving_info=[]

		for i in range(num1):
			if gps_speed[i]>100:
				bad_driving_time.append(location_time[i])
				bad_driving_lng.append(lng[i])
				bad_driving_lat.append(lat[i])
				bad_driving_name.append('超速')
				bad_driving_info.append('速度达到'+str(gps_speed[i])+'km/h,超过100km/h')     #判断超速并输出详细信息
			if acceleration_data[i]>3:
				bad_driving_time.append(location_time[i])
				bad_driving_lng.append(lng[i])
				bad_driving_lat.append(lat[i])
				bad_driving_name.append('急加速')
				bad_driving_info.append('加速度达到'+str(acceleration_data[i])+'m/s^2,超过3m/s^2')     #判断急加速并输出详细信息
			if acceleration_data[i]<-3:
				bad_driving_time.append(location_time[i])
				bad_driving_lng.append(lng[i])
				bad_driving_lat.append(lat[i])
				bad_driving_name.append('急减速')
				bad_driving_info.append('加速度达到'+str(acceleration_data[i])+'m/s^2,超过-3m/s^2')     #判断急减速并输出详细信息
			if acc_state[i]==0 and gps_speed[i]>0:
				bad_driving_time.append(location_time[i])
				bad_driving_lng.append(lng[i])
				bad_driving_lat.append(lat[i])
				bad_driving_name.append('熄火滑行')
				bad_driving_info.append('熄火后仍在前进')     #判断熄火滑行并输出详细信息
			if direction_angle_v[i]>30:
				bad_driving_time.append(location_time[i])
				bad_driving_lng.append(lng[i])
				bad_driving_lat.append(lat[i])
				bad_driving_name.append('急变道')
				bad_driving_info.append('方向角变化数为：'+str(direction_angle_v[i])+',超过30')     #判断急变道并输出详细信息
			if i!=0 and acc_state[i-1]==0 and acc_state[i]==1 and gps_speed[i]==0:
				for k in range(i,num1):
					status=k
					if gps_speed[k]>0:
						break
				time_status=posi1_second[status]+posi1_minute[status]*60+posi1_hour[status]*3600+posi1_day[status]*3600*24
				time_i=posi1_second[i]+posi1_minute[i]*60+posi1_hour[i]*3600+posi1_day[i]*3600*24
				time_d=time_status-time_i
				if time_d>120:
					bad_driving_time.append(location_time[i])
					bad_driving_lng.append(lng[i])
					bad_driving_lat.append(lat[i])
					bad_driving_name.append('怠速预热')
					bad_driving_info.append('怠速预热时长为'+str(time_d)+'秒,超过120秒')     #判断怠速预热并输出详细信息
			if i!=0 and acc_state[i]==1 and gps_speed[i-1]>0 and gps_speed[i]==0:
				for k in range(i,num1):
					status2=k
					if gps_speed[k]>0:
						break
				time_status2=posi1_second[status2]+posi1_minute[status2]*60+posi1_hour[status2]*3600+posi1_day[status2]*3600*24
				time_i=posi1_second[i]+posi1_minute[i]*60+posi1_hour[i]*3600+posi1_day[i]*3600*24
				time_d=time_status2-time_i
				if time_d>120:
					bad_driving_time.append(location_time[i])
					bad_driving_lng.append(lng[i])
					bad_driving_lat.append(lat[i])
					bad_driving_name.append('超长怠速')
					bad_driving_info.append('超长怠速时长为'+str(time_d)+'秒,超过120秒')     #判断超长怠速并输出详细信息
			if i!=0 and (gps_speed[i-1]>=30 or gps_speed[i-1]==0) and gps_speed[i]!=0 and gps_speed[i]<30:
				for k in range(i,num1):
					status3=k
					if gps_speed[k]>=30 or gps_speed[k]==0:
						break
				time_status3=posi1_second[status3]+posi1_minute[status3]*60+posi1_hour[status3]*3600+posi1_day[status3]*3600*24
				time_i=posi1_second[i]+posi1_minute[i]*60+posi1_hour[i]*3600+posi1_day[i]*3600*24
				time_d=time_status3-time_i
				if time_d>60:
					bad_driving_time.append(location_time[i])
					bad_driving_lng.append(lng[i])
					bad_driving_lat.append(lat[i])
					bad_driving_name.append('长时间低速行驶')
					bad_driving_info.append('长时间低速行驶时长为'+str(time_d)+'秒,超过60秒')     #判断长时间低速行驶并输出详细信息
			if i!=0 and acc_state[i-1]==0 and acc_state[i]==1:
				for k in range(i,num1):
					status4=k
					
					if acc_state[k]==0:
						for n in range(k,num1):
							status5=n
							if acc_state[n]==1:
								break
						time_status5=posi1_second[status5]+posi1_minute[status5]*60+posi1_hour[status5]*3600+posi1_day[status5]*3600*24
						time_k=posi1_second[k]+posi1_minute[k]*60+posi1_hour[k]*3600+posi1_day[k]*3600*24
						time_d=time_status5-time_k
						if time_d>=1200:       #判断中间休息时间是否大于等于20分钟
							break
					
				time_status4=posi1_second[status4]+posi1_minute[status4]*60+posi1_hour[status4]*3600+posi1_day[status4]*3600*24
				time_i=posi1_second[i]+posi1_minute[i]*60+posi1_hour[i]*3600+posi1_day[i]*3600*24
				time_d=time_status4-time_i
				if time_d>=14400:     #判断连续驾驶时间是否大于等于4个小时
					bad_driving_time.append(location_time[i])
					bad_driving_lng.append(lng[i])
					bad_driving_lat.append(lat[i])
					bad_driving_name.append('疲劳驾驶')
					bad_driving_info.append('疲劳驾驶时长为'+str(time_d)+'秒,超过14400秒')     #判断疲劳驾驶并输出详细信息
		
		df=DataFrame({'bad_driving_time':Series(bad_driving_time),'bad_driving_lng':Series(bad_driving_lng),'bad_driving_lat':Series(bad_driving_lat),'bad_driving_name':Series(bad_driving_name),'bad_driving_info':Series(bad_driving_info)})
		csv_path=os.path.join('r',file_out_path, vehicleplate_number+'_bd.csv')
		df.to_csv(csv_path,index=False,encoding="utf_8_sig")
		
		m = folium.Map([lat[0], lng[0]],zoom_start=8)
		m.add_child(folium.LatLngPopup()) #在地图上显示经纬度；

		posi2=pd.read_csv(csv_path)
		num2=posi2.shape[0]       #读取的记录行数

		bad_driving_time = np.array(posi2["bad_driving_time"][0:num2]) # 获取数据采集时间
		bad_driving_lat = np.array(posi2["bad_driving_lat"][0:num2]) # 获取维度之维度值 
		bad_driving_lng = np.array(posi2["bad_driving_lng"][0:num2]) # 获取经度值 
		bad_driving_name = np.array(posi2["bad_driving_name"][0:num2])
		bad_driving_info = np.array(posi2["bad_driving_info"][0:num2])

		route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
			map_data,    #将坐标点连接起来
			weight=3,  #线的大小为3
			color='blue',  #线的颜色为橙色
			opacity=0.8    #线的透明度
		).add_to(m)    #将这条线添加到刚才的区域m内

		for i in range(num1):
			for k in range(num2):
				if location_time[i]==bad_driving_time[k]:
					str_info='时间：'+bad_driving_time[k]+'；    类型：'+bad_driving_name[k]+'；    详细信息：'+bad_driving_info[k]
					
					folium.Marker(
						location=[lat[i], lng[i]],
						popup=folium.Popup(str_info, max_width=2650)
					).add_to(m)
		html_path=os.path.join('r',file_out2_path, vehicleplate_number+'_bd.html')
		m.save(html_path)      #将结果以HTML形式保存
		webbrowser.open(html_path,new = 1)
		print('恭喜您，转换成功！','\n')
	
	con_quit_a=input("请选择您接下来的操作（按q退出程序，按c继续操作）：")
	return con_quit_a

