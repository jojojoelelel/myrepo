import pandas as pd
import uuid
import numpy as np
from elasticsearch import Elasticsearch
from tqdm import tqdm

csv_path = 'cv-valid-dev.csv'
df = pd.read_csv(csv_path)
df = df.replace(np.nan, None)

es = Elasticsearch("http://localhost:9200")

if not es.ping():
    raise ValueError('Connection to Elasticsearch failed')
else:
    print("Connected to Elasticsearch!")

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

for _, row in tqdm(df.iterrows(), total=len(df)):
    doc = {
        "generated_text": row.get("generated_text"),
        "duration": row.get("duration"),
        "age": row.get("age"),
        "gender": row.get("gender"),
        "accent": row.get("accent")
    }
    es.index(index=index_name, id=str(uuid.uuid4()), body=doc)

print('Indexing complete')


