import pandas as pd
import json
import requests


#read the csv residing in the data folder

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path

df = pd.read_csv(path + '/written_by.csv')

author_ids = df['authorId'].unique()

# Define the base URL for the author details endpoint
base_url = "https://api.semanticscholar.org/graph/v1/author/"

# Define headers with API key
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

headers = {'X-API-KEY': api_key}

# Define the fields you would like to receive in the response
author_data_query_params = {'fields': 'name,affiliations'}

author_details = []

mock_universities = [
    "University of California, Berkeley",
    "Stanford University",
    "Massachusetts Institute of Technology",
    "Harvard University",
    "California Institute of Technology",
    "University of Oxford",
    "University of Cambridge",
    "University of California, Los Angeles",
    "University of Chicago",
    "Yale University",
    "Princeton University",
    "Columbia University",
    "University of Pennsylvania",
    "University of California, San Diego",
    "University of Washington",
    "University of Michigan",
]

def get_author_details(author_id):
    url = base_url + str(author_id)
    response = requests.get(url, params=author_data_query_params, headers=headers)
    if response.status_code == 200:
        response = response.json()
        if(response['affiliations'] == []):
            #choose one random university from the mock_universities list
            response['affiliations'] = mock_universities[author_id % len(mock_universities)]
            #response['affiliations'] = "None"
        elif(len(response['affiliations']) > 1):
            response['affiliations'] = response['affiliations'][0]
        email = response['name'].replace(" ", "_") + "@gmail.com"
        response['email'] = email
        return response
    else:
        return None

for author_id in author_ids:
    author_data = get_author_details(author_id)
    if author_data is not None:
        author_details.append(author_data)
    else:
        print("Failed to retrieve author details for author_id:", author_id)

#convert this list of dictionaries to a csv file
import csv

df = pd.DataFrame(author_details)
#df.to_csv('authors.csv', index=False)