import pickle
import pandas as pd
import streamlit as st

@st.cache_data
def load_recommendation_model():
    try:
        with open('./data/knn_model.pkl', 'rb') as f:
            knn_model = pickle.load(f)
        with open('./data/preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        df = pd.read_pickle('./data/processed_tracks_df.pkl')
        return knn_model, preprocessor, df, True
    except FileNotFoundError:
        return None, None, None, False
    
def get_song_recommendations(song_title, n_recommendations=5):
    knn_model, preprocessor, df, model_available = load_recommendation_model()
    
    if not model_available:
        return [], "No model"
    
    song_matches = df[df['track_name'].str.lower() == song_title.lower()]
    
    if len(song_matches) == 0:
        return [], f"'{song_title}' 곡을 찾을 수 없습니다."
    
    song_index = song_matches.index[0]
    
    # 학습에 활용할 feature 정리
    numerical_features = [
        'album_release_date', 'tempo', 'energy', 
        'danceability', 'valence', 'acousticness', 'loudness'
    ]
    categorical_features = ['key', 'mode']

    feature_cols = numerical_features + categorical_features
    
    song_features = df.iloc[[song_index]][feature_cols]
    song_features_transformed = preprocessor.transform(song_features)
    
    # KNN 모델 반환값 -> 거리와 요소
    distances, indices = knn_model.kneighbors(song_features_transformed, n_neighbors=n_recommendations + 1)
    
    recommendation_indices = indices.flatten()[1:]
    recommended_songs = []
    
    # 추천 목록 리스트화
    for idx in recommendation_indices:
        song_info = df.iloc[idx]
        recommended_songs.append({
            'track_name': song_info['track_name'],
            'artist_name': song_info.get('artist_name', 'Unknown Artist'),
            'album_name': song_info.get('album_name', 'Unknown Album'),
            'similarity': 1 - distances.flatten()[list(indices.flatten()).index(idx)]
        })
    
    return recommended_songs, None