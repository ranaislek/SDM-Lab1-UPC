import pandas as pd

#read the data

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"

df = pd.read_csv(path + '/papers_details.csv')

#for each paper, create 8 fake versions of it with same author but add -1, -2, -3, -4, -5, -6, -7, -8 to the paper id and title
dfs = []
for i in range(1, 9):
    df_copy = df.copy()
    df_copy["paperId"] = df_copy["paperId"].astype(str) + "-" + str(i)
    df_copy["title"] = df_copy["title"] + "-" + str(i)
    dfs.append(df_copy)

for df_copy in dfs:
    df = pd.concat([df, df_copy])
#FİND papers having id 00040bdd447f041a50ae95fd51926cf435ef1eba in their ids
# df_select = df[df['paperId'].str.contains("00040bdd447f041a50ae95fd51926cf435ef1eba")]
# print(df_select[["paperId", "title"]])
df.to_csv(path + '/papers_details_enriched.csv', index=False)
