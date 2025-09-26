import pandas as pd
import spotipy
import streamlit as st

from project_mini.code.api_settings import get_api
from project_mini.ml.get_reco import get_song_recommendations

# --- Spotify API 객체 가져오기
sp = get_api()

# --- Streamlit 페이지 설정
st.set_page_config(
    page_title="🎧Hear Here",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- 페이지 타이틀
spotify_logo = "./assets/spotify_logo.png"

col_title1, col_title2 = st.columns([0.1, 0.9])
with col_title1:
    st.image(spotify_logo, width="stretch")
with col_title2:
    st.header("Spotify 기반 곡 추천기")

search_query = st.text_input(
    label="곡 제목 또는 Spotify URL을 입력하세요.",
    placeholder="ex) Dynamite 또는 https://open.spotify.com/track/..."
)

# --- 검색 시작
if search_query:
    try:
        track_id = None

        # Spotify 트랙 URL일 경우 ID 추출
        if "open.spotify.com/track/" in search_query:
            track_id = search_query.split('/')[-1].split('?')[0]
        
        # ID가 아니라면, API의 search 쿼리 호출
        if not track_id:
            results = sp.search(q=search_query, type='track', limit=1)
            if not results['tracks']['items']:
                st.error(f"'{search_query}'에 대한 검색 결과가 없습니다.")

            track_id = results['tracks']['items'][0]['id']

        # track_id를 사용하여 곡 상세 정보 가져오기
        track_info = sp.track(track_id)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(" ") # 레이아웃 정렬을 위한 빈 줄
            album_cover_url = track_info['album']['images'][0]['url']
            st.markdown(f"""
                <img src="{album_cover_url}" alt="Album Cover" 
                style="width: 100%; border-radius: 10px; 
                       box-shadow: 4px 4px 4px gray;">
                """, unsafe_allow_html=True)

        with col2:
            # 곡 제목
            st.markdown(f"## **{track_info['name']}**")

            # 아티스트
            artists = ", ".join([artist['name'] for artist in track_info['artists']])
            st.markdown(f"### *{artists}*")

            # 앨범명과 발매일
            album_name = track_info['album']['name']
            release_date = track_info['album']['release_date']

            # 재생 시간
            duration_ms = track_info['duration_ms']
            duration_s = duration_ms // 1000
            minutes = duration_s // 60
            seconds = duration_s % 60

            st.write(f"**앨범:** {album_name}")
            st.write(f"**발매일:** {release_date}")
            st.write(f"**재생 시간:** {minutes}분 {seconds}초")

        st.markdown("---") # 구분선

        # Spotify 플레이어 구현
        embed_code = f"""
            <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/track/6CFPFnS9EcLs2I0nWqtWci?utm_source=generator{track_id}?utm_source=generator" 
            width="100%"
            height="352"
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy"></iframe>
        """
        st.components.v1.html(embed_code, height=360)

        st.markdown("---") # 구분선

        # --- 이 곡과 비슷한 추천곡 보기 ---
        with st.expander("이 곡과 비슷한 추천곡 보기", expanded=True):
            with st.spinner("추천곡을 찾는 중..."):
                recommendations, error_msg = get_song_recommendations(track_info['name'], 5)
            
            if error_msg:
                st.warning(f"{error_msg}")
                st.info("추천 기능을 사용하려면 추천 모델 파일이 필요합니다. 'recommendation_logic.py' 파일을 확인해주세요.")
            elif recommendations:
                st.write("다음은 추천곡 리스트입니다:")
                # 추천곡 리스트를 보기 좋게 표시
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"**{i}. {rec['track_name']}** - *{rec.get('artist_name', '정보 없음')}*")
                    st.markdown(f"    앨범: {rec.get('album_name', '정보 없음')}")
                    if rec.get('similarity'):
                        st.markdown(f"    유사도: {rec['similarity']}")
                    st.markdown("---") # 각 추천곡 사이 구분선
            else:
                st.info("이 곡에 대한 추천곡을 찾을 수 없습니다.")

    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Spotify API 오류: {e}")
        st.info("Spotify Client ID 또는 Secret을 확인하거나, 유효한 Spotify 트랙 ID/URL을 입력해주세요.")
    except Exception as e:
        st.error(f"예기치 않은 오류가 발생했습니다: {e}")
        st.info("입력 형식이 올바른지 다시 확인해주세요.")