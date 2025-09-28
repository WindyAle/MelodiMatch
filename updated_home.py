import streamlit as st
import pandas as pd
import pickle
import re
import os
import sys
from streamlit.components.v1 import iframe
from difflib import get_close_matches

# --- 경로 설정 및 모듈 임포트 ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code.get_reco import load_recommendation_model
from spotify_utils import get_multiple_track_details

# --- CSS 스타일 ---
# 배경 검정색, 버튼 등 녹색
# 텍스트 색상은 흰색으로 지정하여 가독성 확보
page_bg_img = """
<style>
/* 메인 콘텐츠 영역 */
[data-testid="stAppViewContainer"] {
    background-color: #000000;
}

hr {
    border-top: 1px solid #555; /* Light gray for dark theme */
}

/* 헤더 영역 (페이지 상단 여백) */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0); /* 투명하게 설정 */
}

[data-testid="stSidebar"] {
    background-color: #000000; /* 검은색 배경 적용 */
    border-right: 1px solid #555; /* Light gray separator */
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

/* 펼쳐진 expander의 내용 배경을 투명하게 만듭니다 */
[data-testid="stExpander"] div[role="region"] {
    background-color: transparent !important;
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

/* 플레이어 컬럼을 스크롤에 따라 고정시킵니다 */
[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    position: sticky;
    top: 5rem;
    align-self: flex-start;
}

</style>
"""

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
        neighbor_indices = indices.flatten()[1:]
        
        st.write("추천 목록을 완성하는 중... 🎁")
        st.session_state.recommendation_indices = neighbor_indices[:n_recommendations]
        st.session_state.show_recommendations = True

# --- 세션 상태 관리 ---
def init_session_state():
    defaults = {
        'search_query': "", 'matching_songs_df': None, 'selected_track_index': None,
        'recommendation_indices': None, 'show_recommendations': False, 'spotify_player_url': None,
        'similar_matches': None
    }
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value

init_session_state()

# --- UI ---
st.title("MelodiMatch")
st.markdown("#### _Spotify 기반 음악 추천 시스템_ ")
st.divider()

# --- 사이드바 ---
with st.sidebar:
    st.header("노래 검색")
    st.markdown("추천받고 싶은 노래 제목을 입력하세요.")
    user_input = st.text_input("노래 제목:", placeholder="예: Circles", value=st.session_state.search_query, key="search_input", label_visibility="collapsed")
    n_recommendations = st.slider("추천 개수", 5, 30, 10, 1)

    if st.button("추천 찾기", use_container_width=True, type="primary"):
        # 위젯 key와 충돌을 피하기 위해 관리할 세션 상태 키를 명시적으로 초기화합니다.
        keys_to_reset = [
            'matching_songs_df', 'selected_track_index', 'recommendation_indices',
            'show_recommendations', 'spotify_player_url', 'similar_matches'
        ]
        for key in keys_to_reset:
            st.session_state[key] = None
        st.session_state.search_query = user_input
        
        if user_input:
            matching_songs_df = df[df['track_name'].str.lower() == user_input.lower()].copy()
            st.session_state.matching_songs_df = matching_songs_df if not matching_songs_df.empty else None
            
            if st.session_state.matching_songs_df is None:
                # 정확히 일치하는 곡이 없을 경우, 유사한 곡명 검색 및 Spotify에서 아티스트 정보 조회
                unique_titles = df['track_name'].str.lower().unique()
                similar_titles = get_close_matches(user_input.lower(), unique_titles, n=5, cutoff=0.6)
                
                if similar_titles:
                    # 각 유사 곡명의 첫 번째 track_id를 가져옵니다.
                    track_ids_to_fetch = []
                    processed_titles = set()
                    for title in similar_titles:
                        if title not in processed_titles:
                            first_match = df[df['track_name'].str.lower() == title].iloc[0]
                            track_ids_to_fetch.append(first_match['track_id'])
                            processed_titles.add(title)
                    
                    # Spotify API로 아티스트 정보를 포함한 상세 정보 조회
                    similar_details = fetch_spotify_data(track_ids_to_fetch)
                    st.session_state.similar_matches = [d for d in similar_details if d]
                else:
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
# 1-2. 유사 곡명 제안
elif st.session_state.get('similar_matches'):
    st.subheader("혹시 이 노래를 찾으셨나요?")
    st.markdown(f"'{st.session_state.search_query}'에 대한 정확한 결과를 찾지 못했습니다. 원하는 곡이 있으신가요?")
    
    # 제안된 곡들을 '곡명 - 아티스트' 형태의 버튼으로 표시
    for details in st.session_state.similar_matches:
        button_label = f"{details['name']} - {details['artists']}"
        if st.button(button_label, key=f"similar_{details['id']}", use_container_width=True):
            # 사용자가 선택한 곡 제목으로 search_query 업데이트
            st.session_state.search_query = details['name']
            st.session_state.similar_matches = None
            # 선택된 곡 제목으로 matching_songs_df 갱신
            matching_songs_df = df[df['track_name'].str.lower() == details['name'].lower()].copy()
            st.session_state.matching_songs_df = matching_songs_df
            # matching_songs_df가 갱신되어 위의 '1. 검색 결과 표시 및 선택' 과정이 진행됨
            st.rerun()

# 2. 추천 결과 표시
if st.session_state.show_recommendations:
    main_col, player_col = st.columns([1.5, 1])
    with main_col:
        # 사용자가 입력한 곡 정보
        selected_song_details = fetch_spotify_data([df.loc[st.session_state.selected_track_index]['track_id']])[0]
        if selected_song_details:
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.image(selected_song_details['album_cover_url'] or "")
            with c2:
                st.markdown(f"## **{selected_song_details['name']}**")
                st.markdown(f"### *{selected_song_details['artists']}*", unsafe_allow_html=True)
                # 추천 페이지가 처음 로드될 때만 플레이어를 설정하고, 사용자가 다른 곡을 선택하면 덮어쓰지 않도록 함
                if st.session_state.spotify_player_url is None:
                    st.session_state.spotify_player_url = f"https://open.spotify.com/embed/track/{selected_song_details['id']}"
            with c3:
                if st.button("▶️ 재생", key=f"play_main_{selected_song_details['id']}", use_container_width=True):
                    st.session_state.spotify_player_url = f"https://open.spotify.com/embed/track/{selected_song_details['id']}"
                    st.rerun()
            
            st.divider()

        # 입력 곡 기반 추천곡
        st.subheader("당신을 위한 추천")
        rec_indices = st.session_state.recommendation_indices
        recommended_df = df.loc[rec_indices]
        rec_track_ids = recommended_df['track_id'].tolist()
        rec_details_list = fetch_spotify_data(rec_track_ids)

        for details in rec_details_list:
            if not details: continue
            expander_title = f"**{details['name']}** by *{details['artists']}*"
            with st.expander(expander_title, expanded=False):
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1: st.image(details['album_cover_url'] or "")
                with c2:
                    st.markdown(f"***{details['name']}***")
                    st.markdown(f"{details['artists']}")
                    st.markdown(f"{details['release_year']}년")
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
if st.session_state.matching_songs_df is None and not st.session_state.show_recommendations and not st.session_state.similar_matches:
    st.info("⬅️ 좋아하는 노래를 검색하고 새로운 음악을 추천받으세요!")