# graph_centrality.py
from py2neo import Graph

# Config (same as your import script)
NEO4J_URI = "bolt://localhost:7688"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "berlin2025"

# Connect to Neo4j
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_pagerank():
    # 1. Project graph
    graph.run("""
    CALL gds.graph.project(
      'companyGraph',
      ['Company','Shop','City'],
      {
        HAS_BRANCH: {orientation: 'UNDIRECTED'},
        LOCATED_IN: {orientation: 'UNDIRECTED'}
      }
    )
    """)

    # 2. Run PageRank and write back
    graph.run("""
    CALL gds.pageRank.write('companyGraph', { writeProperty: 'pagerank' })
    YIELD nodePropertiesWritten, ranIterations
    """)

    # 3. Drop projection
    graph.run("CALL gds.graph.drop('companyGraph')")

    print("PageRank scores written to Company nodes (property: pagerank).")

def run_degree_centrality():
    # 1. Project graph
    graph.run("""
    CALL gds.graph.project(
      'shopGraph',
      ['Shop','Company','City'],
      {
        HAS_BRANCH: {orientation: 'UNDIRECTED'},
        LOCATED_IN: {orientation: 'UNDIRECTED'}
      }
    )
    """)

    # 2. Run Degree Centrality and write back
    graph.run("""
    CALL gds.degree.write('shopGraph', { writeProperty: 'degree' })
    YIELD nodePropertiesWritten
    """)

    # 3. Drop projection
    graph.run("CALL gds.graph.drop('shopGraph')")

    print("Degree centrality scores written to Shop nodes (property: degree).")

def show_top_companies():
    query = """
    MATCH (c:Company)
    RETURN c.name AS company, c.pagerank AS pagerank
    ORDER BY pagerank DESC
    LIMIT 10;
    """
    results = graph.run(query).data()
    print("Top Companies by PageRank:")
    for r in results:
        print(f"{r['company']}: {r['pagerank']:.4f}")

def show_top_shops():
    query = """
    MATCH (s:Shop)
    RETURN s.name AS shop, s.degree AS degree
    ORDER BY degree DESC
    LIMIT 10;
    """
    results = graph.run(query).data()
    print("Top Shops by Degree Centrality:")
    for r in results:
        print(f"{r['shop']}: {r['degree']}")

if __name__ == "__main__":
    run_pagerank()
    run_degree_centrality()
    show_top_companies()
    show_top_shops()

#MATCH (c:Company) RETURN c.name, c.pagerank ORDER BY c.pagerank DESC LIMIT 10;

# degree centrality
#MATCH (s:Shop) RETURN s.name, s.degree ORDER BY s.degree DESC LIMIT 10;
