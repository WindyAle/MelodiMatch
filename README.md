# SKN19-mini-2Team
# Spotify 트랙 데이터 분석 프로젝트

## 👨‍👩‍👧‍👦 팀 소개
| 김종민 | 마한성 | 배상준 | 이인재 |
|:--:|:--:|:--:|:--:|
| <img width="100" alt="Image" src="https://github.com/user-attachments/assets/e96992fe-13f0-4666-a9af-787d9a6e68c5" /> | <img width="100" alt="Image" src="https://github.com/user-attachments/assets/5ae03301-5869-4dd8-9c8a-831ead2b95aa" /> | <img width="100" alt="Image" src="https://github.com/user-attachments/assets/d2af51c8-8a1e-4fcc-99bd-0b7d69354398" /> | <img width="100" alt="Image" src="https://github.com/user-attachments/assets/8c3f07a5-7e5f-45f7-bc34-4f20354b044a" /> |

## 📊 프로젝트 개요

Spotify 데이터를 활용한 시대별 음악 선호도 분석(추후 수정)


**발표자**: 마한성

## 📂 데이터셋

- **데이터명**: Almost a million Spotify tracks
- **데이터 크기**: 899,702개 트랙(row)
- **데이터 출처**: [Zenodo](https://zenodo.org/records/11453410) (유럽집행위원회 및 CERN 운영)
- **파일명**: `tracks.csv`

## 🎯 프로젝트 목표

시대별 음악 장르의 선호도 변화를 분석하여 음악 트렌드의 변화 패턴을 파악합니다.

## 📈 데이터 구조

### 전체 데이터 정보
- **총 컬럼 수**: 개 (숫자형: 개, 객체형: 개) -> 
- **메모리 사용량**:  MB -> MB

### columns 설명

| 컬럼명 | 설명 | 데이터 타입 |
|--------|------|-------------|
| track_id | 트랙 고유 ID | object |
| streams | 스트리밍 횟수 | float64 |
| artist_followers | 아티스트 팔로워 수 | float64 |
| genres | 장르 정보 | object |
| album_total_tracks | 트랙이 속한 앨범에 있는 전체 곡의 수 | float64 |
| track_artists | 아티스트 이름 | object | 
| artist_popularity | 아티스트 인기도 | float64 |
| explicit | 부적절한 표현 여부 | float64 |
| chart | 트랙이 속한 차트의 이름 | object |


| album_release_date | 앨범 발매일 | object |
| energy | 에너지 수치 | float64 |
| tempo | 템포 | float64 |
| danceability | 댄스 가능성 | float64 |
| valence | 긍정도 | float64 |
| acousticness | 어쿠스틱 정도 | float64 |
| loudness | 음량 | float64 |





album_release_date: 앨범 발매일 - 트랙이 속한 앨범의 발매 날짜입니다.

energy: 에너지 - 스포티파이가 추정한 트랙의 활력 및 강도 지표입니다.

key: 키 - 스포티파이가 추정한 트랙의 조(tonality)입니다.

added_at: 추가된 시간 - 트랙이 업로드된 시점입니다.

popularity: 인기도 - 스포티파이가 추정한 트랙의 인기도입니다.

track_album_album: 앨범 유형 - 트랙이 속한 앨범의 유형입니다.

duration_ms: 재생 시간 (밀리초) - 트랙의 길이를 밀리초 단위로 나타낸 것입니다.

available_markets: 이용 가능 국가 - 트랙을 이용할 수 있는 국가 목록입니다.

track_track_number: 트랙 번호 - 스포티파이 기준 앨범 내의 트랙 번호입니다.

rank: 순위 - 차트 내에서 트랙의 순위입니다 (해당하는 경우).

mode: 모드 - 트랙의 장/단조(major/minor)를 나타내는 지표입니다.

time_signature: 박자 - 트랙의 박자(예: 4/4박자)를 나타냅니다.

album_name: 앨범 이름 - 트랙이 속한 앨범의 이름입니다.

speechiness: 말소리 비율 - 스포티파이가 추정한 트랙에 포함된 말소리(보컬, 랩 등)의 비율입니다.

region: 지역 - 차트가 속한 지역입니다 (해당하는 경우).

danceability: 댄스 지수 - 스포티파이가 추정한 춤추기 좋은 정도를 나타내는 지표입니다.

valence: 긍정성 - 스포티파이가 추정한 트랙의 긍정적인 감정 지표입니다.

acousticness: 어쿠스틱 지수 - 스포티파이가 추정한 어쿠스틱(비전기) 사운드의 정도입니다.

liveness: 라이브 지수 - 스포티파이가 추정한 라이브 공연에서 녹음된 정도를 나타내는 지표입니다.

trend: 순위 변화 - 차트 내에서 트랙 순위의 변화입니다 (예: 순위 상승, 하락).

instrumentalness: 연주곡 지수 - 스포티파이가 추정한 트랙에 보컬이 없는 정도를 나타내는 지표입니다.

loudness: 음량 - 스포티파이가 추정한 트랙의 전체적인 음량(데시벨)입니다.

name: 트랙 제목 - 스포티파이에 표시되는 트랙의 제목입니다.

## 🔍 EDA 과정

### 1. 데이터 로드
```python
df = pd.read_csv('./data/tracks.csv')
```

### 2. 데이터 구조 확인
- `info()`: 전체 데이터 개수 및 결측치 확인
- `describe()`: 기초 통계량 분석
- `columns`: 컬럼 정보 확인

### 3. 결측치 및 이상치 탐색
- 결측치 분포 확인: `df.isnull().sum()`
- 이상치 탐지: `df.boxplot()`
- 데이터 정제 방안 수립

### 4. 데이터 시각화
- **히트맵 분석** 결과:
  - `acousticness`와 `instrumentalness` 간 양의 상관관계 확인
  - 두 컬럼 모두 다른 컬럼들과 전체적으로 음의 상관관계

### 5. 데이터 정제

#### 삭제 대상 컬럼
```python
drop_columns = [
    'streams', 'album_total_tracks', 'chart', 
    'available_markets', 'region', 'mode', 
    'track_id', 'album_name', 'track_track_number', 
    'rank', 'trend', 'duration_ms'
]
```

#### 삭제 사유
- `streams`: 결측치 과다 (5,870/899,702)
- `duration_ms`: 결측치 99.2%
- `trend`: 분석에 불필요
- `added_at`: 결측치 50만개, `album_release_date`와 중복

## 👥 팀원별 담당 컬럼

### 김종민 (컬럼 0-5)
- `artist_followers`: 스케일링으로 처리
- `genres`: 주요 장르로 추려서 활용
- `track_artists`: 제거 대상 (Bach 데이터 등 1900년대 이전 포함)

### 배상준 (컬럼 6-11)  
- `added_at`: 결측치 과다로 제거
- `track_album_album`: 싱글/정규 구분, 필요시 활용

### 이인재 (컬럼 12-17)
- `duration_ms`: 결측치 99.2%로 제거
- 나머지 컬럼 결측치 행 제거

### 마한성 (컬럼 18-22)
- `loudness`: 이상치 범위 확장
- `liveness`: 이상치 범위 확장  
- `trend`: 제거

## 🔧 전처리 계획

### 6. 데이터 변환 및 피처 엔지니어링
- 로그 변환 적용
- 다항식 피처 추가 검토
- `added_at` + `album_release_date` 통합

### 7. 데이터 분할
- 학습용/테스트용 데이터 분할
- `train_test_split()` 활용

## 📋 다음 단계

1. Feature importance 확인을 통한 최종 컬럼 선정
2. 시대별 장르 선호도 분석 모델링
3. 결과 시각화 및 인사이트 도출

## 🛠️ 사용 기술

- **언어**: Python
- **라이브러리**: pandas, numpy, matplotlib, seaborn
- **환경**: Jupyter Notebook

---

*이 프로젝트는 시대별 음악 트렌드 변화를 데이터 과학적 방법론으로 분석하는 것을 목표로 합니다.*
