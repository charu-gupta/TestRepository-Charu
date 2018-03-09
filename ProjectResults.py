# Original FIle C:\AgilyticsCharu\PyExe-Charu\RFPQueries\xls-RFP-2Aii-TL-Hway-Lanes.py
import MySQLdb
import yaml
from openpyxl import load_workbook
import MySQLdb
import yaml
import re
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'RFPQueries')) #os.path.dirname(__file__) just gives you the directory that your current python file is in, and then we navigate to 'TrialPackage/' the directory and import 'TrialPackage' the module.
from RFPQueries import HandleErrorMessages as error
# cfg=yaml.load(open("../config.yaml"))
# print (cfg['DB_NAME'])

arrError = []
arrErrorCell = []


def ftnGetProjectResults(xlsFile, dbCon):
    data = []
    record = ()

    listConsultant = []
    try:
        # Load in the workbook
        wb = load_workbook(xlsFile, False)
        # Get the sheet by Name
        sheetName = "RFP2 - Project Adequacy"
        mysheet = wb.get_sheet_by_name(sheetName)  # wb.active
        error.ClearErrorMessages(xlsFile, sheetName)
        error.ClearErrorFormat(xlsFile, sheetName, 3, 2, 3, 2)  # 'B3':'B3'
        error.ClearErrorFormat(xlsFile, sheetName, 8, 1, 17, 12)  # 'A8': 'N12'
        print("----------------- CHARU Sheet Data -------------- ")
        PROJKM = 0
        valProjKM = mysheet['B3'].value
        if None == valProjKM:
            print("PROJECT KM is none")
            arrError.append("(Upcoming) Project KM in cell " +'B3' + " should be a non-negative number ( greater than 0 )")
            arrErrorCell.append('B3')
        elif ((isinstance(valProjKM, int) or isinstance(valProjKM, float)) and valProjKM > 0):
            PROJKM = valProjKM
            print("valProjKM== ", valProjKM)
        else:
            arrError.append("(Upcoming) Project KM in cell " +'B3' + " should be a non-negative number (greater than 0) ")
            arrErrorCell.append('B3')
            print("NAN NAN NAN NAN NANNANNANANANANANAN")
        print("PROJKM #####", PROJKM)

        for rowNo, rowOfCellObjects in enumerate(mysheet['A10':'AZ21']):
            MULTIPLIER2_PROJCOST = 0
            MULTIPLIER4_6 = 0
            MULTIPLIER2 = 0
            MULTIPLIERKM = 0
            RFPName =""
            defaultExp = -1  # No. of Projects
            defaultExpUnit = ''
            defaultMarks = -1
            additionalMarks = -1
            maxMarks = -1
            print("-----------------********************------------- ROW DATA (--", rowNo,
                  "--)------------ **************************************------------- ")
            # sql = 'select * from work_details_in_depth where designation IN (select designation from master_designation where code IN (%s,%s))'
            data = []
            sql=""
            # sql = 'select * from work_details_in_depth where designation IN (select designation from master_designation where code IN '
            #sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT '
            for cellObj in rowOfCellObjects:
                print(cellObj.column, cellObj.coordinate, cellObj.value)
                arrProjType = []
                if (cellObj.column == 'A'):
                    print("RFP NAME/NO. -->>> ", cellObj.value, cellObj.column,type(cellObj.value))
                    RFPName = cellObj.value
                    print("C",RFPName)
                if (cellObj.column == 'B'):
                    if None == cellObj.value or 'Select' == cellObj.value:
                        # dont add ProjType parameter in query
                        print("arrProjType is none")
                    else:
                        if(sql==""):
                            sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT '

                        sql = sql + " and "
                        cellVal = cellObj.value.strip()
                        arrProjType = cellVal.split("/")
                        print(arrProjType, "arrProjType")
                        for n, val in enumerate(arrProjType):
                            print("n===", n, len(arrProjType), '<<<<<len(arrProjType)')
                            if (n == 0):
                                sql = sql + "( " + val.replace(" ", "") + "= 1"
                            else:
                                sql = sql + " or " + val.replace(" ", "") + "= 1"
                            if (n == len(arrProjType) - 1):
                                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                                sql = sql + ")"
                            print(n, "<<<<<<< n", val, ".replace)", val.replace(" ", ""), "sql=== ", sql)

                arrDesig = []
                if (cellObj.column == 'C'):
                    if None == cellObj.value or 'Select' == cellObj.value:
                        # dont add designation parameter in query
                        print("designation is none")
                    else:
                        if (sql == ""):
                            sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT and '


                        #print("where===>>>", (sql.find('where')))
                        sql += " and designation IN (select designation from master_designation where code IN "
                        desig = cellObj.value.strip()
                        arrDesig = desig.split("/")
                        print(arrDesig, "arrDesig")
                        # 'TL', 'RE', 'BE'
                        for n, val in enumerate(arrDesig):
                            print("n===", n, len(arrDesig), '<<<<<len(arrDesig)')
                            if (n == 0):
                                sql = sql + "(%s"
                            else:
                                sql = sql + ", %s"
                            data = data + [val]
                            if (n == len(arrDesig) - 1):
                                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                                sql = sql + "))"
                            print(n, "<<<<<<< n", val, "sql=== ", sql)

                            # data = data + [arrDesig]

                arrNatureAssignment = []
                if (cellObj.column == 'D'):
                    # print(cellObj.column,"  arrNatureAssignmentarrNatureAssignmentarrNatureAssignmentarrNatureAssignmentarrNatureAssignmentarrNatureAssignment::::::::::::",cellObj.value)
                    if None == cellObj.value or 'Select' == cellObj.value:
                        # dont add NatureAssignment parameter in query
                        print("Nature of Assignment is none")
                    else:
                        #print("where===>>>", (sql.find('where')))
                        if (sql == ""):
                            sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT '
                        sql = sql + " and "
                        sql = sql + " NatureOfAssignment IN (select assignmentNature from master_assgnmentnature where code IN "
                        assgnmnt = cellObj.value.strip()
                        arrNatureAssignment = assgnmnt.split("/")
                        print(arrNatureAssignment, "arrNatureAssignment")

                        for n, val in enumerate(arrNatureAssignment):
                            print("n===", n, len(arrNatureAssignment), '<<<<<len(arrNatureAssignment)', arrNatureAssignment)
                            if (n == 0):
                                sql = sql + "(%s"
                            else:
                                sql = sql + ", %s"
                            data = data + [val]
                            if (n == len(arrNatureAssignment) - 1):
                                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^--------------------^^^^^^^^^^^^^^^^^^")
                                sql = sql + "))"
                            print(n, "^^^^^^^^^^^^^^^^^^^ ---------------- NatureAssignment___________ n", val, "sql=== ",
                                  sql)

                            # data = data + [arrNatureAssignment]

                # MINMONTH = 0
                if (cellObj.column == 'I'):
                    print("Min Months on Project-----------------cell val==", cellObj.value, cellObj.column,
                          type(cellObj.value))
                    if None == cellObj.value:
                        print("Min Months on Project is none")
                        # MINMONTH = 0
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value,
                                                                        float)) and cellObj.value >= 0):  # and cellObj.value <= 1
                        if (sql == ""):
                            sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT '

                        # MINMONTH = cellObj.value
                        sql = sql + " and "
                        sql = sql + " TIMESTAMPDIFF(MONTH, StartDate,CompletionDate) >= %s "
                        data = data + [cellObj.value]
                        print("MINMONTH=+++++++++= ", cellObj.value)
                    else:
                        arrError.append("MIN months on Project in cell "+ cellObj.coordinate + " should be a number ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN")

                    print(cellObj.value, " cellObj.value", "**************MINMONTH", "sql=== ", sql)

                if (cellObj.column == 'E'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # MULTIPLIER2 = 1
                        print("MULTIPLIER2 is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        MULTIPLIER2 = cellObj.value
                        print("MULTIPLIER2== ", MULTIPLIER2)
                    else:
                        arrError.append("Multiplier for 2 Lane in cell "+ cellObj.coordinate + " should be a non-negative number (greater than 0) ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN")

                    print(cellObj.value, " cellObj.value", MULTIPLIER2, ".MULTIPLIER2", "sql=== ", sql)

                if (cellObj.column == 'F'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        print("MULTIPLIER2_PROJCOST is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value >= 0):
                        MULTIPLIER2_PROJCOST = cellObj.value
                        print("MULTIPLIER2_PROJCOST== ", MULTIPLIER2_PROJCOST)
                    else:
                        arrError.append(
                            "Project Cost MULTIPLIER for 2 Lane in cell "+ cellObj.coordinate + " should be a non-negative number (greater than 0) ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN")

                    print(cellObj.value, " cellObj.value", MULTIPLIER2_PROJCOST, ".:::::::MULTIPLIER2_PROJCOST", "sql=== ",
                          sql)

                if (cellObj.column == 'G'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # MULTIPLIER4_6 = 1
                        print("MULTIPLIER4_6 is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        MULTIPLIER4_6 = cellObj.value
                        print("MULTIPLIER4_6== ", MULTIPLIER4_6)
                    else:
                        arrError.append("MULTIPLIER 4 and 6 Lane in cell "+ cellObj.coordinate + " should be a non-negative number (greater than 0) ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN")

                    print(cellObj.value, " cellObj.value", MULTIPLIER4_6, "**************MULTIPLIER4_6", "sql=== ", sql)

                if (cellObj.column == 'H'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        print("MULTIPLIERKM is none")
                        MULTIPLIERKM = 1
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value,
                                                                        float)) and cellObj.value > 0):  # and cellObj.value <= 1
                        MULTIPLIERKM = cellObj.value
                        print("MULTIPLIERKM=+++++++++= ", MULTIPLIERKM)
                    else:
                        arrError.append("MULTIPLIER for Project Length in cell "+ cellObj.coordinate + " should be a number up to 1 (greater than 0) ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN")

                    print(cellObj.value, " cellObj.value", MULTIPLIERKM, "**************MULTIPLIERKM", "sql=== ", sql)

                if (cellObj.column == 'J'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # defaultExp = 1
                        print("Default Experience (in Units) is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        defaultExp = cellObj.value
                        print("defaultExp== ", defaultExp)
                    else:
                        arrError.append("Default Experience (in Units) in cell "+ cellObj.coordinate + " should be a non-negative number ")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN Default Experience (in Units)")

                    print(cellObj.value, " cellObj.value", defaultExp, "**************defaultExp", "sql=== ", sql)

                if (cellObj.column == 'K'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value or 'Select' == cellObj.value:
                        # defaultExpUnit = 1
                        print("Please select the Unit for Default Experience ")
                        if defaultExp >= 0:
                            arrError.append("Please select the Unit for Default Experience in cell "+ cellObj.coordinate )
                            arrErrorCell.append(cellObj.coordinate)
                            print("Please select Unit for the given Default Experience ")
                    else:
                        defaultExpUnit = cellObj.value
                        print("defaultExpUnit== ", defaultExpUnit)

                    print(cellObj.value, " cellObj.value", defaultExpUnit, "**************defaultExpUnit", "sql=== ", sql)

                if (cellObj.column == 'L'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
                    if None == cellObj.value:
                        # defaultMarks = 1
                        print("Default Marks is none")
                    elif ((isinstance(cellObj.value, int) or isinstance(cellObj.value, float)) and cellObj.value > 0):
                        defaultMarks = cellObj.value
                        print("defaultMarks== ", defaultMarks)
                    else:
                        arrError.append("Default Marks in cell "+ cellObj.coordinate + " should be a non-negative number")
                        arrErrorCell.append(cellObj.coordinate)
                        print("NAN NAN NAN NAN NANNANNANANANANANAN Default Marks ")

                    print(cellObj.value, " cellObj.value", defaultMarks, "**************defaultMarks", "sql=== ", sql)

                if (cellObj.column == 'M'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
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

                if (cellObj.column == 'N'):
                    print("cell val==", cellObj.value, cellObj.column, type(cellObj.value))
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

            KMCheck2 = 0
            KMCheck4_6 = 0
            if (len(arrError) > 0):
                print("ProjectResults.py******  EXIT   EXIT EXIt *******????????????**********?????????????", arrError)
                error.PrintErrorMessages(arrError, arrErrorCell, xlsFile, sheetName, 'error')

                exit(1)
            else:
                print("MULTIPLIER2", MULTIPLIER2, "MULTIPLIER4_6MULTIPLIER4_6MULTIPLIER4_6", MULTIPLIER4_6)
                if (MULTIPLIER2 > 0 or MULTIPLIER4_6 > 0):
                    if (sql == ""):
                        sql = 'select w.id_consultant, count(ID_work_details_in_depth), sum(ProjectDuration), min(ProjectCost), max(ProjectCost) , name , DOB, email, c.state, district, address , pan , mobile , alter_mobile , landline from work_details_in_depth  w, sa_consultant c where c.ID_CONSULTANT=w.ID_CONSULTANT '
                    sql = sql + " and "
                    # sql = sql + "( "
                    if (MULTIPLIER2 > 0 and MULTIPLIER4_6 > 0):
                        sql = sql + " ((Highway2Lane_KM >= %s and ProjectCost >= %s ) OR Highway4Lane_KM >= %s OR Highway6Lane_KM >= %s )"
                        data = data + [PROJKM * MULTIPLIER2 * MULTIPLIERKM, MULTIPLIER2_PROJCOST,
                                       PROJKM * MULTIPLIER4_6 * MULTIPLIERKM, PROJKM * MULTIPLIER4_6 * MULTIPLIERKM]
                    elif (MULTIPLIER2 > 0):
                        sql = sql + " (Highway2Lane_KM >= %s and ProjectCost >= %s )"
                        # KMCheck2 = PROJKM * MULTIPLIER2 * MULTIPLIERKM
                        data = data + [PROJKM * MULTIPLIER2 * MULTIPLIERKM, MULTIPLIER2_PROJCOST]
                    else:  # case MULTIPLIER4_6 > 0
                        sql = sql + " ( Highway4Lane_KM >= %s OR Highway6Lane_KM >= %s )"
                        data = data + [PROJKM * MULTIPLIER4_6 * MULTIPLIERKM, PROJKM * MULTIPLIER4_6 * MULTIPLIERKM]
                        # data PROJKM * MULTIPLIER4_6 * MULTIPLIERKM, PROJKM * MULTIPLIER4_6 * MULTIPLIERKM)
                        KMCheck4_6 = PROJKM * MULTIPLIER4_6 * MULTIPLIERKM
                    # sql = sql + " )"
                    print("KMCheck = PROJKM * MULTIPLIER2---->>>>", KMCheck2, "KMCheck4_6==>>>", KMCheck4_6)

                try:
                    # Open database connection
                    # db = MySQLdb.connect(cfg['DB_HOST'], cfg['DB_USER'], cfg['DB_USER_PASSWORD'], cfg['DB_NAME'])
                    if(sql !=""):
                        # prepare a cursor object using cursor() method
                        cursor = dbCon.cursor()
                        sql = sql + "group by ID_CONSULTANT  order by sum(ProjectDuration)desc, count(ID_work_details_in_depth) desc, max(ProjectCost) desc LIMIT 20 "#LIMIT 50 "  # Adding final bit to the Query
                        # data =
                        print("sql==:::::::::::::>>>>>", sql, "data****", data, "data length===", len(data))
                        # Execute the SQL command
                        cursor.execute(sql, data)
                        # arrDesig=['TL', 'BE', 'RE']
                        # cursor.execute("select * from work_details_in_depth where designation IN(select  designation from master_designation where code IN(%s, %s, %s)) ", arrDesig)
                        # Commit your changes in the database
                        results = cursor.fetchall()
                        print("------------------------**************** RFP Output *******************------------------------------")
                        for i, row in enumerate(results):
                            RFPMarks = 0
                            # print("Data is-----", row)
                            # print("Data is-----", row[0],"ProjDur",row[1])
                            id = row[0]
                            if defaultExpUnit == 'No. Of Projects (count)':
                                totalExp = row[1]
                            else:
                                totalExp = row[2]
                            name = row[5]
                            DOB = row[6]
                            email = row[7]
                            state = row[8]
                            district = row[9]
                            address = row[10]
                            pan = row[11]
                            mobile = row[12]
                            alter_mobile = row[13]
                            landline = row[14]

                            if (defaultMarks >= 0 or additionalMarks >= 0 or maxMarks >= 0):
                                if (totalExp >= defaultExp):
                                    RFPMarks = defaultMarks + ((int(totalExp) - defaultExp) * additionalMarks)
                                    if (RFPMarks > maxMarks):
                                        RFPMarks = maxMarks
                                else:
                                    RFPMarks = 0
                            else:
                                RFPMarks = -1
                            print(RFPName,"<<<<RFPName")
                            record = (id, RFPName, RFPMarks,name , DOB , email , state , district , address , pan , mobile , alter_mobile , landline, totalExp, defaultExpUnit)
                            listConsultant = listConsultant + [record]
                            print(i, "<<<<<<<i", "id==", id, " (RFP  Marks)--->>>> ", RFPMarks, "totalExpYrs-->", totalExp,
                                  "defaultExpUnit::::::::::::: ", defaultExpUnit, listConsultant,"********************* listConsultant")
                except Exception as err:
                    print("ProjectResults [[[[2]]] Exception occured:::", err)
                    # return back
                    # Rollback in case there is any error
                    dbCon.rollback()
    except Exception as err:
        print("ProjectResults [[[[1]]]Exception occured:::", err)
    return  listConsultant