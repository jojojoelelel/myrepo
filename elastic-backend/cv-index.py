import uuid
from elasticsearch import Elasticsearch
from tqdm import tqdm
import csv

es = Elasticsearch(
    "http://localhost:9200",
)

try:
    if es.ping():
        print("Successfully connected to Elasticsearch!")
    else:
        print("Failed to connect to Elasticsearch.")
except Exception as e:
    print(f"Error: {e}")

index_name = 'cv-transcriptions'

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        'mappings': {
            'properties': {
                'generated_text': {'type': 'text'},
                'duration': {'type': 'float'},
                'age': {'type': 'keyword'},
                'gender': {'type': 'keyword'},
                'accent': {'type': 'keyword'}
            }
        }
    })

csv_path = 'cv-valid-dev.csv'



with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in tqdm(reader):
        doc = {
            "generated_text": row.get("generated_text") or None,
            "duration": float(row["duration"]) if row.get("duration") else None,
            "age": row.get("age") or None,
            "gender": row.get("gender") or None,
            "accent": row.get("accent") or None
        }
        es.index(index=index_name, id=str(uuid.uuid4()), body=doc)

print('Indexing complete')

