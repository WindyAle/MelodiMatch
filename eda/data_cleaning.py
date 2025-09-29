import pandas as pd
import ast
import os

def clean_data(input_path='data/tracks.csv', output_path='data/tracks_over_2000.csv'):
    """
    Cleans the raw Spotify tracks data, filters for tracks since the year 2000
    with popularity over 40, and prepares it for recommendation.
    """
    print(f"Starting data cleaning process for {input_path}...")
    try:
        df = pd.read_csv(input_path, low_memory=False)
        print(f"✅ Loaded {len(df)} raw tracks.")
    except FileNotFoundError:
        print(f"❌ Error: {input_path} not found.")
        return

    if 'album_release_date' in df.columns:
        df['album_release_date'].fillna('0', inplace=True)
        df['album_release_date'] = df['album_release_date'].str[:4]
        df['album_release_date'] = pd.to_numeric(df['album_release_date'], errors='coerce')
        df.dropna(subset=['album_release_date'], inplace=True)
        df['album_release_date'] = df['album_release_date'].astype(int)
        
        df = df[df['album_release_date'] >= 2000].copy()
        print(f"🔍 Found {len(df)} tracks released since 2000.")

    if 'popularity' in df.columns:
        df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')
        df.dropna(subset=['popularity'], inplace=True)
        df = df[df['popularity'] >= 40].copy()
        print(f"🔍 Found {len(df)} tracks with popularity >= 40.")

    if 'name' in df.columns:
        df.rename(columns={'name': 'track_name'}, inplace=True)

    cols_to_drop = [
        'streams', 'chart', 'added_at', 'track_artists', 'track_album_album', 'duration_ms',
        'track_track_number', 'rank', 'region', 'trend', 'album_total_tracks',
        'available_markets' # 'genres' is now handled below
    ]
    df.drop(columns=cols_to_drop, axis=1, inplace=True, errors='ignore')

    if 'genres' in df.columns:
        def process_genres(genres_str):
            if isinstance(genres_str, str) and genres_str.startswith('['):
                try:
                    genres_list = ast.literal_eval(genres_str)
                    return ' '.join(genres_list)
                except (ValueError, SyntaxError):
                    return 'unknown'
            return 'unknown'

        df['track_genre'] = df['genres'].apply(process_genres)
        df.drop(columns=['genres'], inplace=True)
        print("✅ Processed 'genres' column into 'track_genre' for TF-IDF.")

    essential_cols = [
        'track_name', 'popularity', 'danceability', 'energy', 'key', 'loudness',
        'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
    ]
    existing_essential_cols = [col for col in essential_cols if col in df.columns]
    df.dropna(subset=existing_essential_cols, inplace=True)

    for col in existing_essential_cols:
        if col not in ['track_name']:
             df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=existing_essential_cols, inplace=True)

    if 'track_id' in df.columns:
        df.sort_values('popularity', ascending=False, inplace=True)
        df.drop_duplicates(subset=['track_id'], keep='first', inplace=True)

    df.reset_index(drop=True, inplace=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\nSuccess! Cleaned and filtered data saved to {output_path}")
    print(f"   Final dataset contains {len(df)} tracks.")

if __name__ == '__main__':
    clean_data(output_path='data/tracks_over_2000.csv')
