import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import requests
import os

# Set page config
st.set_page_config(
    page_title="🎬 CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #eaeaea;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff, #0099ff, #6600ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #00d4ff;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .movie-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .movie-card:hover {
        border-color: rgba(0, 212, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(0, 212, 255, 0.5);
        transform: translateY(-5px);
    }
    
    .movie-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 0.5rem;
    }
    
    .movie-info {
        color: #b0b0b0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .recommendation-num {
        display: inline-block;
        background: linear-gradient(135deg, #00d4ff, #0099ff);
        color: white;
        font-weight: bold;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        line-height: 40px;
        text-align: center;
        margin-right: 1rem;
        font-size: 1.2rem;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        color: #eaeaea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0099ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
    }
    
    .stats-box {
        background: linear-gradient(180deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #00d4ff, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #b0b0b0;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_resource
def load_data():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths
    movie_list_path = os.path.join(script_dir, 'movie_list.pkl')
    similarity_path = os.path.join(script_dir, 'similarity.pkl')
    
    movies = pickle.load(open(movie_list_path, 'rb'))
    similarity = pickle.load(open(similarity_path, 'rb'))
    return movies, similarity

movies, similarity = load_data()

# Function to recommend movies
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    recommendations = []
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_idx = i[0]
        score = round(i[1] * 100, 2)  # Convert to percentage
        recommendations.append({
            'title': movies.iloc[movie_idx]['title'],
            'score': score,
            'genres': movies.iloc[movie_idx].get('genres', 'N/A'),
            'overview': movies.iloc[movie_idx].get('overview', 'No overview available'),
        })
    
    return recommendations

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-title">🎬 CineMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Discover Your Next Favorite Movie</div>', unsafe_allow_html=True)

# Stats Section
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stats-box">
        <div class="stats-number">{len(movies)}</div>
        <div class="stats-label">Total Movies</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-number">AI</div>
        <div class="stats-label">Powered</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-number">∞</div>
        <div class="stats-label">Possibilities</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### 🎯 Find Your Perfect Movie")
    selected_movie = st.selectbox(
        "Select a movie you like:",
        movies['title'].values,
        help="Choose a movie as a reference to get recommendations"
    )
    
    if st.button("🚀 Get Recommendations", use_container_width=True):
        if selected_movie:
            st.success(f"✓ Finding movies similar to **{selected_movie}**...")
            recommendations = recommend(selected_movie)
            
            st.markdown("### 🎥 Top Recommendations For You")
            
            for idx, movie in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="movie-card">
                    <div>
                        <span class="recommendation-num">{idx}</span>
                        <span class="movie-title">{movie['title']}</span>
                    </div>
                    <div class="movie-info">
                        <div style="margin-top: 1rem;">
                            <b style="color: #00d4ff;">Match Score:</b> 
                            <span style="color: #00ff88; font-weight: bold;">{movie['score']}%</span>
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <b style="color: #00d4ff;">Overview:</b><br>
                            {movie['overview'][:150]}...
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📌 Quick Tips")
    st.info("""
    🎬 **How it works:**
    
    1. Select a movie you enjoy
    2. Click "Get Recommendations"
    3. See similar movies ranked by match score
    
    The AI analyzes:
    - Genres
    - Keywords
    - Cast & Crew
    - Themes & Style
    """)
    
    st.markdown("### ⭐ Why CineMatch?")
    st.success("""
    ✓ Intelligent recommendations
    
    ✓ Content-based analysis
    
    ✓ Personalized for you
    
    ✓ Always discovering
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🎬 CineMatch v1.0 | Powered by Machine Learning | Made with ❤️</p>
</div>
""", unsafe_allow_html=True)

#streamlit run app.py
