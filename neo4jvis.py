import os
import xml.etree.ElementTree as ET
from neo4j import GraphDatabase

# Neo4j connection details
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "Tech@Stuttgart"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

synaf_dir = "synaf_xml"

def create_word_node(tx, word_id, word, lemma, pos, title, year):
    tx.run(
        """
        MERGE (w:Word {id: $word_id})
        SET w.word = $word,
            w.lemma = $lemma,
            w.pos = $pos,
            w.text_title = $title,
            w.year = $year
        """,
        word_id=word_id, word=word, lemma=lemma, pos=pos, title=title, year=year
    )

def create_dep_relation(tx, from_id, to_id, dep):
    tx.run(
        """
        MATCH (from:Word {id: $from_id}), (to:Word {id: $to_id})
        MERGE (from)-[r:DEPENDS_ON {dep: $dep}]->(to)
        """,
        from_id=from_id, to_id=to_id, dep=dep
    )

def process_file(session, filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Extract metadata
    meta = root.find("Meta")
    title = meta.find("Title").text if meta is not None and meta.find("Title") is not None else "Unknown"
    year = meta.find("Year").text if meta is not None and meta.find("Year") is not None else "Unknown"

    # Create nodes
    nodes = {}
    for node in root.findall(".//Nodes/Node"):
        node_id = node.attrib["id"]
        word = node.attrib.get("word", "")
        lemma = node.attrib.get("lemma", "")
        pos = node.attrib.get("pos", "")
        nodes[node_id] = (word, lemma, pos)

        session.write_transaction(create_word_node, node_id, word, lemma, pos, title, year)

    # Create relationships
    for edge in root.findall(".//Edges/Edge"):
        from_id = edge.attrib["fromID"]
        to_id = edge.attrib["toID"]
        dep = edge.attrib.get("dep", "")
        session.write_transaction(create_dep_relation, from_id, to_id, dep)

def main():
    with driver.session() as session:
        for filename in os.listdir(synaf_dir):
            if filename.endswith(".xml"):
                filepath = os.path.join(synaf_dir, filename)
                print(f"Processing {filename}")
                process_file(session, filepath)

if __name__ == "__main__":
    main()
