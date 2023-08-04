import pandas as pd
import streamlit as st
import pickle

import requests


movies_dict = pickle.load(open('Moviesdict.pkl', 'rb'))
similarmovies = pd.DataFrame(pickle.load(open('similarMovies.pkl', 'rb')))

movieslist = pd.DataFrame(movies_dict)

def Recommend(movie):
    movie_index=movieslist[movieslist['title'] == movie].index[0]
    distance = similarmovies[movie_index]
    recommendmovies=[]
    recommendedmovie_posters = []
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movie_list:
         movieID=movieslist.iloc[i[0]].movie_id
         # fetch the posters from API
         poster=fetchposter(movieID)
         recommendedmovie_posters.append(poster)
         recommendmovies.append(movieslist.iloc[i[0]].title)


    return recommendmovies,recommendedmovie_posters


def fetchposter(movieID):
    import requests

    url = "https://api.themoviedb.org/3/movie/{}?api_key=demo&language=en-US".format(movieID)

    response = requests.get(url)
    data=response.json()

    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']

st.title('Movie Recommender System')
option = st.selectbox("Select a movie", movieslist['title'].values)


if st.button('Recommend'):
    recommendmovies, recommendedmovie_posters=Recommend(option)
    col1,col2,col3,col4,col5 =st.columns(5)
    with col1:
        st.image(recommendedmovie_posters[0])
        # Using the 'markdown' function to display bold text
        st.markdown(f"**{recommendmovies[0]}**")
    with col2:
        st.image(recommendedmovie_posters[1])
        st.markdown(f"**{recommendmovies[1]}**")
    with col3:
        st.image(recommendedmovie_posters[2])
        st.markdown(f"**{recommendmovies[2]}**")
    with col4:
        st.image(recommendedmovie_posters[3])
        st.markdown(f"**{recommendmovies[3]}**")
    with col5:
        st.image(recommendedmovie_posters[4])
        st.markdown(f"**{recommendmovies[4]}**")

st.text('created by:Razia Patel')