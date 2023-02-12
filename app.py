import streamlit as st
import pandas as pd
import requests

movies_list = pd.read_pickle('movies.pkl')
similarity = pd.read_pickle('similarity.pkl')
movies = movies_list['title'].values

def fetch_poster(movie_id):
    print("The movie id is --- ",movie_id)
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d8332cd45460e0024e48795b998655db&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    top_movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []

    for movie in top_movies_list:
        movie_id = movies_list.iloc[movie[0]].movie_id

        recommended_movies.append(movies_list.iloc[movie[0]].title)

        #Fetching the poster of the movie from an API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

st.title('My Movie Recommendor System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies)

if st.button('Recommend'):
    recommendations,posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])