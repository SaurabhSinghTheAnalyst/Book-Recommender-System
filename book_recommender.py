# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset (e.g., Book-Crossings dataset)
books = pd.read_csv("goodreads_data.csv")

# Preprocess the data (remove duplicates, handle missing values, etc.)

# Fill NaN values in the 'Description' column with an empty string
books['Description'] = books['Description'].fillna('')

# Create a TF-IDF Vectorizer object
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books['Description'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get book recommendations based on book title
def get_recommendations(book_title, cosine_sim=cosine_sim, data=books):
    # Check if the book title exists in the dataset
    if book_title not in data['Book'].values:
        return "Book title not found in the dataset"
    
    # Get the index of the book that matches the title
    idx = data[data['Book'] == book_title].index
    if len(idx) == 0:
        return "Book title not found in the dataset"
    
    idx = idx[0]  # Get the first index if multiple matches
    
    # Get the pairwise similarity scores with that book
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top 10 most similar books
    sim_scores = sim_scores[1:11]
    
    # Get the book indices
    book_indices = [i[0] for i in sim_scores]
    
    # Return the top 10 recommended books
    return data['Book'].iloc[book_indices]

# Streamlit App to host the Book Recommender System
def main():
    st.title("Book Recommender System")
    
    # Sidebar to input book title
    book_title = st.sidebar.text_input("Enter a Book Title")
    
    if st.sidebar.button("Recommend"):
        if book_title:
            recommended_books = get_recommendations(book_title)
            st.subheader("Recommended Books:")
            for i, book in enumerate(recommended_books):
                st.write(f"{i+1}. {book}")
        else:
            st.write("Please enter a valid book title.")

if __name__ == '__main__':
    main()