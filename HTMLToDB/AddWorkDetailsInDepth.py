import codecs
from bs4 import BeautifulSoup
import re
import sys
import glob
from datetime import datetime
import MySQLdb
from ast import literal_eval
import yaml
cfg=yaml.load(open("config.yaml"))
#print (cfg['DB_NAME'])

print(":::::::::: :::::::: Inside AddWorkDetailsInDepth.py-----::::::::::::::sys.argv[1]sys.argv length-->",sys.argv.__len__())
e_id=""
if (sys.argv.__len__() >= 2):# and ".html" in sys.argv[1]):
     e_id=sys.argv[1]
     filepath=cfg['CV_FOLDER']+'\\'+sys.argv[2]+cfg['DETAILWORK_FILEPATTERN']
     print("WRK Detailsin Depth:::: path--->",filepath)
else:
     filepath=cfg['CV_FOLDER']+"SamirMukundbhaiBhavsar-4l-wrk1.html"
     filepath=cfg['CV_FOLDER']+"9810865160-Wrk2.html"
     print("WRK Detailsin Depth:::: FILENAME NOT SUPPLIED  :::::::::::::::::::::::::::::path--->####",filepath)
#filepath=path+"9810865160-Wrk2.html"

print("files is ================ ",filepath)
arrFiles=glob.glob(filepath)
listLaneType=["lane", "km","type","Terrain","q1","ans1"]
print("listLaneType",len(listLaneType))
#listLaneType=["lane", "km","tpye","hillTerrain","plainTerrain","q1","ans1"]
list2Lane=[]
list4Lane=[]
list6Lane=[]
flag2Lane=""
flag4Lane=""
flag6Lane =""
count2Lane=1
headingsB=[]
dictCells = {}
counter_files=0
print("WRK Detailsin Depth:::: path--->#### ",filepath,"arrfiles==>>",arrFiles)
for file in arrFiles:
    f = codecs.open(file, 'r', 'utf-8')
    print("file name is -->>",file)
    soup = BeautifulSoup(f, "html.parser")
    counter_files=counter_files+1
    HighwayProject=BridgeProject=TunnelProject=RevenueProject=OthersProject=ExpresswayProject=AirportRunwayProject=ITProject=False

    NameOfWork=Country=State=State1=State2=State3=EmployerName=EmployerAddress=Client=ClientAddress=""
    StartDate=CompletionDate=""
    ProjectCost=0
    EPC=PPP=HybridAnnuityModel=False

    Designation=EnterDesignation=BriefDescritionOfDuties=NatureOfAssignment=""

    Highway2Lane_KM=Highway4Lane_KM=Highway6Lane_KM=0

    Highway2Lane_LandType=Highway4Lane_LandType=Highway6Lane_LandType=""
    Highway2Lane_TerrainHill=Highway4Lane_TerrainHill=Highway6Lane_TerrainHill=0
    Highway2Lane_TerrainPlain=Highway4Lane_TerrainPlain=Highway6Lane_TerrainPlain=0

    ArbitrationCaseHandled=False
    ArbitrationCaseHandled_Number=0

    AchievedFinancialClosure=False
    AchievedFinancialClosure_NoOfProjects=0

    EIAProjectInfrastructre=False
    EIAProjectInfrastructre_NoOfProjects=0

    Bridges6To60M_Number=Bridges60To200M_Number=Bridges200To500M_Number=Bridges500To1000M_Number=BridgesAbove1000M_Number=0
    MaxIndividualSpan=MaxIndividualLength=TotalLength=0.0

    BridgesWithPileWellFoundation=BridgesWithRehabilitationAndRepairWork=BridgesWithCantilever=0

    TunnelUpto200M_Number=Tunnel200To500M_Number=Tunnel500To1000M_Number=TunnelAbove1000M_Number=0
    Tunnel_MaxIndividualLength=Tunnel_TotalLength=0.0
    TunnelSlopeStabalityEvln=Tunnel_HydrologicalEvln=Tunnel_SeepageAnalysis=Tunnel_DesignSoftwares=Tunnel_SrGeologistSeepageAnalysis=Tunnel_TunnelDesignSoftwaresUsed=Tunnel_UGrndAndExcvnSystem=False

    RevenueWork_InvolvedInLandAcquisition=False

    for tableNo, table in enumerate(soup.find_all("table")):
        #print("tableNo==",tableNo)
        if 0==tableNo:
            table0="0"

        if 1==tableNo:
            for rowNo,row in enumerate(table.find_all("tr")):
                for cellNo, cell in enumerate(row.find_all("td")):
                    if cell.find('b'):
                        headingsB.append(cell.text)

                    else:
                        #         #print([headingsB.__len__()]," [headingsB.__len__()]")
                        dictCells[headingsB[(headingsB.__len__() - 1)]] = cell.text
                    #print("data ---> ",cell)
            for lightBlueRow in table.find_all("tr", {"bgcolor": "#cfe6fc"}):
                print('inside table for blueRow', lightBlueRow)
                if (lightBlueRow.find('td').text.strip() == 'Highway'):
                    print("found hwayRow")
                    hwayTable = lightBlueRow.findNext('table')
                    #print("hwayyyyTable-->>", hwayTable)
                    for hwayRowNo, hwayRow in enumerate(hwayTable.find_all("tr")):
                        for hwayCellNo, hwayCell in enumerate(hwayRow.find_all("td")):
                            if(hwayCellNo == 0):
                                if (hwayRowNo == 1):
                                    hway2lane = re.findall(r"[-+]?\d*\.\d+|\d+",hwayCell.text)
                                    Highway2Lane_KM = hway2lane[0]

                                if (hwayRowNo == 2):
                                    Highway2Lane_LandType = hwayCell.text
                                    #print("Highway2Lane_LandType::::",Highway2Lane_LandType)
                                    Highway2Lane_LandType = re.sub('Lane Tpye','', Highway2Lane_LandType).strip()
                                    #print("Highway2Lane_LandType--->>", Highway2Lane_LandType)
                                if (hwayRowNo == 4):
                                    Highway2Lane_Terrain = hwayCell.text
                                    #print("Highway2Lane_Terrain",Highway2Lane_Terrain)
                                    hway2terrainArr = re.findall(r"[-+]?\d*\.\d+|\d+", Highway2Lane_Terrain)
                                    #print("hway2terrainArr", hway2terrainArr[0], hway2terrainArr[1])
                                    Highway2Lane_TerrainHill = hway2terrainArr[0]
                                    Highway2Lane_TerrainPlain = hway2terrainArr[1]

                                if (hwayRowNo == 6):
                                    print("hwayCell.text.strip()--->>>",hwayCell.text.strip())
                                    if (hwayCell.text.strip().find('Yes') >= 0):
                                        ArbitrationCaseHandled = True
                                        hwayVar = re.findall(r'\d+', hwayCell.text.strip())
                                        if (hwayVar.__len__() >= 1):
                                            ArbitrationCaseHandled_Number = hwayVar[0]
                                        else:
                                            ArbitrationCaseHandled_Number = 0
                                    else:
                                        ArbitrationCaseHandled = False
                                        ArbitrationCaseHandled_Number = 0
                                    #print("ArbitrationCaseHandled",ArbitrationCaseHandled)
                            if (hwayCellNo == 1):
                                if (hwayRowNo == 1):
                                    hway4lane = re.findall(r"[-+]?\d*\.\d+|\d+", hwayCell.text)
                                    Highway4Lane_KM = hway4lane[0]
                                    #print("celltext===>>", hwayCell.text, 'Highway4Lane_KM==>>', Highway4Lane_KM)
                                if (hwayRowNo == 2):
                                    Highway4Lane_LandType = hwayCell.text
                                   # print("Highway4Lane_LandType",Highway4Lane_LandType)
                                    Highway4Lane_LandType = re.sub('Lane Tpye','',Highway4Lane_LandType).strip()
                                    #print("Highway4Lane_LandType--->>",Highway4Lane_LandType)
                                if (hwayRowNo == 4):
                                    Highway4Lane_Terrain = hwayCell.text
                                    hway4terrainArr = re.findall(r"[-+]?\d*\.\d+|\d+", Highway4Lane_Terrain)
                                    #print("hway4terrainArr",hway4terrainArr[0],hway4terrainArr[1])
                                    Highway4Lane_TerrainHill = hway4terrainArr[0]
                                    Highway4Lane_TerrainPlain = hway4terrainArr[1]

                                if (hwayRowNo == 6):
                                    if (hwayCell.text.strip().find('Yes') >= 0):
                                        AchievedFinancialClosure = True
                                        hwayVar = re.findall(r'\d+', hwayCell.text.strip())
                                        if (hwayVar.__len__() >= 1):
                                            AchievedFinancialClosure_NoOfProjects = hwayVar[0]
                                        else:
                                            AchievedFinancialClosure_NoOfProjects = 0
                                    else:
                                        AchievedFinancialClosure = False
                                        AchievedFinancialClosure_NoOfProjects = 0
                                        #print("AchievedFinancialClosure",AchievedFinancialClosure)
                            if (hwayCellNo == 2):
                                if (hwayRowNo == 1):
                                    hway6lane= re.findall(r"[-+]?\d*\.\d+|\d+", hwayCell.text)
                                    Highway6Lane_KM = hway6lane[0]

                                if (hwayRowNo == 2):
                                    Highway6Lane_LandType = hwayCell.text
                                    Highway6Lane_LandType = re.sub('Lane Tpye', '', Highway6Lane_LandType).strip()
                                    #print("Highway6Lane_LandType--->>", Highway6Lane_LandType)
                                if (hwayRowNo == 4):
                                    Highway6Lane_Terrain = hwayCell.text
                                    hway6terrainArr = re.findall(r"[-+]?\d*\.\d+|\d+", Highway6Lane_Terrain)
                                    #print("hway6666terrainArr", hway6terrainArr[0], hway6terrainArr[1])
                                    Highway6Lane_TerrainHill = hway6terrainArr[0]
                                    Highway6Lane_TerrainPlain = hway6terrainArr[1]
                                if (hwayRowNo == 6):
                                    if(hwayCell.text.strip().find('Yes') >= 0):
                                        EIAProjectInfrastructre= True
                                        hwayVar = re.findall(r'\d+', hwayCell.text.strip())
                                        if (hwayVar.__len__() >= 1):
                                            EIAProjectInfrastructre_NoOfProjects = hwayVar[0]
                                        else:
                                            EIAProjectInfrastructre_NoOfProjects = 0
                                    else:
                                        EIAProjectInfrastructre = False
                                        EIAProjectInfrastructre_NoOfProjects = 0
                                        #print("EIAProjectInfrastructre",EIAProjectInfrastructre)
                if (lightBlueRow.find('td').text.strip() == 'Number of Bridges'):
                    print("found ******************** Bridges")
                    bridgeTable = lightBlueRow.findNext('table')
                    for brdgRowNo, brdgRow in enumerate(bridgeTable.find_all("tr")):
                        for brdgCellNo, brdgCell in enumerate(brdgRow.find_all("td")):
                            # Skipping Row No. 0, as it is for heading
                            if (brdgRowNo == 1):
                                if (brdgCellNo == 0):
                                    brdgNo = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    #print("brdgNo-->",brdgNo)
                                    Bridges6To60M_Number = brdgNo[0]
                                if (brdgCellNo == 1 ):
                                    brdgNo = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    #print("brdgNo-->", brdgNo)
                                    Bridges60To200M_Number = brdgNo[0]
                                if (brdgCellNo == 2):
                                    brdgNo = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    #print("brdgNo-->", brdgNo)
                                    Bridges200To500M_Number = brdgNo[0]
                                if (brdgCellNo == 3):
                                    brdgNo = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    #print("brdgNo-->", brdgNo)
                                    Bridges500To1000M_Number = brdgNo[0]
                                if (brdgCellNo == 4):
                                    brdgNo = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    #print("brdgNo-->", brdgNo)
                                    BridgesAbove1000M_Number = brdgNo[0]
                            if (brdgRowNo == 2):
                                if (brdgCellNo == 0):
                                    brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    if (brdgVar.__len__() >= 1):
                                        MaxIndividualSpan = brdgVar[0]
                                    else:
                                        MaxIndividualSpan = 0
                                    print(brdgCell.text,"<<<----MaxIndividualSpan",MaxIndividualSpan)
                                if (brdgCellNo == 1):
                                    brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    print("brdgVar.__len__()",brdgVar.__len__())
                                    if (brdgVar.__len__() >= 1):
                                        MaxIndividualLength = brdgVar[0]
                                    else:
                                        MaxIndividualLength = 0
                                    print(brdgCell.text, "<<<----MaxIndividualLength", MaxIndividualLength)
                                if (brdgCellNo == 2):
                                    brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                    if (brdgVar.__len__() >= 1):
                                        TotalLength = brdgVar[0]
                                    else:
                                        TotalLength = 0
                                    print(brdgCell.text, "<<<----TotalLength", TotalLength)
                            if (brdgRowNo == 3):
                                brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                print("brdgVar.__len__()", brdgVar.__len__())
                                if (brdgVar.__len__() >= 1):
                                    BridgesWithPileWellFoundation = brdgVar[0]
                                else:
                                    BridgesWithPileWellFoundation = 0
                            if (brdgRowNo == 4):
                                brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                print("brdgVar.__len__()", brdgVar.__len__())
                                if (brdgVar.__len__() >= 1):
                                    BridgesWithRehabilitationAndRepairWork = brdgVar[0]
                                else:
                                    BridgesWithRehabilitationAndRepairWork = 0
                            if (brdgRowNo == 5):
                                brdgVar = re.findall(r"[-+]?\d*\.\d+|\d+", brdgCell.text)
                                print("brdgVar.__len__()", brdgVar.__len__())
                                if (brdgVar.__len__() >= 1):
                                    BridgesWithCantilever = brdgVar[0]
                                else:
                                    BridgesWithCantilever = 0


    print("dictCells details--->>",dictCells)
    e_major = dictCells['Major Activities'].strip()
    #print("e_major--->>>>>",e_major)
    if (e_major.find('Highway Project') >= 0):
        #print("1111")
        HighwayProject = True
    if (e_major.find('Bridge Project') >= 0):
        #print("2222")
        BridgeProject = True
    if (e_major.find('Tunnel Project') >= 0):
        #print("3333")
        TunnelProject = True
    if (e_major.find('Revenue Project') >= 0):
        RevenueProject = True
    if (e_major.find('Other') >= 0):
        OthersProject = True
    if (e_major.find('Expressway Project') >= 0):
        ExpresswayProject = True
    if (e_major.find('Airport Runway Project') >= 0):
        AirportRunwayProject = True
    if (e_major.find('IT Project') >= 0):
        ITProject = True
    NameOfWork = dictCells['Name of Work']
    if (dictCells.get('Country')):
        Country = dictCells['Country']
    if (dictCells.get('State')):
        State = dictCells['State']
    if (dictCells.get('Employer Name')):
        EmployerName = dictCells['Employer Name']
    EmployerAddress = dictCells['Employer Address']
    Client = dictCells['Client']
    ClientAddress = dictCells['Client Address']
    #print(dictCells['Start Date'],"<--start-->",dictCells['Start Date'][2:],"start date withput")
    if (dictCells.get('Start Date')):
        StartDate = (datetime.strptime(dictCells['Start Date'].strip(), '%d/%m/%Y'))
    #print(dictCells.get('Completion Date:'),'Completion Date:...................')
    if (dictCells.get('Completion Date:') and '' != dictCells.get('Completion Date:')):
        CompletionDate = (datetime.strptime(dictCells['Completion Date:'].strip(), '%d/%m/%Y'))#date has \r\n\t appened in the beginning so trimming the date
    else:
        CompletionDate ='00/00/0000'
    ProjectCost = dictCells['Project Cost']
    e_model = dictCells['Whether EPC or PPP or  Hybrid Annuity Model'].strip()
    #print(e_model, "<<<---- e_model *********************")
    #print(e_model, "<<<---- e_model *********************",e_model.find('EPC'),e_model.find('PPP'),e_model.find('Hybrid Annuity Model'))
    if (e_model.find('EPC')==0):
        EPC = True
    if (e_model.find('PPP') == 0):
        PPP = True
    if (e_model.find('Hybrid Annuity Model')==0):
        HybridAnnuityModel = True
    Designation = dictCells['Designation']
    #EnterDesignation =
    BriefDescritionOfDuties = dictCells['Description of Duties']
    NatureOfAssignment = dictCells['Nature of Assignment']
    # Open database connection
    db = MySQLdb.connect(cfg['DB_HOST'], cfg['DB_USER'], cfg['DB_USER_PASSWORD'], cfg['DB_NAME'],use_unicode=True, charset="utf8")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    emailmatch_sql = "SELECT count(*) from SA_CONSULTANT where email LIKE %s"
    select_consultant_sql = "SELECT * from SA_CONSULTANT where email LIKE %s"

    try:
        '''
        select the work_detaills
        if exists then update record
        else 
        insert record
        '''
        print("1aaaaaaaaaaaaaaaaaaa  11111111111111111111aaaaaaaaaaaaaaaaaaaaaaaaaa")
        select_sql= "select ID_work_details_in_depth from work_details_in_depth " \
                    "where ID_CONSULTANT = '%s' " \
                    "and NameOfWork = '%s' " \
                    "and StartDate = '%s' " \
                    "and EmployerName = '%s' " \
                    "and Client = '%s' " \
                    "and NatureOfAssignment = '%s' " \
                    "and Designation = '%s'" %\
                 (e_id,
                  NameOfWork, StartDate, EmployerName, Client, NatureOfAssignment, Designation
                  )
        print("11111111111111111111111111111 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB   11111111111111111111111111111111 select_sql",select_sql)
        cursor.execute(select_sql)
        print("22222222222222222222   222222222222222")
        result = cursor.fetchone()
        print(" 333333333333333   333333333333333333333")
        id_work_details = 0
        print("select_sql result==>>", result)

        if None != result:
            print("5555555555555555               555555555555555555555")
            id_work_details = result[0]
            print("id_work_details=====>>>> ",id_work_details)
            # Update record
            print("update_sql --(e_id,  --->>>", e_id, id_work_details, "id_work_details")
            # update_sql = "UPDATE work_details_in_depth SET BriefDescritionOfDuties=%s, Country=%s, state=%s, EmployerAddress=%s, ClientAddress=%s" \
            #              "WHERE ID_work_details_in_depth=%s and ID_CONSULTANT=%s"
            update_sql = "UPDATE work_details_in_depth SET HighwayProject='%d', BridgeProject='%d', TunnelProject=  '%d', RevenueProject =  '%d', " \
                         "OthersProject = '%d', ExpresswayProject = '%d', AirportRunwayProject = '%d', ITProject = '%d', " \
                         "NameOfWork = '%s', Country = '%s', State = '%s', EmployerName = '%s', EmployerAddress = '%s', Client = '%s', ClientAddress = '%s',  " \
                         "StartDate = '%s', CompletionDate = '%s', " \
                         "ProjectCost = '%f', EPC = '%d', PPP = '%d', HybridAnnuityModel = '%d', Designation = '%s', " \
                         "BriefDescritionOfDuties = '%s', NatureOfAssignment = '%s', " \
                         "Highway2Lane_KM = '%f', Highway4Lane_KM = '%f', Highway6Lane_KM = '%f', Highway2Lane_LandType = '%s', Highway4Lane_LandType = '%s', Highway6Lane_LandType = '%s', " \
                         "Highway2Lane_TerrainHill = '%f', Highway2Lane_TerrainPlain = '%f', Highway4Lane_TerrainHill = '%f', Highway4Lane_TerrainPlain = '%f', " \
                         "Highway6Lane_TerrainHill = '%f', Highway6Lane_TerrainPlain = '%f', " \
                         "ArbitrationCaseHandled = '%d', AchievedFinancialClosure = '%d', EIAProjectInfrastructre = '%d', ArbitrationCaseHandled_Number = '%d', AchievedFinancialClosure_NoOfProjects = '%d', EIAProjectInfrastructre_NoOfProjects = '%d', " \
                         "Bridges6To60M_Number = '%d', Bridges60To200M_Number = '%d', Bridges200To500M_Number = '%d', Bridges500To1000M_Number = '%d', BridgesAbove1000M_Number = '%d', " \
                         "MaxIndividualSpan = '%f', MaxIndividualLength = '%f', TotalLength = '%f', " \
                         "BridgesWithPileWellFoundation = '%d', BridgesWithRehabilitationAndRepairWork = '%d', BridgesWithCantilever = '%d' " \
                         " WHERE ID_work_details_in_depth=%s and ID_CONSULTANT=%s" % \
                         (HighwayProject, BridgeProject, TunnelProject, RevenueProject,
                          OthersProject, ExpresswayProject, AirportRunwayProject, ITProject,
                          NameOfWork, Country, State, EmployerName, EmployerAddress, Client, ClientAddress,
                          StartDate, CompletionDate,
                          float(ProjectCost.replace(',', '')), EPC, PPP, HybridAnnuityModel, Designation,
                          BriefDescritionOfDuties, NatureOfAssignment,
                          float(Highway2Lane_KM), float(Highway4Lane_KM), float(Highway6Lane_KM), Highway2Lane_LandType, Highway4Lane_LandType, Highway6Lane_LandType,
                          float(Highway2Lane_TerrainHill), float(Highway2Lane_TerrainPlain),
                          float(Highway4Lane_TerrainHill), float(Highway4Lane_TerrainPlain),
                          float(Highway6Lane_TerrainHill), float(Highway6Lane_TerrainPlain),
                          ArbitrationCaseHandled, AchievedFinancialClosure, EIAProjectInfrastructre,
                          int(ArbitrationCaseHandled_Number), int(AchievedFinancialClosure_NoOfProjects), int(EIAProjectInfrastructre_NoOfProjects),
                          int(Bridges6To60M_Number), int(Bridges60To200M_Number), int(Bridges200To500M_Number), int(Bridges500To1000M_Number), int(BridgesAbove1000M_Number),
                          float(MaxIndividualSpan), float(MaxIndividualLength), float(TotalLength),
                          int(BridgesWithPileWellFoundation), int(BridgesWithRehabilitationAndRepairWork), int(BridgesWithCantilever),
                          id_work_details, int(e_id))


            #data = [NameOfWork, State, State, EmployerAddress, ClientAddress, id_work_details, e_id]
            #data = [id_work_details, e_id]
            cursor.execute(update_sql)
            db.commit()
        else:
            print("6666666666666666666666  666666666666666")
            select_max_sql = "select max(ID_work_details_in_depth) from work_details_in_depth " \
                    "where ID_CONSULTANT = %s "
            cursor.execute(select_max_sql,[e_id])
            result  = cursor.fetchone()
            print("result--------<<<<",result)
            if None == result or None == result[0]:
                id_work_details= 1
            else:
                id_work_details = result[0] + 1

            # insert record
            print(id_work_details, "id_work_details ::::::: bfr insert record-->>", ProjectCost, " e_id==", e_id,
                  " project_id==", counter_files)
            insert_sql = "INSERT INTO work_details_in_depth (ID_work_details_in_depth, ID_CONSULTANT, HighwayProject, BridgeProject, TunnelProject, RevenueProject, OthersProject, ExpresswayProject, AirportRunwayProject, ITProject, " \
                         "NameOfWork, Country, State, EmployerName, EmployerAddress, Client, ClientAddress, StartDate, " \
                         "CompletionDate, " \
                         "ProjectCost, EPC, PPP, HybridAnnuityModel, Designation, BriefDescritionOfDuties, NatureOfAssignment, " \
                         "Highway2Lane_KM, Highway4Lane_KM, Highway6Lane_KM, Highway2Lane_LandType, Highway4Lane_LandType, Highway6Lane_LandType, " \
                         "Highway2Lane_TerrainHill, Highway2Lane_TerrainPlain, Highway4Lane_TerrainHill, Highway4Lane_TerrainPlain, Highway6Lane_TerrainHill, Highway6Lane_TerrainPlain, " \
                         "ArbitrationCaseHandled, AchievedFinancialClosure, EIAProjectInfrastructre,  ArbitrationCaseHandled_Number, AchievedFinancialClosure_NoOfProjects, EIAProjectInfrastructre_NoOfProjects, " \
                         "Bridges6To60M_Number, Bridges60To200M_Number, Bridges200To500M_Number, Bridges500To1000M_Number, BridgesAbove1000M_Number," \
                         "MaxIndividualSpan, MaxIndividualLength, TotalLength, " \
                         "BridgesWithPileWellFoundation, BridgesWithRehabilitationAndRepairWork, BridgesWithCantilever" \
                         ") " \
                         "VALUES ('%d','%d', '%d', '%d', '%d', '%d','%d', '%d', '%d', '%d', " \
                         "'%s', '%s', '%s', '%s','%s','%s','%s','%s'," \
                         "'%s', " \
                         "'%f','%d', '%d', '%d','%s','%s','%s'," \
                         "'%f', '%f', '%f', '%s','%s', '%s', " \
                         "'%f', '%f', '%f', '%f', '%f', '%f', " \
                         "'%d', '%d', '%d', '%d', '%d', '%d', " \
                         "'%d', '%d', '%d', '%d', '%d', " \
                         "'%f', '%f', '%f'," \
                         "'%d', '%d', '%d' )" % \
                         (id_work_details, int(e_id), HighwayProject, BridgeProject, TunnelProject, RevenueProject,
                          OthersProject, ExpresswayProject, AirportRunwayProject, ITProject,
                          NameOfWork, Country, State, EmployerName, EmployerAddress, Client, ClientAddress, StartDate,
                          CompletionDate,
                          float(ProjectCost.replace(',', '')), EPC, PPP, HybridAnnuityModel, Designation,
                          BriefDescritionOfDuties, NatureOfAssignment,
                          float(Highway2Lane_KM), float(Highway4Lane_KM), float(Highway6Lane_KM), Highway2Lane_LandType,
                          Highway4Lane_LandType, Highway6Lane_LandType,
                          float(Highway2Lane_TerrainHill), float(Highway2Lane_TerrainPlain),
                          float(Highway4Lane_TerrainHill), float(Highway4Lane_TerrainPlain),
                          float(Highway6Lane_TerrainHill), float(Highway6Lane_TerrainPlain),
                          ArbitrationCaseHandled, AchievedFinancialClosure, EIAProjectInfrastructre,
                          int(ArbitrationCaseHandled_Number), int(AchievedFinancialClosure_NoOfProjects),
                          int(EIAProjectInfrastructre_NoOfProjects),
                          int(Bridges6To60M_Number), int(Bridges60To200M_Number), int(Bridges200To500M_Number),
                          int(Bridges500To1000M_Number), int(BridgesAbove1000M_Number),
                          float(MaxIndividualSpan), float(MaxIndividualLength), float(TotalLength),
                          int(BridgesWithPileWellFoundation), int(BridgesWithRehabilitationAndRepairWork),
                          int(BridgesWithCantilever)
                          )
            cursor.execute(insert_sql)
            # Commit your changes in the database
            print("details work cmmmmmmit (e_id,  --->>>", e_id, )
            db.commit()
            # if email already in the database do not insert, Update the record
    except Exception as err:
        print("Exception occured:::",err)
        db.rollback()
    finally:
        db.close()
