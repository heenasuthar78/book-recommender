import pandas as pd
import streamlit as st

st.set_page_config(page_title="Book Recommender", page_icon="📚", layout="wide")
st.title("📚 Book Recommender")

books = pd.DataFrame([
    {"Title": "Harry Potter and the Philosopher's Stone", "Author": "J.K. Rowling", "Genre": "Fantasy", "Rating": 4.7, "About": "A boy learns he is a wizard and starts school at Hogwarts."},
    {"Title": "The Hobbit", "Author": "J.R.R. Tolkien", "Genre": "Fantasy", "Rating": 4.6, "About": "A hobbit joins a group of dwarves on a quest to win back treasure from a dragon."},
    {"Title": "And Then There Were None", "Author": "Agatha Christie", "Genre": "Mystery", "Rating": 4.6, "About": "Ten strangers on an island are killed one by one."},
    {"Title": "The Hound of the Baskervilles", "Author": "Arthur Conan Doyle", "Genre": "Mystery", "Rating": 4.4, "About": "Sherlock Holmes investigates a family curse on the moors."},
    {"Title": "Dune", "Author": "Frank Herbert", "Genre": "Science Fiction", "Rating": 4.5, "About": "A young heir fights for control of a desert planet and its precious spice."},
    {"Title": "The Martian", "Author": "Andy Weir", "Genre": "Science Fiction", "Rating": 4.6, "About": "An astronaut stranded on Mars must find a way to survive."},
    {"Title": "Atomic Habits", "Author": "James Clear", "Genre": "Self-Help", "Rating": 4.8, "About": "Small daily changes that build better habits."},
    {"Title": "Ikigai", "Author": "Hector Garcia and Francesc Miralles", "Genre": "Self-Help", "Rating": 4.2, "About": "The Japanese idea of finding your purpose in life."},
    {"Title": "Pride and Prejudice", "Author": "Jane Austen", "Genre": "Romance", "Rating": 4.6, "About": "Elizabeth Bennet and Mr. Darcy overcome pride and first impressions."},
    {"Title": "Me Before You", "Author": "Jojo Moyes", "Genre": "Romance", "Rating": 4.3, "About": "A young woman becomes a caregiver and changes both their lives."},
    {"Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Genre": "Classic", "Rating": 4.7, "About": "A lawyer defends an innocent man in a prejudiced small town."},
    {"Title": "1984", "Author": "George Orwell", "Genre": "Classic", "Rating": 4.5, "About": "Life under constant government surveillance."},
    {"Title": "Wings of Fire", "Author": "A.P.J. Abdul Kalam", "Genre": "Non-Fiction", "Rating": 4.6, "About": "The life story of India's missile man and former President."},
    {"Title": "Sapiens", "Author": "Yuval Noah Harari", "Genre": "Non-Fiction", "Rating": 4.5, "About": "A short history of how humans came to rule the world."},
])

st.sidebar.header("Find a book")
genre = st.sidebar.selectbox("Genre", ["All"] + sorted(books["Genre"].unique()))
min_rating = st.sidebar.slider("Minimum rating", 3.0, 5.0, 4.0, 0.1)
search = st.sidebar.text_input("Search title or author")
sort_by = st.sidebar.selectbox("Sort by", ["Rating", "Title"])

result = books.copy()
if genre != "All":
    result = result[result["Genre"] == genre]
result = result[result["Rating"] >= min_rating]
if search:
    mask = (
        result["Title"].str.contains(search, case=False)
        | result["Author"].str.contains(search, case=False)
    )
    result = result[mask]
result = result.sort_values(sort_by, ascending=(sort_by == "Title"))

if st.button("🎲 Surprise me!"):
    pick = books.sample(1).iloc[0]
    st.success(f"Try **{pick['Title']}** by {pick['Author']} ({pick['Genre']})")

c1, c2 = st.columns(2)
c1.metric("Books found", len(result))
c2.metric("Average rating", f"{result['Rating'].mean():.1f}" if len(result) else "-")

if result.empty:
    st.info("No books match. Try lowering the minimum rating or clearing the search.")

for _, b in result.iterrows():
    with st.container(border=True):
        st.subheader(b["Title"])
        st.caption(f"by {b['Author']} • {b['Genre']} • ⭐ {b['Rating']}")
        st.write(b["About"])