import streamlit as st
import pickle
import requests


# Set page configuration (optional)
st.set_page_config(page_title="Netflix Movie Recommender", layout="wide")


#header
st.header("Netflix Movie Recommender")

#load the movies list for the dropdown
movies = pickle.load(open("movies_list.pkl", 'rb'))
#load the movies list for the dropdown
similarity = pickle.load(open("similarity.pkl", 'rb'))
#get the titles
movies_list=movies['title'].values
#create a dropdown
selected_movie = st.selectbox("Select a movie from the dropdown", movies_list)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=*********"
    data=requests.get(url)
    print("Response:", data) 
    data=data.json()
    poster_path=data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#main recommender function
def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key=lambda vector: vector[1])
    recommend_movies=[]
    recommend_poster=[]
    #we want to recomend top 5 similar movies
    for i in distances[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movies, recommend_poster

if st.button("Show similar movies"):
    movie_name, movie_poster = recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
   





