# %%
from opensearchpy import Field, Document, Keyword, Text, Date
from opensearchpy import OpenSearch
import numpy as np
import pandas as pd
import datetime

# %%
df_movies = pd.read_csv('../../data/peliculas.csv')
df_users = pd.read_csv('../../data/usuarios.csv')
movie_embeddings_matrix = np.load('../../vectors/movie_embeddings_matrix.npy')
user_embeddings_matrix = np.load('../../vectors/user_embeddings_matrix.npy')
user2Idx = np.load('../../vectors/user2Idx.npy', allow_pickle=True).item()
movie2Idx = np.load('../../vectors/movie2Idx.npy', allow_pickle=True).item()
# %%
movie_embeddings_matrix[2]

# %%
df_users['userIdx'] = df_users['id'].apply(lambda x: user2Idx[x])
df_movies['movieIdx'] = df_movies['id'].apply(lambda x: movie2Idx[x])
movie_embeddings_matrix.shape[1],user_embeddings_matrix.shape[1]
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
client.cluster.health()
# %%
client.indices.delete('movie')
# %%
class KNNVector(Field):
    name = "knn_vector"
    def __init__(self, dimension, method, **kwargs):
        super(KNNVector, self).__init__(dimension=dimension, method=method, **kwargs)

method = {
    "name": "hnsw",
    "space_type": "cosinesimil",
    "engine": "nmslib"
}

# %%
index_name = 'movie'
class Movie(Document):
    movie_id = Keyword()
    name = Text()
    created_at = Date()

    vector = KNNVector(
        movie_embeddings_matrix.shape[1],
        method
    )
    class Index:
        name = index_name
        settings = {
                'index': {
                'knn': True
            }
        }

    def save(self, ** kwargs):
        self.meta.id = self.movie_id
        return super(Movie, self).save(** kwargs)
#%%
client.indices.get(index="*")
# %%
Movie.init(using=client)
# %%
client.indices.exists('movie')
# %%
client.indices.get('movie')
# %%
for i, row in df_movies.iterrows():
    mv = Movie(
        movie_id = row.id,
        name = row['Name'],
        vector = list(movie_embeddings_matrix[row.movieIdx]),
        created_at = datetime.datetime.now()
    )
    mv.save(using=client)
# %%
Movie.search(using=client).count()
# %%
movie_idx_to_search = 5
df_movies[df_movies['id'] == movie_idx_to_search]
# %%
movie_embeddings_matrix[movie_idx_to_search]
# %%
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
# %%
for h in response['hits']['hits']:
    print(h)

# %%
