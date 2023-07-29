import numpy as np
import matplotlib.pyplot as plt

"""
把txt重新輸出成一張map +各個不同參數的npz檔案
可以仿造其他機器學習呼叫的模式
"""
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

import re
import matplotlib.pyplot as plt
import numpy as np

def detect_peaks(image):

    neighborhood = generate_binary_structure(2,2)
    local_max = maximum_filter(image, footprint=neighborhood)==image
    background = (image==0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    detected_peaks = local_max ^ eroded_background

    return detected_peaks,np.where(detected_peaks)

f= open('Map_0119.txt')
f1  = open('variable_0120.txt')

text,text1 = [],[]
for line in f:
    text.append(line)

for line in f1:
    text1.append(line)
E= 0
n,n1,n2,n3,n4=[],[],[],[],[]
E_total,Map_total,region25,region21,z0_total_list,z1_total_list=[],[],[],[],[],[]
gamma0E,gamma0MCE,gamma1E,gamma1MCE = [],[],[],[]
M_list,M0,M1,M0_sum,M1_sum=[],[],[],[],[]
d= 0
M0_21=[]
for N in range(1142696):
    try:
        x,y,z,z_copy=[],[],[],[]
        for i in range(len(text[N].split())):
            t  = text[N].split()[i]
            x.append(int(t.split(",")[0].split("(")[1]))
            y.append(int(t.split(",")[1]))

            z.append(float(t.split(",")[2].split(")")[0]))
            z_copy.append(float(t.split(",")[2].split(")")[0]))
            
        M = np.zeros((27, 50))
        for i in range(len(x)):
            M[x[i]][y[i]]=z[i]
        M_list.append(M)
        z_copy.sort()
        particle0=z_copy[-1]
        particle1=z_copy[-2]
        m0 = np.zeros((27, 50))
        m1 = np.zeros((27, 50))

        
        x1_p=detect_peaks(M)[1][0][0]
        y1_p=detect_peaks(M)[1][1][0]
        try:
            x2_p=detect_peaks(M)[1][0][1]
            y2_p=detect_peaks(M)[1][1][1]
        except:
            x2_p=x1_p
            y2_p=y1_p
        try:
            x3_p=detect_peaks(M)[1][0][2]
            y3_p=detect_peaks(M)[1][1][2]
            z_p=[M[x1_p][y1_p],M[x2_p][y2_p],M[x3_p][y3_p]]
        except:
            z_p=[M[x1_p][y1_p],M[x2_p][y2_p]]
        z_p.sort()
        particle0_p=z_p[-1]
        particle1_p=z_p[-2]
        x0_p=int(np.where(M==particle0_p)[0])
        x1_p=int(np.where(M==particle1_p)[0])   
        y0_p=int(np.where(M==particle0_p)[1])
        y1_p=int(np.where(M==particle1_p)[1])
        
        distance=((x0_p-x1_p)**2+(y0_p-y1_p)**2)**0.5
        E = text1[N].split()[0]
        E_total.append(float(E))
        
        if float(text1[N].split()[2])>=float(text1[N].split()[4]):
            gamma0E.append(float(text1[N].split()[1]))
            gamma0MCE.append(float(text1[N].split()[2]))
            gamma1E.append(float(text1[N].split()[3]))
            gamma1MCE.append(float(text1[N].split()[4]))
        if float(text1[N].split()[2])<float(text1[N].split()[4]):
            gamma1E.append(float(text1[N].split()[1]))
            gamma1MCE.append(float(text1[N].split()[2]))
            gamma0E.append(float(text1[N].split()[3]))
            gamma0MCE.append(float(text1[N].split()[4]))
    
        center_x_p=int((np.where(M==particle0_p)[0]+np.where(M==particle1_p)[0])*1/2)
        center_y_p=int((np.where(M==particle0_p)[1]+np.where(M==particle1_p)[1])*1/2)

        m0_21 = np.zeros((21,21))
        k=0
        for i in range(center_x_p-10,center_x_p+11):
            l=0
            for j in range(center_y_p-10,center_y_p+11):
                try:
                    m0_21[k][l]=M[i][j]
                except:
                    m0_21[k][l]=0
                l+=1
            k+=1

        M0_21.append(m0_21)


    except:
        pass

np.savez('Gamma_Map.npz', M0_21=M0_21,gamma0E=gamma0E,gamma1E=gamma1E,gamma0MCE=gamma0MCE,gamma1MCE=gamma1MCE)


