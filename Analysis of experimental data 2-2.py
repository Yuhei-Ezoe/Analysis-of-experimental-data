#!/usr/bin/env python
# coding: utf-8

# In[8]:


import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


#文字列を日付に変更
date_in = "181029"
date_out = "181106"
date_in_str = str(int(date_in) + 20000000)
date_out_str = str(int(date_out) + 20000000)

date_in_formatted = datetime.datetime.strptime(date_in_str, "%Y%m%d")
date_out_formatted = datetime.datetime.strptime(date_out_str, "%Y%m%d")


#必要な日付をリストに格納
date_list = []

#日付の計算
i = 0
while i < 100:
    if date_in_formatted != date_out_formatted + datetime.timedelta(days=1):
        
        date_list.append(date_in_formatted)
        date_in_formatted = date_in_formatted + datetime.timedelta(days=1)
        
    else:
        
        break
    
    i += 1

    
#日付をint型に変更
date_str = []
j = 0
while j < len(date_list):
    date_str.append(int(date_list[j].strftime("%Y%m%d"))-20000000)
    
    j += 1

    
#周波数を格納
F = np.arange(10, 210, 10)
F = np.append(F, 108)


#dfの作成
df = pd.DataFrame({"Wavelength_nm" : np.arange(550, 1700, 10)})

#WavelengthをPhoton Energy (eV)に変換し、Photon Energyの列を追加
df["Photon Energy_eV"] = 1239.8/df["Wavelength_nm"]


#txtファイルを読み込む
k = 0
while k < len(date_str):
    for n in F:
        
        flag = 0

        try:
            csv_input = pd.read_csv("***"+str(date_str[k])+"***"+str(n)+"***.txt", header=20)  

        except:
            flag = 1
            pass
        
        
        if flag == 0:
            #不要な列を削除
            num = np.arange(4, 10, 1)
            
            l = 0
            while l < len(num):
                csv_input.drop(["Unnamed: "+ str(num[l])], axis=1, inplace=True)
    
                l += 1
        
            #列名を変更 ([]が悪さをするため)
            csv_input.columns = ["Wavelength_nm", "Response_A/W", "Voltage_uV", "Phase_deg."]
                  
            #dfに列(Response)を追加
            df[n] = csv_input["Response_A/W"]
            
    k += 1
    

#列名を周波数順に変更
#列名の抜き出し及び並び替え
lst = df.columns.values
lst_num_only = np.delete(lst, [0, 1])
columns_nd_sorted = np.sort(lst_num_only)

#ndarrayをlistに変換
columns_list_sorted = columns_nd_sorted.tolist()


#x = 1.25(108Hz)で規格化

#新たなデータフレームを作成
Normalized_df = pd.DataFrame({"Wavelength_nm" : df["Wavelength_nm"],
                             "Photon Energy_eV" : df["Photon Energy_eV"]})

#波長990nm=約1.25eVのindexを取得
Peak_idx = Normalized_df.query("Wavelength_nm == 990").index[0]

#全ての周波数のResponseを規格化
c_num = 0
while c_num < len(columns_list_sorted):
    
    #x = 1.25eVのときの各周波数のResponseを取得
    Res_max = df[columns_list_sorted].iloc[Peak_idx, c_num]

    #規格化
    Normalized_Res = df[columns_list_sorted].iloc[:, c_num]/Res_max

    #データフレームに格納
    Normalized_df["Normalized: "+str(columns_list_sorted[c_num])+"Hz"] = Normalized_Res
    
    c_num += 1


#グラフの表示設定
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(1, 1, 1)

#グラフを作成
m = 2
while m < len(columns_list_sorted):
    
    #グラフにプロット
    ax.plot(Normalized_df["Photon Energy_eV"], Normalized_df.iloc[:, m], label="F="+str(columns_list_sorted[m])+"Hz")

    #x, yの値の範囲を設定
    ax.set_xlim([1, 1.5])
    ax.set_ylim([0, 5])    
    
    #軸ラベル
    ax.set_xlabel("Photon Energy (eV)", fontsize = 15)
    ax.set_ylabel("arb.unit.", fontsize = 15)
        
    #凡例表示
    ax.legend()
        
    m += 1
    
#グラフを保存
plt.savefig("***.jpg")    
    
#グラフを表示
plt.show()

#csvファイルとして保存
df[columns_list_sorted].to_csv("***.txt")


# In[ ]:




