import pandas as pd

#importing dataset
movies = pd.read_csv('top10K-TMDB-movies.csv')

movies.describe()

movies.columns

# Feature Selection

#From the columns, what we need is: Id, title, genre, overview

#make the dataset smaller to only use the features we would need
movies = movies[['id', 'title', 'genre', 'overview']]


#let's remove the nulls to make it cleaner and more describable
movies = movies.dropna()
movies

#we want to build "Content Based" recommender system, so lets focus on overview mainly

#let's merge overview and genre in new column tags
movies['tags']= movies['overview'] + movies['genre']

#and lets drop the column overview and genre from the original dataset and create a new one
new_data = movies.drop(columns=['overview', 'genre'])
new_data

#now we need to convert the tags (text) into vector representation

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=9985, stop_words='english')

vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
vector.shape

#we need to find the similarity between the tags to base our recommendation on, so we use cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)
similarity

#now we need to access the index so our API can find the infomation about the movie
def recommend(movies):
    index = new_data[new_data['title']==movies].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key=lambda vector: vector[1])
    
    #we want to recomend top 5 similar movies
    for i in distances[0:5]:
        print(new_data.iloc[i[0]].title)
        

recommend("Avatar")

#Now lets save this so we can use in our web app!

import pickle

#create a file with movies list
pickle.dump(new_data, open('movies_list.pkl', 'wb'))


#and similarity
pickle.dump(similarity, open('similarity.pkl', 'wb'))


pickle.load(open('movies_list.pkl', 'rb'))


pickle.load(open('similarity.pkl', 'rb'))