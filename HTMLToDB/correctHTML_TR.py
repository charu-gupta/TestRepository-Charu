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
    #print(">>>>>>>>>>>>>>>>",myfile.read())
    dataOrig=myfile.read()
    data = dataOrig.replace('\n', '')
    #print("data==> ", data)
    print("XXXXXXXXXXXXXXXXXXXXXXX --->> ", data.rfind("</form>"), len(data))
    print("YYYY", data.rfind("</form>", 0, 49259))
    print("40 letters",dataOrig[:40])
    startPos = 0
    endPos = len(data)
    index = 0
    print("endPos", endPos)
    #while startPos < len(data) and index != -1:
    indexTD = data.find("<b>PAN Number</b><label></td>", startPos, endPos)#"<td><label for="+'\"'+'\"'+"><b>PAN Number</b><label></td>"
    print("-----indexTD----",indexTD)
    if(indexTD != -1):
        indexEndTR = data.rfind("</tr",startPos, indexTD)
        indexStartTR = data.rfind("<tr",startPos, indexTD)
        if (indexStartTR < indexEndTR):
            print(indexStartTR,"<=indexStartTR,,,,INSERTing <TR> tag::::::::::::::::::indexEndTR=",indexEndTR," indexTD=",indexTD)
            print("===============>> ",dataOrig)
            dataOrig = "sgydwywb hweiwyyw"
            #myfile.seek(indexStartTR,0)
            #print("charuiiiii",myfile.read())
            #print("myfile bfr PAN ;;;",dataOrig[:indexTD])
            #print("myfile after PAN",myfile.read()[indexTD:indexTD+50])
            myfile.seek(0,0)
            myfile.writelines()
            myfile.write(dataOrig)

    print("--------------------------  START  -------------------------------")
    # print(index, "data ", len(data[index:]))
    # print("****************************  END  ********************************")
    # startPos = index + 1