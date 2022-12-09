import decimal
import json
import urllib
from sqlalchemy import create_engine, Table, MetaData, text, update
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=173.248.174.46,1533;"
                                 "DATABASE=sb091002.nighby.com;"
                                 "UID=sa;"
                                 "PWD=xkJDuQv0*GfdS0sb")


engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

metadata_obj = MetaData()
listings = Table("EOL_SERPIndex", metadata_obj, autoload_with=engine)
column_labels = [c.name for c in listings.columns]

master_list = []
with engine.connect() as connection:
    result = connection.execute(text("select * from dbo.EOL_SERPIndex"))
    for row in result:
        result_dict = {}
        for i,j in enumerate(row):
            result_dict.update({column_labels[i]:j})
        master_list.append(result_dict)

dead_keys = []
for i,j in enumerate(master_list):
    k = {key:val for key, val in j.items() if val != None}
    master_list[i] = k
    for (key, val) in master_list[i].items():
        if not isinstance(val, str):
            try: 
                master_list[i][key] = float(val)
                if float(val).is_integer():
                   master_list[i][key] = int(val)
            except: 
                master_list[i][key] = str(val)
def removecapt(dictionary):
    new_dictionary = {}
    for a in dictionary.keys():
        new_dictionary[a.lower()] = dictionary[a]
    return new_dictionary
for i,j in enumerate(master_list):
    master_list[i]=removecapt(j)
    location = str(j.pop("Longitude")) +", "+str(j.pop("Latitude"))
    master_list[i].update({"geopoint":location})
for i in master_list:
    i.pop('serpindexid')
print(master_list[0])

with open('data.json', 'w') as json_file:
    json.dump(master_list, json_file)


