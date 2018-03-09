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

e_id=0
filepath=""
if (sys.argv.__len__() >= 2):# and ".html" in sys.argv[1]):
     e_id=int(sys.argv[2])
     #filepath=cfg['CV_FOLDER']+sys.argv[1]
     filepath=sys.argv[1]
#filepath = "C:\AgilyticsCharu\PyExe-Charu\RFP-Mahuava NH-8E\8800297444-santosh kumar shrivastava-TL.html"
db = MySQLdb.connect(cfg['DB_HOST'], cfg['DB_USER'], cfg['DB_USER_PASSWORD'], cfg['DB_NAME'],use_unicode=True, charset="utf8")
print("filepath==",filepath)
# prepare a cursor object using cursor() method
cursor = db.cursor()
bothIDmatch_sql="SELECT count(*) from sa_qualification where ID_CONSULTANT = %d and ID_QUALIFICATION = %d"
IDmatch_sql = "SELECT count(*) from sa_qualification where ID_CONSULTANT = %d"
delete_sql = "DELETE FROM sa_qualification WHERE ID_CONSULTANT = %s"
        #(e_photo,  e_name, e_dob, e_mname, e_email, e_state, e_district, e_address, e_pstate, e_pdistrict,e_paddress,e_pan, e_passport,e_mobile,e_amobile,e_landline)
update_sql = "UPDATE `sa_qualification` SET " \
             "`qualificationLevel` = '%s', `qualificationName` = '%s', " \
             "`subjects` = '%s', `college` = '%s', " \
             "`passingYear` = '%s', `percentage` = '%sf, " \
             "`certificateDetails` = '%s', `certificateUploaded` = '%s' " \
             "WHERE `ID_CONSULTANT` = %d AND `ID_QUALIFICATION` = %d"

#headings=[] #['Sno', 'Work Name', 'Client', 'Designation', 'Project Cost (Cr)', 'Start Date', 'Completion Date', 'Country', 'Details': 'View']
#headingsB=[]
counter_records = 0
headingsQ=[]
headingsCo=[]
headingsWrk=[]
dictCells = {}
#listRowsBData=[]
listRowsQData=[]
listRowsCoData=[]
listRowsWrkData=[]
'''[1] BASIC DETAILS'''
FlagB=""
updateFlagB=""
'''[2] QUALIFICATION DETAILS'''
FlagQ=""
updateFlagQ=""
'''[3] COMPANIES DETAILS'''
FlagCo=""
updateFlagCo=""
'''[4] DETAILED WORK DETAILS'''
FlagWrk=""
updateFlagWrk=""
arrFiles = glob.glob(filepath)
'''
1 chk if data thr in Quali tbl for the corresponding table
2 if yes update the rows for this ID / delete rows for this ID
3 else insert all rows freshly
'''
print("BFR DELETE,,,,id====",e_id)
cursor.execute(delete_sql,(e_id,  ) )
db.commit()

print("delete over.....id==",e_id)

for file in arrFiles:
    f = codecs.open(file, 'r', 'utf-8')
    soup = BeautifulSoup(f, "html.parser")
    rowie= soup.find(text='BASIC DETAILS').findNext('table')
    #print("rowie...:::",rowie)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@")
    for rowNo,row in enumerate(rowie.find_all("tr")):
        del dictCells
        dictCells = {}
        e_percentage=0
        #print("###############  rowrow....",row)
        for cellNo, cell in enumerate(row.find_all("td")):
            #print("^^^^^^^^333333^^^^^^^^^^^^  cell", cell.text, cellNo)
            if (cell.text == 'QUALIFICATION DETAILS'):  # 'VIEW CONSULTANT DETAILS','Last Modified','BASIC DETAILS','QUALIFICATION DETAILS','COMPANIES DETAILS','DETAILED WORK DETAILS'
                # print("QUALIFICATION DETAILS   QUALIFICATION DETAILS   QUALIFICATION DETAILSQUALIFICATION DETAILS")
                FlagQ = "YES"
                continue
            if cell.text == 'COMPANIES DETAILS':
                FlagQ = "NO"
                FlagCo = "YES"
                exit()
            if cell.find_all('b'):
                headingsQ.append(cell.text)
                print("textt--->>", cell.text)
            else:
               # print("cellNocellNo===>>>>", cellNo)
                print("cellNocellNo===>>>>", cellNo)
                print("headingsQ[cellNo]", headingsQ[cellNo], cell.text, cellNo)
                dictCells[headingsQ[cellNo]] = cell.text
                updateFlagQ = "YES"
        if ("YES" == updateFlagQ):
            counter_records = counter_records + 1
            print("[2] listRowsQData ===>>>>", listRowsQData, "e_percentage==", (dictCells['Percentage']))
            listRowsQData.append(dictCells)
            passingYearAsDate = (datetime.strptime(dictCells['Year Of Passing'].strip(), '%Y'))

            varDateArr = re.findall(r"[-+]?\d*\.\d+|\d+", str(passingYearAsDate))
            passingYear = varDateArr[0]
            var1 = re.findall(r"[-+]?\d*\.\d+|\d+", dictCells['Percentage'])
            print("e_percentage.__len__()", var1.__len__(),"passingYearAsDate===>>>>",passingYearAsDate,"passingYear==",passingYear)
            if (var1.__len__() >= 1):
                e_percentage = var1[0]
            else:
                e_percentage = 0
            print("e_percentage---e_percentage-->>>",e_percentage)
            insert_sql = "INSERT INTO `sa_qualification` (`ID_CONSULTANT`, `ID_QUALIFICATION`, `qualificationLevel`, `qualificationName`, `subjects`, `college`, `university_board`, `passingYearAsDate`, `passingYear`, `percentage`, `certificateDetails`, `certificateUploaded`)" \
                         "VALUES ('%d', '%d', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%f',  '%s', '%s')" % \
                         (e_id, counter_records, dictCells['Level'], dictCells['Qualification Level'], dictCells['Topic of the Subject'],
                          dictCells['College'],dictCells['University/Board'] ,passingYearAsDate, passingYear , float(e_percentage), dictCells['Certificate Details'], 0)
            print(filepath,e_id,"XXXXXXXXXXXXXXXXXXXXX insert sql==",insert_sql,"e_percentage=",e_percentage)
            cursor.execute(insert_sql)
            db.commit()
            #print("[2] charu :::::::::::::::::::::after insert::::::::::::::::::: listRowsData==after=>>> ",                  listRowsQData)
            updateFlagQ = "NO"

    listRowsQData = []