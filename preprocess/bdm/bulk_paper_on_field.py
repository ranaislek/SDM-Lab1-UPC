import requests
import time
import json

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


def fetch_all_results_on_topic(query_params,amount = 1000):
   
   

    #create query parameters for each subject in each fields
 
    fields = ['Machine Learning', 'Game Development', 'Database Management']
    all_results = []
    for field in fields:

        papers_in_field = 0
        while True:
            

            if (papers_in_field >= amount):
                filename = f"matched_papers_{field}.json"
                # Write the data to the JSON file
                #path is in bdm_data folder
                path = "/home/furkanbk/SDM/P1/data"
                with open(f"{path}/{filename}", 'w') as json_file:
                    json.dump(all_results, json_file, indent=2)
                all_results = []
                break
            response = search_papers(query_params)
            if 'data' not in response:
                break
            for result in response['data']:
            
                if(result['title'].find(field) != -1):            
                    papers_in_field += 1
                    if(papers_in_field >= amount):
                        break
                    all_results.append({'paperId': result['paperId'], 'title': result['title']})
            # all_results.extend(response['data'])
            if 'token' not in response:
                break
            query_params['token'] = response['token']
            #latency of 0.5 seconds
            #time.sleep(0.5)
        print(f"Matched paper count for {field}: {papers_in_field}")
        #remove token
        query_params.pop('token', None)
    return all_results


all_result = fetch_all_results_on_topic(query_params, 100)

#export the results to a json file
path = "/home/furkanbk/SDM/P1/data"
filename = "matched_papers.json"
# Write the data to the JSON file
with open(f"{path}/{filename}", 'w') as json_file:
        json.dump(all_result, json_file, indent=2)





