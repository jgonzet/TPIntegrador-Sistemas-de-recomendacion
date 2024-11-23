import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import numpy as np 
from datetime import datetime
from matplotlib import pyplot as plt

import helper

class Pelicula:
    '''Esta es la clase pelicula
    Tiene los atributos: nombre(string), anio, generos (lista de strings), id(opcional)'''
    def __init__(self, nombre, anio, generos, id = None):
        self.nombre = nombre
        self.anio = anio
        self.generos = generos
        self.id = id

    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        output = f"Nombre: {self.nombre}\nAño: {self.anio}\nGenero: {self.generos}"
        return output    

    def write_df(self, df_mov):
        # Este método recibe el dataframe de películas y agrega la película
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.
        if self.id in df_mov["id"].values: return -1        
        if self.id is None: self.id = df_mov["id"].max() + 1 if not df_mov.empty else 1  
        new_row = helper.parse_movie(self, df_mov)      #todo/ validar posible error
        df_mov.loc[len(df_mov)] = new_row   
        return df_mov

    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su estructura 
        # y devuelve un DataFrame con la información cargada del archivo 'filename'.        
        try:
            df = pd.read_csv(filename)            
            if (df.columns.tolist() !=  helper.get_movies_structure()):                
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")
            df = df.dropna()
            return df        
        except Exception as e:
            print(f"Error al procesar el archivo CSV '{filename}': {str(e)}")
            return None

    @classmethod
    def get_from_df(cls, df_mov, id=None, nombre=None, anios=None, generos=None):
        # Este class method devuelve una lista de objetos 'Pelicula' buscando por:
        # id, nombre, anios: [desde_año, hasta_año], generos: [generos]
        mask = helper.get_df_from_df(df_mov,id=id,nombre=nombre,anios=anios,generos=generos)
        peliculas = []
        for index, row in mask.iterrows():
            pelicula = cls(id=row['id'], nombre = row["Name"],anio=helper.get_year_from_df(row['Release Date']), generos = helper.gen_from_one_hot(row))
            peliculas.append(pelicula)        
        return peliculas
    
    @classmethod
    def get_stats(cls, df_mov, anios=None, generos=None):
        # Este class method imprime una serie de estadísticas calculadas sobre
        # los resultados de una consulta al DataFrame df_mov. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # anios: [desde_año, hasta_año]
        # generos: [generos]
        # Las estadísticas son:
        # - Datos película más vieja
        # - Datos película más nueva
        # - Bar plots con la cantidad de películas por año/género.
        movies_selected = helper.get_df_from_df(df_mov,anios=anios,generos=generos)
        print(movies_selected["Release Date"].iloc[0])
        movies_selected["Fecha"] = movies_selected["Release Date"].apply(lambda x:datetime.strptime(x,"%d-%b-%Y"))
        movies_selected["Anio"] = movies_selected["Release Date"].apply(lambda x: int(x[-4:]))
        movies_selected = movies_selected.reset_index(drop=True)        
        # pelicula_mas_vieja
        row = movies_selected.iloc[movies_selected["Fecha"].idxmin()]
        print("Película más vieja:")
        pelicula_mas_vieja = cls(id=row['id'], nombre = row["Name"],anio=helper.get_year_from_df(row['Release Date']), generos = helper.gen_from_one_hot(row))
        print(pelicula_mas_vieja)        
        # pelicula_mas_vieja
        row = movies_selected.iloc[movies_selected["Fecha"].idxmax()]
        print("Película más nueva:")
        pelicula_mas_nueva = cls(id=row['id'], nombre = row["Name"],anio=helper.get_year_from_df(row['Release Date']), generos = helper.gen_from_one_hot(row))
        print(pelicula_mas_nueva)        
        #grafico de generos
        plt.figure(figsize=(10, 6))
        conteo_generos = movies_selected[helper.get_gens()].sum()
        conteo_generos.plot(kind='bar')
        plt.title('Cantidad de películas por genero')
        plt.xlabel('Genero')
        plt.ylabel('Cantidad de películas')
        plt.show()
        #grafico de anios
        plt.figure(figsize=(10, 6))
        movies_selected['Anio'].value_counts().sort_index().plot(kind='bar')
        plt.title('Cantidad de películas por año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de películas')
        plt.show()
        
    def remove_from_df(self, df_mov):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error
        new_row = helper.parse_movie(self, df_mov)      #todo/ validar posible error
        df_new_row = pd.DataFrame(columns=df_mov.columns)
        df_new_row.loc[0] = new_row
        if(((df_mov == df_new_row.iloc[0]).all(axis=1)).any()):
            index_to_drop = df_mov[(df_mov == df_new_row.iloc[0]).all(axis=1)].index
            df_mov.drop(index_to_drop, inplace=True)
            print("La pelicula ha sido eliminada con exito")
        else: print("La pelicula no existe en la DB.")


