import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from scipy import stats
import pickle
import os
import re
from difflib import get_close_matches

def create_recommendation_model(data_path='data/tracks_over_2000.csv'):
    """
    정제된 데이터를 로드하고, 오디오 및 장르 특성을 기반으로 KNN 모델을 학습시킨 후,
    나중에 사용할 수 있도록 모델, 전처리기, 데이터프레임을 저장합니다.
    """
    # 데이터 로드
    try:
        df = pd.read_csv(data_path)
        # TF-IDF를 위해 track_genre의 NaN 값을 'unknown'으로 채웁니다.
        if 'track_genre' in df.columns:
            df['track_genre'].fillna('unknown', inplace=True)
        print(f"트랙 로드 완료: {len(df)}개")
    except FileNotFoundError:
        print(f"Error: '{data_path}'를 찾을 수 없습니다. data_cleaning.py를 먼저 실행해주세요.")
        return

    # 학습에 활용할 특성 정리
    print("\n학습 전 특성 정리 중...")
    skewed_features = []
    normal_features = []

    audio_features = ['energy', 'danceability', 'valence', 'acousticness',
                      'tempo', 'loudness', 'speechiness', 'instrumentalness', 'liveness']

    for feature in audio_features:
        if feature in df.columns:
            skewness = stats.skew(df[feature].dropna())
            if abs(skewness) > 1.5:
                skewed_features.append(feature)
            else:
                normal_features.append(feature)

    # 특성 선택
    numerical_features = normal_features
    robust_features = skewed_features
    if 'popularity' in df.columns and 'popularity' not in robust_features:
        robust_features.append('popularity')
    
    categorical_features = ['key', 'mode']
    text_features = 'track_genre'

    # 실제 존재하는 컬럼만 필터링
    numerical_features = [f for f in numerical_features if f in df.columns]
    robust_features = [f for f in robust_features if f in df.columns]
    categorical_features = [f for f in categorical_features if f in df.columns]
    has_text_feature = text_features in df.columns

    print(f"\n== 선택된 특성 ==")
    print(f"  정규 분포 특성: {numerical_features}")
    print(f"  왜도가 높은 특성: {robust_features}")
    print(f"  범주형 특성: {categorical_features}")
    if has_text_feature:
        print(f"  텍스트 특성: {text_features}")

    # 전처리
    transformers = []
    if numerical_features:
        transformers.append(('normal', StandardScaler(), numerical_features))
    if robust_features:
        transformers.append(('robust', RobustScaler(), robust_features))
    if categorical_features:
        transformers.append(('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features))
    if has_text_feature:
        transformers.append(('tfidf', TfidfVectorizer(stop_words='english', max_features=300), text_features))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop'
    )

    # 모델에 사용할 특성만 있는 데이터프레임 생성
    feature_cols = numerical_features + robust_features + categorical_features
    if has_text_feature:
        feature_cols.append(text_features)
        
    features_df = df[feature_cols]

    # 전처리기 학습 및 데이터 변환
    features_transformed = preprocessor.fit_transform(features_df)
    print(f"📐 변환된 데이터 형태: {features_transformed.shape}")

    # 모델 학습
    n_neighbors = min(20, features_transformed.shape[0] - 1)
    knn_model = NearestNeighbors(
        metric='cosine',
        algorithm='brute',
        n_neighbors=n_neighbors
    )
    knn_model.fit(features_transformed)

    # 결과물 저장
    os.makedirs('data', exist_ok=True)
    with open('data/knn_model.pkl', 'wb') as f: pickle.dump(knn_model, f)
    with open('data/preprocessor.pkl', 'wb') as f: pickle.dump(preprocessor, f)

    feature_info = {
        'numerical': numerical_features,
        'robust': robust_features,
        'categorical': categorical_features,
        'text': text_features if has_text_feature else None,
        'all': feature_cols
    }
    with open('data/feature_info.pkl', 'wb') as f: pickle.dump(feature_info, f)
    
    df.to_pickle('data/processed_tracks_df.pkl')
    print("\n추천 모델 생성 완료")

def get_recommendations_interactive():
    """
    사용자로부터 입력을 받아 대화형으로 추천을 제공합니다.
    """
    print("\n" + "="*60)
    print("Spotify 기반 노래 추천기")
    print("="*60)

    # 모델 파일 로드
    try:
        with open('data/knn_model.pkl', 'rb') as f: knn_model = pickle.load(f)
        with open('data/preprocessor.pkl', 'rb') as f: preprocessor = pickle.load(f)
        with open('data/feature_info.pkl', 'rb') as f: feature_info = pickle.load(f)
        df = pd.read_pickle('data/processed_tracks_df.pkl')
        print("모델 로드 완료\n")
    except FileNotFoundError:
        print("모델 파일 없음. 새로운 모델을 생성 중...")
        create_recommendation_model()

        try:
            with open('data/knn_model.pkl', 'rb') as f: knn_model = pickle.load(f)
            with open('data/preprocessor.pkl', 'rb') as f: preprocessor = pickle.load(f)
            with open('data/feature_info.pkl', 'rb') as f: feature_info = pickle.load(f)
            df = pd.read_pickle('data/processed_tracks_df.pkl')
            print("모델 로드 완료\n")
        except FileNotFoundError:
            print("생성 후에도 모델을 찾을 수 없음. 스크립트 종료.")
            return

    while True:
        print("\n" + "-"*60)
        print("노래 제목 입력 (종료: 'quit', 'exit', 'q')")
        print("예시: 'Painkiller', 'Lose Yourself'")
        print("-"*60)

        # 사용자 입력 받기
        user_input = input("\n노래 제목: ").strip()

        # 종료 조건
        if user_input.lower() in ['quit', 'exit', 'q']:
            break

        if not user_input:
            print("노래 제목을 입력해주세요.")
            continue
        
        # 'track_name' 컬럼이 없는 경우에 대한 예외 처리
        if 'track_name' not in df.columns:
            print("'track_name' 컬럼 없음.")
            break

        # 연도 파싱
        year_filter = None
        clean_title = user_input
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', user_input)
        if year_match:
            year_filter = int(year_match.group())
            clean_title = re.sub(r'\b(19\d{2}|20\d{2})\b', '', user_input).strip()
            print(f"연도 필터 감지: {year_filter}")

        # 일치하는 노래 찾기
        matching_songs = df[df['track_name'].str.lower() == clean_title.lower()]
        # 없으면 비슷한 노래 추천 - similar
        if matching_songs.empty:
            print(f"\n'데이터 없음: {clean_title}'")
            similar = get_close_matches(clean_title, df['track_name'].unique().tolist(), n=5, cutoff=0.6)
            if similar:
                print("\n가능성 있는 이름의 곡")
                for i, title in enumerate(similar, 1):
                    print(f"  {i}. {title}")
            continue

        selected_index = None
        if len(matching_songs) > 1:
            print(f"\n'{clean_title}'의 {len(matching_songs)}가지 버전")
            for idx, (original_idx, row) in enumerate(matching_songs.iterrows(), 1):
                info = f"  {idx}. "
                if 'album_release_date' in row:
                    info += f"연도: {int(row['album_release_date'])}"
                if 'popularity' in row:
                    info += f", 인기도: {row['popularity']}"
                print(info)

            if year_filter:
                year_filtered = matching_songs[matching_songs['album_release_date'] == year_filter]
                if not year_filtered.empty:
                    selected_index = year_filtered.index[0]
                    print(f"\n{year_filter}년 버전 자동 선택")
                else:
                    year_diff = abs(matching_songs['album_release_date'] - year_filter)
                    selected_index = year_diff.idxmin()
                    selected_year = matching_songs.loc[selected_index, 'album_release_date']
                    print(f"\n{year_filter}년 버전 없음.")
                    print("가장 가까운 연도의 버전 사용: {int(selected_year)}년")
            else:
                print("\n유사한 제목의 노래")
                print("  0. 가장 인기 있는 버전 자동 선택")
                print("  1-N. 특정 버전 선택")
                while True:
                    try:
                        choice = input("\n선택 (자동은 0): ").strip()
                        if choice == "" or choice == "0":
                            if 'popularity' in matching_songs.columns:
                                selected_index = matching_songs['popularity'].idxmax()
                                print("가장 인기 있는 버전")
                            else:
                                selected_index = matching_songs.index[0]
                                print("첫 번째 버전")
                            break
                        else:
                            choice_num = int(choice)
                            if 1 <= choice_num <= len(matching_songs):
                                selected_index = matching_songs.index[choice_num - 1]
                                print(f"{choice_num}번 버전")
                                break
                            else:
                                print(f"1에서 {len(matching_songs)} 사이의 숫자를 입력해주세요.")
                    except ValueError:
                        print("유효한 숫자를 입력해주세요.")
        else:
            selected_index = matching_songs.index[0]

        print("\n몇 개의 노래를 추천받으시겠습니까? (기본값: 10): ", end="")
        rec_input = input().strip()
        n_recommendations = 10
        if rec_input:
            try:
                n_recommendations = int(rec_input)
                n_recommendations = max(1, min(50, n_recommendations))
            except ValueError:
                print("기본값인 10개로 추천합니다.")

        selected_song = df.loc[selected_index]
        print(f"\n선택된 노래: '{selected_song['track_name']}' (ID: {selected_song['track_id']})")
        if 'track_genre' in selected_song and selected_song['track_genre'] != 'unknown':
            print(f"   장르: {selected_song['track_genre']}")
        if 'album_release_date' in selected_song:
            print(f"   연도: {int(selected_song['album_release_date'])}")
        if 'popularity' in selected_song:
            print(f"   인기도: {selected_song['popularity']}")

        print("\n비슷한 노래를 찾고 있습니다...")
        
        song_features = df.loc[[selected_index]][feature_info['all']]
        song_features_transformed = preprocessor.transform(song_features)

        n_candidates = min(50, len(df) - 1)
        distances, indices = knn_model.kneighbors(
            song_features_transformed,
            n_neighbors=n_candidates + 1
        )

        neighbor_indices = indices.flatten()[1:]
        neighbor_distances = distances.flatten()[1:]
        
        candidates = df.iloc[neighbor_indices].copy()
        candidates['cosine_similarity'] = 1 - neighbor_distances

        # 입력된 노래와 같은 제목의 모든 버전을 추천 목록에서 제외
        original_title = selected_song['track_name'].lower()
        candidates = candidates[candidates['track_name'].str.lower() != original_title]

        if 'popularity' in candidates.columns:
            pop_min, pop_max = candidates['popularity'].min(), candidates['popularity'].max()
            if pop_max > pop_min:
                candidates['popularity_normalized'] = (candidates['popularity'] - pop_min) / (pop_max - pop_min)
            else:
                candidates['popularity_normalized'] = 0.5
            
            candidates['final_score'] = (0.9 * candidates['cosine_similarity']) + (0.1 * candidates['popularity_normalized'])
            candidates.sort_values('final_score', ascending=False, inplace=True)
        else:
            candidates.sort_values('cosine_similarity', ascending=False, inplace=True)

        print(f"\n상위 {n_recommendations}개 추천:")
        print("-"*60)

        for i, (_, row) in enumerate(candidates.head(n_recommendations).iterrows(), 1):
            print(f"\n{i:2}. {row['track_name']}")
            print(f"    ID: {row['track_id']}") # track_id 추가
            print(f"    유사도: {row['cosine_similarity']:.3f}")
            if 'popularity' in row:
                print(f"    인기도: {row['popularity']}")
            if 'album_release_date' in row:
                print(f"    연도: {int(row['album_release_date'])}")

        # 계속할지 묻기
        print("\n" + "-"*60)
        continue_choice = input("다른 노래를 검색하려면 Enter를 누르거나, 종료하려면 'quit'을 입력하세요: ").strip()
        if continue_choice.lower() in ['quit', 'exit', 'q']:
            print("\n추천 시스템을 이용해주셔서 감사합니다!")
            break

if __name__ == '__main__':
    # 모델 존재 여부 확인
    model_files = ['knn_model.pkl', 'preprocessor.pkl', 'processed_tracks_df.pkl', 'feature_info.pkl']
    
    if not all(os.path.exists(f'data/{fname}') for fname in model_files):
        print("모델 파일을 찾을 수 없습니다. 먼저 새로운 모델을 생성합니다...")
        create_recommendation_model()
    
    # 대화형 시스템 실행
    get_recommendations_interactive()
