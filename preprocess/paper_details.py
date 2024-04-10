import json
import requests
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from faker import Faker
import pandas as pd

# Ensure you've downloaded the necessary NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')

faker = Faker()

# Update the path to where your JSON data is stored and where you want to save the CSV
path = "/home/ranaislek/Desktop/SDM-P1-GRAPH/data"  # Adjust this to your actual data directory

# Load raw paper data from a JSON file
with open(f'{path}/matched_papers_on_topics.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)

# Extract paper IDs from the loaded JSON data
paper_ids = [paper['paperId'] for paper in raw_paper_data]

# Semantic Scholar API setup
api_key = "q6oxPwzi1a4IL9ijR8XLX4yw9e4awxvF6It1DE7D"  # Replace with your actual API key
headers = {'X-API-KEY': api_key}

def nltk_keywords(abstract):
    """Extract keywords from an abstract using NLTK."""
    if abstract is None:
        return ""
    tokens = word_tokenize(abstract.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    freq_dist = FreqDist(filtered_tokens)
    keywords = freq_dist.most_common(20)
    return ','.join([keyword[0] for keyword in keywords])

def get_paper_data(paper_id):
    """Fetch paper data from Semantic Scholar API and process keywords."""
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}'
    authors_url = f'{url}/authors'
    paper_main_author_params = {'fields': 'name'}
    
    # Attempt to fetch main author data
    response = requests.get(authors_url, headers=headers, params=paper_main_author_params)
    name, email = faker.name(), faker.email()  # Default to fake data if real data is unavailable
    
    if response.status_code == 200 and 'data' in response.json() and response.json()['data']:
        # Ensure there's at least one author before attempting to access the list
        name = response.json()['data'][0]['name']
        email = name.replace(" ", "_") + "@example.com"
    
    # Fetch the main paper data
    paper_data_query_params = {'fields': 'title,abstract,year,embedding.specter_v2,externalIds'}
    response = requests.get(url, headers=headers, params=paper_data_query_params)
    
    if response.status_code == 200:
        response_data = response.json()
        response_data['MA_name'] = name
        response_data['MA_email'] = email
        response_data['keywords'] = nltk_keywords(response_data.get('abstract', ''))
        response_data['doi'] = response_data.get('externalIds', {}).get('DOI', None)
        return response_data
    else:
        print(f"Failed to fetch data for paper ID: {paper_id}")
        return None
    
# Process each paper ID to fetch and prepare paper details
paper_details_temp = [get_paper_data(pid) for pid in paper_ids]
# Filter out None values after collecting responses
paper_details = [pd for pd in paper_details_temp if pd]

# Convert the list of paper details into a DataFrame and save as a CSV file
df = pd.DataFrame([pd for pd in paper_details if pd])  # Filter out any None values
df.to_csv(f'{path}/papers_details.csv', index=False)
print("CSV file saved.")
