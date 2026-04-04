import csv
import json
import argparse
import os


def csv_to_json_file(input_path, output_path, delimiter=',', indent=2, encoding='utf-8'):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Le fichier d'entrée n'existe pas : {input_path}")

    with open(input_path, 'r', encoding=encoding, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError("Le fichier CSV doit contenir une ligne d'en-tête avec les noms de colonnes.")
        data = [row for row in reader]

    with open(output_path, 'w', encoding=encoding, newline='') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=indent)


def convert_path(path, output_path=None, delimiter=',', indent=2, encoding='utf-8'):
    if os.path.isdir(path):
        csv_files = [
            entry.path
            for entry in os.scandir(path)
            if entry.is_file() and entry.name.lower().endswith('.csv')
        ]
        if not csv_files:
            raise FileNotFoundError(f"Aucun fichier CSV trouvé dans le dossier : {path}")

        destination_dir = path if output_path is None else output_path
        if output_path is not None and not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
        elif output_path is not None and not os.path.isdir(destination_dir):
            raise ValueError(f"Le chemin de sortie doit être un dossier quand l'entrée est un dossier : {output_path}")

        for csv_file in csv_files:
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            json_file = os.path.join(destination_dir, f"{base_name}.json")
            csv_to_json_file(csv_file, json_file, delimiter=delimiter, indent=indent, encoding=encoding)
            print(f"Converti : {csv_file} -> {json_file}")
        return csv_files

    if not os.path.exists(path):
        raise FileNotFoundError(f"Le fichier d'entrée n'existe pas : {path}")
    if os.path.isdir(path):
        raise ValueError(f"Le chemin d'entrée ne doit pas être un dossier : {path}")

    if output_path is None:
        base, _ = os.path.splitext(path)
        output_path = f"{base}.json"
    else:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    csv_to_json_file(path, output_path, delimiter=delimiter, indent=indent, encoding=encoding)
    print(f"Converti : {path} -> {output_path}")
    return [path]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convertit un fichier CSV ou tous les CSV d\'un dossier en JSON.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('path', help='Chemin vers le fichier CSV ou le dossier contenant les CSV')
    parser.add_argument('output', nargs='?', help='Chemin du fichier JSON de sortie ou dossier de sortie')
    parser.add_argument('-d', '--delimiter', default=',', help='Délimiteur utilisé dans les CSV')
    parser.add_argument('-i', '--indent', type=int, default=2, help='Indentation JSON')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Encodage du fichier CSV et JSON')
    args = parser.parse_args()

    try:
        convert_path(args.path, args.output, delimiter=args.delimiter, indent=args.indent, encoding=args.encoding)
        print('Conversion terminée.')
    except Exception as e:
        print(f"Erreur : {e}")
        raise
