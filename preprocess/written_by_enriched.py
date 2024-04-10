#read written_by.csv
import pandas as pd

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"
df = pd.read_csv(path + '/written_by.csv')

dfs = []    
for i in range(1, 9):
    df_copy = df.copy()
    df_copy["paperId"] = df_copy["paperId"].astype(str) + "-" + str(i)
    dfs.append(df_copy)

for df_copy in dfs:
    df = pd.concat([df, df_copy])

df_selected = df[df['paperId'].str.contains("00040bdd447f041a50ae95fd51926cf435ef1eba")]
print(df_selected[["paperId", "authorId"]])

df.to_csv(path + '/written_by_enriched.csv', index=False)