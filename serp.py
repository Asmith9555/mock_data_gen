from faker import Faker;
import base64
import json;
from faker.providers import company, lorem, misc, address, python;
from sqlalchemy import create_engine, Table, MetaData;

fake = Faker()
fake.add_provider(company)
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(address)
fake.add_provider(python)
fake_listings = [{
    'Title':fake.text(max_nb_chars=20),
    'Reviewed':fake.random_int(min=0, max=1),
    'ListingID':fake.random_int(min=1, max=100000),
    'ActiveDate':fake.date_between(start_date='-30d', end_date='today').strftime("%Y-%m-%d"),
    'ExpireDate':fake.date_between(start_date='today', end_date='+90d').strftime("%Y-%m-%d"),
    'Detail':fake.paragraph(nb_sentences=4),
    'ImageSmall':'https://source.unsplash.com/250x200',
    'ImageLarge':'https://source.unsplash.com/350x300',
    'Price':fake.pyfloat(right_digits=2, left_digits=2, positive=True),
    'MSRP':fake.pyfloat(right_digits=2, left_digits=2, positive=True),
    'ProviderId':fake.random_int(min=1, max= 100),
    'Address1': fake.address(),
    'City':fake.city(),
    'PostalCode':fake.postcode(),
    'Brand':fake.company(),
    'Phone':fake.phone_number(),
    'Email':fake.email(),
    'ProviderVerified':fake.random_int(min=0, max=1),
    'NighbyCertified':fake.random_int(min=0, max=1),
    'ChamberMember': fake.random_int(min=0, max=1),
    'CharterMember': fake.random_int(min=0, max=1),
    'Markets': fake.random_element(elements=('Morrilton', 'Clinton', 'Damascus', 'Benton', 'Mayflower', 'Conway', 'Greenbrier')),
    'Longitude':float(fake.latitude()),
    'Latitude':float(fake.longitude()),
    'Categories':fake.random_element(elements=('Food', 'Outdoors', 'Pets', 'Farm', 'Household Supplies', 'Hardware', 'Auto')),
    'Tags':fake.words(nb=6),
    'RecordDate':'2022-11-10 15:10:10',
    "ProviderImage":"https://source.unsplash.com/50x50"
    } for x in range(100)]
print(fake_listings)
for i in fake_listings: 
    print(i)
    list_tags = i["Tags"]
    str_tags = ""
    for f in list_tags:
        str_tags += f
        str_tags += ', '
    str_tags = str_tags[:-2]
    print(i["Tags"])
    i["Tags"]=str_tags
    phone = i['Phone']
    phone_fixed = phone.split('x')[0].replace('.', '').replace('001','').replace('-','').replace('+1','').replace('(','').replace(')','')
    print(phone_fixed)
    i['Phone']=phone_fixed

with open('data.json', 'w') as jsonFile:
    json.dump(fake_listings, jsonFile)


import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=173.248.174.46,1533;"
                                 "DATABASE=sb091002.nighby.com;"
                                 "UID=sa;"
                                 "PWD=xkJDuQv0*GfdS0sb")


engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
metadata_obj = MetaData()
listings = Table("EOL_SERPIndex", metadata_obj, autoload_with=engine)
for i in fake_listings:
    with engine.begin() as connection:
        connection.execute(listings.insert(), i)