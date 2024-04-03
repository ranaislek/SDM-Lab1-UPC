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

    'isOpenAccess':'true',
}

def search_papers(query_params):
    url_bulk = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
    search_response = requests.get(url_bulk, headers=headers, params=query_params)
    return search_response.json()


def fetch_all_results_on_topic(query_params,amount = 1000,field = 'Machine Learning'):
    all_results = []
    papers_in_field = 0
    while True:
        
        if (papers_in_field >= amount):
            break
        response = search_papers(query_params)
        for result in response['data']:
        
            if(result['title'].find(field) != -1):            
                papers_in_field += 1
                all_results.append({'paperId': result['paperId'], 'title': result['title']})
       # all_results.extend(response['data'])
        if 'token' not in response:
            break
        query_params['token'] = response['token']
        #latency of 0.5 seconds
        #time.sleep(0.5)
    return all_results

field = 'Machine Learning'
all_result = fetch_all_results_on_topic(query_params, 10, field)
matched_paper_count = len(all_result)
print("Matched paper count: ", matched_paper_count)

print("Paper Id  |  Title")
for result in all_result:
    print(result['paperId'], " | ", result['title'])

#save the results to a json file
import json


filename = f"matched_papers_on_field_{field}_bdm.json"
# Write the data to the JSON file
with open(filename, 'w') as json_file:
    json.dump(all_result, json_file, indent=2)