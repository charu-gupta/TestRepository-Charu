import sys
import MySQLdb
import yaml
cfg=yaml.load(open("config.yaml"))
#print (cfg['DB_NAME'])

print(":::::::::: :::::::: Inside AddWorkDuration.py-----::::::::::::::sys.argv[1]sys.argv length-->",sys.argv.__len__())
e_id=""
if (sys.argv.__len__() >= 1):# and ".html" in sys.argv[1]):
     e_id=sys.argv[1]
     print("WRK AddWorkDuration Depth:::: path--->")
else:
     print("WRK AddWorkDuration Depth:::: FILENAME NOT SUPPLIED  :::::::::::::::::::::::::::::path--->####")

# Open database connection
db = MySQLdb.connect(cfg['DB_HOST'], cfg['DB_USER'], cfg['DB_USER_PASSWORD'], cfg['DB_NAME'],use_unicode=True, charset="utf8")
# prepare a cursor object using cursor() method
cursor = db.cursor()

try:
    ProjDur_sql = "update work_details_in_depth a " \
                  "left join (Select ID_CONSULTANT, StartDate, CompletionDate, datediff(replace(CompletionDate,'0000-00-00', sysdate()), StartDate) / (365 * count(*)) as ProjDur " \
                  "from `work_details_in_depth` group by ID_CONSULTANT, StartDate, CompletionDate) b " \
                  "on a.ID_consultant = b.ID_consultant and a.StartDate = b.StartDate and a.CompletionDate = b.CompletionDate " \
                  "set a.ProjectDuration = b.ProjDur " \
                  "where a.ID_CONSULTANT = %s"
    # if email already in the database do not insert, Update the record
    print("bfr updating proj duration in record--========================>>", )
    cursor.execute(ProjDur_sql,(e_id,  ))
    # Commit your changes in the database
    print("ProjDur_sql cmmmmmmit")
    db.commit()
except Exception as err:
    print("Exception occured:::",err)
    db.rollback()
finally:
    db.close()