import uuid
from elasticsearch import Elasticsearch
# from tqdm import tqdm

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
                # 'filename': { 'type': 'text' },
                'generated_text': {'type': 'text'},
                'duration': {'type': 'float'},
                'age': {'type': 'keyword'},
                'gender': {'type': 'keyword'},
                'accent': {'type': 'keyword'}
            }
        }
    })

csv_path = 'cv-valid-dev.csv'

# pandas and numpy

# import pandas as pd
# import numpy as np

# df = pd.read_csv(csv_path)
# df = df.replace(np.nan, None)

# for _, row in tqdm(df.iterrows(), total=len(df)):
#     doc = {
#         "generated_text": row.get("generated_text"),
#         "duration": row.get("duration"),
#         "age": row.get("age"),
#         "gender": row.get("gender"),
#         "accent": row.get("accent")
#     }
#     es.index(index=index_name, id=str(uuid.uuid4()), body=doc)

# print('Indexing complete')

# python csv

import csv

with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        doc = {
            # "filename": row.get("filename").split("/")[1] or None,
            "generated_text": row.get("generated_text") or None,
            "duration": float(row["duration"]) if row.get("duration") else None,
            "age": row.get("age") or None,
            "gender": row.get("gender") or None,
            "accent": row.get("accent") or None
        }
        es.index(index=index_name, id=str(uuid.uuid4()), body=doc)

print('Indexing complete')

