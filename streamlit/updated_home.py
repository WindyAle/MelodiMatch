import streamlit as st
import pandas as pd
import pickle
import re
import os
import sys
from streamlit.components.v1 import iframe

# --- 경로 설정 및 모듈 임포트 ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code.get_reco import load_recommendation_model
from spotify_utils import get_multiple_track_details

# --- CSS 스타일 ---
# Spotify의 녹색(#1DB954)에서 검은색(#000000)으로 변하는 세로 그라데이션 배경
# 텍스트 색상은 흰색으로 지정하여 가독성 확보
page_bg_img = """
<style>
/* 메인 콘텐츠 영역 */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(to bottom, #1DB954, #000000);
}

/* 헤더 영역 (페이지 상단 여백) */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0); /* 투명하게 설정 */
}

[data-testid="stSidebar"] {
    background-color: #000000; /* 검은색 배경 적용 */
}

/* 사이드바 내부의 텍스트 색상을 흰색으로 변경 */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: white !important;
}

[data-testid="stExpander"],
[data-testid="stInfo"],
[data-testid="stSelectbox"] {
    background-color: rgba(28, 28, 28, 0.8); /* 반투명 검은색 배경 */
    border-radius: 10px; /* 둥근 모서리 */
    padding: 1rem; /* 내부 여백 */
}

/* 버튼 스타일링 */
[data-testid="stButton"] > button {
    border: 1px solid #1DB954; /* 스포티파이 녹색 테두리 */
    background-color: transparent; /* 투명 배경 */
    color: #1DB954; /* 녹색 텍스트 */
    padding: 0.5rem 1rem;
    border-radius: 20px;
    transition: all 0.2s ease-in-out; /* 부드러운 전환 효과 */
}

/* 버튼에 마우스를 올렸을 때 효과 */
[data-testid="stButton"] > button:hover {
    background-color: #1DB954; /* 녹색 배경으로 채우기 */
    color: white; /* 흰색 텍스트 */
    border: 1px solid #1DB954;
}

/* 흰색 텍스트 색상 적용 (가독성 향상) */
h1, h2, h3, h4, h5, h6, p, li, .st-emotion-cache-1kyxreq, .st-emotion-cache-1y4p8pa {
    color: white !important;
}

</style>
"""



    # border: 1px solid rgba(255, 255, 255, 0.1); /* 희미한 흰색 테두리 */

# CSS를 앱에 적용
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎵 MelodiMatch - 당신의 취향 저격 음악",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 데이터 및 모델 로드 ---
@st.cache_data
def load_data():
    # get_reco.py의 함수를 사용하여 기본 모델/데이터 로드
    knn_model, preprocessor, df, model_available = load_recommendation_model()
    if not model_available:
        st.error("모델 또는 데이터 파일을 찾을 수 없습니다. `ml/recommendation.py`를 실행하여 모델을 먼저 생성해주세요.")
        st.stop()

    # 추가적으로 feature_info.pkl 로드 (개선된 추천 로직에 필요)
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    try:
        with open(os.path.join(data_path, 'feature_info.pkl'), 'rb') as f:
            feature_info = pickle.load(f)
    except FileNotFoundError:
        st.error("`feature_info.pkl` 파일을 찾을 수 없습니다. `ml/recommendation.py`를 다시 실행해주세요.")
        st.stop()
    
    df = df[df['track_id'].notna()]
    return knn_model, preprocessor, df, feature_info

knn_model, preprocessor, df, feature_info = load_data()

# --- API 정보 캐싱 ---
@st.cache_data(show_spinner=False)
def fetch_spotify_data(track_ids):
    return get_multiple_track_details(track_ids)

# --- 추천 로직 ---
def get_recommendations(selected_index, n_recommendations):
    with st.status("🎶 당신의 취향을 분석하고 있어요..."):
        st.write("선택한 곡의 특징을 추출 중... ✨")
        song_features = df.loc[[selected_index]][feature_info['all']]
        song_features_transformed = preprocessor.transform(song_features)
        
        st.write("비슷한 곡들을 찾고 있어요... 🕵️‍♀️")
        n_candidates = min(100, len(df) - 1)
        distances, indices = knn_model.kneighbors(song_features_transformed, n_neighbors=n_candidates + 1)
        
        # 자기 자신을 제외한 이웃 인덱스
        neighbor_indices = indices.flatten()[1:] 
        
        st.write("추천 목록을 완성하는 중... 🎁")
        
        # 추천 후보 목록에서 원본 곡과 관련된 곡들 제외
        original_song = df.loc[selected_index]
        original_song_title = original_song['track_name'].lower()
        original_song_artists = original_song['artist_name'].lower()

        candidates_df = df.loc[neighbor_indices]

        # 조건 1: 곡 제목이 원본 곡 제목을 포함하는가?
        title_match = candidates_df['track_name'].str.lower().str.contains(original_song_title, na=False)
        # 조건 2: 아티스트 이름이 원본 곡 아티스트를 포함하는가?
        artist_match = candidates_df['artist_name'].str.lower().str.contains(original_song_artists, na=False)

        # 두 조건이 모두 참인 경우(즉, 제외 대상)를 제외하고 필터링
        filtered_candidates = candidates_df[~(title_match & artist_match)]
        
        # 필터링된 결과에서 n_recommendations 개수만큼 선택
        st.session_state.recommendation_indices = filtered_candidates.head(n_recommendations).index.tolist()
        st.session_state.show_recommendations = True

