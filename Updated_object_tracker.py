# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 01:33:17 2020

@author: Hitesh
"""
import cv2
import numpy as np
import os

def dist(x1,y1,x2,y2):
    d=(x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
    return d 

def obupdate(objects,newcent):
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #print(objects)
    #print(newcent)
    #print(len(objects),len(newcent))
    news=[0,0,0]*len(objects)
    for x in range(0,len(newcent)):
        corr=len(objects)
        x1,y1=newcent[x][1],newcent[x][2]
        d=[0]*len(objects)
        for y in range (0,len(objects)):
            #print(y)
            x2,y2=objects[y][1],objects[y][2]
            d[y]=dist(x1,y1,x2,y2)
            #print(x2,y2,x1,y1,d[y])
        din=min(d)
        index=d.index(din)
        #print(din,index)
        if din<4000 and (y1>y2-20) :#din changed fron 500 to 10000
            #print("old:",objects[index][1:],"   NEW:",newcent[x][1:],"   Dist:",din)
            objects[index]=([index,newcent[x][1],newcent[x][2]])
        else:
            #print()
            #print("HERE",corr,x1,y1)
            objects.append([corr,x1,y1])
    
    #objects= sorted(objects, key=lambda x:x[1])
    #print(objects)
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return objects


path=cv2.VideoCapture('vids/track3.mp4')
time=0
cent=[[]*3]

""" TESTING """
prelen=0
init=1
start=1
allobs=[]
oldie=[]
objects=[]
oldobs=[]
frame0=cv2.imread('vids/track3data/white.jpg')
cv2.imshow("",frame0)
while time<15 :  
    newcent=[]
    ret,frame1=path.read()
    ret,frame2=path.read()
    diff=cv2.absdiff(frame1,frame2)
    #cv2.imshow("1",frame1)
    #cv2.imshow("2",frame2)
    ntnt=cent
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    name='./vids/track3data/d2/frame'+str(time)+'.jpg'
    name0='./vids/track3data/d0/frame'+str(time)+'.jpg'
    prevlen=len(cent)
    #print(prevlen)
    print("################",time)
    #print(oldie)
    k=0
    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour)<900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.rectangle(frame0, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cent.append([time,x+0.5*w,y+0.5*h])
        newcent.append([time,x+0.5*w,y+0.5*h])
        #print([time,x+0.5*w,y+0.5*h])
        if(time==0):
            #print("aye")
            objects.append([k,x+0.5*w,y+0.5*h])
            k=k+1
        cv2.rectangle(frame1,(x+int(0.45*w),y+int(0.45*h)),(x+int(0.55*w),y+int(0.55*h)),(0,0,255),5)
        #cv2.rectangle(frame0,(x+int(0.45*w),y+int(0.45*h)),(x+int(0.55*w),y+int(0.55*h)),(0,0,255),5)
    #print("old object",objects)
    #print(newcent)
    if(time!=0):
        objects=obupdate(objects,newcent)
        init=0
    #print(time)
    #print("11111111111111111111",oldobs)
    #print("22222222222222222222",objects)
    for k in objects:
        
        idout="Object"+str(k[0])
        x=int(k[1]-20)
        y=int(k[2]-10)
        index=k[0]
        #print(k)
        """
        for l in oldobs:
            if(k==l):
                #print(l)
                continue
            
        """
        print("HI",k)
        text="object"+str(k[0])
        #cv2.putText(frame1,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0,),1) 
        cv2.putText(frame1,idout.format('Moverment'),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0,),1)   
        #cv2.putText(frame0,idout.format('Moverment'),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0,),1)
        
   
    
    
    cv2.imwrite(name,frame1)
    time=time+1
    i=0
    oldobs=objects.copy()
    
cv2.destroyAllWindows()