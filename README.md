Shakespeare Text Technology Project
This project processes Shakespeare's plays using natural language processing (NLP) and text analysis techniques. It downloads the texts from DraCor, parses the TEI XML format, performs syntactic dependency analysis using spaCy, and converts the output into SynAF (Syntactic Annotation Format). It also provides a Neo4j-based visualization of syntactic graphs.

📌 Project Motivation
Shakespeare's texts are rich in linguistic patterns, style, and historical significance. By applying modern NLP and graph analysis tools, we can explore:

How characters interact syntactically
How language evolves across plays and time
How dependency structures inform meaning in dramatic dialogue


🔧 Architecture Overview

Download Shakespeare plays (TEI XML) from the DraCor API.
Parse TEI files to extract structured dialogue.
Analyze syntax using spaCy and generate dependency trees.
Export the dependency output into SynAF XML.
Visualize the syntactic network using Neo4j graph database.


🗂️ Files and Scripts



File
Purpose



dracorshakes.py
Downloads Shakespeare plays from DraCor API in TEI format


parse.py
Parses TEI XML files to extract dialogues and structure


parsedataToSynAf.py
Performs spaCy-based syntactic analysis and exports SynAF XML


upload_to_neo4j.py
(Optional) Uploads SynAF-based structures to Neo4j graph database



⚙️ Setup Instructions

Install required packages:pip install requests lxml spacy
python -m spacy download en_core_web_sm
python dracorshakes.py         # Step 1: Download TEI files
python parse.py                # Step 2: Parse and extract dialogues
python parsedataToSynAf.py     # Step 3: Convert parsed data to SynAF format
python upload_to_neo4j.py      # Step 4: Push syntactic graph to Neo4j




🧠 Dependencies

Python 3.7+
requests - For API interaction
lxml - For parsing TEI XML files
spaCy - NLP processing and dependency parsing
en_core_web_sm - spaCy’s English model


📂 Directory Structure
shakespeare-project/
│
├── tei_files/           # Raw TEI XML downloads
├── parsed_output/       # Cleaned and structured JSON output (optional)
├── synaf_xml/           # Generated SynAF XML files with syntactic annotations
├── neo4j_upload/        # Files for Neo4j graph uploads
│
├── dracorshakes.py
├── parse.py
├── parsedataToSynAf.py
├── upload_to_neo4j.py
└── README.md


🔎 Sample Output (SynAF XML snippet)
<synaf>
  <node id="1" word="king" lemma="king" pos="NOUN"/>
  <node id="2" word="becoming" lemma="become" pos="VERB"/>
  <dep from="2" to="1" type="npadvmod"/>
</synaf>


🧠 Neo4j Integration
You can visualize dependencies as a graph using Neo4j.

Nodes represent words.
Edges represent syntactic relations (e.g., nsubj, obj, poss).

Useful for exploring dependency structures, character interactions, and sentence complexity.

Example Neo4j Cypher Query
MATCH (w:Word)
WITH w.lemma AS lemma, w.year AS year, COUNT(*) AS freq
WHERE lemma IS NOT NULL AND year IS NOT NULL
MERGE (l:Lemma {name: lemma})
MERGE (y:Year {year: year})
MERGE (l)-[r:APPEARS_IN]->(y)
SET r.freq = freq
RETURN l, r, y
LIMIT 100


💡 Applications

Digital Humanities: Study syntactic change across Shakespeare's corpus or compare linguistic structures in other historical texts.
Education: Use the dependency graphs to teach grammar, style, and structure.
Entertainment & Script Analysis: Track character dialogues, analyze sentence complexity or style for writers and dramaturges.
AI Dialogue Systems: Improve natural dialogue understanding by modeling syntactic structures in training datasets.


📚 References

DraCor API Documentation
SynAF Specification (ISO 24615)
spaCy Documentation
Neo4j Graph DB


👥 Contributors

Kanak Pandit
Prasoon Tiwari
Luis Miguel Amores Valderas
