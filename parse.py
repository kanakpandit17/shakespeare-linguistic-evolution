import os
import xml.etree.ElementTree as ET
import csv

tei_dir = "/Users/kanakpandit/Desktop/TextTechnology/tei_files"
output_csv = "tei_speaker_lines_with_metadata.csv"

# TEI namespace (adjust if your files use a different one)
NS = {'tei': 'http://www.tei-c.org/ns/1.0'}

with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Title", "Year", "Speaker", "Line"])

    for filename in os.listdir(tei_dir):
        if filename.endswith(".xml"):
            filepath = os.path.join(tei_dir, filename)
            print(f"Processing: {filename}")
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()

                # Extract metadata
                title_elem = root.find(".//tei:titleStmt/tei:title", namespaces=NS)
                title = title_elem.text.strip() if title_elem is not None else ""

                date_elem = root.find(".//tei:sourceDesc//tei:date", namespaces=NS)
                year = date_elem.text.strip() if date_elem is not None else ""

                # Find all <sp> blocks
                sp_blocks = root.findall(".//tei:sp", namespaces=NS)
                if not sp_blocks:
                    print(f"  No <sp> elements found in {filename}")

                # This must be inside try, so indent it here:
                for sp in sp_blocks:
                    speaker_elem = sp.find("tei:speaker", namespaces=NS)
                    if speaker_elem is None:
                        print(f"  No <speaker> found in one <sp> block in {filename}")
                        continue

                    speaker_words = [w.text.strip() for w in speaker_elem.findall("tei:w", namespaces=NS) if w.text]
                    speaker = ' '.join(speaker_words).strip()
                    if not speaker:
                        who = sp.attrib.get('who', '')
                        speaker = who.lstrip('#').strip() if who else "Unknown"

                    for l in sp.findall(".//tei:l", namespaces=NS):
                        words = ' '.join((elem.text or '') for elem in l if elem.tag in [f"{{{NS['tei']}}}w", f"{{{NS['tei']}}}pc"])
                        words = words.strip()
                        if words:
                            writer.writerow([filename, title, year, speaker, words])

            except ET.ParseError as e:
                print(f"Error parsing {filename}: {e}")
