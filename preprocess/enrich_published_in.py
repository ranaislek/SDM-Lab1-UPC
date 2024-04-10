#read conferences
import pandas as pd
from faker import Faker
import uuid

faker = Faker()

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
conferences = pd.read_csv(path + '/conferences.csv')


df = pd.DataFrame(conferences)
#print(df.head())

#for each conference, create a editions and add city and year information

editions = []

for index, row in conferences.iterrows():
    conference_name = row['name']
    url = row['url']
    #create a random integer between 3 and 6
    edition_count = faker.random_int(4, 8)
    for i in range(1,edition_count):
        city = faker.city()
        year = faker.year()
        edition = i
        conference_id = uuid.uuid4()
        editions.append({
            "ss_venue_id": conference_id,
            "name": conference_name,
            "url": url,
            "city": city,
            "year": year,
            "edition": edition
        }) 

df = pd.DataFrame(editions)
#only have 7 different conferences with different names
names = df['name'].unique()
#choose 7 random names from the list
names = faker.random_choices(names, length=7)
#filter the df with the chosen names
df = df[df['name'].isin(names)]


df.to_csv(path + '/conferences_enriched.csv', index=False)
#print(df.head())

#read journals

journals = pd.read_csv(path + '/journals.csv')



#print(df.head())

#for each journal, create a volumes and add volume and year information

volumes = []

for index, row in journals.iterrows():
    journal_name = row['name']
    url = row['url']
    issn = row['issn']
    #create a random integer between 3 and 6
    volume_count = faker.random_int(4, 8)
    for i in range(1,volume_count):
        year = faker.year()
        volume = i
        journal_id = uuid.uuid4()
        volumes.append({
            "ss_venue_id": journal_id,
            "name": journal_name,
            "url": url,
            "year": year,
            "volume": volume
        })

df = pd.DataFrame(volumes)
#only have 7 different journals with different names
names = df['name'].unique()
#choose 7 random names from the list
names = faker.random_choices(names, length=7)
#filter the df with the chosen names
df = df[df['name'].isin(names)]

df.to_csv(path + '/journals_enriched.csv', index=False)
#print(df.head())



#read papers
papers = pd.read_csv(path + '/papers_details.csv')



choice = ['conference', 'journal']
published_in = []
for index, row in papers.iterrows():
    paper_id = row['paperId']

    #random choice between conference and journal
    venue_type = faker.random.choice(choice)

    #create a random integer between 1 and 8
    publish_count = faker.random_int(1, 8)

    if venue_type == "conference":
        venue = faker.random.choice(conferences['name'])
        #read conferences_enriched.csv
        conferences =  pd.read_csv(path + '/conferences_enriched.csv')
        for i in range(1,publish_count):
        #get the ss_venue_id of the venue with name venue and with edition i

            conferences_with_same_name = conferences[conferences['name'] == venue]

            conference_with_edition = conferences_with_same_name[conferences_with_same_name['edition'] == i]
            
            if conference_with_edition.empty:
                break
            
            ss_venue_id = conference_with_edition['ss_venue_id'].values[0]
            print(ss_venue_id)

            #create a random publish year between 2017 and 2023
            year = faker.date_time_between(start_date='-5y', end_date='now').year
            
            published_in.append({
                "paper_id": paper_id,
                "ss_venue_id": ss_venue_id,
                "year": year
            })


    else:
        venue = faker.random.choice(journals['name'])
        #read journals_enriched.csv

        journals =  pd.read_csv(path + '/journals_enriched.csv')
        for i in range(1,publish_count):
        #get the ss_venue_id of the venue with name venue and with volume i
            journals_with_same_name = journals[journals['name'] == venue]
            journal_with_edition = journals_with_same_name[journals_with_same_name['volume'] == i]

            if journal_with_edition.empty:
                break
          
            ss_venue_id = journal_with_edition['ss_venue_id'].values[0]
            year = faker.date_time_between(start_date='-5y', end_date='now').year
            published_in.append({
                "paper_id": paper_id,
                "ss_venue_id": ss_venue_id,
                "year" : year
            })

df = pd.DataFrame(published_in)
df.to_csv(path + '/published_in_enriched.csv', index=False)
print(df.head())
   


