import spacy
import json
import os
import uuid
import xml.etree.ElementTree as ET

# Load spaCy model with disabled NER for speed
nlp = spacy.load("en_core_web_sm", disable=["ner"])

os.makedirs("synaf_xml", exist_ok=True)

def create_synaf_xml(entry, doc):
    root = ET.Element("SynAF")
    meta = ET.SubElement(root, "Meta")
    for k in ["title", "speaker", "line"]:
        ET.SubElement(meta, k.capitalize()).text = str(entry.get(k, ""))
    ET.SubElement(meta, "Year").text = str(entry.get("year", ""))

    nodes = ET.SubElement(root, "Nodes")
    edges = ET.SubElement(root, "Edges")
    token_map = {}

    for token in doc:
        node_id = str(uuid.uuid4())
        token_map[token.i] = node_id
        ET.SubElement(nodes, "Node", id=node_id, word=token.text, lemma=token.lemma_, pos=token.pos_)

    for token in doc:
        if token.dep_ != "ROOT":
            ET.SubElement(edges, "Edge",
                          fromID=token_map[token.head.i],
                          toID=token_map[token.i],
                          dep=token.dep_)

    return ET.ElementTree(root)

with open("parsed_lines.json", "r", encoding="utf-8") as f:
    parsed_data = json.load(f)

# Extract all lines for batch processing
texts = [entry["line"] for entry in parsed_data]

# Use nlp.pipe to process lines in batch
docs = nlp.pipe(texts, batch_size=50)  # adjust batch_size for your RAM and CPU

for i, (entry, doc) in enumerate(zip(parsed_data, docs)):
    xml_tree = create_synaf_xml(entry, doc)
    filename = f"synaf_xml/{entry['title'].replace(' ', '_')}_{entry['year']}_{i}.xml"
    xml_tree.write(filename, encoding="utf-8", xml_declaration=True)
