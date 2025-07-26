# Annotation Encoding – Comparing Syntactical Annotations in Historical Drama

## Overview

This project aims to investigate the linguistic evolution of William Shakespeare's literary works, focusing on plays written between 1591 and 1613. Our approach combines traditional corpus linguistics with modern natural language processing (NLP) methods. Specifically, we study how word usage, syntactic structures, and parts-of-speech (POS) frequencies changed over time in Shakespeare's plays. In addition to statistical metrics, we employ dependency parsing and graph-based representations to analyze structural relationships within the text.

We start with TEI-encoded XML files representing Shakespearean plays, which we parse into JSON format. These files are tokenized, annotated with lemmas and POS tags, and serialized for further processing. We further enrich the text data by creating syntactic graphs using SynAF and storing them in Neo4j, a graph database. The motivation behind this project is to offer deeper insights into authorial style, historical linguistics, and computational literature analysis.

By focusing on syntactic dependencies and lexeme patterns, we explore how grammatical preferences shifted in Shakespeare's evolving style, and whether syntactic complexity varied over time. This multi-layered approach highlights both stylistic and linguistic changes with temporal precision.

Furthermore, this investigation aims to answer broader research questions: Does Shakespeare’s syntax evolve toward more complex constructions over time? Are certain lexical choices more dominant in early or late works? How do syntactic graphs of characters compare across genres (tragedy vs. comedy)? This project delivers tools and annotated data for addressing such inquiries.

## Table of Contents