##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

class Usuario:
    def __init__(self, ocupacion, fecha_alta, id = None):
        self.ocupacion = ocupacion
        self.fecha_alta = fecha_alta
        self.id = id

    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        output = f"ID: {self.id}\nOcupacion: {self.ocupacion}\nFecha de alta: {self.fecha_alta}"
        return output    

    def write_df(self, df_usr):
        # Este método recibe el dataframe de usuarios y agrega al usuario
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.
        print(self.id)
        if self.id in df_usr["id"].values: return -1        
        if self.id is None: self.id = df_usr["id"].max() + 1
        new_row = [self.id,self.ocupacion,self.fecha_alta]     
        df_usr.loc[len(df_usr)] = new_row   
        return df_usr
    
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su estructura 
        # y devuelve un DataFrame con la información cargada del archivo 'filename'.        
        try:
            df = pd.read_csv(filename)            
            if (df.columns.tolist() !=  helper.get_users_structure()):                
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")
            return df        
        except Exception as e:
            print(f"Error al procesar el archivo CSV '{filename}': {str(e)}")
            return None

    @classmethod
    def get_from_df(cls, df_usr, id = None, ocupaciones=None , fechas=None):
        # Este class method devuelve una lista de objetos 'Usuario' buscando por:
        # id, nombre, anios: [desde_fecha, hasta_fecha], ocupacion: [ocupaciones]
        if fechas is not None:
            fechas_dt = list ( map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),fechas))
            mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones,fechas=fechas_dt)
        else: mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones)        
        usuarios = []
        for index, row in mask.iterrows():
            user = cls(id=row['id'], ocupacion = row["Occupation"], fecha_alta=row['Active Since'])
            usuarios.append(user)        
        return usuarios
    
    @classmethod
    def df_filter(cls,df_usr, id=None, fechas=None,ocupaciones=None):
        mask = df_usr.copy()
        if id is not None:
            mask = mask[mask['id'] == id]
        if fechas is not None:
            mask = mask[(mask['Active Since'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))>= fechas[0]) & (mask['Active Since'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S')) <= fechas[1])]        
        if ocupaciones is not None:
            mask = mask[mask['Occupation'].isin(ocupaciones)]
        return mask

    @classmethod
    def get_stats(cls, df_usr, fechas=None, ocupaciones=None):
        # Este class method imprime una serie de estadísticas calculadas sobre los resultados de una consulta al DataFrame df_usr. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # fechas: [desde_fecha, hasta_fecha]
        # ocupacion: [ocupaciones]
        # Las estadísticas son:
        # - Datos usuario más viejo
        # - Datos usuario más nuevo
        # - Bar plots con la cantidad de usuarios por anio/ocupacion.
        if fechas is not None:
            fechas_dt = list ( map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),fechas))            
            mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones,fechas=fechas_dt)
        else: mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones)

        mask["Active Since"] = mask["Active Since"].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        mask = mask.reset_index(drop=True)

        # user mas viejo
        row = mask.iloc[mask["Active Since"].idxmin()]
        print("Usuario más viejo: ")
        older_user = cls(id=row['id'], ocupacion=row["Occupation"], fecha_alta=row["Active Since"])
        print(older_user)        
        # user mas nuevo
        row = mask.iloc[mask["Active Since"].idxmax()]
        print("Usuario más nuevo: ")
        last_user = cls(id=row['id'], ocupacion=row["Occupation"], fecha_alta=row["Active Since"])
        print(last_user)    
        #grafico de generos
        conteo = mask['Occupation'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de usuarios por Ocupacion')
        plt.xlabel('Ocupaciones')
        plt.ylabel('Cantidad de Usuarios')
        plt.show()

        #grafico de anios
        mask["anio"] = mask["Active Since"].apply(lambda x: x.year)
        conteo = mask['anio'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de usuarios por año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de Usuarios')
        plt.show()

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

class Persona: #id,Full Name,year of birth,Gender,Zip Code
    def __init__(self, full_name, year_birth, gender, zip_code,id = None):
        self.name = full_name
        self.birth_year = year_birth
        self.gender = gender
        self.zip_code = zip_code
        self.id = id

    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        output = f"ID: {self.id}\nNombre completo: {self.name}\nAnio nacimiento: {self.birth_year}\nGenero:{self.gender}\nCod.Postal:{self.zip_code}"
        return output    

    def write_df(self, df_ppl):
        # Este método recibe el dataframe de usuarios y agrega al usuario
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.
        if self.id in df_ppl["id"].values: return -1        
        if self.id is None: self.id = df_ppl["id"].max() + 1  
        new_row = [self.id,self.name,self.birth_year,self.gender,self.zip_code]  
        df_ppl.loc[len(df_ppl)] = new_row   
        return df_ppl
    
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su estructura 
        # y devuelve un DataFrame con la información cargada del archivo 'filename'.        
        try:
            df = pd.read_csv(filename)
            if (df.columns.tolist() !=  helper.get_pple_structure()):                
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")
            return df        
        except Exception as e:
            print(f"Error al procesar el archivo CSV '{filename}': {str(e)}")
            return None

    @classmethod
    def df_filter(cls,df_ppl,name=None, years=None, gender=None, zip_code=None,id = None):
        mask = df_ppl.copy()
        if id is not None:
            mask = mask[mask['id'] == id]
        if gender is not None:
            mask = mask[mask['Gender'] == gender]
        if zip_code is not None:
            mask = mask[mask['Zip Code'].apply(lambda x:int(x))== zip_code]
        if years is not None:
            mask = mask[(mask['year of birth'].apply(lambda x: int(x))>= years[0]) & (mask['year of birth'].apply(lambda x: int(x))<= years[1])]
        if name is not None:
           mask = mask[mask['Full Name'].str.contains(name)]        
        return mask

    @classmethod
    def get_from_df(cls, df_ppl, nombre=None, years=None, gender=None, zip_code=None,id = None):
        # Este class method devuelve una lista de objetos 'Persona' buscando por: id, anios, genero, cod.postal        
        mask = Persona.df_filter(df_ppl,name=nombre,years=years,gender=gender,zip_code=zip_code,id=id)        
        personas = []
        for index, row in mask.iterrows():
            persona = cls(full_name = row["Full Name"],
                          id = row["id"],
                          year_birth=row["year of birth"],
                          zip_code=row["Zip Code"],
                          gender=row["Gender"])
            personas.append(persona)        
        return personas

    @classmethod
    def get_stats(cls, df_ppl, years=None, gender=None):
        # Este class method imprime una serie de estadísticas calculadas sobre los resultados de una consulta al DataFrame df_ppl. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # fechas: [desde_anio, hasta_anio]
        # genero
        # Las estadísticas son: - Bar plots con la cantidad de usuarios por anios/generos.
        mask = Persona.df_filter(df_ppl,years=years,gender=gender)
        mask = mask.reset_index(drop=True)

        #grafico por Genero
        conteo = mask['Gender'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de personas por genero')
        plt.xlabel('Genero')
        plt.ylabel('Cantidad de personas')
        plt.show()

        #grafico de anios
        conteo = mask['year of birth'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de personas por año de nacimiento')
        plt.xlabel('Año de nacimiento')
        plt.ylabel('Cantidad de personas')
        plt.show()

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

class Trabajador: #id,Position,Category,Working Hours,Start Date
    def __init__(self, position, category, working_hours, start_date,id = None):
        self.position = position
        self.category = category
        self.working_hours = working_hours
        self.start_date = start_date
        self.id = id

    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        output = f"ID: {self.id}\nPosicion: {self.position}\nCategoria: {self.category}\nHorario trabajo: {self.working_hours}\nFecha de comienzo: {self.start_date}"
        return output    

    def write_df(self, df_wkr):
        # Este método recibe el dataframe de usuarios y agrega al usuario
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el 
        # id ya existe, no la agrega y devuelve un error.
        if self.id in df_wkr["id"].values: return -1        
        if self.id is None: self.id = df_wkr["id"].max() + 1 if not df_wkr.empty else 1  
        new_row = [self.id,self.position,self.category,self.working_hours,self.start_date]  
        df_wkr.loc[len(df_wkr)] = new_row   
        return df_wkr
    
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su estructura 
        # y devuelve un DataFrame con la información cargada del archivo 'filename'.        
        try:
            df = pd.read_csv(filename)
            if (df.columns.tolist() !=  helper.get_worker_structure()):                
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")
            return df        
        except Exception as e:
            print(f"Error al procesar el archivo CSV '{filename}': {str(e)}")
            return None
    
    @classmethod
    def df_filter(cls,df_wkr,position=None, category=None, working_hours=None, start_date=None,id = None):
        mask = df_wkr.copy()
        if id is not None:
            mask = mask[mask['id'] == id]
        if position is not None:
            mask = mask[mask['Position'] == position]
        if category is not None:
            mask = mask[mask['Category']== category]
        if start_date is not None:
            mask = mask[(mask['Start Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))>= start_date[0]) & (mask['Start Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))<= start_date[1])]
        if working_hours is not None:
           mask = mask[mask['Working Hours']==working_hours]
        
        return mask

    @classmethod
    def get_from_df(cls, df_wkr, position=None, category=None, working_hours=None, start_date=None,id = None):
        # Este class method devuelve una lista de objetos 'Persona' buscando por: id, anios, genero, cod.postal        
        mask = Trabajador.df_filter(df_wkr,position=position, category=category, working_hours=working_hours, start_date=start_date,id=id)
        trabajadores = []
        for index, row in mask.iterrows():
            trabajador = cls(position = row["Position"],
                          category = row["Category"],
                          working_hours=row["Working Hours"],
                          start_date=row["Start Date"],
                          id=row["id"])
            trabajadores.append(trabajador)        
        return trabajadores
    

    @classmethod
    def get_stats(cls,  df_wkr, position=None, category=None, working_hours=None, start_date=None,id = None):
        # Este class method imprime una serie de estadísticas calculadas sobre los resultados de una consulta al DataFrame df_usr. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # fechas: [desde_fecha, hasta_fecha]
        # ocupacion: [ocupaciones]
        # Las estadísticas son:
        # - Datos usuario más viejo
        # - Datos usuario más nuevo
        # - Bar plots con la cantidad de usuarios por anio/ocupacion.
        mask = Trabajador.df_filter(df_wkr,position=position, category=category, working_hours=working_hours, start_date=start_date,id=id)

        mask["Start Date"] = mask["Start Date"].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
        mask = mask.reset_index(drop=True)

        # worker mas viejo
        row = mask.iloc[mask["Start Date"].idxmin()]
        print("Trabajador más viejo: ")
        older_worker = cls(position = row["Position"],category = row["Category"],working_hours=row["Working Hours"],start_date=row["Start Date"],id=row["id"])
        print(older_worker)        
        # worker mas viejo
        row = mask.iloc[mask["Start Date"].idxmax()]
        print("Trabajador más nuevo: ")
        last_worker = cls(position = row["Position"],category = row["Category"],working_hours=row["Working Hours"],start_date=row["Start Date"],id=row["id"])
        print(last_worker)        
       
        # #grafico de posiciones
        conteo = mask['Position'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de trabajadores por Posicion')
        plt.xlabel('Posicion')
        plt.ylabel('Cantidad de trabajadores')
        plt.show()

        #grafico de categoria
        conteo = mask['Category'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de trabajadores por categoria')
        plt.xlabel('Categoria')
        plt.ylabel('Cantidad de trabajadores')
        plt.show()

        #grafico de turnos horarios
        conteo = mask['Working Hours'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de trabajadores por turno horario')
        plt.xlabel('Turno Horario')
        plt.ylabel('Cantidad de trabajadores')
        plt.show()

        #Grafico por anio de ingreso
        mask["anio"] = mask["Start Date"].apply(lambda x: x.year)
        conteo = mask['anio'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de trabajadores por año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de trabajadores')
        plt.show()

##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

class Score: #,user_id,movie_id,rating,Date
    def __init__(self, user_id, movie_id, rating, date):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.date = date
        
    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        output = f"ID usuario: {self.user_id}\nID pelicula: {self.movie_id}\nRating: {self.rating}\nFecha: {self.date}"
        return output    

    def write_df(self, df_scores):
        # Este método recibe el dataframe de scores y agrega al score
        new_row = [self.user_id,self.movie_id,self.rating,self.date] 
        df_scores.loc[len(df_scores)] = new_row   
        return df_scores

    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su estructura 
        # y devuelve un DataFrame con la información cargada del archivo 'filename'.        
        try:
            df = pd.read_csv(filename)
            if (df.columns.tolist() !=  helper.get_score_structure()):                
                raise ValueError("El archivo CSV no contiene todas las columnas requeridas.")
            df = df[df.columns[1:]]
            return df        
        except Exception as e:
            print(f"Error al procesar el archivo CSV '{filename}': {str(e)}")
            return None
    
    @classmethod
    def df_filter(cls,df_score,user_id=None, movie_id=None, rating=None, date=None):
        mask = df_score.copy()
        if user_id is not None:
            mask = mask[mask['user_id'] == user_id]
        if movie_id is not None:
            mask = mask[mask['movie_id'] == movie_id]
        if rating is not None:
            mask = mask[mask['rating']== rating]
        if date is not None:
            mask = mask[(mask['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))>= datetime.strptime(date[0],'%Y-%m-%d %H:%M:%S')) & (mask['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))<= datetime.strptime(date[1],'%Y-%m-%d %H:%M:%S'))]
        return mask

    @classmethod
    def get_from_df(cls,df_score,user_id=None, movie_id=None, rating=None, date=None):
        # Este class method devuelve una lista de objetos 'Persona' buscando por: id, anios, genero, cod.postal        
        mask = Score.df_filter(df_score,user_id=user_id, movie_id=movie_id, rating=rating, date=date)
        puntajes = []
        for index, row in mask.iterrows():
            puntaje = cls(user_id = row["user_id"],
                          movie_id = row["movie_id"],
                          rating=row["rating"],
                          date=row["Date"])
            puntajes.append(puntaje)        
        return puntajes
    
    @classmethod
    def get_stats(cls,df_score, rating=None, date=None):
        # Este class method imprime una serie de estadísticas calculadas sobre los resultados de una consulta al DataFrame df_score. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # fechas: [desde_fecha, hasta_fecha]
        # user_id: [user_id]
        # Las estadísticas son:
        # - Datos usuario más viejo
        # - Datos usuario más nuevo
        # - Bar plots con la cantidad de usuarios por anio/ocupacion.
        mask = Score.df_filter(df_score,rating=rating, date=date)

        mask["Date"] = mask["Date"].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        mask = mask.reset_index(drop=True)

        # puntaje mas viejo
        row = mask.iloc[mask["Date"].idxmin()]
        print("Trabajador más viejo: ")
        first_score = cls(user_id = row["user_id"],movie_id = row["movie_id"],rating=row["rating"],date=row["Date"])
        print(first_score)        
        # puntaje mas nuevo
        row = mask.iloc[mask["Date"].idxmax()]
        print("Trabajador más nuevo: ")
        last_score =  cls(user_id = row["user_id"],movie_id = row["movie_id"],rating=row["rating"],date=row["Date"])
        print(last_score)        
       
        #grafico de movie_id
        conteo = mask['rating'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de peliculas por puntajes')
        plt.xlabel('Puntaje')
        plt.ylabel('Cantidad de peliculas')
        plt.show()

        #Grafico por anio del puntaje
        mask["anio"] = mask["Date"].apply(lambda x: x.year)
        conteo = mask['anio'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de scores por año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de scores')
        plt.show()


##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

class Sistema:
    def __init__(self,folder = '../Data/'):            
        self.df_movies = Pelicula.create_df_from_csv(folder+'peliculas.csv')
        self.df_scores = Score.create_df_from_csv(folder+'scores.csv')
        self.df_people = Persona.create_df_from_csv(folder+'personas.csv')
        self.df_users = Usuario.create_df_from_csv(folder+'usuarios.csv')
        self.df_employees = Trabajador.create_df_from_csv(folder+'trabajadores.csv')
    
    def alta_user(self,full_name,year_of_birth,gender,zip_code,ocupacion=None, active_since=None):
        id = self.df_people['id'].max()+1
        new_person = Persona(full_name = full_name,year_birth = year_of_birth, gender = gender, zip_code = zip_code,id=id)
        self.df_people = new_person.write_df(self.df_people)
        new_user = Usuario(ocupacion=ocupacion,fecha_alta=active_since,id=id)
        self.df_users = new_user.write_df(self.df_users)    
    def baja_user(self,id,erase_person=False):    
        self.df_users = self.df_users[self.df_users['id'] != id]
        if erase_person:
            self.df_people = self.df_people[self.df_people['id'] != id]

    def alta_empleado(self,full_name,year_of_birth,gender,zip_code,position=None, category=None,working_hours=None,start_date=None):
        id = self.df_people['id'].max()+1
        new_person = Persona(full_name = full_name,year_birth = year_of_birth, gender = gender, zip_code = zip_code,id=id)
        self.df_people = new_person.write_df(self.df_people)
        new_employee = Trabajador(position=position,category=category,working_hours=working_hours,start_date=start_date,id=id)
        self.df_employees = new_employee.write_df(self.df_employees)
    def baja_empleado(self,id,erase_person=False):
        self.df_employees = self.df_employees[self.df_employees['id'] != id]
        if erase_person:
            self.df_people = self.df_people[self.df_people['id'] != id]

    def alta_pelicula(self,nombre, anio, generos, id = None):
        new_movie = Pelicula(nombre=nombre,anio=anio,generos=generos,id=id)
        self.df_movies = new_movie.write_df(self.df_movies)
    def baja_pelicula(self,id):
        self.df_movies = self.df_movies[self.df_movies['id'] != id]

    def alta_puntaje(self, user_id, movie_id, rating, date):
        new_score = Score(user_id=user_id,movie_id=movie_id,rating=rating,date=date)
        self.df_scores = new_score.write_df(self.df_scores)
    def baja_puntaje(self,id):
        self.df_scores = self.df_scores[(self.df_scores['movie_id'] != movie_id) & (self.df_scores['user_id'] != user_id)]

    def get_stats(self,user_id=None,movie_id=None):
        #- Estadísticas por Usuario/Película: Calificación promedio de usuario, Calificación promedio por película.  
        if user_id is not None:
            user = self.df_people[self.df_people['id']==user_id].reset_index(drop=True)
            user_name = user['Full Name'].iloc[0]
            mask_scores = self.df_scores[self.df_scores['user_id']==user_id]
            print(f"Votacion promedio de {user_name}: {mask_scores['rating'].mean()}")
            
        if movie_id is not None:
            movie = self.df_movies[self.df_movies['id']==movie_id].reset_index(drop=True)
            movie_name = movie.loc[0,'Name']
            mask_scores = self.df_scores[self.df_scores['movie_id']==movie_id]
            print(f"Votacion promedio de {movie_name}: {mask_scores['rating'].mean()}")

        if ((movie_id is None) & (user_id is None)): 
            print("Completar funcion")
            # mask["Date"] = mask["Date"].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
            # mask = mask.reset_index(drop=True)

            # # puntaje mas viejo
            # row = mask.iloc[mask["Date"].idxmin()]
            # print("Trabajador más viejo: ")
            # first_score = cls(user_id = row["user_id"],movie_id = row["movie_id"],rating=row["rating"],date=row["Date"])
            # print(first_score)        
            # # puntaje mas nuevo
            # row = mask.iloc[mask["Date"].idxmax()]
            # print("Trabajador más nuevo: ")
            # last_score =  cls(user_id = row["user_id"],movie_id = row["movie_id"],rating=row["rating"],date=row["Date"])
            # print(last_score)        
        
            # #grafico de movie_id
            score_movies = self.df_scores.groupby('movie_id').agg({'rating':('count','mean')})
            print(score_movies)
            # plt.figure(figsize=(10, 6))
            # conteo.plot(kind='bar')
            # plt.title('Cantidad de peliculas por puntajes')
            # plt.xlabel('Puntaje')
            # plt.ylabel('Cantidad de peliculas')
            # plt.show()

            # #Grafico por anio del puntaje
            # mask["anio"] = mask["Date"].apply(lambda x: x.year)
            # conteo = mask['anio'].value_counts()
            # plt.figure(figsize=(10, 6))
            # conteo.plot(kind='bar')
            # plt.title('Cantidad de scores por año')
            # plt.xlabel('Año')
            # plt.ylabel('Cantidad de scores')
            # plt.show()