import os
import sys
import fileinput
import re


textToSearch = "<td><label for="+'\"'+'\"'+"><b>PAN Number</b><label></td>"#"<b>PAN Number</b><label></td>"#input( "> " )
textToReplace = "<tr><td><label for=\"\"><b>PAN Number</b><label></td>"
fileToSearch  = 'C:\AgilyticsCharu\CVHunt_SA_6Feb18\CV Folder 7Feb2018\8340237203-Abhay Kumar-TL.html'#input( "> " )

tempFile = open(fileToSearch, 'r+')

# print(textToSearch,"texttosearch")
for line in fileinput.input(fileToSearch):
    print(line, "line<<-- both _________>>>>", re.search(r'\s*^(?:<form|</form).*?>', line))
    tempFile.write(line.replace(textToSearch, textToReplace))
    #tempFile.write(re.sub(r'\s*^(?:<form|</form).*?>', "", line))
tempFile.close()
