import spotipy
import os

from code.api_settings import get_api

_spotify_client = None
_track_details_cache = {}

def get_spotify_client():
    """Spotify API 클라이언트를 생성하고 반환합니다."""
    global _spotify_client
    if _spotify_client:
        return _spotify_client

    try:
        # api_settings.py의 함수를 사용하여 클라이언트 가져오기
        _spotify_client = get_api()
        return _spotify_client
    except Exception as e:
        # get_api()가 streamlit에 종속적이므로, 여기서는 일반 예외 처리
        raise RuntimeError(f"Spotify 클라이언트 초기화 중 오류 발생: {e}")

def get_track_details_by_id(track_id):
    """Spotify에서 단일 트랙 ID로 상세 정보를 가져옵니다."""
    if track_id in _track_details_cache:
        return _track_details_cache[track_id]

    sp = get_spotify_client()
    try:
        track = sp.track(track_id)
        if not track:
            return None

        details = {
            'id': track['id'],
            'name': track['name'],
            'artists': ", ".join([artist['name'] for artist in track['artists']]),
            'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'release_year': int(track['album']['release_date'].split('-')[0]) if track['album']['release_date'] else None,
            'spotify_url': track['external_urls']['spotify'],
            'preview_url': track['preview_url']
        }
        _track_details_cache[track_id] = details
        return details

    except Exception as e:
        print(f"Spotify API 단일 트랙 조회 중 오류 발생 (ID: {track_id}): {e}")
        return None

def get_multiple_track_details(track_ids):
    """Spotify에서 여러 트랙 ID로 상세 정보를 한 번에 가져옵니다."""
    sp = get_spotify_client()
    
    results = {}
    ids_to_fetch = []
    for track_id in track_ids:
        if track_id in _track_details_cache:
            results[track_id] = _track_details_cache[track_id]
        else:
            ids_to_fetch.append(track_id)

    for i in range(0, len(ids_to_fetch), 50):
        chunk = ids_to_fetch[i:i+50]
        try:
            tracks_data = sp.tracks(chunk)
            for track in tracks_data['tracks']:
                if track:
                    details = {
                        'id': track['id'],
                        'name': track['name'],
                        'artists': ", ".join([artist['name'] for artist in track['artists']]),
                        'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'release_year': int(track['album']['release_date'].split('-')[0]) if track['album']['release_date'] else None,
                        'spotify_url': track['external_urls']['spotify'],
                        'preview_url': track['preview_url']
                    }
                    results[track['id']] = details
                    _track_details_cache[track['id']] = details
        except Exception as e:
            print(f"Spotify API 다중 트랙 조회 중 오류 발생: {e}")
            continue
            
    return [results.get(track_id) for track_id in track_ids]