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
- [Troubleshooting](#troubleshooting)  
- [Contributors](#contributors)  
- [License](#license)


## Installation

1. Clone the repository or download the source.  
2. Navigate to the project directory.  
3. Install the required dependencies.


pip install -r requirements.txt

Note: Some components may require a local Neo4j database instance if using neo4jvis.py.

Usage
Run tei_extraction.py to process TEI-encoded XML files:

bash
Copy
Edit
python tei_extraction.py
For visualization or Neo4j-based processing, explore neo4jvis.py or related scripts.

Features
✅ TEI and SynAF XML parsing

✅ Syntactic annotation extraction and comparison

✅ JSON and CSV export formats

✅ Neo4j integration for graph-based visualization

✅ Tokenized line data for detailed linguistic analysis

Project Structure
graphql
Copy
Edit
TextTechnology/
├── neo4jvis.py                         # Visualization with Neo4j
├── tei_extraction.py                  # Core XML parsing logic
├── dracorshakes.py                    # Processing DraCor Shakespeare data
├── otherenglish.py                    # Additional English-language processing
├── tokenized_lines.json               # Token-level annotation data
├── tei_speaker_lines_with_corrected_year.csv  # Speaker data with metadata
├── tei_files_others/                  # Additional TEI XML documents
├── synaf_xml/                         # SynAF-based annotation files
Dependencies
Manually listed here (or see requirements.txt):

lxml

pandas

neo4j

json

csv

os, glob, re (standard libraries)

Configuration
Some scripts may require you to adjust file paths or configure Neo4j connection details directly within the Python files.

Documentation
Inline comments are provided in most Python files to aid understanding. For deeper insight into TEI or SynAF standards, consult their official documentation.

Examples
To process and analyze a TEI XML file:

bash
Copy
Edit
python tei_extraction.py
For Neo4j graph export:

bash
Copy
Edit
python neo4jvis.py
Ensure Neo4j is running and properly configured beforehand.

Troubleshooting
Ensure all required libraries are installed (pip install -r requirements.txt)

For Neo4j issues, verify credentials and connection settings

XML parsing errors usually indicate invalid TEI structure

Contributors
Kanak

Prasoon

Luis
