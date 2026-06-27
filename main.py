import streamlit as st
import pickle
import pandas as pd
import requests

OMDB_API_KEY = 'be90f836'
def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            return data.get("Poster")
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/300x450?text=Network+Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_name = movies.iloc[i[0]].title

        recommended_movies.append(movie_name)

        recommended_movies_posters.append(fetch_poster(movie_name))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])