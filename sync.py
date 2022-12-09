import urllib
from sqlalchemy import create_engine, Table, MetaData, text, update
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=173.248.174.46,1533;"
                                 "DATABASE=sb091002.nighby.com;"
                                 "UID=sa;"
                                 "PWD=xkJDuQv0*GfdS0sb")


engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
metadata_obj = MetaData()
provider_dict = {}
with engine.connect() as connection:
    result = connection.execute(text("select ProviderId, ProviderName from dbo.EOL_Providers"))
    for row in result:
        provider_dict.update({row["ProviderId"]:row["ProviderName"]})
print(provider_dict)

listings_update = []
with engine.connect() as connection:
    result = connection.execute(text("select ProviderId, SERPIndexID from dbo.EOL_SERPIndex"))
    for row in result:
       listings_update.append({"ProviderName":provider_dict[row["ProviderId"]],"SERPIndexID":row["SERPIndexID"]})

print(listings_update)

listings = Table("EOL_SERPIndex", metadata_obj, autoload_with=engine)
for i in listings_update:
    with engine.begin() as connection:
     connection.execute(listings.update().where(listings.c.SERPIndexID == i["SERPIndexID"]),{"ProviderName":i["ProviderName"]} )

