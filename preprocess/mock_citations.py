import json
import requests
import time
import random
#read json file
path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
raw_paper_data = None
start_time = time.time()
with open(path + '/matched_papers_on_topics.json', 'r') as json_file:
    raw_paper_data = json.load(json_file)


#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]

#create 10 mock citations for each paper in the paper_ids list to another paper in the paper_ids list
reference_details = []
for paper in paper_ids:
    for i in range(10):
        referenceId = random.choice(paper_ids)
        if paper != referenceId:
           
            reference_details.append({'paperId': paper, 'referenceId': referenceId})
        #paper cannot be a reference to itself


import csv
import pandas as pd
df = pd.DataFrame(reference_details)
print(df.head(15))

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
df.to_csv(path + '/citations.csv', index=False)

print("Completed in: ", time.time()-start_time, " seconds")

