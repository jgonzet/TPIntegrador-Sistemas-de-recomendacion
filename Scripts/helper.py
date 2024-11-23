import pandas as pd

cols_df_users = ["id","Occupation","Active Since"]
cols_df_pple = ["id","Full Name","year of birth","Gender","Zip Code"]
cols_df_worker = ["id","Position","Category","Working Hours","Start Date"]
cols_df_score = ["Unnamed: 0","user_id","movie_id","rating","Date"]
cols_df_movies = ["id", "Name", "Release Date", "IMDB URL", "unknown", "Action","Adventure","Animation", "Children's", "Comedy", "Crime","Documentary", "Drama", "Fantasy", "Film-Noir","Horror", "Musical","Mystery", "Romance","Sci-Fi", "Thriller", "War", "Western"]
pos_gens = 4

def get_gens():
    return cols_df_movies[pos_gens:]

def parse_movie(pelicula, df_movies):
    new_row = [pelicula.id,pelicula.nombre,"01-Jan-"+str(pelicula.anio),"unkown URL"]
    if len(pelicula.generos) == 0: new_row.append(1)
    else: new_row.append(0)
    for gen in df_movies.columns.tolist()[5:]:
        if gen in pelicula.generos: new_row.append(1)
        else: new_row.append(0)
    return new_row

def get_movies_structure():
    return cols_df_movies
def get_users_structure():
    return cols_df_users
def get_pple_structure():
    return cols_df_pple
def get_worker_structure():
    return cols_df_worker
def get_score_structure():
    return cols_df_score

def get_year_from_df(date):
    return int(date[-4:])
def get_date_from_df(date):
    return int(date[-4:])

def get_df_from_df(df_mov,id=None,nombre=None,anios=None,generos=None):
    mask = df_mov.copy()
    if id is not None:
        mask = mask[mask['id'] == id]
    if nombre is not None:
        mask = mask[mask['Name'].str.contains(nombre)]
    if anios is not None:
        mask = mask[(mask["Release Date"].apply(get_year_from_df)>= anios[0]) & (mask['Release Date'].apply(get_year_from_df) <= anios[1])]
    if generos is not None:
        for genero in generos:
            mask = mask[mask[f'{genero}'] == 1]
    return mask

def gen_from_one_hot(serie):
    serie_aux = serie[cols_df_movies[pos_gens:]]
    return serie_aux.index[serie_aux==1].tolist()