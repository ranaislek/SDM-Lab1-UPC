import requests
import time
#url = "https://api.semanticscholar.org/graph/v1/paper/649def34f8be52c8b66281af98ae884c09aef38b"
url = "https://api.semanticscholar.org/graph/v1/paper/search"
url_bulk = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"
# Define headers with API key
headers = {'X-API-KEY': api_key}

query_params = {
    'fields': 'title,paperId' ,

    'minCitationCount': '10',

    'fieldsOfStudy': 'Computer Science',

    'openAccessPDF': 'true' 
}

def search_papers(query_params):
    url_bulk = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
    search_response = requests.get(url_bulk, headers=headers, params=query_params)
    return search_response.json()

paper_count = 0
def fetch_all_results(query_params, amount,field ):
    all_results = []
    while True:
        if(len(all_results) >= amount):
            break
        response = search_papers(query_params)
        if(response['data']['title'].find(field) != -1):
            #add id and title pairs to the list
            all_results.append({'paperId': result['data']['paperId'], 'title': result['data']['title']})
        # all_results.extend(response['data'])
        if 'token' not in response:
            break
        query_params['token'] = response['token']
        #latency of 0.5 seconds
        #time.sleep(0.5)
    return all_results

def fetch_papers_on_field(query_params, amount = 10000 ,field = 'Machine Learning'):
    all_results_on_field = fetch_all_results(query_params, 2000, field)

all_result = fetch_all_results(query_params,2000)
print(len(all_result))

ml_paper_count = 0
for result in all_result:
    if(result['title'].find('Machine Learning') != -1):
        ml_paper_count += 1

print("ML related papers count: ", ml_paper_count)

#print paper ids and titles
print("Paper Id  |  Title")
for result in all_result:
    print(result['paperId'], " | ", result['title'])
    print("\n")

