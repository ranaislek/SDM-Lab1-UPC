#create mock reviews data

import json
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import pandas as pd

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path

raw_paper_data = None
with open(path + '/matched_papers_on_field_Machine Learning.json', 'r') as json_file:   
    raw_paper_data = json.load(json_file)

#extract paperId from raw_paper_data
paper_ids = [paper['paperId'] for paper in raw_paper_data]

authors = pd.read_csv(path + '/written_by.csv')

unique_authors = authors['authorId'].unique()


#extract authorId from raw_authors_data

faker = Faker()
# Random decisions
decisions = ["Accepted", "Rejected"]

# Generate random reviews

reviews = []
reviewed_by = []
for paper in paper_ids:

    # GENERATE RANDOM REVIEWS

    # Random decision
    decision = random.choice(decisions)
    
    # Random date within a range (e.g., last 6 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1800)

    # Generate random date


    random_date = faker.date_time_between(start_date, end_date)
    date = random_date.strftime("%Y-%m-%d")
    
    # Generate random abstract
    abstract = faker.paragraph(nb_sentences=random.randint(3, 6))
    
    review_id = str(uuid.uuid4())
    # Create and append review object
    
    reviews.append({
        "review_id": review_id,
        "decision": decision,
        "date": date,
        "abstract": abstract
    })
    #print(f"Review Id: {review_id}\nDecision: {decision}\nDate: {date}\nAbstract: {abstract}\n")

    #assign random authors to reviews between 2 to 5 reviewers
    num_reviewers = random.randint(3, 5)
    reviewers = random.sample(list(unique_authors), num_reviewers)

    # author cannot review his/her own paper
    for reviewer in reviewers:
        if reviewer in authors[authors['paperId'] == paper]['authorId'].values:
            reviewers.remove(reviewer)
    
    print(f"Paper Id: {paper}\nReviewers: {reviewers}\n")
    

    #create csv file for reviewed_by
    for reviewer in reviewers:
        reviewed_by.append({
            "review_id": review_id,
            "author_id": reviewer
        })
        
#create csv file for reviews
df = pd.DataFrame(reviews)
df.to_csv(path + '/reviews.csv', index=False)

#create csv file for reviewed_by
df = pd.DataFrame(reviewed_by)
df.to_csv(path + '/reviewed_by.csv', index=False)

print("Reviews and reviewed_by csv files created successfully")