import requests
import os

# List of play IDs from your metadata
play_ids = [
    "a-midsummer-nights-dream",
    "alls-well-that-ends-well",
    "antony-and-cleopatra",
    "as-you-like-it",
    "coriolanus",
    "cymbeline",
    "hamlet",
    "henry-iv-part-1",
    "henry-iv-part-2",
    "henry-v",
    "henry-vi-part-1",
    "henry-vi-part-2",
    "henry-vi-part-3",
    "henry-viii",
    "julius-caesar",
    "king-john",
    "king-lear",
    "loves-labors-lost",
    "macbeth",
    "measure-for-measure",
    "much-ado-about-nothing"
    # Add the rest if needed
]

base_url = "https://dracor.org/api/v1/corpora/shake/plays/{}/tei"
output_dir = "tei_files"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Download loop
for play_id in play_ids:
    tei_url = base_url.format(play_id)
    try:
        response = requests.get(tei_url)
        response.raise_for_status()  # Raise exception for HTTP errors

        filename = os.path.join(output_dir, f"{play_id}.xml")
        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"✅ Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {play_id}: {e}")
