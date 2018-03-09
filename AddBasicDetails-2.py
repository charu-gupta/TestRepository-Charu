import MySQLdb
import glob
import codecs
from datetime import datetime
from bs4 import BeautifulSoup
#import yaml
import time
import configparser
import tkinter
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'HTMLToDB')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.
from HTMLToDB import CorrectFormat_InHTML as correctFormat

#cfg=yaml.load(open("config.yaml"))
cfg = configparser.RawConfigParser()
cfg.read("config.cfg")
#headings=[] #['Sno', 'Work Name', 'Client', 'Designation', 'Project Cost (Cr)', 'Start Date', 'Completion Date', 'Country', 'Details': 'View']

headingsB=[]
dictCells = {}
listRowsBData=[]
'''[1] BASIC DETAILS'''
FlagB1=""
FlagB=""
updateFlagB=""

#path="C:\AgilyticsCharu\PyExe-Charu\RFP-Mahuava NH-8E"
#filename="*-TL.html"
filepath=cfg.get('General','CV_FOLDER')+"\\"+cfg.get('General','CV_FILEPATTERN')
print("path for basic CV-->> ",filepath)
#path="C:\AgilyticsCharu\PyExe-Charu\santosh kumar shrivastava-4l.html"
arrFiles=glob.glob(filepath)

for file in arrFiles:
    print("Basic CV ************ file=====>> ", file)
    correctFormat.RemoveFormTag(file)
    correctFormat.AddTRForPanTD(file)
    headingsB = []
    dictCells = {}
    e_photo = ""
    e_name = ""
    e_dob = ""
    e_mname = ""
    e_email = ""
    e_state = ""
    e_district = ""
    e_address = ""
    e_pstate = ""
    e_pdistrict = ""
    e_paddress = ""
    e_pan = ""
    e_passport = ""
    e_mobile = ""
    e_amobile = ""
    e_landline = ""
    f = codecs.open(file, 'r', 'Latin-1')
    soup = BeautifulSoup(f, "html.parser")
    #print("111111111111 ",soup.find(text='BASIC DETAILS').findNext('td').find('b').string)
    rowie= soup.find(text='VIEW CONSULTANT DETAILS').findNext('table')
    #print("roo", rowie)
        #.findNext('tr')
    for rowNo,row in enumerate(rowie.find_all("tr")):
        for cellNo, cell in enumerate(row.find_all('td')):
            if cell.find('b'):
                headingsB.append(cell.text)

            else:
        #         #print([headingsB.__len__()]," [headingsB.__len__()]")
                dictCells[headingsB[(headingsB.__len__()-1)]] = cell.text
                #print(dictCells)
                #print("piccccccccccccccc--->>",dictCells['Photo'])
        #         updateFlagB = "YES"

    # Open database connection
    db = MySQLdb.connect(cfg.get('General', 'DB_HOST'),cfg.get('General', 'DB_USER'),cfg.get('General', 'DB_USER_PASSWORD'),cfg.get('General', 'DB_NAME'))

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    # sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
    #        LAST_NAME, AGE, SEX, INCOME) \
    #        VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
    #        ('Mac', 'Mohan', 20, 'M', 2000)

    e_photo = dictCells['Photo']
    e_name = dictCells['Name']
    e_dob = (datetime.strptime(dictCells['DOB'], '%d/%m/%Y'))
    e_mname = dictCells['Mother Name']
    e_email = dictCells['Email']
    e_state = dictCells['Current State']
    e_district = dictCells['Current District']
    e_address = dictCells['Current Address']
    e_pstate = dictCells['Permanent State']
    e_pdistrict=dictCells['Permanent District']
    e_paddress=dictCells['Permanent Address']
    if(dictCells.get('PAN Number')):
        e_pan = dictCells['PAN Number']
    if(dictCells.get('Passport Number')):
        e_passport = dictCells['Passport Number']
    if (dictCells.get('Mobile')):
        e_mobile = dictCells['Mobile']
    if (dictCells.get('Alternate Mobile')):
        e_amobile = dictCells['Alternate Mobile']
    if (dictCells.get('Landline Number')):
        e_landline = dictCells['Landline Number']
    emailmatch_sql="SELECT count(*) from SA_CONSULTANT where email LIKE %s"
    select_sql="SELECT * from SA_CONSULTANT where email LIKE %s"
    insert_sql = "INSERT INTO SA_CONSULTANT(photo, name,dob, mother_name, email, state, district, address, permanant_state, permanant_district, permanant_address, pan, passport, mobile,alter_mobile,landline) \
          VALUES ('%s',  '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" %\
    (e_photo,  e_name, e_dob, e_mname, e_email, e_state, e_district, e_address, e_pstate, e_pdistrict,e_paddress,e_pan, e_passport,e_mobile,e_amobile,e_landline)
    update_sql = "UPDATE SA_CONSULTANT SET photo=%s, name=%s,dob=%s, mother_name=%s, state=%s, district=%s, address=%s, permanant_state=%s, permanant_district=%s, permanant_address=%s, pan=%s, passport=%s, mobile=%s,alter_mobile=%s,landline=%s WHERE email=%s"

    #try:
    # if email already in the database do not insert, Update the record

    cursor.execute(emailmatch_sql,[e_email])
    result=cursor.fetchall()
    #print("fetchinnnnnnggg:::",result[0][0])
    if (result[0][0] >0):
        #NO INSERT
        print("updating the record ---->> todo ",e_email," name==",e_name," e_mobile==",e_mobile)
        data=[e_photo, e_name, e_dob, e_mname, e_state, e_district, e_address, e_pstate, e_pdistrict,e_paddress,e_pan, e_passport,e_mobile,e_amobile,e_landline, e_email ]
        cursor.execute(update_sql,data)
        #print("result--->>",result)
        # st.rowcount))
        db.commit()
    else:
        # Execute the SQL command
        print("bfr insert record-->>",e_email," name==",e_name," e_mobile==",e_mobile)
        cursor.execute(insert_sql)
        # Commit your changes in the database
        print("sdhsd cmmmmmmit")
        db.commit()

    cursor.execute(select_sql, [e_email])
    result = cursor.fetchone()
    if None != result:
        e_id=result[0]

    db.close()


    print("CHARU14FEB ***************   ************  e_mobile==>>",e_mobile)
    from subprocess import call
    call(["python", 'HTMLToDB/TestQualiTable.py', file, str(e_id), e_email, e_mobile])
    call(["python", "HTMLToDB/TestCompaniesTable.py", file, str(e_id), e_email, e_mobile])
    if (e_mobile > str(0) and None != e_mobile):
        call(["python", "HTMLToDB/AddWorkDetailsInDepth.py", str(e_id), e_mobile])
    else:
        call(["python", "HTMLToDB/AddWorkDetailsInDepth.py", str(e_id), e_email])
    call(["python", "HTMLToDB/AddWorkDuration.py", str(e_id)])
input("Press any key to exit!!")