import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import json

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# === CONFIGURATION ===
compare_mode = False  #  Set to False to view only one play
play1 = "A Midsummer Night’s Dream"
play2 = "Hamlet"  # Ignored if compare_mode is False
chunk_size = 20 # Adjust depending on mode or precision wanted (for comparison around 100; for single play around 20)

# === Load data ===
with open("tokenized_lines.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def extract_sentiment_scores(play_title):
    lines = [entry for entry in data if entry["title"] == play_title]
    scores = []
    for entry in lines:
        tokens = entry["tokens"]
        text = " ".join(token for token_dict in tokens for token in token_dict)
        polarity = sia.polarity_scores(text)["compound"]
        scores.append(polarity)
    return scores

def chunk_sentiment_analysis(sentiment_scores, chunk_size):
    chunk_indices = []
    avg_sentiments = []
    contrast_scores = []

    for i in range(0, len(sentiment_scores), chunk_size):
        chunk = sentiment_scores[i:i + chunk_size]
        if not chunk:
            continue
        avg_sent = np.mean(chunk)
        pos_count = sum(1 for s in chunk if s > 0.05)
        neg_count = sum(1 for s in chunk if s < -0.05)
        contrast = 2 * min(pos_count, neg_count) / (pos_count + neg_count) if (pos_count + neg_count) > 0 else 0
        avg_sentiments.append(avg_sent)
        contrast_scores.append(contrast)
        chunk_indices.append(i + chunk_size // 2)
    return chunk_indices, avg_sentiments, contrast_scores

# === Plot ===
if compare_mode:
    scores1 = extract_sentiment_scores(play1)
    indices1, avg_sent1, contrast1 = chunk_sentiment_analysis(scores1, chunk_size)
    median1 = np.median(scores1)

    scores2 = extract_sentiment_scores(play2)
    indices2, avg_sent2, contrast2 = chunk_sentiment_analysis(scores2, chunk_size)
    median2 = np.median(scores2)

    fig, axes = plt.subplots(2, 2, figsize=(16, 8), sharex='col', gridspec_kw={'height_ratios': [3, 1]})

    # Play 1
    axes[0, 0].plot(indices1, avg_sent1, color='blue', label=play1)
    axes[0, 0].axhline(median1, color='red', linestyle='--', label='Median')
    axes[0, 0].set_title(f"Sentiment in '{play1}'")
    axes[0, 0].set_ylabel("Avg Sentiment")
    axes[0, 0].legend()
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    axes[1, 0].bar(indices1, contrast1, width=chunk_size*0.8, color='red', alpha=0.7)
    axes[1, 0].set_ylabel("Contrast Score")
    axes[1, 0].set_xlabel("Line Index")
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    # Play 2
    axes[0, 1].plot(indices2, avg_sent2, color='green', label=play2)
    axes[0, 1].axhline(median2, color='red', linestyle='--', label='Median')
    axes[0, 1].set_title(f"Sentiment in '{play2}'")
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)

    axes[1, 1].bar(indices2, contrast2, width=chunk_size*0.8, color='orange', alpha=0.7)
    axes[1, 1].set_xlabel("Line Index")
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

else:
    scores = extract_sentiment_scores(play1)
    indices, avg_sent, contrast = chunk_sentiment_analysis(scores, chunk_size)
    median = np.median(scores)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})

    ax1.plot(indices, avg_sent, label="Average Sentiment", color='blue', linewidth=2)
    ax1.axhline(median, color='red', linestyle='--', linewidth=1.2, label='Median Sentiment')
    ax1.set_title(f"Sentiment Evolution in '{play1}'", fontsize=14)
    ax1.set_ylabel("Average Sentiment", fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    ax2.bar(indices, contrast, width=chunk_size * 0.8, color='red', alpha=0.7, label="Emotional Contrast")
    ax2.set_title("Contrast of Emotion (Positive vs Negative)", fontsize=13)
    ax2.set_ylabel("Contrast Score (0–1)", fontsize=12)
    ax2.set_xlabel("Line Index (approximate)", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    plt.show()
