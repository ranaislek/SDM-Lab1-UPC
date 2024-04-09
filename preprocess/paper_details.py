import json
import requests
import time
import string
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from faker import Faker
#read json file
faker = Faker()
raw_paper_data = None
path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
with open(path + '/matched_papers_on_topics.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)

#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]


paper_search_url = 'https://api.semanticscholar.org/graph/v1/paper/search'
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"

# Define headers with API key
headers = {'X-API-KEY': api_key}
def nltk_keywords(abstract):
    # Tokenize the paragraph
    if abstract is None:
        return []
    tokens = word_tokenize(abstract.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Remove punctuation and ensure complete words
    filtered_tokens = [re.sub(r'[^\w\s]', '', token) for token in filtered_tokens if re.sub(r'[^\w\s]', '', token)]

    # Calculate frequency distribution
    freq_dist = FreqDist(filtered_tokens)

    # Get the most common words as keywords
    keywords = freq_dist.most_common(20)

    return [keyword[0] for keyword in keywords]
def generate_keywords(title):
    # Tokenize the title by splitting it into words
    words = title.split()

    # Remove punctuation and convert words to lowercase
    keywords = [''.join(c for c in word if c not in string.punctuation).lower() for word in words]

    #eliminate stopwords
    stopwords = ["for", "and", "of", "in", "on", "the", "to", "a", "an", "is", "at", "by", "with", "from"]
    keywords = [word for word in keywords if word not in stopwords]

    return keywords

def get_paper_data(paper_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id
    
    # Define which details about the paper you would like to receive in the response
    
    authors_url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id + '/authors'


    

    #find main author
    #paper_data_query_params = {'fields': 'authors.authorId'}
    paper_main_author_params = {'fields': 'name'}
    response = requests.get(authors_url, params=paper_main_author_params, headers=headers)
    #get the first author name
    #print(response.json())
    # print(response.json()['data'][0]['name'])
    
    name = faker.name()
    email = faker.email()
    
    if response.status_code != 200:
        if "data" in response.json().keys():
            name = response.json()['data'][0]['name']
            #create a mock email
            email = response.json()['data'][0]['name'].replace(" ", "_") + "@gmail.com"
    
    
        # print(email)
    #paper_data_query_params = {'fields': 'title,abstract,year,authors.authorId,embedding.specter_v2,venue,publicationVenue, journal'}
    paper_data_query_params = {'fields': 'title,abstract,year,embedding.specter_v2,externalIds'}
    #paper_data_query_params = {'fields': 'externalIds'}
    
    
    #Send the API request and store the response in a variable
    response = requests.get(url, params=paper_data_query_params, headers=headers)
   
    if response.status_code == 200:
        response = response.json()
        
        #keywords = generate_keywords(response['title'])
        #response['keywords'] = keywords
        response['MA_name'] = name
        response['MA_email'] = email

        keywords = nltk_keywords(response['abstract'])
        #print(keywords)
        response['keywords'] = keywords
        doi = None
        if 'DOI' in response['externalIds']:
           doi = response['externalIds']['DOI']
        response['doi'] = doi
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
import csv
import pandas as pd
df = pd.DataFrame(paper_details)
print(df.head())

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
df.to_csv(path + '/papers_details.csv', index=False)
print("done")

