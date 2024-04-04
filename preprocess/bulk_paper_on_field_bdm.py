import requests
import time
import json

#url = "https://api.semanticscholar.org/graph/v1/paper/649def34f8be52c8b66281af98ae884c09aef38b"
url = "https://api.semanticscholar.org/graph/v1/paper/search"
url_bulk = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
api_key = "1R3UkH1BdY6QtZr1wUUtw65hU2bWHe8T69Pq1VFT"
# Define headers with API key
headers = {'X-API-KEY': api_key}

top_subjects_dict = {
    "Computer Science": ["Machine Learning", "Artificial Intelligence"],
    "Chemistry": ["Organic", "Physical"],
    "Biology": ["Genetics", "Ecology"],
    "Business": ["Management", "Marketing"],
    "Law": ["Criminal", "International"]
}

query_params = {
    'fields': 'title,paperId' ,

    'minCitationCount': '10',

    'fieldsOfStudy': 'Computer Science',

    'isOpenAccess':'true',
}

study_fields = top_subjects_dict.keys()

def search_papers(query_params):
    url_bulk = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
    search_response = requests.get(url_bulk, headers=headers, params=query_params)
    return search_response.json()


def fetch_all_results_on_topic(query_params,amount = 1000):
    all_results = []
   

    #create query parameters for each subject in each fields
    for field in study_fields:
        query_params['fieldsOfStudy'] = field
        for top_subject in top_subjects_dict[field]:
            
            print(f"Fetching papers for {field} - {top_subject}...")

            papers_in_field = 0
            while True:
                

                if (papers_in_field >= amount):
                    filename = f"matched_papers_{field}_{top_subject}.json"
                    # Write the data to the JSON file
                    #path is in bdm_data folder
                    with open(f"bdm_data/{filename}", 'w') as json_file:
                        json.dump(all_results, json_file, indent=2)
                    all_results = []
                    break
                response = search_papers(query_params)
                if 'data' not in response:
                    break
                for result in response['data']:
                
                    if(result['title'].find(top_subject) != -1):            
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
            print(f"Matched paper count for {field} - {top_subject}: {papers_in_field}")
            #remove token
            query_params.pop('token', None)
    return all_results


all_result = fetch_all_results_on_topic(query_params, 100)
# matched_paper_count = len(all_result)
# print("Matched paper count: ", matched_paper_count)

# print("Paper Id  |  Title")
# for result in all_result:
#     print(result['paperId'], " | ", result['title'])




