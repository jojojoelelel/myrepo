# CV Transcription Search App

## Branches

- `main`: Codebase for **local development**.
- `deployment`: Codebase used for **deployment to AWS**.
- 
You can access the deployed application here: [http://3.107.8.57:3000](http://3.107.8.57:3000)
Information of the deployment can be found in the deployment branch

---

## Instructions for Running Locally : `main` branch

### **1. Getting Started**

#### a. Create a virtual environment
In the project root directory `/myrepo/` :

```bash
python -m venv myenv
```
#### b. Activate virtual environment
```bash
myenv\Scripts\Activate
```
#### c. Install dependencies 
```bash
cd asr
pip install -r requirements.txt
```

### **2. Automatic Speech Recognition (ASR)**

#### a. Download the [Common Voice dataset](https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0).
#### b. Place `cv-valid-dev` folder (containing all 4076 `.mp3` files) into the `/asr` directory.
#### c. Place `cv-valid-dev.csv` into `/asr/input` directory.

#### d. Start asr-api service in the `/asr/` directory
```bash
cd asr
docker-compose up
curl http://localhost:9200/ping 
```
Should receive 'pong' if asr-api service is running correctly

#### e. Transcribe the mp3 files in `cv-valid-dev`
##### Run `cv-decode.py` located in the `/asr` directory.
```bash
cd asr
python cv-decode.py
```
`cv-decode.py` will 

i. Read `input/cv-valid-dev.csv`

ii. Call the `/asr` API on each mp3 file in `cv-valid-dev` folder

iii. Write the `generated_text` and `duration` obtained from the `/asr` API into new columns

iv. Save it into `output/cv-valid-dev.csv`

### 3. Elastic Backend
For first-time setup

#### a. Create docker network `esnet`
```bash
docker network create esnet
```
Ensure docker network `esnet` exists
```bash
docker network ls
```
Should see
```bash
NAME   DRIVER
esnet  bridge
```
if `esnet` network was created properly

#### b. Create docker volume `certs`
```bash
docker volume create certs
```
Ensure docker volume `certs` exists
```bash
docker volume ls
```
Should see
```bash
DRIVER   VOLUME NAME
local    certs
```
if `certs` volume was created properly

#### c. Start up the es01 service in the `/elastic-backend/es02`
##### es01 is the first node in the cluster
```bash
cd es01
docker-compose up
```

#### d. Start up the es02 service in the `/elastic-backend/es02`
##### es02 is the second node in the cluster
```bash
cd es02
docker-compose up
```

#### e. Ensure that the backend service is running properly
```bash
curl -u elastic:123456 http://localhost:9200/_cluster/health?pretty 
```
Should see 
```bash
'cluster_name': cv-cluster
'status': green
'number_of_nodes: 2
```
if Elasticsearch service is running properly

#### If first time set up, do step `f-g` (Indexing), else skip to `Step 4`
#### f. Indexing
1. Check that the index `cv-transcriptions` does not exist
```bash
curl -u elastic:123456 -X POST http://localhost:9200/cv-transcriptions/_search?pretty
```
Should see 
```bash
'error'
'reason': 'no such index [cv-transcriptions]'
'status': 404
```
if index `cv-transcriptions` does not exist

2. Copy the `cv-valid-dev.csv` file in the `/asr/output` folder to `/elastic-backend/` folder
   
4. Run `cv-index.py` fron the `/elastic-backend/` directory
```bash
cd elastic-backed
python cv-index.py
```
`cv-index.py` will 
i. Connect to the Elasticsearch client on port 9200
ii. Read the `cv-valid-dev.csv` file that was copied into `/elastic-backend/` folder in step `f.2`
iii. Index the records in `cv-valid-dev.csv` into a new index called `cv-transcriptions`

5. Check that the index `cv-transcriptions` has been added successfully
```bash
curl -X POST http://localhost:9200/cv-transcriptions/_search?pretty
```
Should see
```bash
'successful': 1
'value': 4076
'_index': 'cv-transcriptions'
```
if `cv-transcriptions` has been added successfully

g. API key generation
An API Key is required to access the Elasticsearch client from the search-ui client
1. Create an API key with curl request
```bash
curl -X POST "http://localhost:9200/_security/api_key" -H "Content-Type: application/json" -u elastic:123456 -d "{\"name\":\"search-ui-read-only\",\"role_descriptors\":{\"search-ui-role\":{\"cluster\":[\"monitor\"],\"indices\":[{\"names\":[\"cv-transcriptions*\"],\"privileges\":[\"read\",\"view_index_metadata\"]}]}},\"metadata\":{\"cluster\":\"cv-cluster\"}}"
```
Should see
```bash
'id': '...' # api key id
'name': 'search-ui-read-only' # name of api key
'api_key': '...' # api key
'encoded': '...==' # the encoded api key *****
```
if API key was generated successfully

2. Save the *encoded* api key into `search-ui/.env`
```bash
VITE_REACT_APP_Encoded_API_Key='...=='
```

### 4. Search-UI 
This is the frontend interface
#### Start search-ui service in the `/search-ui/` directory
```bash
cd search-ui
docker-compose up
```

Search-ui frontend will be availabe at [http://localhost:3000](http://localhost:3000)
