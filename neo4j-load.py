from neo4j import GraphDatabase
import pandas as pd
import os

# Define Neo4j connection parameters
# uri = "bolt://localhost:7687"  # default bolt port
# username = "neo4j"
# password = "adminadmin"  # default password is "neo4j"

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "neo4j")


# Function to create authors
def create_conferences(tx, conferences):
    query = """
    UNWIND $conferences AS conference
    MERGE (c: Conference {ss_venue_id: conference.ss_venue_id})
    SET c.name = conference.name, c.url = conference.url
    """
    tx.run(query, conferences=conferences)

# Function to create papers
def create_papers(tx, papers):
    query = """
    UNWIND $papers AS paper
    MERGE (p:Paper {id: paper.paperId, title: paper.title})
    """
    tx.run(query, papers=papers)

# Function to create relationships between authors and papers
def create_relationships(tx, relationships):
    query = """
    UNWIND $relationships AS rel
    MATCH (a:Author {id: rel.author_id}), (p:Paper {id: rel.paper_id})
    MERGE (a)-[:WROTE]->(p)
    """
    tx.run(query, relationships=relationships)

def delete_node(tx):
    query = f"""
    MATCH (n:{'Paper'})
    DELETE n
    """
    tx.run(query)

driver = GraphDatabase.driver(URI, auth=(AUTH[0],AUTH[1]))
# Connect to Neo4j
#driver = GraphDatabase.driver(URI, auth=AUTH)



path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"
csv_to_load = "conferences.csv"
csv_file_path = os.path.join(path, csv_to_load)

df= pd.read_csv(csv_file_path)
print(df.head())


# Create authors, papers, and relationships
with driver.session() as session:
    session.write_transaction(create_conferences, df)
    #session.write_transaction(create_papers, df[['paperId', 'title']])
    # session.write_transaction(delete_node)
    # session.write_transaction(create_relationships, df[['author_id', 'paper_id']])
    pass
# Close Neo4j driver
driver.close()