import csv
from src.parsing.parser import parse_athlete


def read_csv_lazy(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def parse_csv(path):
    return map(parse_athlete, read_csv_lazy(path))
