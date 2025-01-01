from flask import Flask, request, jsonify
from opensearchpy import OpenSearch

app = Flask(__name__)

# Conexión a OpenSearch
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=('admin', '@Thinkpad57!')
)
    

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API para consultas a OpenSearch"}), 200

@app.route("/search_movie", methods=["POST"])
def search():
    try:
        print("Solicitud recibida")  # Mensaje para confirmar la llegada de la solicitud
        data = request.json
        
        query_id = data.get("ID")  # ID del vector
        k = data.get("K")

        if not isinstance(query_id, int) or query_id <= 0:
            return jsonify({"error": "El ID debe ser un número entero válido mayor a 0"}), 400
        
        if not isinstance(k, int) or k <= 0:
            return jsonify({"error": "El valor de K debe ser un número entero positivo"}), 400

        # Query
        try:
            query = {
                "size": k,
                "query": {
                    "knn": {
                    "vector": {
                        "vector": movie_embeddings_matrix[query_id],
                        "k" : k
                    }
                    }
                }
            }
        
        response = client.search(index="movie", id=query_id)
        
        if response["found"]:
            # Si se encuentra el documento, devuelve el vector
            return response['hits']['hits']  # Asumiendo que el campo se llama 'embedding'
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el vector por ID: {str(e)}")
        return None

        # Extraer los resultados
        results = [{"id": hit["_id"], "score": hit["_score"], "vector": hit["_source"]["embedding"]} for hit in response["hits"]["hits"]]
        
        return jsonify({"results": results}), 200
    
    except Exception as e:
        print("Error en la búsqueda:", str(e))
        return jsonify({"error": str(e)}), 500
