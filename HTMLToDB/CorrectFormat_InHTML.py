#!/usr/bin/env python
import os
import sys
import fileinput
import re

def AddTRForPanTD(fileToSearch):
    textToSearch = "<td><label for="+'\"'+'\"'+"><b>PAN Number</b><label></td>"#"<b>PAN Number</b><label></td>"#input( "> " )
    textToReplace = "<tr><td><label for=\"\"><b>PAN Number</b><label></td>"
    #fileToSearch  = 'C:\AgilyticsCharu\CVHunt_SA_6Feb18\CV Folder 12Jan2018\8340237203-Abhay Kumar-TL.html'#input( "> " )

    tempFile = open( fileToSearch, 'r+', encoding="utf-8" )
    print("File CorrectFormat_InHTML.py Function AddTRForPAN fileToSearch====>>>", fileToSearch, "textToSearch==>>", textToSearch)
    #print(textToSearch,"texttosearch")
    for line in fileinput.input( fileToSearch, openhook=fileinput.hook_encoded("utf-8")):
        #print("File CorrectFormat_InHTML.py Function AddTRForPAN fileToSearch====>>>",fileToSearch, "line>>>>", line, "textToSearch==>>", textToSearch)
        tempFile.write(line.replace(textToSearch, textToReplace))
    tempFile.close()


def RemoveFormTag(fileToSearch):
    textToSearch = "\s*^(?:<form|</form).*?>"
    textToReplace = ""
    #fileToSearch  = 'C:\AgilyticsCharu\CVHunt_SA_6Feb18\CV Folder 12Jan2018\8340237203-Abhay Kumar-TL.html'#input( "> " )

    tempFile = open(fileToSearch, 'r+')
    print("File CorrectFormat_InHTML.py Function RemoveFormTag fileToSearch====>>>", fileToSearch, "textToSearch==>>",textToSearch)
    # print(textToSearch,"texttosearch")
    for line in fileinput.input(fileToSearch, openhook=fileinput.hook_encoded("utf8")):
        #print("File CorrectFormat_InHTML.py Function RemoveFormTag  fileToSearch====>>>",fileToSearch, "line>>>>", line, "textToSearch==>>", r'\s*^(?:<form|</form).*?>')
        #print("deere==> ",re.search(r'\s*^(?:<form|</form).*?>', line))
        if (re.search(r'\s*^(?:<form|</form).*?>', line) != None):
            #print("helllo")
            tempFile.write(re.sub(r'\s*^(?:<form|</form).*?>', textToReplace, line))
    tempFile.close()

def correctHTMLFormat(fileToSearch, textToSearch, textToReplace):
    tempFile = open(fileToSearch, 'r+')
    print("File CorrectFormat_InHTML.py Function AddTRForPAN fileToSearch====>>>", fileToSearch, "textToSearch==>>",
          textToSearch)
    for line in fileinput.input(fileToSearch, openhook=fileinput.hook_encoded("ISO-8859-1")):
        #print("File CorrectFormat_InHTML.py Function correctHTMLFormat  fileToSearch====>>>",fileToSearch, "line>>>>", line, "textToSearch==>>", textToSearch)
        tempFile.write(line.replace(textToSearch, textToReplace))
    tempFile.close()
