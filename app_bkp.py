
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Wolrd!"


@app.route('/search')
def search():
    host = 'localhost'
    port = 9200
    auth = ('admin', '@Thinkpad57!')

    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        )

    index = 'movie'
    
    body = {
        "query": {
            "size": 5,
            "query": {
                "knn": {
                "vector": {
                    "vector": movie_embeddings_matrix[movie_idx_to_search],
                    "k" : 20
                        }
                    }
                }
            }
     }

    response = requests.get(f"{OPENSEARCH_URL}/{index}/_search", json=body, headers=HEADERS)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

