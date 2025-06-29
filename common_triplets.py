import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
#import pandas as pd
import nltk
from nltk.corpus import stopwords
from neo4j import GraphDatabase

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Neo4j connection details
URI = "neo4j://127.0.0.1:7687" # adjust to own Neo4j
USER = "neo4j"
PASSWORD = "Tech@Stuttgart"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Load your tokenized_lines.json file
with open('tokenized_lines.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def generate_triplets(tokens):
    return [(tokens[i], tokens[i+1], tokens[i+2]) for i in range(len(tokens) - 2)]

# Collect lemma triplets per year from JSON data
triplets_by_year = defaultdict(Counter)
for entry in data:
    year = entry.get('year')
    tokens = entry.get('tokens', [])
    if not year:
        continue
    try:
        year_int = int(year)
    except:
        continue
    lemmas = [list(token.values())[0].lower() for token in tokens if token]
    triplets = generate_triplets(lemmas)
    triplets_by_year[year_int].update(triplets)

# Fetch all distinct years in Neo4j (for exploration/debug)
def fetch_all_years():
    query = """
    MATCH (w:Word)
    WHERE w.year IS NOT NULL
    RETURN DISTINCT toInteger(w.year) AS year
    ORDER BY year
    """
    years = []
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            years.append(record["year"])
    return years

print("Available years in Neo4j:", fetch_all_years())

# Fetch SVO triplets from Neo4j, with year converted to int
def fetch_svo_triplets():
    query = """
    MATCH 
      (verb:Word)-[r1:DEPENDS_ON {dep:'nsubj'}]->(subj:Word),
      (verb)-[r2:DEPENDS_ON]->(obj:Word)
    WHERE 
      r2.dep IN ['obj', 'dobj'] AND
      subj.year = verb.year AND
      obj.year = verb.year AND
      verb.year IS NOT NULL
    RETURN 
      subj.word AS subject,
      verb.word AS verb,
      obj.word  AS object,
      toInteger(verb.year) AS year
    LIMIT 5000
    """
    svo_triplets = defaultdict(Counter)
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            year = record["year"]
            if year is None:
                continue
            triplet = (record["subject"].lower(), record["verb"].lower(), record["object"].lower())
            svo_triplets[year].update([triplet])
    return svo_triplets

svo_triplets_by_year = fetch_svo_triplets()

def group_by_year(triplets_by_year):
    years = defaultdict(Counter)
    for year, counter in triplets_by_year.items():
        try:
            y = int(year)
            years[y].update(counter)
        except Exception:
            continue
    return years

years_all = group_by_year(triplets_by_year)
years_no_stop = defaultdict(Counter)
for year, counter in years_all.items():
    filtered = Counter({t: c for t, c in counter.items() if not all(w in stop_words for w in t)})
    years_no_stop[year].update(filtered)

years_svo = group_by_year(svo_triplets_by_year)

# Plot comparison per year of top triplets
def plot_comparison_by_year(top_n=10):
    years = sorted(years_all.keys())
    for year in years:
        top_all = years_all[year].most_common(top_n)
        top_no_stop = years_no_stop[year].most_common(top_n)
        top_svo = years_svo.get(year, Counter()).most_common(top_n)

        if not top_all and not top_no_stop and not top_svo:
            continue

        labels_all = [' '.join(t) for t, _ in top_all]
        counts_all = [c for _, c in top_all]

        labels_no_stop = [' '.join(t) for t, _ in top_no_stop]
        counts_no_stop = [c for _, c in top_no_stop]

        labels_svo = [' '.join(t) for t, _ in top_svo]
        counts_svo = [c for _, c in top_svo]

        fig, axs = plt.subplots(1, 3, figsize=(18, 7), sharey=True)
        fig.suptitle(f'Top {top_n} Triplets Comparison in Year {year}', fontsize=16)

        # Plot 1: All Triplets
        axs[0].barh(labels_all[::-1], counts_all[::-1], color='skyblue')
        axs[0].set_title('All Triplets (JSON)')
        axs[0].set_xlabel('Frequency')
        axs[0].grid(axis='x', linestyle='--', alpha=0.5)

        # Plot 2: No All-Stopword Triplets
        axs[1].barh(labels_no_stop[::-1], counts_no_stop[::-1], color='coral')
        axs[1].set_title('No All-Stopword Triplets (JSON)')
        axs[1].set_xlabel('Frequency')
        axs[1].grid(axis='x', linestyle='--', alpha=0.5)

        # Plot 3: SVO Triplets
        axs[2].barh(labels_svo[::-1], counts_svo[::-1], color='lightgreen')
        axs[2].set_title('Subject-Verb-Object Triplets (Neo4j)')
        axs[2].set_xlabel('Frequency')
        axs[2].grid(axis='x', linestyle='--', alpha=0.5)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()


plot_comparison_by_year()
