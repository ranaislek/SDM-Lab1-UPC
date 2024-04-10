from neo4j import GraphDatabase

class GraphAlgorithms:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_query(self, query):
        with self.driver.session() as session:
            result = session.run(query).data()
        return result

    def project_graph(self, graph_name):
        query = f"""
        CALL gds.graph.project(
            '{graph_name}',
            ['Paper', 'Author'],  
            {{
                CITED_BY: {{type: 'CITED_BY', orientation: 'REVERSE'}},  
                WRITTEN_BY: {{type: 'WRITTEN_BY', orientation: 'UNDIRECTED'}}  
            }}
        )
        YIELD graphName, nodeCount, relationshipCount
        """
        result = self.execute_query(query)
        if result:
            print(f"Graph '{graph_name}' projected successfully with {result[0]['nodeCount']} nodes and {result[0]['relationshipCount']} relationships.")
        else:
            print("Graph projection failed.")




    def run_pagerank(self, graph_name):
        query = f"""
        CALL gds.pageRank.stream('{graph_name}')
        YIELD nodeId, score
        RETURN id(gds.util.asNode(nodeId)) AS paperId, gds.util.asNode(nodeId).title AS paper, score
        ORDER BY score DESC
        LIMIT 10;
        """
        result = self.execute_query(query)
        print("PageRank Results:")
        for record in result:
            print(f"Paper ID: {record['paperId']}, Title: {record['paper']}, Score: {record['score']}")


    def run_louvain(self, graph_name):
        query = f"""
        CALL gds.louvain.stream('{graph_name}')
        YIELD nodeId, communityId
        RETURN communityId, collect(gds.util.asNode(nodeId).name) AS authors
        ORDER BY size(authors) DESC
        LIMIT 5;
        """
        result = self.execute_query(query)
        print("Louvain Method Results:")
        for record in result:
            print(f"Community ID: {record['communityId']}, Authors: {', '.join(record['authors'])}")


    
    def drop_graph(self, graph_name):
        query = f"CALL gds.graph.drop('{graph_name}')"
        self.execute_query(query)
        print(f"Graph '{graph_name}' dropped.")



if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "adminadmin"  # Update with your password

    graph_algorithms = GraphAlgorithms(uri, user, password)
    graph_name = "MyAcademicGraph"  # Name your graph projection
    graph_algorithms.drop_graph(graph_name)
    graph_algorithms.project_graph(graph_name)
    graph_algorithms.run_pagerank(graph_name)  # Pass graph_name as argument
    graph_algorithms.run_louvain(graph_name)  # Pass graph_name as argument
    graph_algorithms.close()

