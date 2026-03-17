
import csv
import glob
import os
import argparse

def process_file(filename, csv_writer, lines=None):
    if lines is None:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print(f"Error: Cannot read {filename} with UTF-8 encoding. Trying windows-1252...")
            with open(filename, 'r', encoding='windows-1252') as f:
                lines = f.readlines()
    # Skip the first 5 lines
    lines = lines[5:]
    original_text = ''.join(lines)
    full_text_lower = original_text.lower()
    # Find the earliest occurrence of "actionnaires" or "administrateurs"
    start_words = ["actionnaires", "administrateurs"]
    start_pos = len(original_text)
    for word in start_words:
        pos = full_text_lower.find(word)
        if pos != -1 and pos < start_pos:
            start_pos = pos
    if start_pos == len(original_text):
        print(f"No starting word (actionnaires or administrateurs) found in {filename}")
        return
    # Find the end of the relevant section
    end_markers = ["établissements"]
    end_pos = len(original_text)
    for marker in end_markers:
        pos = full_text_lower.find(marker, start_pos)
        if pos != -1 and pos < end_pos:
            end_pos = pos
    if end_pos == len(original_text):
        print(f"No end marker (établissements) found in {filename}")
        return
    # Extract the relevant section
    extracted = original_text[start_pos:end_pos].strip()
    extracted_lines = extracted.splitlines()
    print(f"\nDebugging lines in {filename}:")
    for i, line in enumerate(extracted_lines):
        print(f"Line {i+1}: {line}")
    # Process shareholders and administrators
    current_person = {}
    section = None
    i = 0
    while i < len(extracted_lines):
        line = extracted_lines[i].strip()
        if not line:
            i += 1
            continue
        line_lower = line.lower()
        if line_lower.startswith("actionnaires"):
            section = "Actionnaires"
            i += 1
            continue
        elif line_lower.startswith("administrateurs") or line_lower.startswith("liste des administrateurs"):
            section = "Administrateurs"
            i += 1
            continue
        elif line_lower.startswith(("dirigeants non membres", "bénéficiaires ultimes", "fondé de pouvoir")):
            if current_person:
                write_person_row(filename, current_person, csv_writer, section)
                current_person = {}
            section = None
            i += 1
            continue
        if section in ["Actionnaires", "Administrateurs"]:
            try:
                # Check for field name with tab
                if line_lower.startswith(("nom de famille", "prénom", "adresse du domicile", "adresse professionnelle", "fonctions actuelles")):
                    field = line_lower.split("\t")[0] if "\t" in line_lower else line_lower
                    # Look for value in the next few lines
                    value = ""
                    if i + 2 < len(extracted_lines) and extracted_lines[i + 1].strip() == ":":
                        value = extracted_lines[i + 2].strip()
                        i += 3
                    elif i + 1 < len(extracted_lines):
                        # Try next line directly (e.g., "Nom de famille : DENIS")
                        next_line = extracted_lines[i + 1].strip()
                        if ":" in next_line:
                            value = next_line.split(":", 1)[1].strip()
                            i += 2
                        else:
                            i += 1
                    else:
                        i += 1
                    context = extracted_lines[max(0, i-3):i+2]
                    if not value and field in ["nom de famille", "prénom"]:
                        print(f"Warning: No value found for {field} in {filename}")
                        print(f"Context: {context}")
                        i += 1
                        continue
                    if field == "nom de famille":
                        if current_person:
                            write_person_row(filename, current_person, csv_writer, section)
                            current_person = {}
                        current_person["Nom"] = value
                    elif field == "prénom":
                        current_person["Prénom"] = value
                    elif field == "adresse du domicile":
                        current_person["Adresse_domicile"] = value
                    elif field == "adresse professionnelle":
                        current_person["Adresse_pro"] = value
                    elif field == "fonctions actuelles" and section == "Administrateurs":
                        current_person["Fonction"] = value
                    continue
            except Exception as e:
                print(f"Error processing line in {filename}: {line} | Error: {e}")
                print(f"Context: {extracted_lines[max(0, i-3):i+2]}")
                i += 1
                continue
        i += 1
    if current_person:
        write_person_row(filename, current_person, csv_writer, section)
    print(f"🎉 Processed {filename}")

def write_person_row(filename, person, csv_writer, section):
    # Write row even if only Nom or Prénom is present
    nom = person.get("Nom", "")
    prenom = person.get("Prénom", "")
    if not nom and not prenom:
        return
    adresse = person.get("Adresse_pro", person.get("Adresse_domicile", ""))
    if adresse == "Adresse non publiable":
        adresse = ""
    fonction = person.get("Fonction", "") if section == "Administrateurs" else ""
    filename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    csv_writer.writerow([filename_without_ext, nom, prenom, adresse, fonction])

# Main part: process all .txt files in the specified directory
parser = argparse.ArgumentParser(description="Extract shareholders/administrators from text files into a CSV")
parser.add_argument(
    "directory",
    nargs="?",
    default="scraping",
    help="Directory containing .txt files to process (default: scraping/scraping)",
)
parser.add_argument(
    "-o",
    "--output",
    default="administrateurs.csv",
    help="Output CSV file path (default: administrateurs.csv)",
)
args = parser.parse_args()

directory = args.directory
output_file = args.output

print(f"Current working directory: {os.getcwd()}")
print(f"Looking for files in: {os.path.join(directory, '*.txt')}")
if not os.path.exists(directory):
    print(f"Directory {directory} does not exist")
    exit(1)
files = glob.glob(os.path.join(directory, "*.txt"))
if not files:
    print(f"No .txt files found in {directory}")
    exit(1)
print(f"Found files: {files}")
with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["NEQ", "Nom", "Prénom", "Adresse", "Fonction"])
    for file in files:
        process_file(file, writer)
print(f"🎉 Processing complete. Data written to {output_file}")
