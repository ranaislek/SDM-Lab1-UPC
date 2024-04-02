import json
import requests
import time
#read json file
path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
raw_paper_data = None
with open(path + '/matched_papers_on_field_Machine Learning.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)


#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]


paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}
# Fetch paper details for each paper_id
reference_details = []
def get_reference_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    paper_data_query_params = {'fields': 'references'}

    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        paperId = response['paperId']
        references = response['references']
        for reference in references:
            referenceId = reference['paperId']
            #create a new dictionary to store the paperId and referenceId
            reference_details.append({'paperId': paperId, 'referenceId': referenceId})
        
    else:
        print(response.status_code)
        
   
for paper_id in paper_ids:
    get_reference_data(paper_id)
#convert this list of dictionaries to a csv file
import csv
import pandas as pd
df = pd.DataFrame(reference_details)
print(df.head(15))
#df.to_csv('papers_details.csv', index=False)
print("done")

