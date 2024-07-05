# In[1]
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# In[2]
Anime_data = pd.read_csv("C:/Users/Aabed's PC/Downloads/anime.csv")
Anime_data.head()

ratings = pd.read_csv("C:/Users/Aabed's PC/Downloads/rating.csv")
ratings.head()

Anime_data.info()
ratings.info()

Anime_data[Anime_data.columns].isnull().sum()
ratings[ratings.columns].isnull().sum()

New_Anime_data = Anime_data.dropna()
New_Anime_data[New_Anime_data.columns].isnull().sum()

ratings = ratings.dropna()
ratings[ratings.columns].isnull().sum()

New_Anime_data.duplicated().sum()
ratings.duplicated().sum()

New_Anime_data = New_Anime_data.sort_values(by = ["members","rating"] ,ascending=False)
New_Anime_data.head(10)

New_Anime_data.info()

New_Anime_data["genre"].head(10)


genres = []
for i in New_Anime_data["genre"]:
    for j in i.split(', '):
        genres.append(j)
genres = pd.unique(genres)
genres = sorted(genres[0:42])
print(genres, "\n number of geners :",len(genres))



types = []
for i in New_Anime_data["type"]:
    types.append(i)
types = sorted(pd.unique(types))
print(types , "\n number of types :",len(types))


tdif = TfidfVectorizer()
tdif_matrix = tdif.fit_transform(New_Anime_data["genre"])
tdif_matrix.shape
cosine_sim = linear_kernel(tdif_matrix, tdif_matrix)
indices = pd.Series(New_Anime_data.index, index = New_Anime_data["name"]).drop_duplicates()

def get_recommendations(name , cosine_sim = cosine_sim):
    idx = indices[name]
    sim_scores = enumerate(cosine_sim[idx])
    sim_scores = sorted(sim_scores, key=lambda X: X[1], reverse=True)
    sim_scores = sim_scores[1:11]
    anime_indices = [i[0] for i in sim_scores]
    print(New_Anime_data["name"].iloc[anime_indices])
    
# In[3]
get_recommendations("Black Clover")

# In[4]
n_ratings = len(ratings)
n_anime = len(ratings['anime_id'].unique())
n_users = len(ratings['user_id'].unique())

print(f"Number of ratings: {n_ratings}")
print(f"Number of unique anime_id's: {n_anime}")
print(f"Number of unique users: {n_users}")
print(f"Average ratings per user: {round(n_ratings/n_users, 2)}")
print(f"Average ratings per anime: {round(n_ratings/n_anime, 2)}")
# In[6]
user_freq = ratings[['user_id', 'anime_id']].groupby(
    'user_id').count().reset_index()
user_freq.columns = ['user_id', 'n_ratings']
user_freq.head()


# Find Lowest and Highest rated anime:
mean_rating = ratings.groupby('anime_id')[['rating']].mean()
mean_rating
# Lowest rated anime
lowest_rated = mean_rating['rating'].idxmin()
New_Anime_data.loc[New_Anime_data['anime_id'] == lowest_rated]
# Highest rated anime
highest_rated = mean_rating['rating'].idxmax()
New_Anime_data.loc[New_Anime_data['anime_id'] == highest_rated]
# show number of people who rated anime rated anime highest
ratings[ratings['anime_id'] == highest_rated]
# show number of people who rated anime rated anime lowest
ratings[ratings['anime_id'] == lowest_rated]

# the above anime has very low dataset. We will use bayesian average
anime_stats = ratings.groupby('anime_id')[['rating']].agg(['count', 'mean'])
anime_stats.columns = anime_stats.columns.droplevel()

# Now, we create user-item matrix using scipy csr matrix


def create_matrix(df):

    N = len(df['user_id'].unique())
    M = len(df['anime_id'].unique())

    # Map Ids to indices
    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    anime_mapper = dict(zip(np.unique(df["anime_id"]), list(range(M))))

    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    anime_inv_mapper = dict(zip(list(range(M)), np.unique(df["anime_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    anime_index = [anime_mapper[i] for i in df['anime_id']]

    X = csr_matrix((df["rating"], (anime_index, user_index)), shape=(M, N))

    return X, user_mapper, anime_mapper, user_inv_mapper, anime_inv_mapper


X, user_mapper, anime_mapper, user_inv_mapper, anime_inv_mapper = create_matrix(
    ratings)

"""
Find similar anime using KNN
"""


def find_similar_anime(anime_id, X, k, metric='cosine', show_distance=False):

    neighbour_ids = []

    anime_ind = anime_mapper[anime_id]
    anime_vec = X[anime_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    anime_vec = anime_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(anime_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(anime_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids

# In[7]
anime_names = dict(zip(New_Anime_data['anime_id'], New_Anime_data['name']))

anime_id = 33950
similar_ids = find_similar_anime(anime_id, X, k=10)
anime_name = anime_names[anime_id]

print(f"Since you watched {anime_name}")
for i in similar_ids:
    print(anime_names[i])