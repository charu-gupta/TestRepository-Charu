import MySQLdb
import glob
import codecs
from datetime import datetime
from dateutil import relativedelta
from bs4 import BeautifulSoup
import yaml
import sys
import re
cfg = yaml.load(open("config.yaml"))
#headings=[] #['Sno', 'Work Name', 'Client', 'Designation', 'Project Cost (Cr)', 'Start Date', 'Completion Date', 'Country', 'Details': 'View']

e_id=1
filepath=""
if (sys.argv.__len__() >= 2):# and ".html" in sys.argv[1]):
     e_id=int(sys.argv[2])
     #filepath=cfg['CV_FOLDER']+sys.argv[1]
     filepath=sys.argv[1]

db = MySQLdb.connect(cfg['DB_HOST'], cfg['DB_USER'], cfg['DB_USER_PASSWORD'], cfg['DB_NAME'],use_unicode=True, charset="utf8")
print("filepath==",filepath)
# prepare a cursor object using cursor() method
cursor = db.cursor()
bothIDmatch_sql="SELECT count(*) from SA_COMPANIES_DETAILS where ID_CONSULTANT = %d and ID_COMPANY = %d"
IDmatch_sql = "SELECT count(*) from SA_COMPANIES_DETAILS where ID_CONSULTANT = %d"
delete_sql = "DELETE FROM SA_COMPANIES_DETAILS WHERE ID_CONSULTANT = %s"
        #(e_photo,  e_name, e_dob, e_mname, e_email, e_state, e_district, e_address, e_pstate, e_pdistrict,e_paddress,e_pan, e_passport,e_mobile,e_amobile,e_landline)
update_sql = "UPDATE `SA_COMPANIES_DETAILS` SET " \
             "`qualificationLevel` = '%s', `qualificationName` = '%s', " \
             "`subjects` = '%s', `college` = '%s', " \
             "`passingYear` = '%s', `percentage` = '%f, " \
             "`certificateDetails` = '%s', `certificateUploaded` = '%s' " \
             "WHERE `ID_CONSULTANT` = %d AND `ID_COMPANY` = %d"

#headings=[] #['Sno', 'Work Name', 'Client', 'Designation', 'Project Cost (Cr)', 'Start Date', 'Completion Date', 'Country', 'Details': 'View']
#headingsB=[]
counter_records = 0
headingsCo=[]
dictCells = {}
listRowsCoData=[]

'''[3] COMPANIES DETAILS'''
FlagCo=""
updateFlagCo=""


arrFiles = glob.glob(filepath)
'''
1 chk if data thr in Quali tbl for the corresponding table
2 if yes update the rows for this ID / delete rows for this ID
3 else insert all rows freshly
'''
print("TestCompaniesTable.py BFR DELETE,,,,id====",e_id)
cursor.execute(delete_sql,(e_id,  ) )
db.commit()

print("delete over.....id==",e_id)

for file in arrFiles:
    f = codecs.open(file, 'r', 'utf-8')
    soup = BeautifulSoup(f, "html.parser")
    rowie= soup.find(text='QUALIFICATION DETAILS').findNext('table')
    #print("rowie...:::",rowie)
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@")
    for rowNo,row in enumerate(rowie.find_all("tr")):
        del dictCells
        dictCells = {}
        e_percentage=0
        #print("###############  rowrow....",row)
        for cellNo, cell in enumerate(row.find_all("td")):
            #print("^^^^^^^^333333^^^^^^^^^^^^  cell", cell.text, cellNo)
            if (cell.text == 'COMPANIES DETAILS'):  # 'VIEW CONSULTANT DETAILS','Last Modified','BASIC DETAILS','QUALIFICATION DETAILS','COMPANIES DETAILS','DETAILED WORK DETAILS'
                # print("QUALIFICATION DETAILS   QUALIFICATION DETAILS   QUALIFICATION DETAILSQUALIFICATION DETAILS")
                FlagCo = "YES"
                continue
            if cell.text == 'DETAILED WORK DETAILS':
                FlagCo = "NO"
                FlagWrk = "YES"
                exit()
            if cell.find_all('b'):
                headingsCo.append(cell.text)
                print("textt--->>", cell.text)
            else:
               # print("cellNocellNo===>>>>", cellNo)
                print("cellNocellNo===>>>>", cellNo)
                print("headingsCo[cellNo]", headingsCo[cellNo], cell.text, cellNo)
                dictCells[headingsCo[cellNo]] = cell.text
                updateFlagCo = "YES"
        if ("YES" == updateFlagCo):
            counter_records = counter_records + 1
            print("[2] listRowsQData ===>>>>", listRowsCoData, "Company Name==", (dictCells['Company Name']))
            listRowsCoData.append(dictCells)

            if (dictCells.get('From Year') and '' != dictCells.get('From Year')):
                fromYearAsDate = (datetime.strptime(dictCells['From Year'].strip(),'%d/%m/%Y'))
            else:
                fromYearAsDate = '00/00/0000'

            if (dictCells.get('To Year') and '' != dictCells.get('To Year')):
                toYearAsDate = (datetime.strptime(dictCells['To Year'].strip(),'%d/%m/%Y'))
            else:
                toYearAsDate = '00/00/0000'
            varProjArr = re.findall(r"[-+]?\d*\.\d+|\d+", dictCells['Number of Projects Completed'].strip())
            if (varProjArr.__len__() >= 1):
                noOfProjects = varProjArr[0]
            else:
                noOfProjects = 0
            insert_sql = "INSERT INTO `SA_COMPANIES_DETAILS` (`ID_CONSULTANT`, `ID_COMPANY`, `sNo`, `companyName`, `fromYearAsDate`, `toYearAsDate`,  `noOfProjectsCompleted`)" \
                         "VALUES ('%d', '%d', '%d', '%s', '%s', '%s','%d')" % \
                         (e_id, counter_records, int(dictCells['Sno'] ), dictCells['Company Name'], fromYearAsDate,
                          toYearAsDate, int(noOfProjects))#int(dictCells['Number of Projects Completed'])
            print(filepath,e_id,"TestCompaniesTable.py insert sql==",insert_sql,"toYear=",toYearAsDate)
            cursor.execute(insert_sql)
            db.commit()
            print("[2] charu :::::::::::::::::::::after insert::::::::::::::::::: listRowsData==after=>>> ",                  listRowsCoData)
            updateFlagCo = "NO"

    listRowsCoData = []