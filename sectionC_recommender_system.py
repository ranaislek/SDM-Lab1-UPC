from neo4j import GraphDatabase

class RecommenderSystem:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.write_transaction(lambda tx: tx.run(query).data())
            return result

    def define_research_communities(self):
        query = """
        MATCH (p:Paper)
        WHERE p.keywords IS NOT NULL AND ANY(keyword IN split(toString(p.keywords), ",") WHERE toLower(keyword) IN ['data', 'management', 'indexing', 'modeling', 'big data', 'processing', 'storage', 'querying'])
        SET p:DatabaseCommunity
        RETURN p
        LIMIT 25
        """
        return self.run_query(query)

    def find_related_conferences_journals(self):
        query = """
        MATCH (p:DatabaseCommunity)-[:PUBLISHED_IN]->(v)
        WITH v, COUNT(p) AS PapersCount
        SET v:RelatedToDatabaseCommunity
        RETURN v, PapersCount
        LIMIT 25
        """
        return self.run_query(query)

    def identify_top_papers(self):
        query = """
        MATCH (p:DatabaseCommunity)-[:CITED_BY]->(cited:Paper)
        WITH p, COUNT(cited) AS citations
        ORDER BY citations DESC
        LIMIT 100
        SET p:TopPaper
        """
        return self.run_query(query)

    def mark_potential_reviewers(self):
        query = """
        MATCH (a:Author)-[:WRITTEN_BY]->(p:TopPaper)
        WITH a
        SET a:PotentialReviewer
        RETURN a.name AS AuthorName
        LIMIT 25
        """
        return self.run_query(query)

    def mark_gurus(self):
        query = """
        MATCH (a:Author)-[:WRITTEN_BY]->(p:TopPaper)
        WITH a, COUNT(p) AS TopPapers
        WHERE TopPapers >= 2
        SET a:Guru
        RETURN a.name AS GuruName, TopPapers
        LIMIT 25
        """
        return self.run_query(query)

if __name__ == "__main__":
    # Update these variables with your Neo4j connection details
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "adminadmin"

    recommender = RecommenderSystem(uri, user, password)
    print("Defining research communities...")
    print(recommender.define_research_communities())
    print("Finding related conferences and journals...")
    print(recommender.find_related_conferences_journals())
    print("Identifying top papers...")
    print(recommender.identify_top_papers())
    print("Marking potential reviewers...")
    print(recommender.mark_potential_reviewers())
    print("Marking gurus...")
    print(recommender.mark_gurus())
    recommender.close()
