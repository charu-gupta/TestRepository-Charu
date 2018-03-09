#Original C:\AgilyticsCharu\PyExe-Charu\RFPQueries\testTupleLists.py
#Next file to include "C:\AgilyticsCharu\PyExe-Charu\Trials\storingRecords.py'
import MySQLdb
#import yaml
import sys, os
import configparser
import tkinter
sys.path.append(os.path.join(os.path.dirname(__file__), 'RFPQueries')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.
from RFPQueries import QualificationResults as quali
from RFPQueries import ProjectResults as projects
from RFPQueries import CompanyResults as cmpy
from RFPQueries import sortingRecords as sortedData
from RFPQueries import writingToExcel as xl
cfg = configparser.RawConfigParser()
#config.read('example.cfg')
cfg.read("config.cfg")


#cfg=yaml.load(open("config.yaml"))
# Open database connection
db = MySQLdb.connect(cfg.get('General', 'DB_HOST'),cfg.get('General', 'DB_USER'),cfg.get('General', 'DB_USER_PASSWORD'),cfg.get('General', 'DB_NAME'))
print("MEMMMMMMEE                MEEEEEEEEEEEEEEEEEEEEEEEEEEE")
print("GOOGOGOGGOGOGO")
print("helllllllllllllllllllllllloooooooooooo")
listConsultant=[]
listProjectConsultant=[]
listCurrCoConsultant=[]
listQualificationConsultant=[]

xlsFile = cfg.get('General','RFP_INPUT_OUTPUT_FILE')
print("xlaasssss",xlsFile)


listQualificationConsultant = quali.ftnGetQualificationResults(xlsFile, db )
print(":::CHARU:: after ftnGetQualificationResults", listQualificationConsultant)

listProjectConsultant = projects.ftnGetProjectResults(xlsFile,db)
print(":::CHARU>>>> listProjectConsultant:: after ftnGetProjectResults", listProjectConsultant)

listCurrCoConsultant = cmpy.ftnGetCurrCompanyResults(xlsFile,db)
print(":::CHARU24-Feb>>>> listCurrCoConsultant:: after ftnGetCurrCompanyResults", listCurrCoConsultant)

listConsultant = sortedData.ftnGetSortedRecords(listQualificationConsultant, listProjectConsultant, listCurrCoConsultant)
print("FINAL:XXXXXXX       XXXXXXXXXXXXXXXXXXXXXXX:::::listConsultant",listConsultant)

xl.ftnWriteRecordsToExcel(xlsFile,"RFP Results", listConsultant)
print("----------------------*** CVHunt_SA ***----------------------------")
print("Information:::: The RFP Result has been published in the xls at location", xlsFile)

print("This is TEST FILE FOR PyInsatller")
print("= ++++                +++++++++++++++++++++         ++++++++++++++             +++")
print("******************---------------------  testFile.py -------------------------------*******************")
print("******************---------------------  testFile.py -------------------------------*******************")
print("******************---------------------  testFile.py -------------------------------*******************")
print("******************---------------------  testFile.py -------------------------------*******************")
print("******************---------------------  testFile.py -------------------------------*******************")
print("= ++++                +++++++++++++++++++++         ++++++++++++++             +++")

input("Press any key to exit!!")
