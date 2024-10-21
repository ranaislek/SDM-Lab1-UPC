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

def create_authors(tx, authors):
    query = """
    UNWIND $authors AS author
    MERGE (a:Author {author_id: author.authorId})
    SET a.name = author.name, a.affiliations = author.affiliations, a.email = author.email
    RETURN count(a) AS createdAuthors
    """
    result = tx.run(query, authors=authors)
    created_authors = result.single()["createdAuthors"]
    print(f"{created_authors} author nodes created successfully")

def create_conferences(tx, conferences):
    query = """
    UNWIND $conferences AS conference
    MERGE (c: Conference {ss_venue_id: conference.ss_venue_id})
    SET c.name = conference.name, c.url = conference.url
    RETURN count(c) AS createdConferences
    """
    result = tx.run(query, conferences=conferences)
    created_conferences = result.single()["createdConferences"]
    print(f"{created_conferences} conference nodes created successfully")

def create_papers(tx, papers):
    query = """
    UNWIND $papers AS paper
    MERGE (p: Paper {paper_id: paper.paperId})
    SET p.title = paper.title, p.abstract = paper.abstract, p.MA_email = paper.MA_email, p.year = paper.MA_name,  p.year = toInteger(paper.year), p.embedding = paper.embedding
    RETURN count(p) AS createdPapers
    """
    result = tx.run(query, papers=papers)
    created_papers = result.single()["createdPapers"]
    print(f"{created_papers} paper nodes created successfully")

def create_journals(tx, journals):
    query = """
    UNWIND $journals AS journal
    MERGE (j: Journal {ss_venue_id: journal.ss_venue_id})
    SET j.name = journal.name, j.url = journal.url, j.issn = journal.issn
    RETURN count(j) AS createdJournals
    """
    result = tx.run(query, journals=journals)
    created_journals = result.single()["createdJournals"]
    print(f"{created_journals} journal nodes created successfully")

def create_written_by(tx, relationships):
    query = """
    UNWIND $relationships AS relationship
    MATCH (p:Paper {paper_id: relationship.paperId}), (a:Author {author_id: relationship.authorId})


    // Create "authored_by" relationship between papers and authors
    MERGE (a)-[:WRITTEN_BY]->(p)
    RETURN count(a) AS createdRelationships
    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} WRITTEN_BY relationships created successfully")

def create_published_in(tx, relationships):
    query = """
    UNWIND $relationships AS relationship
 
    MATCH (p:Paper {paper_id: relationship.paper_id}), 
            (v {ss_venue_id: relationship.ss_venue_id})
    WHERE (v:Conference) OR (v:Journal)


    // Create "published_in" relationship between papers and conferences/journals
    MERGE (p)-[:PUBLISHED_IN]->(v)
    RETURN count(p) AS createdRelationships

    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} PUBLISHED_IN relationships created successfully")

def delete_node(node,tx):
    query = f"""
    MATCH (n:{node})
    DELETE n
    """
    print(query)
    tx.run(query)

def delete_all_entities(tx):
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    tx.run(query)


path = "/home/furkanbk/SDM/P1/SDM-P1-GRAPH/data"

print("[1]- Insert [2]- Delete [3]- Delete Everything [4]- Create A2(Basic) Model")
operation = input("Enter the number of operation: ")





csv_to_load = ""    
entity = ""

if operation != "3" and operation != "4":

    print("Available Nodes: [1]- Author, [2]- Paper, [3]- Conference, [4]- Journal")
    print("Available Relationships: [5]- Written_by [6]- Published_in")
    #ask user what csv file to load
    num = input("Enter the number of entity: ")
    if num == "1":
        csv_to_load = "authors.csv"
        entity = "Author"
    elif num == "2":
        csv_to_load = "papers_details.csv"
        entity = "Paper"
    elif num == "3":
        csv_to_load = "conferences.csv"
        entity = "Conference"
    elif num == "4":
        csv_to_load = "journals.csv"
        entity = "Journal"
    elif num == "5":
        csv_to_load = "written_by.csv"
        entity = "WRITTEN_BY"
    elif num == "6":
        csv_to_load = "published_in.csv"
        entity = "PUBLISHED_IN"


csv_file_path = os.path.join(path, csv_to_load)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    if operation == "2":
        with driver.session() as session:
            with session.begin_transaction() as tx:
                try:

                    delete_node(entity, tx)
                    tx.commit()
                    print("Nodes with label", entity, "deleted successfully")
                except Exception as e:
                    # If there's any error, roll back the transaction
                    print("Error occurred:", e)
                    tx.rollback()
    elif operation == "3":
        with driver.session() as session:
            with session.begin_transaction() as tx:
                try:
                    delete_all_entities(tx)
                    tx.commit()
                    print("All nodes deleted successfully")
                except Exception as e:
                    # If there's any error, roll back the transaction
                    print("Error occurred:", e)
                    tx.rollback()
    elif operation == "4":
        with driver.session() as session:
            with session.begin_transaction() as tx:
                try:
                    #create all nodes
                    df= pd.read_csv(os.path.join(path, "authors.csv"))
                    create_authors(tx, df.to_dict('records'))
                    df= pd.read_csv(os.path.join(path, "papers_details.csv"))
                    create_papers(tx, df.to_dict('records'))
                    df= pd.read_csv(os.path.join(path, "conferences.csv"))
                    create_conferences(tx, df.to_dict('records'))
                    df= pd.read_csv(os.path.join(path, "journals.csv"))
                    create_journals(tx, df.to_dict('records'))
                    df= pd.read_csv(os.path.join(path, "written_by.csv"))
                    create_written_by(tx, df.to_dict('records'))
                    df= pd.read_csv(os.path.join(path, "published_in.csv"))
                    create_published_in(tx, df.to_dict('records'))
                    tx.commit()
                    print("A2(Basic) Graph database created successfully")
                except Exception as e:
                    # If there's any error, roll back the transaction
                    print("Error occurred:", e)
                    tx.rollback()
        
    else:
        df= pd.read_csv(csv_file_path)
        print(df.head())
        #check if database is empty
        with driver.session() as session:
            with session.begin_transaction() as tx:
                try:
                    if num == "1":
                        create_authors(tx, df.to_dict('records'))
                        tx.commit()
                        print("Author nodes created successfully")
                    if num == "2":
                        create_papers(tx, df.to_dict('records'))
                        tx.commit()
                        print("Paper nodes created successfully")
                    if num == "3":
                        create_conferences(tx, df.to_dict('records'))
                        tx.commit()
                        print("Conference nodes created successfully")
                    if num == "4":
                        create_journals(tx, df.to_dict('records'))
                        tx.commit()
                        print("Journal nodes created successfully")
                    if num == "5":
                        create_written_by(tx, df.to_dict('records'))
                        tx.commit()
                        print("WRITTEN_BY relationships created successfully")
                    if num == "6":
                        create_published_in(tx, df.to_dict('records'))
                        tx.commit()
                        print("PUBLISHED_IN relationships created successfully")

                        
                except Exception as e:
                    # If there's any error, roll back the transaction
                    print("Error occurred:", e)
                    tx.rollback()


# # Close Neo4j driver
driver.close()
