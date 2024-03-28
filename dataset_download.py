import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define the paper search endpoint URL
url = 'https://api.semanticscholar.org/graph/v1/paper/search'

api_key = os.getenv('API_KEY')  # Use this line instead if you have set the API key as an environment variable
# Define headers with API key
headers = {'x-api-key': api_key}



# Define the required query parameter and its value (in this case, the keyword we want to search for)
query_params = {
    'query': 'KnowledgeGraph',
    'limit': 10
}

# Define a separate function to make a request to the paper details endpoint using a paper_id. This function will be used later on (after we call the paper search endpoint).
def get_paper_data(paper_id):
  url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

  # Define which details about the paper you would like to receive in the response
  paper_data_query_params = {'fields': 'title,year,abstract,authors.name'}

  # Send the API request and store the response in a variable
  response = requests.get(url, params=paper_data_query_params, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    return None

# Make the GET request to the paper search endpoint with the URL and query parameters
search_response = requests.get(url, params=query_params, headers=headers)
print(search_response)
# Check if the request was successful (status code 200)
if search_response.status_code == 200:
  search_response = search_response.json()

  # Retrieve the paper id corresponding to the 1st result in the list
  paper_id = search_response['data'][0]['paperId']
  # print(paper_id)

  # Retrieve the paper details corresponding to this paper id using the function we defined earlier.
  paper_details = get_paper_data(paper_id)

  # Check if paper_details is not None before proceeding
  if paper_details is not None:
    
    # Your code to work with the paper details goes here
    print(paper_details)
    
  else:
    print("Failed to retrieve paper details.")

else:
  # Handle potential errors or non-200 responses
  print(f"Relevance Search Request failed with status code {search_response.status_code}: {search_response.text}")