import MySQLdb
import glob
import codecs
from datetime import datetime
from dateutil import relativedelta
from bs4 import BeautifulSoup
import yaml
import re

cfg = yaml.load(open("../config.yaml"))

filepath = cfg['CV_FOLDER'] + "\\" + cfg['CV_FILEPATTERN']
print("path for basic CV-->> ", filepath)

arrFiles = glob.glob(filepath)

with open('C:\AgilyticsCharu\CVHunt_SA_6Feb18\CV Folder 7Feb2018\8340237203-Abhay Kumar-TL.html', 'r+') as myfile:
    for line in myfile:
        print(line)
    myfile.seek(0,0)
    print("XXXXXXXXXXXXXXXXXX  ",str(myfile.read()).find("PAN"),"88888=",str(myfile.read()).find("PAN")*8)
    myfile.seek(0, 0)
    print("DO ITITITITIT",myfile.seek(str(myfile.read()).find("PAN Number"),0))
    myfile.write("MY Name is CHARU---------------------")
    print("DONE DO ITITITITIT", myfile.seek(str(myfile.read()).find("PAN") , 0))
    #myfile.seek(0,0)
    #print(myfile.readlines().find("PAN"))
    print("STARTTTTTTTTTT   ",myfile.readlines(),"linesssssssssssssssss")