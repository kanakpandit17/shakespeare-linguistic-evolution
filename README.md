# Shakespeare Text Technology Project

This project processes Shakespeare's plays using natural language processing and text analysis techniques.

## Overview

The project downloads Shakespeare's plays from the DraCor API, parses the TEI XML files, and performs syntactic analysis using spaCy to create SynAF (Syntactic Annotation Format) XML files.

## Files

- `dracorshakes.py` - Downloads Shakespeare plays from DraCor API
- `parse.py` - Parses TEI XML files and extracts dialogue
- `parsedataToSynAf.py` - Converts parsed data to SynAF XML format using spaCy

## Setup

1. Install required packages:
```bash
pip install requests lxml spacy
python -m spacy download en_core_web_sm
```

2. Run the scripts in order:
```bash
python dracorshakes.py  # Download TEI files
python parse.py         # Parse TEI files
python parsedataToSynAf.py  # Convert to SynAF format
```

## Data Sources

- **DraCor API**: Shakespeare plays in TEI XML format
- **spaCy**: English language model for syntactic analysis

## Output

- `tei_files/` - Downloaded TEI XML files
- `synaf_xml/` - Generated SynAF XML files with syntactic annotations

## Requirements

- Python 3.7+
- requests
- lxml
- spacy
- en_core_web_sm language model 