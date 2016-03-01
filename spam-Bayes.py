# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 21:00:21 2016

@author: nju-hyhb
"""
from __future__ import division 
from numpy import *
from os import listdir
import re
 

def file2list(filename):
    fr=open(filename)
    ftext=fr.read()
    textlist=re.split('\W*',ftext)
    returnList=[strr.lower() for strr in textlist if len(strr)>2]
    return returnList

def dataClection(dir1,k):
    Data=[]
    Labels=[]
    hamList=listdir(dir1)
    hamSize=len(hamList)
    for index in range(hamSize):
        filename=hamList[index]
        listOffile=file2list('%s' % dir1+'\/'+filename)    
        Data.append(listOffile)
        if label ==3:
            Labels.append(int(filename.split('_')[0]))
        else:
            Labels.append(k)
    return Data,Labels
    
def creatStrList(Data):
    ListSet=set([])
    for line in Data:
        ListSet=ListSet | set(line)
    return list(ListSet)

def str2Matrix(Data):
    global strList
    strList=creatStrList(Data)
    cols=len(strList)
    rows=size(Data)
    returnMatrix=zeros((rows,cols))
    for row in range(rows):
        for strr in Data[row]:
            returnMatrix[row,strList.index(strr)]+=1
    return returnMatrix
    
def str2Matrix_test(Data,traingData,cols):
    #strList=creatStrList(traingData)
    rows=size(Data)
    returnMatrix=zeros((rows,cols))
    for row in range(rows):
        for strr in Data[row]:
            if strr in strList:
                returnMatrix[row,strList.index(strr)]+=1
    return returnMatrix
    
def spamTraining(Data,Labels):
    length=len(Data[0])
    Num1=ones(length)
    Num2=ones(length)
    rowLen=len(Data)
    pSpam=1-sum(Labels)/len(Labels)
    for row in range(rowLen):
        if Labels[row]==1:
            Num1+=Data[row]
        else:
            Num2+=Data[row]
    numT1=sum(Num1)+2;numT2=sum(Num2)+2
    p1V=log(Num1/numT1)
    p0V=log(Num2/numT2)
    return p1V,p0V,pSpam  
    
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass0):
    p1 = sum(vec2Classify * p1Vec) + log(1.0-pClass0)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(pClass0)
    if p1 > p0:
        return 1
    else: 
        return 0


trainingData=[]
trainingLabels=[]

dir1='ham';label=1
trainingDataham,trainingLabelsham=dataClection(dir1,label)
trainingData.extend(trainingDataham)
trainingLabels.extend(trainingLabelsham)

dir1='spam';label=0
trainingDataSpam,trainingLabelsSpam=dataClection(dir1,label)
trainingData.extend(trainingDataSpam)
trainingLabels.extend(trainingLabelsSpam)

strMatrix=str2Matrix(trainingData)

p1V,p0V,pSpam=spamTraining(strMatrix,trainingLabels)


testData=[]
testLabel_ori=[]    # The labels of the test mail,which is not defined yet
classVerified=[]
dir1='test';label=3          # The dir of the test mail, and the test label 3
testData,testLabels=dataClection(dir1,label)
testMatrix=str2Matrix_test(testData,trainingData,size(strMatrix[0]))

for row in range(len(testMatrix)):
    classVerified.append(classifyNB(testMatrix[row], p0V, p1V, pSpam))
count=0
for i in range(size(testLabels)):
    if testLabels[i] != classVerified[i] :
        count+=1
     
print 'The error rate is: %s %%' % (100*count/(size(testLabels)))

    

    











