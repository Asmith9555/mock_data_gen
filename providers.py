from faker import Faker;
import json;
from faker.providers import company;
from sqlalchemy import create_engine, Table, MetaData;

fake = Faker()
fake.add_provider(company)

provider_ids = range(3, 101)
print(provider_ids)
provider_list=[]
for i in provider_ids:
    provider_list.append({
        "ProviderName":fake.company(),
    })


print(provider_list)


import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=173.248.174.46,1533;"
                                 "DATABASE=sb091002.nighby.com;"
                                 "UID=sa;"
                                 "PWD=xkJDuQv0*GfdS0sb")


engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
metadata_obj = MetaData()
listings = Table("EOL_Providers", metadata_obj, autoload_with=engine)
for i in provider_list:
    with engine.begin() as connection:
        connection.execute(listings.insert(), i)