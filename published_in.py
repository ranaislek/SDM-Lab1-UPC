import json
import requests
import time
#read json file
raw_paper_data = None
with open('matched_papers_on_field_Machine Learning.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)

#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]


paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}

def get_paper_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

    #paper_data_query_params = {'fields': 'title,abstract,year,authors.authorId,embedding.specter_v2,venue,publicationVenue, journal'}
    paper_data_query_params = {'fields': 'publicationVenue'}
    
    
    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        print(response["publicationVenue"].keys())
        return response
    else:
        print(response.status_code)
        return None
   
# Fetch paper details for each paper_id
paper_details = []
for paper_id in paper_ids:
    paper_data = get_paper_data(paper_id)
    if paper_data is not None:
        paper_details.append(paper_data)
    else:
        print(f"Failed to retrieve paper details for paper ID: {paper_id}")
    #time.sleep(0.5)  # Add a short delay to avoid hitting rate limits
#convert this list of dictionaries to a csv file
# import csv
# import pandas as pd
# df = pd.DataFrame(paper_details)
# print(df.head())
# #df.to_csv('papers_details.csv', index=False)
# print("done")

