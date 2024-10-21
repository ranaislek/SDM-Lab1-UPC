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
    SET a.name = author.name, a.email = author.email
    RETURN count(a) AS createdAuthors
    """
    result = tx.run(query, authors=authors)
    created_authors = result.single()["createdAuthors"]
    print(f"{created_authors} author nodes created successfully")

def create_conferences(tx, conferences):
    query = """
    UNWIND $conferences AS conference
    MERGE (c: Conference {ss_venue_id: conference.ss_venue_id})
    SET c.name = conference.name, c.url = conference.url, c.city = conference.city, c.year = toInteger(conference.year), c.edition = toInteger(conference.edition)
    RETURN count(c) AS createdConferences
    """
    result = tx.run(query, conferences=conferences)
    created_conferences = result.single()["createdConferences"]
    print(f"{created_conferences} conference nodes created successfully")

def create_papers(tx, papers):
    query = """
    UNWIND $papers AS paper
    MERGE (p: Paper {paper_id: paper.paperId})
    SET p.title = paper.title, p.abstract = paper.abstract, p.MA_email = paper.MA_email, p.year = paper.MA_name,  p.year = toInteger(paper.year), p.embedding = paper.embedding,
    p.keywords = paper.keywords, p.doi = paper.doi
    RETURN count(p) AS createdPapers
    """
    result = tx.run(query, papers=papers)
    created_papers = result.single()["createdPapers"]
    print(f"{created_papers} paper nodes created successfully")

def create_journals(tx, journals):
    query = """
    UNWIND $journals AS journal
    MERGE (j: Journal {ss_venue_id: journal.ss_venue_id})
    SET j.name = journal.name, j.url = journal.url, j.issn = journal.issn, j.year = toInteger(journal.year), j.volume = toInteger(journal.volume)
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
    WITH p, v, toInteger(relationship.year) AS year


    // Create "published_in" relationship between papers and conferences/journals
    MERGE (p)-[pi:PUBLISHED_IN {year: year} ]->(v)
    RETURN count(p) AS createdRelationships

    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} PUBLISHED_IN relationships created successfully")


def create_affiliated_with(tx, relationships):
    query = """
    UNWIND $relationships AS relationship
    MATCH (a:Author {author_id: relationship.authorId}), (af:Affiliation {affiliation_name: relationship.affiliation})
    MERGE (a)-[:AFFILIATED_WITH]->(af)
    RETURN count(a) AS createdRelationships
    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} AFFILIATED_WITH relationships created successfully")


def create_affiliation(tx, affiliations):
    query = """
    UNWIND $affiliations AS affiliation
    MERGE (af:Affiliation {affiliation_name: affiliation.name})
    SET af.type = affiliation.type, af.address = affiliation.address, af.email = affiliation.email, af.phone_number = affiliation.phone_number, af.website = affiliation.website
    RETURN count(af) AS createdAffiliations
    """
    result = tx.run(query, affiliations=affiliations)
    created_affiliations = result.single()["createdAffiliations"]
    print(f"{created_affiliations} affiliation nodes created successfully")

def create_reviewed_by(tx, relationships):
    query = """
    UNWIND $relationships AS relationship
    MATCH (r:Review {review_id: relationship.review_id}), (a:Author {author_id: relationship.author_id})
    MERGE (a)-[:REVIEWED_BY]->(r)
    RETURN count(a) AS createdRelationships
    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} REVIEWED_BY relationships created successfully")

def create_reviews(tx, reviews):
    query = """
    UNWIND $reviews AS review
    MERGE (r:Review {review_id: review.review_id})
    SET r.decision = review.decision, r.date = datetime(review.date), r.abstract = review.abstract
    RETURN count(r) AS createdReviews
    """
    result = tx.run(query, reviews=reviews)
    created_reviews = result.single()["createdReviews"]
    print(f"{created_reviews} review nodes created successfully")

def create_review_on(tx, relationships):
    query = """
    UNWIND $relationships AS relationship
    MATCH (r:Review {review_id: relationship.review_id}), (p:Paper {paper_id: relationship.paper_id})
    MERGE (r)-[:REVIEW_ON]->(p)
    RETURN count(r) AS createdRelationships
    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} REVIEW_ON relationships created successfully")

def create_cited_by(tx, relationships):
    #add year information to the relationship

    query = """
    UNWIND $relationships AS relationship
    MATCH (p1:Paper {paper_id: relationship.paperId}), (p2:Paper {paper_id: relationship.referenceId})
    MERGE (p1)-[r:CITED_BY {year: toInteger(relationship.year)}]->(p2)
    RETURN count(p1) AS createdRelationships
    """
    result = tx.run(query, relationships=relationships)
    created_relationships = result.single()["createdRelationships"]
    print(f"{created_relationships} CITED_BY relationships created successfully")
    
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

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    while True:
        print("[1]- Delete Everything [2]- Create A3(Evolved) Model [3]- Exit")
        operation = input("Enter the number of operation: ")





        csv_to_load = ""    
        entity = ""



        csv_file_path = os.path.join(path, csv_to_load)

        

        if operation == "1":
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    try:
                        delete_all_entities(tx)
                        tx.commit()
                        print("*******All nodes are deleted successfully********")
                    except Exception as e:
                        # If there's any error, roll back the transaction
                        print("Error occurred:", e)
                        tx.rollback()
        elif operation == "2":
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    try:
                        #create all nodes
                        df= pd.read_csv(os.path.join(path, "papers_details_enriched.csv"))
                        create_papers(tx, df.to_dict('records'))
                        
                        df= pd.read_csv(os.path.join(path, "authors.csv"))
                        create_authors(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "conferences_enriched.csv"))
                        create_conferences(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "journals_enriched.csv"))
                        create_journals(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "written_by_enriched.csv"))
                        create_written_by(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "published_in_enriched_v2.csv"))
                        create_published_in(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "affiliations.csv"))
                        create_affiliation(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "affiliated_with.csv"))
                        create_affiliated_with(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "reviews.csv"))
                        create_reviews(tx, df.to_dict('records'))

                        df= pd.read_csv(os.path.join(path, "reviewed_by.csv"))
                        create_reviewed_by(tx, df.to_dict('records'))

                        df = pd.read_csv(os.path.join(path, "review_on.csv"))
                        create_review_on(tx, df.to_dict('records'))

                        
                        df= pd.read_csv(os.path.join(path, "citations.csv"))
                        create_cited_by(tx, df.to_dict('records'))


                        tx.commit()
                        print("*******A3(Evolved) Graph database created successfully******")
                    except Exception as e:
                        # If there's any error, roll back the transaction
                        print("Error occurred:", e)
                        tx.rollback()
        elif operation == "3":
            break

    # # Close Neo4j driver
    driver.close()
