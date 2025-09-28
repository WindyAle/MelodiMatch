import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api():
    # API 정보 가져오기
    try:
        spotify_api = {
            'ID': os.getenv("SP_CLIENT_ID"),
            'SECRET': os.getenv("SP_CLIENT_SECRET")
        }

        # Spotify API 초기화
        client_credentials_manager = SpotifyClientCredentials(
            client_id=spotify_api['ID'],
            client_secret=spotify_api['SECRET']
        )
        
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
    except Exception as e:
        st.error(f"API 인증 중 오류가 발생했습니다: {e}")
        st.stop()
    