# Import libraries
import uuid
import csv
from elasticsearch import Elasticsearch
from tqdm import tqdm

# Initialise Elasticsearch client
es = Elasticsearch(
    "http://localhost:9200",
)

# Connect to Elasticsearch service
try:
    if es.ping():
        print("Successfully connected to Elasticsearch!")
    else:
        print("Failed to connect to Elasticsearch.")
except Exception as e:
    print(f"Error: {e}")

# Define index name
index_name = 'cv-transcriptions'

# Check if index exists
if not es.indices.exists(index=index_name):
    # If not, create index with the following mappings
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

# Set the csv file containing the records to be indexed
csv_path = 'cv-valid-dev.csv'

# Open the csv file
with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    # Create a reader object
    reader = csv.DictReader(csvfile)
    # Iterate through each record in the csv file
    for row in tqdm(reader):
        doc = {
            "generated_text": row.get("generated_text") or None,
            "duration": float(row["duration"]) if row.get("duration") else None,
            "age": row.get("age") or None,
            "gender": row.get("gender") or None,
            "accent": row.get("accent") or None
        }
        # Add the record into the index
        es.index(index=index_name, id=str(uuid.uuid4()), body=doc)

# Acknowledgement
print('Indexing complete')

