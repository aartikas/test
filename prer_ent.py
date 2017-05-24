#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:33:26 2017

@author: ilab
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:24:53 2017

@author: ilab
"""

import pandas as pd
import numpy as np


colnames = ['Question','target_class_qsid','entropy','pred_class1_qsid']
#data = pd.read_csv('/home/ilab/prerna_work/siamese_HIS_test.csv',names=colnames)
data = pd.read_csv('/home/ilab/prerna_work/RCNN_Leave_test.csv',names=colnames)
#colnames = ['year', 'name', 'city', 'latitude', 'longitude']

target = data.target_class_qsid.tolist()#entr
entropy= data.entropy.tolist()#pred
pred = data.pred_class1_qsid.tolist()#targer
 
 #entrophy.append(int(line_content[2]))


target_a=np.array(target)
ent=np.array(entropy)           
test_a=np.array(pred)
unique=np.unique(target_a)
fp=0.0
tp=0.0
tn=0.0
average_tp=[]
average_tn=[]
average_fp=[]
g_average_tp=[]
g_average_tn=[]
g_average_fp=[]

ths=[0.5,1,1.5,2,2.5,3,3.5,4]

#
for th in ths:
    print("threshold value:",th)
    average_tp=[]
    average_tn=[]
    average_fp=[]
    for p,i_uniq in enumerate(unique):
        print ("Class_id",i_uniq)
        indices = [i for i, x in enumerate(target_a) if x == i_uniq] 
        print(indices)
        tp=0
        tn=0
        fp=0
        
        for j in indices:
            #count=1
            
            if(target_a[j]==test_a[j] and ent[j]<th):
                 print(j,"test")
                 #tp.append(ent[j])
                 tp+=1
                 print("tp",tp)
            elif(target_a[j]==test_a[j] and ent[j]>=th):
                  print(j,"jtn")
                  tn+=1
                  print("tn",tn)
            elif(target_a[j]!=test_a[j] and ent[j]<th):
                  print(j,"jfp") 
                  fp+=1
            elif(target_a[j]!=test_a[j] and ent[j]>=th):
                  print(j,"jtn") 
                  tn+=1
                  print("tn",tn)
            #count+=1
    #    if(len(fp)>0):
    #        average_fp.append(sum(fp)/float(len(fp)))
    #    else:
    #       average_fp.append(0)
        print("indices",indices,"indiceslen",len(indices),"count_tp",tp,"count_tn",tn,"cpunt_fp",fp)
        if(tp>0):
            ans=float(tp) /len(indices)
            average_tp.append(ans)
            #print ("average_tp ",average_tp)
        else:
            average_tp.append(0.0)
        if(tn>0):
            #average_tn.append(float(tn/len(indices)))
             ans1=float(tn) /len(indices)
             average_tn.append(ans1)
            #print ("average_tn",average_tn)
        else:
            average_tn.append(0.0)
        if(fp>0):
             ans2=float(fp) /len(indices)
             average_fp.append(ans2)
            #average_fp.append(float(fp/len(indices)))

#            #print ("average_fp",average_fp)
        else:
            average_fp.append(0.0)
#        
        print ("average_fp",average_fp)
        print ("average_tp",average_tp)
        print ("average_tn",average_tn)
    
    
    print("avrge tpSum",sum(average_tp),"len unique",len(unique))
    print("avrge tnSum",sum(average_tn),"len unique",len(unique))
    print("avrge fpSum",sum(average_fp),"len unique",len(unique))
    g_average_tp.append(sum(average_tp)/len(unique))
    g_average_tn.append(sum(average_tn)/len(unique))
    g_average_fp.append(sum(average_fp)/len(unique))
#    
#import itertools
#for a, b, c in itertools.izip(g_average_tp, g_average_tn, g_average_fp):
#    g_average_tp=g_average_tp/float(len(ths))
#    g_average_tn=g_average_tn/float(len(ths))
#    g_average_fp=g_average_fp/float(len(ths))
#    

import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
g_average_fp=np.array(g_average_fp)

g_average_tp=np.array(g_average_tp)


g_average_tn=np.array(g_average_tn)

print(g_average_fp)
print(g_average_tp)
print(g_average_tn)



trace1 = go.Bar(
    x=[.5,1,1.5,2,2.5,3,3.5,4],
    y=[g_average_tp[0], g_average_tp[1], g_average_tp[2],g_average_tp[3],g_average_tp[4],g_average_tp[5],g_average_tp[6],g_average_tp[7]],
    name='True positive'
)
trace2 = go.Bar(
    x=[.5,1,1.5,2,2.5,3,3.5,4],
    y=[g_average_tn[0], g_average_tn[1], g_average_tn[2],g_average_tn[3],g_average_tn[4],g_average_tn[5],g_average_tn[6],g_average_tn[7]],
    name='True Negitive+false negative'
)
trace3 = go.Bar(
    x=[.5,1,1.5,2,2.5,3,3.5,4],
    y=[g_average_fp[0], g_average_fp[1], g_average_fp[2],g_average_fp[3],g_average_fp[4],g_average_fp[5],g_average_fp[6],g_average_fp[7]],
    name='False positive'
)

data = [trace1, trace3,trace2]
layout = go.Layout(
    barmode='stack'
    )
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='stacked-rnn')