- [Introduction](#introduction)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Features](#features)
- [Project Structure](#project-structure)  
- [Dependencies](#dependencies)  
- [Configuration](#configuration)  
- [Documentation](#documentation)  
- [Examples](#examples)
- [Queries](#queries)
- [Troubleshooting](#troubleshooting)  
- [Contributors](#contributors)  



## Installation

1. Clone the repository or download the source.  
2. Navigate to the project directory.  
3. Install the required dependencies.

```
pip install -r requirements.txt
```

Note: Some components may require a local Neo4j database instance if using neo4jvis.py.

Usage
Run tei_extraction.py to process TEI-encoded XML files:

```
python tei_extraction.py
```

For visualization or Neo4j-based processing, explore neo4jvis.py or related scripts.

## Features

✅ TEI and SynAF XML parsing  
✅ Syntactic annotation extraction and comparison  
✅ JSON and CSV export formats  
✅ Neo4j integration for graph-based visualization  
✅ Tokenized line data for detailed linguistic analysis  


## Project Structure

```
TextTechnology/
├── neo4jvis.py                           # Visualization with Neo4j
├── tei_extraction.py                    # Core XML parsing logic
├── dracorshakes.py                      # Processing DraCor Shakespeare data
├── otherenglish.py                      # Additional English-language processing
├── tokenized_lines.json                 # Token-level annotation data
├── tei_speaker_lines_with_corrected_year.csv  # Speaker data with metadata
├── tei_files_others/                    # Additional TEI XML documents
└── synaf_xml/                           # SynAF-based annotation files
```




## Dependencies

Manually listed here (or see `requirements.txt`):

- `lxml`
- `pandas`
- `neo4j`
- `json`
- `csv`
- `os`, `glob`, `re` (standard libraries)


## Configuration
Some scripts may require you to adjust file paths or configure Neo4j connection details directly within the Python files.

## Documentation
Inline comments are provided in most Python files to aid understanding. For deeper insight into TEI or SynAF standards, consult their official documentation.
- TEI: https://tei-c.org/release/doc/tei-p5-doc/en/html/index.html
- SynAF: https://www.iso.org/obp/ui/en/#iso:std:iso:24615:-1:ed-1:v1:en

## Examples
To process and analyze a TEI XML file:

```
python tei_extraction.py
```


## For Neo4j graph export:

```
python neo4jvis.py
```

Ensure Neo4j is running and properly configured beforehand.

### Queries
# Neo4j Queries for Shakespeare Linguistic Analysis

---

### See words from a specific year:

```cypher
MATCH (w:Word {year: "1595"})
RETURN w.word, w.lemma, w.pos, w.text_title
LIMIT 50
```

### Explore the network around a particular word:

```cypher
MATCH (w:Word {word: "king"})-[r:DEPENDS_ON]-(related)
RETURN w, r, related
LIMIT 50
```

### Find the most common lemmas by year:

```cypher
MATCH (w:Word)
WITH w.year AS year, w.lemma AS lemma, COUNT(*) AS freq
ORDER BY year, freq DESC
RETURN year, lemma, freq
LIMIT 50
```
```text
Sample Output

```


### Co-occurrence of words


```cypher
MATCH (w1:Word), (w2:Word)
WHERE w1.sentence_id = w2.sentence_id AND w1.lemma <> w2.lemma
WITH w1.lemma AS lemma1, w2.lemma AS lemma2, COUNT(*) AS cooccurrence
WHERE cooccurrence > 5
MERGE (l1:Lemma {name: lemma1})
MERGE (l2:Lemma {name: lemma2})
MERGE (l1)-[r:CO_OCCURS_WITH]->(l2)
SET r.weight = cooccurrence
RETURN l1, r, l2
LIMIT 200
```

### Queries requiring SynAF annotations (r:DEPENDS_ON relationships)

```cypher
MATCH (:Word)-[r:DEPENDS_ON]->(:Word)
WITH r.dep AS dep, COUNT(*) AS freq, COLLECT(DISTINCT startNode(r).year) AS years
UNWIND years AS year
MERGE (d:DepType {name: dep})
MERGE (y:Year {year: year})
MERGE (d)-[rel:USED_IN]->(y)
SET rel.freq = freq
RETURN d, rel, y
LIMIT 100
```

### Co-occurrence of words filtered by POS and year:

```cypher
MATCH (w1:Word)-[r:DEPENDS_ON]->(w2:Word)
WHERE toInteger(w1.year) >= 1500 AND toInteger(w1.year) < 1800
  AND w1.pos IN ['VERB', 'NOUN', 'ADJ', 'PRON']
  AND w2.pos IN ['VERB', 'NOUN', 'ADJ', 'PRON']
WITH w1.lemma AS lemma1, w2.lemma AS lemma2, w1.pos AS pos1, w2.pos AS pos2, COUNT(*) AS freq
WHERE freq > 5 AND lemma1 <> lemma2
MERGE (l1:Lemma {name: lemma1, pos: pos1})
MERGE (l2:Lemma {name: lemma2, pos: pos2})
MERGE (l1)-[co:CO_OCCURS_WITH]->(l2)
SET co.weight = freq
RETURN l1.name, l1.pos, l2.name, l2.pos, co.weight
ORDER BY co.weight DESC
LIMIT 100
```

Note: Queries containing r:DEPENDS_ON require SynAF annotations to be present in your Neo4j database.

Below is the demo of how the Neo4j analysis works:
video



## Results
Some of the results are attached here:
The below figure shows the comparison of Top 10 triplets in year 1599:
image 2

The below figure explores the network around a particular word-”King”:
image 3

Sentiment Analysis is carried out to examine the emotions behind his works. The nltk VADER sentiment analyzer is used to evaluate the emotional tone of text.
The below figure shows the average sentiment of Shakespeare's plays over time.
image 4

The following figure shows the distribution of Sentiment Scores per Play in chronological order
image 5


The following figure compares the sentiment evolution of two plays side-by-side, average sentiment and emotional contrast score over line chunks.
image 6

The below figure shows Top Words per Year in Shakespeare's Plays where Bubble Size = Frequency
image 7

The following figure explores the frequency of occurrence of POS Tag over Years
image 8
  

## Troubleshooting
- Ensure all required libraries are installed (pip install -r requirements.txt)

- For Neo4j issues, verify credentials and connection settings

- XML parsing errors usually indicate invalid TEI structure



## Contributors
[Kanak ](https://github.com/kanakpandit17)

[Luis](https://github.com/avlmg)

[Prasoon](https://github.com/Prasoon-millennial)

