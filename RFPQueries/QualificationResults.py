# Original File C:\AgilyticsCharu\PyExe-Charu\RFPQueries\IncompleteQualificationResults.py ..... C:\AgilyticsCharu\PyExe-Charu\RFPQueries\RFP-1i-Graduate-Civil.py and C:\AgilyticsCharu\PyExe-Charu\RFPQueries\RFP-1ii-PostGraduate-CivilSpecialisedStream.py
# have code fetching Quali from DB also has code for XLS read
import MySQLdb
import yaml
from openpyxl import load_workbook
import MySQLdb
import yaml
import re
import traceback
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'RFPQueries')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.
from RFPQueries import HandleErrorMessages as error
# cfg=yaml.load(open("../config.yaml"))
# print (cfg['DB_NAME'])

arrError = []
arrErrorCell = []


def ftnGetQualificationResults(xlsFile, dbCon):
    data = []
    record = ()

    listConsultant = []
    try:
        # Load in the workbook
        wb = load_workbook(xlsFile, False)
        # Get the sheet by Name
        sheetName="RFP1 - Qualification"
        mysheet = wb.get_sheet_by_name(sheetName)  # wb.active
        error.ClearErrorMessages(xlsFile,sheetName)
        error.ClearErrorFormat(xlsFile,sheetName,8,1,12,4)#'A8':'D12'
        print("----------------- CHARU Sheet Data -------------- ")


        for rowNo, rowOfCellObjects in enumerate(mysheet['A8':'D14']):
            RFPName =""
            defaultMarks = -1
            print("-----------------********************------------- ROW DATA (--", rowNo, "--)------------ **************************************------------- ")
            data = []
            sql = ""
            for cellObj in rowOfCellObjects:
                print(cellObj.column, cellObj.coordinate, cellObj.value)
                if (cellObj.column == 'A'):
                    #if None == cellObj.value #if RFP name is not given
                    print("RFP NAME/NO. -->>> ", cellObj.value, cellObj.column,type(cellObj.value))
                    RFPName = cellObj.value
                    print("RFPName>>>>>>>>>>>>>>",RFPName)

                arrQualiLevel = []
                if (cellObj.column == 'B'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value or 'Select' == cellObj.value:
                        print("Qualification Level is none")
                        #qualiLevel = ""
                    else:
                        #if (sql.lower().find('where') < 0):
                        if sql =="":
                            sql='select q.ID_CONSULTANT, ID_QUALIFICATION , name , DOB , email , state , district , address , pan , mobile , alter_mobile , landline from sa_qualification q, sa_consultant c where c.ID_CONSULTANT=q.ID_CONSULTANT '

                        #qualiLevel = cellObj.value.strip()
                        sql += " and qualificationLevel = %s "
                        data += [cellObj.value.strip()]

                        # value = cellObj.value.strip()
                        # arrQualiLevel = value.split("/")
                        # print(arrQualiLevel, "arrQualiLevel")

                        # for n, val in enumerate(arrQualiLevel):
                        #     print("n===", n, len(arrQualiLevel), '<<<<<len(arrQualiLevel)',arrQualiLevel)
                        #     if (n == 0):
                        #         sql = sql + "(%s"
                        #     else:
                        #         sql = sql + ", %s"
                        #     data = data + [val]
                        #     if (n == len(arrQualiLevel) - 1):
                        #         print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^--------------------^^^^^^^^^^^^^^^^^^")
                        #         sql = sql + "))"
                        #     print(n, "^^^^^^^^^^^^^^^^^^^ ---------------- NatureAssignment___________ n", val,
                        #           "sql=== ",
                        #           sql)
                        #
                        # #data += [qualiLevel]
                        # #print("qualiLevel=+++++++++= ", qualiLevel)
                    print(cellObj.value, " cellObj.value", "**************qualiLevel ******", "sql=== ", sql, "data===>>",data)

                arrQualiName = []
                if (cellObj.column == 'C'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value or 'Select' == cellObj.value:
                        print("Qualification Name is none")
                        # qualiName = ""
                    else:
                        #if (sql.lower().find('where') < 0):
                        if sql =="":
                            sql = 'select q.ID_CONSULTANT, ID_QUALIFICATION , name , DOB , email , state , district , address , pan , mobile , alter_mobile , landline from sa_qualification q, sa_consultant c where c.ID_CONSULTANT=q.ID_CONSULTANT '

                        #sql += " and qualificationName in  (select qualificationName from master_qualificationname where code = %s ) "
                        #sql += " and qualificationName = %s  "

                        sql += " and ( qualificationName = %s or qualificationName in (select qualificationName from master_qualificationname where code = %s )) "

                        value = cellObj.value.strip()
                        arrQualiName=value.split("-")
                        if None!= len(arrQualiName) and len(arrQualiName) > 1:
                            data += [arrQualiName[1].strip(),arrQualiName[1].strip()]
                        else:
                            data += [arrQualiName[0].strip(),arrQualiName[0].strip()]

                        print(cellObj.value, " cellObj.value", arrQualiName, "arrQualiName-", "sql===>>>>>>>>&&&&&&&&&&&", sql," *****data==>>",data)

                        # for n, val in enumerate(arrQualiName):
                        #     print("n===", n, len(arrQualiName), '<<<<<len(arrQualiName)', arrQualiName)
                        #     if (n == 0):
                        #         sql = sql + "(%s"
                        #     else:
                        #         sql = sql + ", %s"
                        #     data = data + [val]
                        #     if (n == len(arrQualiName) - 1):
                        #         print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^--------------------^^^^^^^^^^^^^^^^^^")
                        #         sql = sql + "))"
                        #     print(n, "^^^^^^^^^^^^^^^^^^^ ---------------- arrQualiName n", val,
                        #           "sql=== ",
                        #           sql)
                    print(cellObj.value, " cellObj.value", arrQualiName, "**************arrQualiName", "sql=== ", sql)

                if (cellObj.column == 'D'):
                    print("DDDD cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # defaultMarks = 1
                        print("Default Marks is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        defaultMarks = cellObj.value
                        print("defaultMarks== ", defaultMarks)
                    else:
                        #if(qualiLevel!= "" or qualiName !=""):
                        msg="Default Marks in the cell "+cellObj.coordinate+" should be a non-negative number"
                        arrError.append(msg)
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN Default Marks ",arrErrorCell)

                    print(cellObj.value, " cellObj.value", defaultMarks, "**************defaultMarks", "sql=== ", sql)

            try:
                if (len(arrError) > 0):
                    print("EXIT   EXIT EXIt *******????????????**********?????????????", arrError)
                    error.PrintErrorMessages(arrError,arrErrorCell,xlsFile,sheetName,'error')

                    exit(1)
                else:
                    if sql != "": #if sql is NOT NULL then perform DB Query
                        cursor = dbCon.cursor()
                        sql += " group by ID_CONSULTANT order by count(ID_QUALIFICATION) desc LIMIT 20 "  # Adding final bit to the Query
                        # data =
                        print("Quali+++++sql==:::::::::::::>>>>>", sql, "data****", data, "data length===", len(data))
                        # Execute the SQL command
                        cursor.execute(sql, data)
                        # arrDesig=['TL', 'BE', 'RE']
                        # cursor.execute("select * from work_details_in_depth where designation IN(select  designation from master_designation where code IN(%s, %s, %s)) ", arrDesig)
                        # Commit your changes in the database
                        results = cursor.fetchall()
                        print("------------------------**************** RFP QUALI Output *******************------------------------------")
                        if None != results:
                            for row in results:
                                RFPMarks = 0
                                # print("Data is-----", row)
                                id_consultant = row[0]
                                id_quali = row[1]
                                name=row[2]
                                DOB=row[3]
                                email=row[4]
                                state=row[5]
                                district=row[6]
                                address=row[7]
                                pan= row[8]
                                mobile=row[9]
                                alter_mobile=row[10]
                                landline=row[11]

                                if (None != id_quali and id_quali > 0):
                                    RFPMarks = defaultMarks
                                # print("Data is-----", row)
                                # print("Data is-----id_q", row[1],"id_consultant",row[0])
                                #if (RFPMarks > maxMarks):
                                #   RFPMarks = maxMarks
                                print("id_consultant==", id_consultant, "id_q==", id_quali, ", (RFP  Marks)--->>>>", RFPMarks)

                                record = (id_consultant, RFPName, RFPMarks,name , DOB , email , state , district , address , pan , mobile , alter_mobile , landline)
                                listConsultant += [record]
                                print("IN GetFile ::::listConsultant----", listConsultant)
            except Exception as err:
                print("QualificationResults [[[[2]]] Exception occured:::", err)
                # Rollback in case there is any error
                dbCon.rollback()
    except Exception as err:
        print("QualificationResults [[[[1]]]Exception occured:::", err)
        traceback.print_tb(err.__traceback__)
    return listConsultant