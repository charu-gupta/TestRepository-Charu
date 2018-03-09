import datetime

def age(when, on=None):
    if on is None:
        on = datetime.date.today()
    was_earlier = (on.month, on.day) < (when.month, when.day)
    return on.year - when.year - (was_earlier)
'''

select w.ID_CONSULTANT, w.ID_work_details_in_depth, dob, designation, Bridges60To200M_Number 
 from work_details_in_depth w, sa_consultant c 
 where w.ID_CONSULTANT=c.ID_CONSULTANT and
  ( HighwayProject= 1)
 and designation IN (select designation from master_designation where code IN ('TL','RE','BE')) 
 and  Bridges60To200M_Number >= 0  and  TotalLength >= 0  and  
 BridgesWithPileWellFoundation >= 0  and  
 BridgesWithRehabilitationAndRepairWork >= 0 and  BridgesWithCantilever >= 0  and  
 ((Highway2Lane_KM >= 10 and ProjectCost >= 1 ) OR Highway4Lane_KM >= 10 OR Highway6Lane_KM >= 10 ) 
 and w.ID_CONSULTANT NOT IN (select ID_CONSULTANT from work_details_in_depth where client in ('Ethiopian Roads Authority' ) and CompletionDate = '0000-00-00' ) 
 and dob >= STR_TO_DATE(CONCAT(year(curdate())-55,'-',month(curdate()),'-',day(curdate())), '%Y-%m-%d');
 
 
select * from sa_companies_details where  TIMESTAMPDIFF(YEAR, fromYearAsDate,curdate()) >= 5 and toYearAsDate='0000-00-00'

'''
data =[]
value = 'PG - M.E/M.Tech in Water Resources Engineering'.strip()
#value = cellObj.value.strip()
arrQualiName = value.split("-")
print("len(arrQualiName)",len(arrQualiName))
if None != len(arrQualiName) and len(arrQualiName) > 1:
    print("111 ",arrQualiName)
    data += [arrQualiName[1]]
else:
    print("2222 ", arrQualiName)
    data += [arrQualiName[0].strip()]

print("dtat",data," **** arrQuali $$$$$ ",arrQualiName)