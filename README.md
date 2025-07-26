# Annotation Encoding – Comparing Syntactical Annotations in Historical Drama

## Introduction

This project focuses on analyzing and comparing syntactical annotations across historical drama texts. It supports working with TEI-encoded documents and SynAF-based annotations, providing tools for extraction, transformation, and visualization of linguistic features. The project is particularly useful for digital humanities scholars working with corpora like DraCor (Drama Corpora) and similar resources.

## Table of Contents

•⁠  ⁠[Introduction](#introduction)
•⁠  ⁠[Installation](#installation)
•⁠  ⁠[Usage](#usage)
•⁠  ⁠[Features](#features)
•⁠  ⁠[Project Structure](#project-structure)
•⁠  ⁠[Dependencies](#dependencies)
•⁠  ⁠[Configuration](#configuration)
•⁠  ⁠[Documentation](#documentation)
•⁠  ⁠[Examples](#examples)
•⁠  ⁠[Troubleshooting](#troubleshooting)
•⁠  ⁠[Contributors](#contributors)
•⁠  ⁠[License](#license)

## Installation

1.⁠ ⁠Clone the repository or download the source.
2.⁠ ⁠Navigate to the project directory.
3.⁠ ⁠Install the required dependencies:

```bash
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
