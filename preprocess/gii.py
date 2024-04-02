import pandas as pd


#read GII-ratings-2021 xlsx

def complete_missing_ratings(collected_classes):
    if collected_classes == 'A':
        return 'A'
    elif collected_classes == 'A+':
        return 'A+'
    elif collected_classes == 'A++':
        return 'A++'
    elif collected_classes == 'A-':
        return 'A-'
    elif collected_classes == 'B':
        return 'B'
    elif collected_classes == 'B-':
        return 'B-'
    else:
        return 'C'

  


path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data" # change the absolute path of data to your own path
df = pd.read_excel(path + '/GII-ratings-2021-raw.xlsx', header=1, index_col=0)

columns = ["Title", "GGS Rating", "Collected Classes"]

#retrieve the columns that we are interested in
df = df[columns]

#Convert work in progress GGS Ratings by feeding collected classes column to the complete missing ratings function
for index, row in df.iterrows():
    if row['GGS Rating'] == 'Work in Progress' or ("Not Rated" in row['GGS Rating']):
        df.loc[index, 'GGS Rating'] = complete_missing_ratings(row['Collected Classes'])

def num_rank(rank):
    if rank == 'A':
        return 5
    elif rank == 'A+':
        return 6
    elif rank == 'A++':
        return 7
    elif rank == 'A-':
        return 4
    elif rank == 'B':
        return 3
    elif rank == 'B-':
        return 2
    elif rank == 'C':
        return 1

# add a new column num_rank

for index, row in df.iterrows():
    df.loc[index, 'num_rank'] = num_rank(row['GGS Rating'])

#convert num_rank to integer
df['num_rank'] = df['num_rank'].astype(int)

#print(df[df.isna().any(axis=1)])

print(df.head(5))   

#save the dataframe to a csv file
df.to_csv('GII-ratings-2021.csv', index=False)
