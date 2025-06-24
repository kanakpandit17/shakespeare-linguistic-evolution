import os
import xml.etree.ElementTree as ET
import json

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
tei_dir = "tei_files"
tei_data = []
tei_token_data = [] # list for lemmatisation

# Mapping play name to year using .xml filenames
play_year_map = {
    "a-midsummer-nights-dream.xml": 1595,
    "alls-well-that-ends-well.xml": 1605,
    "antony-and-cleopatra.xml": 1606,
    "as-you-like-it.xml": 1599,
    "coriolanus.xml": 1608,
    "cymbeline.xml": 1610,
    "hamlet.xml": 1603,
    "henry-iv-part-1.xml": 1598,
    "henry-iv-part-2.xml": 1598,
    "henry-v.xml": 1599,
    "henry-vi-part-1.xml": 1591,
    "henry-vi-part-2.xml": 1591,
    "henry-vi-part-3.xml": 1591,
    "henry-viii.xml": 1613,
    "julius-caesar.xml": 1599,
    "king-john.xml": 1596,
    "king-lear.xml": 1606,
    "loves-labors-lost.xml": 1595,
    "macbeth.xml": 1606,
    "measure-for-measure.xml": 1604,
    "much-ado-about-nothing.xml": 1600,
    "othello.xml": 1604,
    "pericles.xml": 1609,
    "richard-ii.xml": 1595,
    "richard-iii.xml": 1593,
    "romeo-and-juliet.xml": 1597,
    "the-comedy-of-errors.xml": 1594,
    "the-merchant-of-venice.xml": 1600,
    "the-merry-wives-of-windsor.xml": 1602,
    "the-taming-of-the-shrew.xml": 1591,
    "the-tempest.xml": 1611,
    "the-winters-tale.xml": 1611,
    "timon-of-athens.xml": 1606,
    "titus-andronicus.xml": 1592,
    "troilus-and-cressida.xml": 1602,
    "twelfth-night.xml": 1601,
    "two-gentlemen-of-verona.xml": 1591,
}


def extract_speaker_lines(filepath, year):
    data = []
    tokens_data = [] # store words as tokens for later use with their lemmas
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        title_elem = root.find(".//tei:titleStmt/tei:title", namespaces=NS)
        title = title_elem.text.strip() if title_elem is not None else ""

        sp_blocks = root.findall(".//tei:sp", namespaces=NS)
        for sp in sp_blocks:
            speaker_elem = sp.find("tei:speaker", namespaces=NS)
            speaker = (
                ' '.join(w.text.strip() for w in speaker_elem.findall("tei:w", namespaces=NS) if w.text).strip()
                if speaker_elem is not None
                else sp.attrib.get("who", "Unknown")
            ) # added w-tag child to localise 'Speaker' inside TEI structure

            for tag in ["l", "p"]: # finds tag for verse play parts <l>...</l> and prose plays <p>...</p>
                for sent in sp.findall(f".//tei:{tag}", namespaces=NS):
                    words = ' '.join((elem.text or '') for elem in sent if elem.tag.endswith('w') or elem.tag.endswith('pc')).strip()
                    if words:
                        data.append({
                            "title": title,
                            "year": year,
                            "speaker": speaker,
                            "line": words
                        })

                    # Stores sentences as dict with Token (key) and lemma (value)
                    tokens = [
                        {elem.text.strip(): elem.attrib.get("lemma", "")}
                        for elem in sent
                        if elem.tag.endswith('w') and elem.text
                    ]
                    if tokens:
                        tokens_data.append({
                            "title": title,
                            "year": year,
                            "speaker": speaker,
                            "tokens": tokens
                        })
    except ET.ParseError as e:
        print(f"Parse error in {filepath}: {e}")
    return data, tokens_data

for filename in os.listdir(tei_dir):
    if filename.endswith(".xml"):
        filepath = os.path.join(tei_dir, filename)
        year = play_year_map.get(filename, "Unknown")
        if year == "Unknown":
            print(f"Year not found for: {filename}")
        else:
            lines, tokens = extract_speaker_lines(filepath, year) # added to store tokens_data
            tei_data.extend(lines)
            tei_token_data.extend(tokens)

with open("parsed_lines.json", "w", encoding="utf-8") as f:
    json.dump(tei_data, f, ensure_ascii=False, indent=2)
# creates json file with tokens associated with their lemmas
with open("tokenized_lines.json", "w", encoding="utf-8") as f:
    json.dump(tei_token_data, f, ensure_ascii=False, indent=2)