# --- 세션 상태 관리 ---
def init_session_state():
    defaults = {
        'search_query': "", 'matching_songs_df': None, 'selected_track_index': None,
        'recommendation_indices': None, 'show_recommendations': False, 'spotify_player_url': None
    }
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value

init_session_state()

# --- UI ---
st.title("MelodiMatch")
st.markdown("##### _Spotify 기반 음악 추천 시스템_ ")
st.divider()

# --- 사이드바 ---
with st.sidebar:
    st.header("노래 검색")
    st.markdown("추천받고 싶은 노래 제목을 입력하세요.")
    user_input = st.text_input("노래 제목:", placeholder="예: Circles", value=st.session_state.search_query, key="search_input", label_visibility="collapsed")
    n_recommendations = st.slider("추천 개수", 5, 30, 10, 1)

    if st.button("추천 찾기", use_container_width=True, type="primary"):
        for key in st.session_state.keys():
            if key not in ['search_query', 'search_input']: st.session_state[key] = None
        init_session_state()
        st.session_state.search_query = user_input
        if user_input:
            matching_songs_df = df[df['track_name'].str.lower() == user_input.lower()].copy()
            st.session_state.matching_songs_df = matching_songs_df if not matching_songs_df.empty else None
            if st.session_state.matching_songs_df is None:
                st.warning("검색된 노래가 없습니다. 다른 제목으로 시도해보세요.")
        st.rerun()

# --- 메인 화면 ---

# 1. 검색 결과 표시 및 선택
if st.session_state.matching_songs_df is not None and not st.session_state.show_recommendations:
    st.subheader(f"'{st.session_state.search_query}' 검색 결과")
    st.markdown("당신이 검색한 노래를 선택해주세요.")
    match_ids = st.session_state.matching_songs_df['track_id'].tolist()
    match_details = fetch_spotify_data(match_ids)
    valid_matches = [(idx, details) for idx, details in zip(st.session_state.matching_songs_df.index, match_details) if details]
    
    if not valid_matches:
        st.error("Spotify API에서 검색 결과에 대한 정보를 가져올 수 없습니다.")
    else:
        option_labels = [f"{d['name']} - {d['artists']} ({d['release_year']})" for _, d in valid_matches]
        selected_label = st.radio("버전 선택:", option_labels, key="song_choice_radio")
        if st.button("이 노래로 추천받기", use_container_width=True):
            selected_idx = option_labels.index(selected_label)
            st.session_state.selected_track_index = valid_matches[selected_idx][0]
            get_recommendations(st.session_state.selected_track_index, n_recommendations)
            st.rerun()

# 2. 추천 결과 표시
if st.session_state.show_recommendations:
    main_col, player_col = st.columns([1.5, 1])
    with main_col:
        # 사용자가 입력한 곡 정보
        selected_song_details = fetch_spotify_data([df.loc[st.session_state.selected_track_index]['track_id']])[0]
        if selected_song_details:
            c1, c2 = st.columns([1, 4])
            with c1:
                st.image(selected_song_details['album_cover_url'] or "")
            with c2:
                st.markdown(f"## **{selected_song_details['name']}**")
                st.markdown(f"### *{selected_song_details['artists']}*", unsafe_allow_html=True)
                st.session_state.spotify_player_url = f"https://open.spotify.com/embed/track/{selected_song_details['id']}"
            
            st.divider()

        # 입력 곡 기반 추천곡
        st.subheader("당신을 위한 추천")
        rec_indices = st.session_state.recommendation_indices
        recommended_df = df.loc[rec_indices]
        rec_track_ids = recommended_df['track_id'].tolist()
        rec_details_list = fetch_spotify_data(rec_track_ids)

        for details in rec_details_list:
            if not details: continue
            expander_title = f"**{details['name']}** :gray[by *{details['artists']}*]"
            with st.expander(expander_title, expanded=False):
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1: st.image(details['album_cover_url'] or "")
                with c2:
                    st.markdown(f"**앨범:** {details['name']}")
                    st.markdown(f"**발매:** {details['release_year']}")
                with c3:
                    if st.button("▶️ 재생", key=f"play_rec_{details['id']}", use_container_width=True):
                        st.session_state.spotify_player_url = f"https://open.spotify.com/embed/track/{details['id']}"
                        st.rerun()
    
    with player_col:
        if st.session_state.spotify_player_url:
            iframe(st.session_state.spotify_player_url, height=360)
        else:
            st.info("재생(▶️) 버튼을 눌러 Spotify 플레이어를 실행하세요.")

# 3. 초기 화면
if st.session_state.matching_songs_df is None and not st.session_state.show_recommendations:
    st.info("⬅️ 좋아하는 노래를 검색하고 새로운 음악을 추천받으세요!")