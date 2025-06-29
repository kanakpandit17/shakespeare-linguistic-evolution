import json
#import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download

# Download VADER lexicon if not already downloaded
download('vader_lexicon')

# Load JSON
with open("tokenized_lines.json", "r", encoding="utf-8") as f:
    lines = json.load(f)

# Setup VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Data structures
sentiment_by_year = defaultdict(list)
sentiment_by_play = defaultdict(list)
line_sentiments = []

# Process each line
for line in lines:
    title = line['title']
    year = line['year']
    lemmas = [list(token.values())[0] for token in line['tokens']]
    sentence = " ".join(lemmas)

    score = sia.polarity_scores(sentence)
    compound = score['compound']  # Ranges -1 (neg) to +1 (pos)

    sentiment_by_year[year].append(compound)
    sentiment_by_play[title].append(compound)
    line_sentiments.append(compound)

# Plot: Average sentiment over time
avg_sentiment_by_year = {year: sum(scores) / len(scores) for year, scores in sentiment_by_year.items()}
plt.figure(figsize=(10, 5))
plt.plot(sorted(avg_sentiment_by_year.keys()),
         [avg_sentiment_by_year[year] for year in sorted(avg_sentiment_by_year.keys())],
         marker='o')
plt.title("Average Sentiment of Shakespeare's Plays Over Time")
plt.xlabel("Year")
plt.ylabel("Sentiment Score (Compound)")
plt.axhline(0, color='gray', linestyle='--')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot: Sentiment per play
# Create mapping play -> year
play_to_year = {}
for line in lines:
    play_to_year[line['title']] = line['year']
sorted_plays = sorted(sentiment_by_play.keys(), key=lambda play: play_to_year.get(play, 0)) # Sort plays by year ascending
labels_with_year = [f"{play} ({play_to_year.get(play, 'n/a')})" for play in sorted_plays]

plt.figure(figsize=(12, 8))
plt.boxplot(
    [sentiment_by_play[play] for play in sorted_plays],
    tick_labels=labels_with_year,  # updated here from labels to tick_labels
    patch_artist=True,
    boxprops=dict(facecolor="cornflowerblue"),
    showfliers=False
)
plt.xticks(rotation=45, ha='right')
plt.ylabel("Compound Sentiment Score")
plt.title("Distribution of Sentiment Scores per Play (VADER) - Chronological")
plt.tight_layout()
plt.show()

# Plot: Histogram of sentiment scores
plt.figure(figsize=(8, 5))
plt.hist(line_sentiments, bins=30, color="mediumseagreen", edgecolor="black")
plt.yscale('log')  # Logarithmic y-axis
plt.title("Histogram of Line Sentiment Scores (VADER)")
plt.xlabel("Sentiment Score")
plt.ylabel("Number of Lines")
plt.tight_layout()
plt.show()
