import os
import xml.etree.ElementTree as ET
import json

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
tei_dir = "tei_files_others"
tei_data = []
tei_token_data = [] # list for lemmatisation

# Mapping play name to year using .xml filenames
play_year_map = {
    "ep000041.xml": 1591,
    "ep000793.xml": 1591,
    "ep000226.xml": 1591,
    "ep000242.xml": 1591,
    "ep000578.xml": 1591,
    "ep000117.xml": 1592,
    "ep000815.xml": 1592,
    "ep000151.xml": 1592,
    "ep000216.xml": 1592,
    "ep000144.xml": 1593,
    "ep000148.xml": 1593,
    "ep000485.xml": 1594,
    "ep000360.xml": 1594,
    "ep000060.xml": 1594,
    "ep000313.xml": 1594,
    "ep000331.xml": 1596,
    "ep000045.xml": 1596,
    "ep000339.xml": 1597,
    "ep000058.xml": 1597,
    "ep000104.xml": 1597,
    "ep000051.xml": 1598,
    "ep000091.xml": 1598,
    "ep000080.xml": 1598,
    "ep000205.xml": 1598,
    "ep000230.xml": 1598,
    "ep000394.xml": 1599,
    "ep000794.xml": 1599,
    "ep000380.xml": 1599,
    "ep000383.xml": 1599,
    "ep000066.xml": 1599,
    "ep000108.xml": 1599,
    "ep000155.xml": 1599,
    "ep000220.xml": 1599,
    "ep000801.xml": 1599,
    "ep000244.xml": 1599,
    "ep000764.xml": 1599,
    "ep000145.xml": 1600,
    "ep000381.xml": 1600,
    "ep000612.xml": 1600,
    "ep000044.xml": 1600,
    "ep000093.xml": 1600,
    "ep000156.xml": 1600,
    "ep000392.xml": 1600,
    "ep000349.xml": 1601,
    "ep000330.xml": 1601,
    "ep000181.xml": 1601,
    "ep000382.xml": 1601,
    "ep000350.xml": 1601,
    "ep000094.xml": 1601,
    "ep000161.xml": 1601,
    "ep000129.xml": 1602,
    "ep000312.xml": 1602,
    "ep000325.xml": 1602,
    "ep000337.xml": 1602,
    "ep000037.xml": 1602,
    "ep000336.xml": 1602,
    "ep000347.xml": 1602,
    "ep000388.xml": 1602,
    "ep000057.xml": 1602,
    "ep000076.xml": 1602,
    "ep000316.xml": 1603,
    "ep000218.xml": 1603,
    "ep000257.xml": 1603,
    "ep000078.xml": 1603,
    "ep000157.xml": 1603,
    "ep000159.xml": 1603,
    "ep000184.xml": 1603,
    "ep000190.xml": 1603,
    "ep000318.xml": 1604,
    "ep000315.xml": 1604,
    "ep000119.xml": 1604,
    "ep000332.xml": 1604,
    "ep000343.xml": 1604,
    "ep000363.xml": 1604,
    "ep000373.xml": 1604,
    "ep000376.xml": 1604,
    "ep000390.xml": 1604,
    "ep000062.xml": 1604,
    "ep000077.xml": 1604,
    "ep000095.xml": 1604,
    "ep000100.xml": 1604,
    "ep000160.xml": 1604,
    "ep000188.xml": 1604,
    "ep000189.xml": 1604,
    "ep000236.xml": 1604,
    "ep000317.xml": 1605,
    "ep000342.xml": 1605,
    "ep000335.xml": 1605,
    "ep000800.xml": 1605,
    "ep000359.xml": 1605,
    "ep000362.xml": 1605,
    "ep000377.xml": 1605,
    "ep000389.xml": 1605,
    "ep000406.xml": 1605,
    "ep000063.xml": 1605,
    "ep000105.xml": 1605,
    "ep000096.xml": 1605,
    "ep000162.xml": 1605,
    "ep000192.xml": 1605,
    "ep000259.xml": 1605,
    "ep000296.xml": 1605,
    "ep000306.xml": 1605,
    "ep000398.xml": 1606,
    "ep000086.xml": 1606,
    "ep000426.xml": 1606,
    "ep000135.xml": 1606,
    "ep000372.xml": 1606,
    "ep000075.xml": 1606,
    "ep000110.xml": 1606,
    "ep000243.xml": 1606,
    "ep000261.xml": 1606,
    "ep000125.xml": 1607,
    "ep000128.xml": 1607,
    "ep000323.xml": 1607,
    "ep000333.xml": 1607,
    "ep000334.xml": 1607,
    "ep000371.xml": 1607,
    "ep000374.xml": 1607,
    "ep000158.xml": 1607,
    "ep000163.xml": 1607,
    "ep000795.xml": 1607,
    "ep000238.xml": 1607,
    "ep000260.xml": 1607,
    "ep000116.xml": 1608,
    "ep000409.xml": 1608,
    "ep000357.xml": 1608,
    "ep000007.xml": 1608,
    "ep000692.xml": 1608,
    "ep000131.xml": 1609,
    "ep000358.xml": 1609,
    "ep000003.xml": 1609,
    "ep000407.xml": 1609,
    "ep000580.xml": 1609,
    "ep000107.xml": 1609,
    "ep000130.xml": 1610,
    "ep000132.xml": 1610,
    "ep000340.xml": 1610,
    "ep000002.xml": 1610,
    "ep000432.xml": 1610,
    "ep000061.xml": 1610,
    "ep000098.xml": 1610,
    "ep000127.xml": 1611,
    "ep000351.xml": 1611,
    "ep000378.xml": 1611,
    "ep000384.xml": 1611,
    "ep000199.xml": 1611,
    "ep000004.xml": 1611,
    "ep000420.xml": 1611,
    "ep000008.xml": 1611,
    "ep000425.xml": 1611,
    "ep000054.xml": 1611,
    "ep000099.xml": 1611,
    "ep000239.xml": 1611,
    "ep000295.xml": 1611,
    "ep000064.xml": 1612,
    "ep000065.xml": 1612,
    "ep000305.xml": 1612,
    "ep000124.xml": 1613,
    "ep000338.xml": 1613,
    "ep000427.xml": 1613,
    "ep000435.xml": 1613,
    "ep000182.xml": 1613,
    "ep000431.xml": 1613,
    "ep000286.xml": 1613,
    "ep000290.xml": 1613,
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

with open("parsed_lines_others.json", "w", encoding="utf-8") as f:
    json.dump(tei_data, f, ensure_ascii=False, indent=2)
# creates json file with tokens associated with their lemmas
with open("tokenized_lines_others.json", "w", encoding="utf-8") as f:
    json.dump(tei_token_data, f, ensure_ascii=False, indent=2)