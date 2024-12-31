from flask import Flask, request, jsonify
from opensearchpy import OpenSearch

app = Flask(__name__)

# Conexión a OpenSearch
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=('admin', '@Thinkpad57!')
)

def get_vector_by_id(query_id):
    try:
        # Realizar una consulta para obtener el documento correspondiente al ID
        response = client.get(index="embedding_index", id=query_id)
        
        if response["found"]:
            # Si se encuentra el documento, devuelve el vector
            return response['hits']['hits']  # Asumiendo que el campo se llama 'embedding'
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el vector por ID: {str(e)}")
        return None
    

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API para consultas a OpenSearch"}), 200

@app.route("/search", methods=["POST"])
def search():
    try:
        print("Solicitud recibida")  # Mensaje para confirmar la llegada de la solicitud
        data = request.json
        
        # Recibir los parámetros ID y K desde la solicitud
        query_id = data.get("ID")  # ID del vector
        k = data.get("K", 3)  # Número de resultados, valor por defecto es 3

        if not isinstance(query_id, int) or query_id <= 0:
            return jsonify({"error": "El ID debe ser un número entero válido mayor a 0"}), 400
        
        if not isinstance(k, int) or k <= 0:
            return jsonify({"error": "El valor de K debe ser un número entero positivo"}), 400

        # Obtener el vector correspondiente al ID de la base de datos (esto depende de cómo esté almacenado en OpenSearch)
        query_vector = get_vector_by_id(query_id)  # Función para obtener el vector correspondiente al ID

        if query_vector is None:
            return jsonify({"error": "El ID proporcionado no existe en la base de datos"}), 404

        # Realizar la búsqueda KNN en OpenSearch usando el vector y K
        response = client.search(
            index="embedding_index",
            body={
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_vector,
                            "k": k
                        }
                    }
                }
            }
        )

        # Extraer los resultados
        results = [{"id": hit["_id"], "score": hit["_score"], "vector": hit["_source"]["embedding"]} for hit in response["hits"]["hits"]]
        
        return jsonify({"results": results}), 200
    
    except Exception as e:
        print("Error en la búsqueda:", str(e))
        return jsonify({"error": str(e)}), 500
