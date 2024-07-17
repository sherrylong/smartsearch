# Local Project Setup

1. Create Docker network

```
docker network create elastic-net
docker run -p 9200:9200 -d --name elasticsearch \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.http.ssl.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0
```

2. Connect Python client

```
python connect_python.py
```

3. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

5. Generate Elasticsearch index

```
flask reindex
```

6. Run application

```
flask run
```
