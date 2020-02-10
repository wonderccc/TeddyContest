from folium import plugins
import folium
import os
import json
import vincent
import webbrowser


def show_route(map_data_p,lat0_p,lng0_p,vehicleplate_number_p,file_out_path_p):
	m = folium.Map([lat0_p, lng0_p],zoom_start=8)

	m.add_child(folium.LatLngPopup())     #在地图上显示经纬度
	
	route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
	map_data_p,    #将坐标点连接起来
	weight=3,  #线的大小为3
	color='blue',  #线的颜色为橙色
	opacity=0.8    #线的透明度
	).add_to(m)    #将这条线添加到刚才的区域m内
	
	html_path=os.path.join('r',file_out_path_p, vehicleplate_number_p+'_route.html')
	m.save(html_path)      #将结果以HTML形式保存
	webbrowser.open(html_path,new = 1)
	
def show_speed(map_data_p,lat0_p,lng0_p,vehicleplate_number_p,num1_p,gps_speed_p,lat_p,lng_p,location_time_p,file_out_path_p):
	m = folium.Map([lat0_p, lng0_p],zoom_start=8)

	m.add_child(folium.LatLngPopup()) #在地图上显示经纬度；
	
	route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
	map_data_p,    #将坐标点连接起来
	weight=3,  #线的大小为3
	color='blue',  #线的颜色为橙色
	opacity=0.8    #线的透明度
	).add_to(m)    #将这条线添加到刚才的区域m内
	
	for i in range(num1_p):
		if i!=0 and i%59==0:
			y_data=[int(gps_speed_p[j]) for j in range(i-59,i+1,1)]
			vis = vincent.Line(y_data,width=320,height=150)
			vis.axis_titles(x=location_time_p[i-59]+'至'+location_time_p[i]+'的速度变化', y='单位：km/h')
			vis_json=vis.to_json()
			tooltip=location_time_p[i-59]+'至'+location_time_p[i]
			
			status=0
			for k in range(i-59,i+1):
				if gps_speed_p[k]>100:
					status=1
			
			if status==1:
				folium.Marker(location=[lat_p[i],lng_p[i]],popup=folium.Popup(max_width=3250).add_child(
				folium.Vega(vis_json, width=380, height=200)),icon=folium.Icon(color='red', icon='info-sign'),tooltip=tooltip).add_to(m)      #在每60条记录处显示一个标记点,且点击标记点可以看到过去的60条记录内车辆的速度变化折线图
			else:
				folium.Marker(location=[lat_p[i],lng_p[i]],popup=folium.Popup(max_width=3250).add_child(
				folium.Vega(vis_json, width=380, height=200)),tooltip=tooltip).add_to(m)      #在每60条记录处显示一个标记点,且点击标记点可以看到过去的60条记录内车辆的速度变化折线图
	
	html_path=os.path.join('r',file_out_path_p, vehicleplate_number_p+'_speed.html')
	m.save(html_path)      #将结果以HTML形式保存
	webbrowser.open(html_path,new = 1)
	
def show_acce(map_data_p,lat0_p,lng0_p,vehicleplate_number_p,num1_p,acceleration_data_p,lat_p,lng_p,location_time_p,file_out_path_p):
	m = folium.Map([lat0_p, lng0_p],zoom_start=8)

	m.add_child(folium.LatLngPopup()) #在地图上显示经纬度；
	
	route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
	map_data_p,    #将坐标点连接起来
	weight=3,  #线的大小为3
	color='blue',  #线的颜色为橙色
	opacity=0.8    #线的透明度
	).add_to(m)    #将这条线添加到刚才的区域m内
	
	for i in range(num1_p):
		if i!=0 and i%59==0:
			y_data=[acceleration_data_p[j] for j in range(i-59,i+1,1)]
			vis = vincent.Line(y_data,width=320,height=150)
			vis.axis_titles(x=location_time_p[i-59]+'至'+location_time_p[i]+'的加速度变化', y='单位：m/s^2')
			vis_json=vis.to_json()
			tooltip=location_time_p[i-59]+'至'+location_time_p[i]
			
			status=0
			for k in range(i-59,i+1):
				if acceleration_data_p[k]>3 or acceleration_data_p[k]<-3:    #判断加速度
					status=1
			
			if status==1:
				folium.Marker(location=[lat_p[i],lng_p[i]],popup=folium.Popup(max_width=3250).add_child(
				folium.Vega(vis_json, width=380, height=200)),icon=folium.Icon(color='red', icon='info-sign'),tooltip=tooltip).add_to(m)      #在每60条记录处显示一个标记点,且点击标记点可以看到过去60条记录内车辆的加速度变化折线图速度变化折线图
			else:
				folium.Marker(location=[lat_p[i],lng_p[i]],popup=folium.Popup(max_width=3250).add_child(
				folium.Vega(vis_json, width=380, height=200)),tooltip=tooltip).add_to(m)      #在每60条记录处显示一个标记点,且点击标记点可以看到过去的60条记录内车辆的加速度变化折线图速度变化折线图
	
	html_path=os.path.join('r',file_out_path_p, vehicleplate_number_p+'_acceleration.html')
	m.save(html_path)      #将结果以HTML形式保存
	webbrowser.open(html_path,new = 1)
	
	