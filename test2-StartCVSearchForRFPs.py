#Original C:\AgilyticsCharu\PyExe-Charu\RFPQueries\testTupleLists.py
#Next file to include "C:\AgilyticsCharu\PyExe-Charu\Trials\storingRecords.py'

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'RFPQueries')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.

from RFPQueries import sortingRecords as sortedData
#from RFPQueries import writingToExcel as xl


print("MEMMMMMMEE                MEEEEEEEEEEEEEEEEEEEEEEEEEEE")
print("GOOGOGOGGOGOGO")
import time
time.sleep(15)#15secs
print("helllllllllllllllllllllllloooooooooooo")
listConsultant=[]
listProjectConsultant=[]
listCurrCoConsultant=[]
listQualificationConsultant=[]

xlsFile = 'C:\AgilyticsCharu\CVHunt_SA_6Feb18\CVSearch.xlsx'
print("xlaasssss",xlsFile)


#listQualificationConsultant = quali.ftnGetQualificationResults(xlsFile, db )
print(":::CHARU:: after ftnGetQualificationResults", listQualificationConsultant)

#listProjectConsultant = projects.ftnGetProjectResults(xlsFile,db)
print(":::CHARU>>>> listProjectConsultant:: after ftnGetProjectResults", listProjectConsultant)
listProjectConsultant = [(3, '2A', 22, 4, 'No. Of Projects (count)'), (3, '2B', 24, 5, 'No. Of Projects (count)'), (1, 3, 25, 11.523200035095215, 'in Years'), (2, 3, 20, 4.589000225067139, 'in Years'), (3, 3, 20, 4.69320011138916, 'in Years'), (5, 3, 20, 4.728799819946289, 'in Years'), (1, None, -1, 58.49850034713745, ''), (2, None, -1, 9.158900141716003, ''), (3, None, -1, 32.85240018367767, ''), (4, None, -1, 22.816400051116943, ''), (5, None, -1, 22.662999510765076, ''), (1, None, -1, 58.49850034713745, ''), (2, None, -1, 9.158900141716003, ''), (3, None, -1, 32.85240018367767, ''), (4, None, -1, 22.816400051116943, ''), (5, None, -1, 22.662999510765076, '')]
listQualificationConsultant = [(2, '1A', 21), (3, '1A', 21), (1, '1B', 3), (2, '1B', 3), (3, '1B', 3), (4, '1B', 3), (5, '1B', 3), (6, '1B', 3), (1, '1C', 1), (2, '1C', 1), (3, '1C', 1), (4, '1C', 1), (5, '1C', 1), (6, '1C', 1), (5, '1D', 7)]# id_consultant, RFPName, RFPMarks

listConsultant = sortedData.ftnGetSortedRecords(listQualificationConsultant, listProjectConsultant, listCurrCoConsultant)
print("FINAL:XXXXXXX       XXXXXXXXXXXXXXXXXXXXXXX:::::listConsultant",listConsultant)

#xl.ftnWriteRecordsToExcel(xlsFile,"RFP Results", listConsultant)
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


