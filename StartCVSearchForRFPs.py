#Original C:\AgilyticsCharu\PyExe-Charu\RFPQueries\testTupleLists.py
#Next file to include "C:\AgilyticsCharu\PyExe-Charu\Trials\storingRecords.py'
import MySQLdb
import yaml
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'RFPQueries')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.
from RFPQueries import QualificationResults as quali
from RFPQueries import ProjectResults as projects
from RFPQueries import sortingRecords as sortedData
from RFPQueries import writingToExcel as xl

cfg=yaml.load(open("config.yaml"))
# Open database connection
db = MySQLdb.connect(cfg['DB_HOST'],cfg['DB_USER'],cfg['DB_USER_PASSWORD'],cfg['DB_NAME'])
print("MEMMMMMMEE                MEEEEEEEEEEEEEEEEEEEEEEEEEEE")
print("GOOGOGOGGOGOGO")
import time
time.sleep(15)#15secs
print("helllllllllllllllllllllllloooooooooooo")
listConsultant=[]
listProjectConsultant=[]
listCurrCoConsultant=[]
listQualificationConsultant=[]

xlsFile = cfg['RFP_INPUT_OUTPUT_FILE']
print("xlaasssss",xlsFile)


listQualificationConsultant = quali.ftnGetQualificationResults(xlsFile, db )
print(":::CHARU:: after ftnGetQualificationResults", listQualificationConsultant)

listProjectConsultant = projects.ftnGetProjectResults(xlsFile,db)
print(":::CHARU>>>> listProjectConsultant:: after ftnGetProjectResults", listProjectConsultant)

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

while True:
    print("This prints once a minute.")
    time.sleep(60)   # Delay for 1 minute (60 seconds).
print("******************---------------------  END -------------------------------*******************")


