import MySQLdb
import glob
import codecs
from datetime import datetime
from dateutil import relativedelta
from bs4 import BeautifulSoup
import yaml
import re



cfg = yaml.load(open("../config.yaml"))

filepath=cfg['CV_FOLDER']+"\\"+cfg['CV_FILEPATTERN']
print("path for basic CV-->> ",filepath)

arrFiles=glob.glob(filepath)
#for file in arrFiles:
    #with open(file) as f:
    #     print("word---",(word for line in f for word in re.findall(r'\w+', line)))
    #     str(f).find_all("<tr>")
    #     #print()

        # for line in f:
        #     print("line==",line)
        #     #for word in re.findall(r'\w+', line):
        #         #print("word by word", word)


with open('C:\AgilyticsCharu\CVHunt_SA_6Feb18\CV Folder 7Feb2018\8340237203-Abhay Kumar-TL.html', 'r') as myfile:
    data=myfile.read().replace('\n', '')
    print("data==> ",data)
    print("XXXXXXXXXXXXXXXXXXXXXXX --->> ",data.rfind("</form>"),len(data))
    print("YYYY",data.rfind("</form>", 0,49259))
    # for "</form>" in data:
    #     print()

    startPos = 0
    endPos = len(data)
    index = 0
    print("endPos", endPos)
    while endPos > 0 and index != -1:
        index = data.rfind("</form", startPos, endPos)
        print("--------------------------  START  -------------------------------")
        print(index, "</form ", len(data[:index]))
        print("****************************  END  ********************************")
        endPos = index - 1

    startPos=0
    endPos = len(data)
    index =0
    print("endPos",endPos)
    while startPos < len(data) and index != -1:
        index = data.find("<form", startPos, endPos)
        print("--------------------------  START  -------------------------------")
        print(index,"data ",len(data[index:]))
        print("****************************  END  ********************************")
        startPos = index + 1