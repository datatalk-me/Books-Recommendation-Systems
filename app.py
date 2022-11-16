# import necessary libraries
import pickle
import numpy as np
import streamlit as st

st.header('Book Recommendation System using Machine Learning')
st.subheader('This app recommends books based on the book you enter')

# load the model
pickle_in = open('artifacts/model_knn.pkl', 'rb')
model_knn= pickle.load(pickle_in)
books_name = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url


   

def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance,suggestion = model_knn.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1, -1), n_neighbors = 6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            book_list.append(j)
    return book_list , poster_url  


    

selected_book = st.selectbox(
    'Type or select a book from the dropdown',
    books_name
    )

if st.button('Show Recommendation'):
    recommended_books,poster_url = recommend_books(selected_book)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])
