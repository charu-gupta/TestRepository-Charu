# Original File C:\AgilyticsCharu\CVHunt_SA-FinalCR\RFPQueries\CompanyResults.py
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


def ftnGetCurrCompanyResults(xlsFile, dbCon):
    data = []
    record = ()

    listConsultant = []
    try:
        # Load in the workbook
        wb = load_workbook(xlsFile, False)
        # Get the sheet by Name
        sheetName="RFP3 - CurrentEmployment"
        mysheet = wb.get_sheet_by_name(sheetName)  # wb.active
        error.ClearErrorMessages(xlsFile,sheetName)
        error.ClearErrorFormat(xlsFile,sheetName,7,1,10,4)#'A8':'D12'
        print("----------------- CHARU Sheet Data -------------- ")


        for rowNo, rowOfCellObjects in enumerate(mysheet['A7':'E10']):
            RFPName =""
            defaultYears = -1
            defaultMarks = -1
            additionalMarks = -1
            maxMarks = -1
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

                if (cellObj.column == 'B'):
                    print("Min Employment Duration Check (in Years)==>>val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None != cellObj.value :
                        if ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                            sql = "select co.ID_CONSULTANT, companyName, name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline , TIMESTAMPDIFF(month, fromYearAsDate,curdate())/12 as yearsCount , fromYearAsDate from sa_companies_details co, sa_consultant c where co.ID_CONSULTANT=c.ID_CONSULTANT and TIMESTAMPDIFF(month, fromYearAsDate,curdate())/12 >= %s and toYearAsDate='0000-00-00' "
                            data += [cellObj.value]
                            defaultYears = cellObj.value
                            print("Min Employment Duration Check (in Years)=+++++++++= ", cellObj.value)
                        else:
                            arrError.append("Min Employment Duration Check (in Years) in cell " + cellObj.coordinate + " should be a number ")
                            arrErrorCell.append(cellObj.coordinate)
                            print("NAN NAN NAN NAN NANNANNANANANANANAN Min Employment Duration Check (in Years)")

                        print(cellObj.value, " cellObj.value", "**************Min Employment Duration Check (in Years)", "sql=== ", sql)


                if (cellObj.column == 'C'):
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

                if (cellObj.column == 'D'):
                    print("D Additional Marks cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # additionalMarks = 1
                        print("Additonal Marks is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        additionalMarks = cellObj.value
                        print("additionalMarks== ", additionalMarks)
                    else:
                        arrError.append("Additional Marks in cell "+ cellObj.coordinate + " should be a non-negative number")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN Additional Marks ")

                    print(cellObj.value, " cellObj.value", additionalMarks, "**************additionalMarks", "sql=== ", sql)

                if (cellObj.column == 'E'):
                    print("E Max Marks cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # maxMarks = 1
                        print("Maximum Marks is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        maxMarks = cellObj.value
                        print("Maximum== ", maxMarks)
                    else:
                        arrError.append("Maximum Marks in cell "+ cellObj.coordinate + " should be a non-negative number")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN Maximum Marks ")

                    print(cellObj.value, " cellObj.value", maxMarks, "**************maxMarks", "sql=== ", sql)

            try:
                if (len(arrError) > 0):
                    print("EXIT   EXIT EXIt *******????????????**********?????????????", arrError)
                    error.PrintErrorMessages(arrError,arrErrorCell,xlsFile,sheetName,'error')

                    exit(1)
                else:
                    if sql != "": #if sql is NOT NULL then perform DB Query
                        cursor = dbCon.cursor()
                        sql += " order by fromYearAsDate asc LIMIT 20 "  # Adding final bit to the Query
                        # data =
                        print("sql==:::::::::::::>>>>>", sql, "data****", data, "data length===", len(data))
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
                                companyName    = row[1]
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
                                emplDuration = row[12]

                                if (None != emplDuration and emplDuration > 0):
                                    RFPMarks = defaultMarks
                                if (defaultMarks >= 0 or additionalMarks >= 0 or maxMarks >= 0):
                                    if (emplDuration >= defaultYears):
                                        RFPMarks = defaultMarks + ((int(emplDuration) - defaultYears) * additionalMarks)
                                        if (RFPMarks > maxMarks):
                                            RFPMarks = maxMarks
                                    else:
                                        RFPMarks = 0
                                else:
                                    RFPMarks = -1
                                record = (id_consultant, RFPName, RFPMarks, name, DOB, email, state, district, address, pan, mobile, alter_mobile, landline, companyName, emplDuration)
                                listConsultant += [record]
                                print("CompanyResults************* id_consultant==", id_consultant, "emplDuration==", emplDuration," companyName==>>",companyName,", (RFP  Marks)--->>>>", RFPMarks,"listConsultant==",listConsultant)

            except Exception as err:
                print("CompanyResults [[[[2]]] Exception occured:::", err)
                # Rollback in case there is any error
                dbCon.rollback()
    except Exception as err:
        print("CompanyResults [[[[1]]]Exception occured:::", err)
        traceback.print_tb(err.__traceback__)
    return listConsultant