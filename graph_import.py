import pandas as pd
import math
from py2neo import Graph, Node, Relationship

# Config
NEO4J_URI = "bolt://localhost:7688"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "berlin2025"
CSV_FILES = ["berlin_cafes.csv", "munich_cafes.csv"]

# Connect to Neo4j
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# clear old data
graph.run("MATCH (n) DETACH DELETE n")

# Safe value replacement
def safe_value(val, fallback="Unknown"):
    """
    Convert NaN/None to a safe string value.
    """
    if val is None:
        return fallback
    if isinstance(val, float) and math.isnan(val):
        return fallback
    return str(val).strip()

# Import Function
def import_cafes(csv_file):
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        # City node (use addr_city if available, else fallback)
        city_name = safe_value(row.get("addr_city")) or safe_value(row.get("city"))
        city = Node("City", name=city_name)

        # Company node (use café name as company)
        company_name = safe_value(row.get("name"))
        company = Node("Company", name=company_name)

        # Shop node
        shop = Node(
            "Shop",
            osm_id=safe_value(row.get("osm_id")),
            name=company_name,
            lat=safe_value(row.get("lat")),
            lon=safe_value(row.get("lon")),
            phone=safe_value(row.get("phone"), ""),
            website=safe_value(row.get("website"), ""),
            addr_street=safe_value(row.get("addr_street"), ""),
            addr_housenumber=safe_value(row.get("addr_housenumber"), ""),
            addr_postcode=safe_value(row.get("addr_postcode"), ""),
            addr_city=city_name,
        )

        # Merge nodes (avoid duplicates)
        graph.merge(city, "City", "name")
        graph.merge(company, "Company", "name")
        graph.merge(shop, "Shop", "osm_id")

        # Create relationships
        graph.merge(Relationship(company, "HAS_BRANCH", shop))
        graph.merge(Relationship(shop, "LOCATED_IN", city))

# Run Import
for file in CSV_FILES:
    import_cafes(file)

print("Cafés imported into Neo4j successfully!")
