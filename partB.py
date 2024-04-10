from neo4j import GraphDatabase
import pandas as pd
import os



URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")

############ CYPHER TO VISUALIZE THE ALL GRAPH IN NEO4J BROWSER ############

# MATCH (n)
# OPTIONAL MATCH (n)-[r]->(m)
# RETURN n, r, m

#############################################################################
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
       



path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    while True:

        print ("[3] - Run query 3 - Find Impact Factor of Journals")
        print ("[4] - Run query 4 - Find the most influential authors")
        print ("[5] - Exit")
        query_num = input("Please enter the query number you want to run: ")
        
        if query_num == "5":
            break

        with driver.session() as session:
            with session.begin_transaction() as tx:
            #run the query3

                if query_num == "3":
                    year = input ("Please enter the year you want to find the impact factor of the journals: ")
                    run_query3(tx, year)
                
          






    # # Close Neo4j driver
    driver.close()