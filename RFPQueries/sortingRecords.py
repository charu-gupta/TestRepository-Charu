#Original file 'C:\AgilyticsCharu\PyExe-Charu\Trials\storingRecords.py'

from operator import itemgetter
#listProjectConsultant = [(3, '2A', 22, 4, 'No. Of Projects (count)'), (3, '2B', 24, 5, 'No. Of Projects (count)'), (1, 3, 25, 11.523200035095215, 'in Years'), (2, 3, 20, 4.589000225067139, 'in Years'), (3, 3, 20, 4.69320011138916, 'in Years'), (5, 3, 20, 4.728799819946289, 'in Years'), (1, None, -1, 58.49850034713745, ''), (2, None, -1, 9.158900141716003, ''), (3, None, -1, 32.85240018367767, ''), (4, None, -1, 22.816400051116943, ''), (5, None, -1, 22.662999510765076, ''), (1, None, -1, 58.49850034713745, ''), (2, None, -1, 9.158900141716003, ''), (3, None, -1, 32.85240018367767, ''), (4, None, -1, 22.816400051116943, ''), (5, None, -1, 22.662999510765076, '')]
#listQualificationConsultant = [(2, '1A', 21), (3, '1A', 21), (1, '1B', 3), (2, '1B', 3), (3, '1B', 3), (4, '1B', 3), (5, '1B', 3), (6, '1B', 3), (1, '1C', 1), (2, '1C', 1), (3, '1C', 1), (4, '1C', 1), (5, '1C', 1), (6, '1C', 1), (5, '1D', 7)]# id_consultant, RFPName, RFPMarks
def ftnGetSortedRecords(listQualificationConsultant,listProjectConsultant, listCurrCoConsultant):
    dict_record ={}
    list_ConsultantResults = []

    for i,row in enumerate(listQualificationConsultant):
        del dict_record
        dict_record = {}
        #dict_record = list_ConsultantResults[dict_record.id==item[0]]
        # write data in xls RFP name, RFP Marks
        print("SORTING     SORTING +++++++++++++++")
        print("________________   SOTRDJDJIHFRhitrihghrhggkrkngnrgn    _________________________  ")
        print("row-->",row,"list_ConsultantResults== ",list_ConsultantResults)
        id_index = next((index for (index, d) in enumerate(list_ConsultantResults) if d['id'] == row[0]), -1)
        if id_index >= 0:
            dict_record = list_ConsultantResults[id_index]
            print(id_index, " id_index", dict_record)
            #dict_record['id'] = row[0]
            dict_record['RFPName'] = dict_record['RFPName'] + (row[1],)
            dict_record['RFPMarks'] = dict_record['RFPMarks'] + (row[2],)
            dict_record['TotalMarks'] = dict_record['TotalMarks'] +  row[2]
            print(dict_record, "row= ", row, "dict_record['RFPName']==", dict_record['RFPName'])
        else:

            dict_record['id'] = row[0]
            dict_record['RFPName']=(row[1],)
            dict_record['RFPMarks']=(row[2], )
            dict_record['TotalMarks']= row[2]

            dict_record['name'] = row[3]
            #dict_record['DOB'] = row[4]
            dict_record['email'] = row[5]
            dict_record['state'] = row[6]
            dict_record['district'] = row[7]
            dict_record['address'] = row[8]
            dict_record['pan'] = row[9]
            dict_record['mobile'] = row[10]
            dict_record['alter_mobile'] = row[11]
            dict_record['landline'] = row[12]

            print(i," <<<<< dict_record",dict_record)
        if(id_index >= 0) :
            list_ConsultantResults[id_index]= dict_record
        else:
            list_ConsultantResults.append(dict_record)


    for i,row in enumerate(listProjectConsultant):
        del dict_record
        dict_record = {}
        #dict_record = list_ConsultantResults[dict_record.id==item[0]]
        # write data in xls RFP name, RFP Marks
        print("row-->",row,"list_ConsultantResults== ",list_ConsultantResults)
        id_index = next((index for (index, d) in enumerate(list_ConsultantResults) if d['id'] == row[0]), -1)
        if id_index >= 0:
            dict_record = list_ConsultantResults[id_index]
            print(id_index, " id_index", dict_record)


            #dict_record['id'] = row[0]
            dict_record['RFPName'] = dict_record['RFPName'] + (row[1],)
            dict_record['RFPMarks'] = dict_record['RFPMarks'] + (row[2],)
            dict_record['TotalMarks'] = dict_record['TotalMarks'] +  row[2]
            print(dict_record, "row= ", row, "dict_record['RFPName']==", dict_record['RFPName'])
        else:

            dict_record['id'] = row[0]
            dict_record['RFPName']=(row[1],)
            dict_record['RFPMarks']=(row[2], )
            dict_record['TotalMarks']= row[2]

            dict_record['name'] = row[3]
            #dict_record['DOB'] = row[4]
            dict_record['email'] = row[5]
            dict_record['state'] = row[6]
            dict_record['district'] = row[7]
            dict_record['address'] = row[8]
            dict_record['pan'] = row[9]
            dict_record['mobile'] = row[10]
            dict_record['alter_mobile'] = row[11]
            dict_record['landline'] = row[12]
            print(i," <<<<< dict_record",dict_record)
        if(id_index >= 0) :
            list_ConsultantResults[id_index]= dict_record
        else:
            list_ConsultantResults.append(dict_record)
    for i,row in enumerate(listCurrCoConsultant):
        del dict_record
        dict_record = {}
        #dict_record = list_ConsultantResults[dict_record.id==item[0]]
        # write data in xls RFP name, RFP Marks
        print("SORTING     SORTING +++++++++++++++ listCurrCoConsultant")
        print("________________   SOTRDJDJIHFRhitrihghrhggkrkngnrgn    _________________________  ")
        print("listCurrCoConsultant row-->",row,"list_ConsultantResults== ",list_ConsultantResults)
        id_index = next((index for (index, d) in enumerate(list_ConsultantResults) if d['id'] == row[0]), -1)
        if id_index >= 0:
            dict_record = list_ConsultantResults[id_index]
            print(id_index, " id_index", dict_record)
            #dict_record['id'] = row[0]
            dict_record['RFPName'] = dict_record['RFPName'] + (row[1],)
            dict_record['RFPMarks'] = dict_record['RFPMarks'] + (row[2],)
            dict_record['TotalMarks'] = dict_record['TotalMarks'] +  row[2]
            print(dict_record, "row= ", row, "dict_record['RFPName']==", dict_record['RFPName'])
        else:

            dict_record['id'] = row[0]
            dict_record['RFPName']=(row[1],)
            dict_record['RFPMarks']=(row[2], )
            dict_record['TotalMarks']= row[2]

            dict_record['name'] = row[3]
            #dict_record['DOB'] = row[4]
            dict_record['email'] = row[5]
            dict_record['state'] = row[6]
            dict_record['district'] = row[7]
            dict_record['address'] = row[8]
            dict_record['pan'] = row[9]
            dict_record['mobile'] = row[10]
            dict_record['alter_mobile'] = row[11]
            dict_record['landline'] = row[12]

            print(i," <<<<< dict_record",dict_record)
        if(id_index >= 0) :
            list_ConsultantResults[id_index]= dict_record
        else:
            list_ConsultantResults.append(dict_record)
    print("-----CHARUUUUUUUUUUUU-------------------------", list_ConsultantResults)
    #list_ConsultantResults.sort(key=itemgetter(0))
    #print("zooom",list_ConsultantResults.sort(key=lambda x: x.'id'))
    #print(sorted(list_ConsultantResults, key=(itemgetter('TotalMarks')), reverse=True),"list_ConsultantResults SORTED ON T marks")
    #list_ConsultantResults=sorted(list_ConsultantResults, key=(itemgetter('TotalMarks'),itemgetter('id')),reverse=True)
    list_ConsultantResults=sorted(list_ConsultantResults, key=(itemgetter('id')),reverse=False)
    print("aft id sorting on IDs and  rev=F :::: ", list_ConsultantResults)
    list_ConsultantResults=sorted(list_ConsultantResults, key=(itemgetter('TotalMarks')),reverse=True)
    print("aft TMrks sorting on TMarks and rev=True :::: ", list_ConsultantResults)
    tom_index = next((index for (index, d) in enumerate(list_ConsultantResults) if d['id'] == 2), None)
    #dict_record = list_ConsultantResults[dict_record.get['id']==row[0]]
    print("tom_index=============>>>",tom_index)
    #print(tom_index,"index data for id==::2d*** LIST FOUND is== ",list_ConsultantResults[tom_index])
    return list_ConsultantResults
