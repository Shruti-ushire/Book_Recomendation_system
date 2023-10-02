import numpy as np
import pandas as pd
import streamlit as st
import pickle
from fuzzywuzzy import fuzz,process
from PIL import Image

df = pd.read_pickle("df.pkl")
indices = pickle.load(open("knn.pkl",'rb'))

all_books_names = list(df.title.values)

def get_index_from_name(name):
    return df[df["title"]==name].index.tolist()[0]

def print_similar_books(query=None):
    suggestion = []
    found_id = get_index_from_name(query)
    for id in indices[found_id][1:]:
        print(df.iloc[id]["title"])
        suggestion.append(df.iloc[id]["title"])
    return suggestion

def find_the_book(find):
    '''
    We need to find, whether the book that the user is searching for is in our book list or not.
    
    For this we use the fuzzywuzzy's process function, where for scoring we use the fuzz function.
    
    We limit out results to 10.
    '''
    find = str(find)
    book_list = process.extract(find,choices=all_books_names, scorer=fuzz.partial_token_sort_ratio, limit=10)
    book_list =  list(map(lambda x : x[0],book_list))
    return book_list

#########################################################################
image = Image.open('ggim.jpeg')

st.title("Shruti Ushire's")
st.markdown("## Book Recommendation System")
st.image(image)

tab1, tab2 = st.tabs(['Book Library', 'Book Recommedation'])

with tab1:
    st.markdown('**Our current library contains of _{}_ books. To make it easier for you to see if we have the book that you are searching for, you can use the below given tool to search in our library.**'.format(df['title'].nunique()))

    naam = st.text_input("Enter a book name:", "")

    possible_books = find_the_book(naam)

    with st.expander("Here are some sugesstions from our Library"):
        if possible_books:
            for i in range(len(possible_books)):
                st.markdown(f"{i + 1}. {possible_books[i]}")
    
with tab2:
    actual_book = st.number_input("Which book did you meant (provide us the book number)", min_value = 1, max_value = 10)
    actual_book = int(actual_book)

    if actual_book:
        book = possible_books[actual_book - 1]
        book = str(book)
        recommendations = print_similar_books(book)
        st.markdown("### Recommeded Books:")
        for i in range(len(recommendations)):
            st.markdown(f"{i + 1}. {recommendations[i]}")