# %%
from opensearchpy import OpenSearch
import numpy as np

# # %%
# df_movies = pd.read_csv('../../data/peliculas.csv')
# df_users = pd.read_csv('../../data/usuarios.csv')

movie_embeddings_matrix = np.load('../../vectors/movie_embeddings_matrix.npy')
user_embeddings_matrix = np.load('../../vectors/user_embeddings_matrix.npy')
user2Idx = np.load('../../vectors/user2Idx.npy', allow_pickle=True).item()
movie2Idx = np.load('../../vectors/movie2Idx.npy', allow_pickle=True).item()
# %%

host = 'localhost'
port = 9200
auth = ('admin', '@Thinkpad57!')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
)
# %%

movie_idx_to_search = 5
query = {
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
# %%
response = client.search(index='movie', body=query)

for h in response['hits']['hits']:
    print(h)

# %%
client.cluster.health()
# %%
client.indices.delete('movie')

# %%
