#POS tag frequency over years

import os
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

synaf_dir = "/Users/kanakpandit/Desktop/TextTechnology/synaf_xml"
files = [f for f in os.listdir(synaf_dir) if f.endswith(".xml")]

# Data holders
year_lemma_counts = defaultdict(Counter)
year_pos_counts = defaultdict(Counter)
year_dep_counts = defaultdict(Counter)

for filename in files:
    filepath = os.path.join(synaf_dir, filename)
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Extract year
    year_elem = root.find(".//Meta/Year")
    year = year_elem.text if year_elem is not None else "Unknown"

    # Parse Nodes (words)
    nodes = {}
    for node in root.findall(".//Nodes/Node"):
        node_id = node.attrib.get("id")
        lemma = node.attrib.get("lemma", "").lower()
        pos = node.attrib.get("pos", "")
        word = node.attrib.get("word", "").lower()
        nodes[node_id] = {"lemma": lemma, "pos": pos, "word": word}

        # Count lemmas and POS
        if lemma:
            year_lemma_counts[year][lemma] += 1
        if pos:
            year_pos_counts[year][pos] += 1

    # Parse Edges (dependencies)
    for edge in root.findall(".//Edges/Edge"):
        dep = edge.attrib.get("dep", "")
        if dep:
            year_dep_counts[year][dep] += 1

# Example: print top 10 lemmas for a sample year
sample_year = "1595"
print(f"Top lemmas in {sample_year}:")
for lemma, count in year_lemma_counts[sample_year].most_common(10):
    print(f"  {lemma}: {count}")

# Plot example: POS tag distribution over years for a few POS tags
pos_tags_to_plot = ["NOUN", "VERB", "ADJ", "PRON"]

years = sorted(year_pos_counts.keys())
for pos_tag in pos_tags_to_plot:
    counts = [year_pos_counts[y].get(pos_tag, 0) for y in years]
    plt.plot(years, counts, label=pos_tag)

plt.xlabel("Year")
plt.ylabel("Count")
plt.title("POS Tag Frequency over Years")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
