
from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd


path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
authors = pd.read_csv(path + '/authors.csv')


fake = Faker()
#find unique affiliations
unique_affiliations = authors['affiliations'].unique()


type = ["University", "Company"]

# generate random affiliations

affiliations = []
for affiliation in unique_affiliations:
    # Random type
    affiliation_type = random.choice(type)
    
    #generate fake address
    address = fake.address()

    #generate fake email
    email = fake.email()

    #generate fake phone number
    phone_number = fake.phone_number()

    #generate fake website
    website = fake.url()

    affiliations.append({
        "name": affiliation,
        "type": affiliation_type,
        "address": address,
        "email": email,
        "phone_number": phone_number,
        "website": website
    })

    # create a affiliated_with relationship between authors and affiliations


df = pd.DataFrame(affiliations)
df.to_csv(path + '/affiliations.csv', index=False)

affiliated_with = []
for index, row in authors.iterrows():
    author_id = row['authorId']
    affiliation = row['affiliations']
    affiliated_with.append({
        "authorId": author_id,
        "affiliation": affiliation
    })

df = pd.DataFrame(affiliated_with)
df.to_csv(path + '/affiliated_with.csv', index=False)
    

