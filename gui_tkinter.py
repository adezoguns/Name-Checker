#!/usr/bin/env python3

from Tkinter import *
import tkFileDialog
#import sqlite3 as lite
import csv
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

root= None

#data=pd.read_excel("/home/deola/Documents/Gustav/A_training data.xlsx")
data=pd.read_excel("Gustav2.xlsx")

    
def check():
    
    global data

    data=pd.DataFrame(data)
    txt= textField.get()  
    vect = CountVectorizer(analyzer="char",
                             lowercase=True,
                             max_features=None,
                             ngram_range=(1, 3))
    vect.fit(data['name'])
    
    if txt !=None and txt!="":

        sample=vect.transform([txt])
        
        nameModel = pickle.load(open("vector.pickel", "rb"))

        if (nameModel.predict(sample)[0])==0:
            label1.config(text="A name")
        else:
            label1.config(text="Not a name")
    else:
        label1.config(text="Enter a word!")
    
def select_file():
    
    global data
    data=pd.DataFrame(data)
    
    root.filename = tkFileDialog.askopenfilename(initialdir = "/home/deola/Document",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    #print (root.filename[:-4])
    dataInput=pd.read_csv(root.filename)
    dataInput.to_csv(root.filename[:-4]+"New.csv",index=None)
    
#    dataInput=dataInput.values
#    print(dataInput[:2,0:1])
    #print (dataInput)
    results = []
    with open(root.filename, 'rb') as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        #next(reader, None)
        for row in reader: # each row is a list
            results.append(row)
        results.pop(0)
    print results
    
    
    vect = CountVectorizer(analyzer="char",
                             lowercase=True,
                             max_features=None,
                             ngram_range=(1, 3))
    nameModel = pickle.load(open("vector.pickel", "rb"))

    vect.fit(data['name'])
    
    tempArr=list()
    finalArr=list()
    for row in results:
        #for element in row:
        #print(element)
        #vect.transform([str(row[0])])
        if (nameModel.predict(vect.transform([str(row[0])]))[0])==0:
            tempArr.append(0)
        else:
            tempArr.append(1)
        if (nameModel.predict(vect.transform([str(row[1])]))[0])==0:
            tempArr.append(0)
        else:
            tempArr.append(1)
        finalArr.append(tempArr)
        tempArr=list()
        
    print finalArr
    
    
    dataInput=pd.read_csv(root.filename[:-4]+"New.csv")
    '''Putting Is_record_generic'''
    tempName=list()
    tempSurname=list()
    for row in finalArr:
        tempName.append(row[0])
        tempSurname.append (row[1])
    dataInput["Is_name_generic"]= tempName
    dataInput["Is_surname_generic"]= tempSurname
    
    
    tempRecordArr=list()
    recordArr=list()
    for row in finalArr:
        
        if row[0] ==row[1] and row[0]==1 and row[1]==1:
            tempRecordArr.append(1)
        else:
            tempRecordArr.append(0)
        recordArr.append(tempRecordArr)
        tempRecordArr=list()
            
    print   recordArr  
    
    #dataInput=pd.read_csv(root.filename[:-4]+"New.csv")
    '''Putting Is_record_generic'''
    
    for row in recordArr:
        for element in row:
            tempRecordArr.append(element)
        
    dataInput["Is_record_generic"]=tempRecordArr
    #print dataInput
    dataInput.to_csv(root.filename[:-4]+"New.csv",index=None)
    label1.config(text="New csv created")
    

   
    
root=Tk()
root.title("Name Checker")

frame1=Frame(root)
frame2=Frame(root)
frame3=Frame(root)
#frame4=Frame(root)

frame1.pack(side=LEFT)
frame2.pack(side=LEFT)
frame3.pack(side=RIGHT)
#frame4.pack(side=BOTTOM)

Firstname = Label(frame1, text="Enter name", bg="gold", height=2, width=10 )
Firstname.pack(side=TOP)

outputName = Label(frame1, text="Output", bg="green", height=2, width=10 )
outputName.pack(side=TOP)


myButton1 = Button(frame3, text="Check name", command=check)
myButton1.pack(side=TOP)
   	
   
myButton = Button(frame3, text="Select csv file", command=select_file)
myButton.pack( side=TOP)
 

#FirstnameTextBox(frame2)
textField=Entry(frame2, width=19, takefocus=True)
textField.bind('<Return>', Check) 
textField.pack(side=TOP)
label1=Label(frame2, text="", bg="white", height=2, width=20 )
label1.pack()
#SurnameTextBox(frame2)

root.resizable(False, False)
root.mainloop()

