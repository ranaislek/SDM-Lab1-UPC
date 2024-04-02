import json
import requests
import time
#read json file
raw_paper_data = None
path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
with open(path + '/matched_papers_on_field_Machine Learning.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)

#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]


paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}

author_details = []

def get_author_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    # Define which details about the paper you would like to receive in the response
    
    authors_url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id + '/authors'


    

    #find main author
    #paper_data_query_params = {'fields': 'authors.authorId'}
    paper_main_author_params = {'fields': 'name'}
    response = requests.get(authors_url, params=paper_main_author_params, headers=headers)
    #get all the authors
    authors = response.json()['data']
    print(authors)

    #create a dictionary pairs that maps paperId to authorId

    for author in authors:
        authorId = author['authorId']

        author_details.append({'paperId': paper_id, 'authorId': authorId})


   
   
# Fetch paper details for each paper_id

for paper_id in paper_ids:
    get_author_data(paper_id)
 
    
import csv
import pandas as pd
df = pd.DataFrame(author_details)
print(df.head())
df.to_csv('written_by.csv', index=False)
print("done")

