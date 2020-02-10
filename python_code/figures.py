import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

posi=pd.read_csv("E:\data\csv_file\AF00373.csv")

num=posi.shape[0]       #读取的记录行数

lat = np.array(posi["lat"][0:num]) # 获取维度之维度值 
lng = np.array(posi["lng"][0:num]) # 获取经度值 

plt.plot(lng,lat)       #利用matplotlib绘制大致的路线图像

plt.savefig('E:\data\python_file\images\AF00373.jpg',dpi = 900)     #保存图像文件