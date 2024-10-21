from neo4j import GraphDatabase
import pandas as pd
import os
import ast



URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")

############ CYPHER TO VISUALIZE THE ALL GRAPH IN NEO4J BROWSER ############

# MATCH (n)
# OPTIONAL MATCH (n)-[r]->(m)
# RETURN n, r, m

#############################################################################

def run_query1(tx):
    query1 = """
    MATCH (c:Conference)<-[:PUBLISHED_IN]-(p:Paper)
    OPTIONAL MATCH (p)<-[:CITED_BY]-(citation)
    WITH c, p, COUNT(citation) AS citations
    ORDER BY c.name, citations DESC
    WITH c, COLLECT(DISTINCT {paper: p, citations: citations}) AS papers
    RETURN c.name AS Conference, 
        [paper in papers | paper.paper.title][..3] AS TopPapers, 
        [paper in papers | paper.citations][..3] AS Citations



    """
    result = tx.run(query1)

    #print results by skipping every 2 next result
    result_num = 0

    for record in result:
        #skip 2 next lines
        result_num += 1 #very innocent skip for duplicate returns :)
        if result_num % 3 != 1:
            continue

        print("Conference: ", record["Conference"], "Top Papers: ", record["TopPapers"], "Citations: ", record["Citations"])
        
def run_query2(tx):
    query2 = """
    MATCH (c:Conference)-[:PUBLISHED_IN]-(p:Paper)-[:WRITTEN_BY]-(a:Author)
    WITH a.name AS author_name, c.name AS conference_name, collect(c.edition) AS editions
    WHERE size(editions) >= 4
    WITH collect(author_name) as community,conference_name
    RETURN conference_name,community 


    """
    result = tx.run(query2)

    for record in result:
        print("Conference Name: ", record["conference_name"], "Community: ", record["community"])
def run_query3(tx, year):
    query3 = f"""

    MATCH (journal:Journal )<-[published:PUBLISHED_IN]-(paper:Paper)
    WHERE published.year >= {year} - 2
    AND published.year <= {year} - 1
    WITH journal, paper
    MATCH (paper)<-[citation:CITED_BY]-(citing_paper:Paper)
    WHERE citation.year = {year}
    WITH journal, COUNT(DISTINCT citing_paper) AS citations_received
    MATCH (journal)<-[published_in: PUBLISHED_IN]-(paper)
    WHERE published_in.year >= {year} - 2
    AND published_in.year <= {year} - 1
    WITH journal, COUNT(DISTINCT paper) AS citable_items, citations_received
    RETURN journal.name AS journal_name, 
        citations_received AS citations_received_current_year, 
        citable_items AS citable_items_current_year,
        citations_received / citable_items AS impact_factor
    """
    query3_2 = f"""
    MATCH (journal:Journal )<-[published:PUBLISHED_IN]-(paper:Paper)
    WHERE published.year >= {year} - 2
    AND published.year <= {year} - 1
    WITH journal, paper
    MATCH (paper)<-[citation:CITED_BY]-(citing_paper:Paper)
    WHERE citation.year = {year}
    WITH journal, COUNT(DISTINCT citing_paper) AS citations_received
    MATCH (journal)<-[published_in: PUBLISHED_IN]-(paper)
    WHERE published_in.year >= {year} - 2
    AND published_in.year <= {year} - 1
    WITH journal, COUNT(DISTINCT paper) AS citable_items, citations_received
    RETURN journal.name AS journal_name, 
        SUM(citations_received) AS citations_received_current_year, 
        SUM(citable_items) AS citable_items_current_year,
        SUM(citations_received) / SUM(citable_items) AS impact_factor

    """

    result = tx.run(query3_2, year=year)
    for record in result:
        

        print("Journal Name: ", record["journal_name"], "Citations Received: ", record["citations_received_current_year"], "Citable Items: ", record["citable_items_current_year"], "Impact Factor: ", record["impact_factor"])
       


def run_query4(tx):
    query4 = """
    MATCH (a:Author)-[:WRITTEN_BY]-(p:Paper)-[:CITED_BY]-(c:Paper)
    WITH a, p, COUNT(c) AS citations
    ORDER BY citations DESC
    WITH a, COLLECT(citations) AS citationList
    WITH a, [i IN RANGE(1, SIZE(citationList)) | REDUCE(s = 0, x IN citationList[..i] | s + x)] AS cumulativeCitations
    WITH a, [i IN RANGE(1, SIZE(cumulativeCitations)) | CASE WHEN cumulativeCitations[i - 1] >= i THEN i ELSE 0 END] AS hIndexes
    WITH a, MAX(hIndexes) AS hIndex
    RETURN a.name, hIndex

    """

    result = tx.run(query4)
    for record in result:
        #convert the list string to list
        list_str = record["hIndex"]
       
        print("Author Name: ", record["a.name"], "H-Index: ", list_str[-1])
        

path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    while True:

        print ("[1] - Run query 1 - Find the top 3 papers with the most citations for each conference")
        print ("[2] - Run query 2 - Find the community of authors who have published in at least 4 editions of the same conference")
        print ("[3] - Run query 3 - Find Impact Factor of Journals")
        print ("[4] - Run query 4 - Find the most influential authors")
        print ("[5] - Exit")
        query_num = input("Please enter the query number you want to run: ")
        
        if query_num == "5":
            break

        with driver.session() as session:
            with session.begin_transaction() as tx:
            #run the query3

                if query_num == "1":
                    run_query1(tx)

                elif query_num == "2":
                    run_query2(tx)
                    
                elif query_num == "3":
                    year = input ("Please enter the year you want to find the impact factor of the journals: ")
                    run_query3(tx, year)

                elif query_num == "4":
                    run_query4(tx)


    # # Close Neo4j driver
    driver.close()
