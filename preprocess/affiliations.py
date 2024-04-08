
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

df = pd.DataFrame(affiliations)
df.to_csv(path + '/affiliations.csv', index=False)
    

