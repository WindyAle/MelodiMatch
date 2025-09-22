# Spotify 트랙 데이터 분석 프로젝트

## 👨‍👩‍👧‍👦 팀 소개
| 김종민 | 마한성 | 배상준 | 이인재 |
|:--:|:--:|:--:|:--:|
| <img width="181" height="278" alt="image" src="https://github.com/user-attachments/assets/c737d324-4044-43fc-83fa-498e1304424d" /> | <img width="185" height="272" alt="image" src="https://github.com/user-attachments/assets/97de638f-2930-4ee1-be6d-195de3089478" /> | <img width="166" height="304" alt="image" src="https://github.com/user-attachments/assets/f16c843f-6f30-48aa-bcf9-26356c69eb08" /> | <img width="153" height="328" alt="image" src="https://github.com/user-attachments/assets/e4fb11be-c4ba-4648-a736-209776cc73dc" /> |


## 📋 WBS 

| 순번 | 진행 순서 | 담당자 | 예상 기간 | 산출물 |
|:----:|-----------|:------:|:---------:|--------|
| **1** | **프로젝트 기획 및 준비** | | | |
| 1-1 | 프로젝트 주제 선정 | 전체 팀 | 9/16-9/17 | 주제 확정 |
| 1-2 | 데이터셋 조사 및 선정 | 전체 팀 | 9/17-9/18 | 데이터셋 선정 |
| 1-3 | 주제 선정 | 전체 팀 | 9/17 | 주제 선정 |
| **2** | **탐색적 데이터 분석(EDA)** | | | |
| 2-1 | 결측치 및 이상치 탐색 | 전체 팀 | 9/18 | 결측치/이상치 분석 |
| 2-2 | 데이터 시각화 (히트맵 및 년도별 특성 변화도 그래프) | 김종민 | 9/18 | 히트맵 및 연도별 특성 변화도 그래프 |
| **3** | **데이터 정제 및 전처리** | | | |
| 3-1 | 담당 컬럼별 데이터 Standardscale/MinMaxscale 비교 | 팀 전체 | 9/19 | 데이터 처리 방법 |
| **4** | **데이터 변환 및 피처 엔지니어링** | | | |
| 4-1 | Feature importance 그래프 작성 | 배상준 | 9/20 | 피처 중요도 차트 |
| **5** | **그 외** | | | |
| 5-1 |  함수 모듈화 | 이인재 | 9/19-9/20 | 코드 |
| 5-2 | 리드미 작성 | 마한성 | 9/20 | 리드미 파일 |


## 🎈 프로젝트 주제 및 선정 배경

- Spotify 트랙 데이터 분석 프로젝트
프로젝트 개요: 
시대별 장르 선호도를 분석하기 위한 Spotify 트랙 데이터 EDA 프로젝트

- 프로젝트 주제 및 선정 배경
주제: 시대별 장르 선호도 변화 분석
1. 주제 및 데이터셋 선정 이유
* 주제 선정 배경
-스포티파이에서 제공하는 방대한 양의 데이터를 통해 여러 인사이트를 도출할 수 있을것을 기대하여 선정하게 되었습니다.

2. Spotify 데이터셋 선정 이유
* 방대한 데이터 규모

약 90만 개의 트랙 데이터로 충분한 샘플 사이즈 확보
다양한 시대(1900년대~현재)와 장르를 아우르는 포괄적인 데이터

* 풍부한 분석 변수

33개의 다양한 컬럼으로 다각도 분석 가능
음악적 특성 (tempo, energy, danceability, valence 등)부터 메타데이터까지 포함
장르, 인기도, 발매일 등 시계열 분석에 필요한 정보 보유

* 데이터 품질 및 접근성

Zenodo (유럽집행위원회, CERN 운영)에서 제공하는 신뢰할 수 있는 데이터 소스
구조화된 CSV 형태로 전처리 및 분석에 용이
결측치가 존재하지만 전체적으로 분석 가능한 수준의 데이터 완성도

* 높은 분석 활용도

시대별 트렌드 변화를 추적할 수 있는 시계열 데이터 구조
머신러닝 모델 적용을 위한 충분한 피처와 데이터 볼륨


## 📂 데이터셋

- **데이터명**: Almost a million Spotify tracks
- **데이터 크기**: 899,702개 트랙(row)
- **데이터 출처**: [Zenodo](https://zenodo.org/records/11453410) (유럽집행위원회 및 CERN 운영)
- **파일명**: `tracks.csv`


## 🎯 프로젝트 목표

각 특성을 분석하여 불필요한 column을 제거하고 비슷한 column은 합치고 scale의 변화등을 통해 EDA를 진행하고 나아가
해당 특성들로 시대별 음악 장르의 선호도 변화를 통해 미래의 선호도를 예측하는 것.

### columns 설명

| 컬럼명 | 설명 | 데이터 타입 |
|--------|------|-------------|
| track_id | 트랙 고유 ID | object |
| name | 트랙의 제목 | object |
| album_name | 앨범 이름 | object |
| album_total_tracks | 트랙이 속한 앨범에 있는 전체 곡의 수 | float64 |
| chart | 트랙이 속한 차트의 이름 | object |
| track_track_number | 앨범 내의 트랙 번호 | float64 |
| track_album_album | 트랙이 속한 앨범의 유형 | object|
| genres | 장르 정보 | object |
| track_artists | 아티스트 이름 | object |
| artist_followers | 아티스트 팔로워 수 | float64 |
| artist_popularity | 아티스트 인기도 | float64 |
| popularity | 인기도 | float64 |
| streams | 스트리밍 횟수 | float64 |
| rank | 차트 내에서 트랙의 순위 | float64 | 
| trend | 순위 변화 | object |
| explicit | 부적절한 표현 여부 | object |
| energy | 에너지 수치 | float64 |
| tempo | 템포 | float64 |
| key | 트랙의 조(tonality) | float64 |
| mode | 트랙의 장/단조 | object |
| time_signature | 박자 | float64 |
| speechiness | 말소리(보컬, 랩등)의 비율 | float64 | 
| danceability | 댄스 가능성 | float64 |
| valence | 긍정도 | float64 |
| acousticness | 어쿠스틱(비전기 사운드) 정도 | float64 |
| liveness | 공연에서 녹음된 정도 | float64 |
| loudness | 음량 | float64 |
| instrumentalness | 보컬이 없는 정도 | float64 | 
| duration_ms | 재생 시간 | float64 |
| album_release_date | 앨범 발매일 | object |
| added_at | 트랙이 업로드 된 시점 | object |
| available_markets | 이용 가능 국가 | object |
| region | 지역 | object |


## 🔍 EDA 과정

### 1. 데이터 로드
```python
df = pd.read_csv('./data/tracks.csv')
```

### 2. 데이터 구조 확인
- `info()`: 전체 데이터 개수 및 결측치 확인
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 899702 entries, 0 to 899701
Data columns (total 33 columns):
 #   Column              Non-Null Count   Dtype  
---  ------              --------------   -----  
 0   track_id            899702 non-null  object 
 1   streams             5870 non-null    float64
 2   artist_followers    892496 non-null  float64
 3   genres              892516 non-null  object 
 4   album_total_tracks  899701 non-null  float64
 5   track_artists       99943 non-null   object 
 6   artist_popularity   892516 non-null  float64
 7   explicit            899701 non-null  object 
 8   tempo               899224 non-null  float64
 9   chart               7040 non-null    object 
 10  album_release_date  899701 non-null  object 
 11  energy              899224 non-null  float64
 12  key                 899224 non-null  float64
 13  added_at            394649 non-null  object 
 14  popularity          899701 non-null  float64
 15  track_album_album   99997 non-null   object 
 16  duration_ms         7040 non-null    float64
 17  available_markets   899701 non-null  object 
 18  track_track_number  99997 non-null   float64
 19  rank                7040 non-null    float64
 20  mode                899224 non-null  float64
 21  time_signature      899224 non-null  float64
 22  album_name          899271 non-null  object 
 23  speechiness         899224 non-null  float64
 24  region              7040 non-null    object 
 25  danceability        899224 non-null  float64
 26  valence             899224 non-null  float64
 27  acousticness        899224 non-null  float64
 28  liveness            899224 non-null  float64
 29  trend               7040 non-null    object 
 30  instrumentalness    899224 non-null  float64
 31  loudness            899224 non-null  float64
 32  name                899215 non-null  object 
dtypes: float64(20), object(13)
memory usage: 226.5+ MB
```

- `describe()`: 기초 통계량 분석
<img width="1353" height="312" alt="image" src="https://github.com/user-attachments/assets/24dd4d60-f421-4246-b284-800ef6df2185" />



- `columns`: 컬럼 정보 확인
Index(['track_id', 'streams', 'artist_followers', 'genres',
       'album_total_tracks', 'track_artists', 'artist_popularity', 'explicit',
       'tempo', 'chart', 'album_release_date', 'energy', 'key', 'added_at',
       'popularity', 'track_album_album', 'duration_ms', 'available_markets',
       'track_track_number', 'rank', 'mode', 'time_signature', 'album_name',
       'speechiness', 'region', 'danceability', 'valence', 'acousticness',
       'liveness', 'trend', 'instrumentalness', 'loudness', 'name'],
      dtype='object')


### 3. 결측치 및 이상치 탐색
- 결측치 분포 확인: `df.isnull().sum()`
- 이상치 탐지: `df.boxplot()`
<img width="927" height="363" alt="image" src="https://github.com/user-attachments/assets/1ee5519e-991b-404c-b60b-ab6119e7e706" />




### 4. 데이터 시각화
- **히트맵 분석**
<img width="1553" height="924" alt="image" src="https://github.com/user-attachments/assets/b1acf844-51c1-435f-a65b-a08e56ce2720" />


   - `acousticness`와 `instrumentalness` 간 양의 상관관계 확인
  - 두 컬럼 모두 다른 컬럼들과 전체적으로 음의 상관관계

- **음악의 특성 분포(Histogram)**
<img width="1583" height="982" alt="image" src="https://github.com/user-attachments/assets/c0e9846a-d1b9-48f1-b17b-befde30bcf55" />

- acousticness가 양 끝 값에 치중된 이유
    - 클래식이나 전자 사운드를 사용하기 전의 음악일 가능성이 있음.
    - 최신곡의 경우 전자 사운드를 대부분 쓰는 경우도 있음.
- loudness가 치우친 정규분포의 형태를 띰
    - 특별히 선호되고 듣기 좋은 음량의 구간이 정해져 있음을 유추 가능.
- speechiness는 0.07정도에서 높은 빈도를 나타냄
    - 선호되는 speechiness의 정도가 있음. 혹은 음악의 특성상 이를 크게 벗어날 수 없음.
- tempo는 120~140 구간이 최다 빈도를 띰
    - 이 구간에 해당하는 BPM을 가진 장르는 팝, 힙합, EDM이 다수.


- **시대별 음악의 특성 변화**
<img width="1165" height="713" alt="image" src="https://github.com/user-attachments/assets/d8d69d35-c46b-470b-bc9e-5efca52c8d2e" />

<img width="1165" height="713" alt="image" src="https://github.com/user-attachments/assets/c6baa8b4-69a0-403f-92b4-2277d25ad60a" />

- 1920년대 key와 tempo의 급격한 상승
    - 미국 흑인사회를 중심으로 재즈음악의 급성장 - 재즈 시대(Jazz Age)
    - 1차 세계대전 이후 미국이 세계 강대국으로 호황을 누리던 황금기 - 광란의 20년대(Roaring 20s)
    - 복잡한 멜로디와 빠른 템포를 가진 신나는 곡
- 1940년대 부근에 급격한 감소 - loudness, tempo
    - 2차 세계대전의 영향일 가능성
    - 전쟁으로 인해 기존의 밴드 음악에서 감성적인 발라드 음악이 유행
- 1960년대 이후부터 loudness, tempo 상승
    - 록(Rock) 음악의 유행으로 강렬한 에너지와 빠른 비트가 대중문화를 지배
- 1990년대 이후 가사에 비속어 포함 급증
    - 스트리밍 서비스 등장: 방송국에서 틀어주는 검열된(Censored) 음악에서 자기가 직접 찾아듣는 시대
    - 갱스터 랩 & 힙합의 유행: 기성세대에 대한 반항과 강렬한 사회적 메세지를 담는 기조
- `loudness`(음량)와 `acousticness`(어쿠스틱함) 반비례 관계 -어쿠스틱함이란 **앰프나 전자 장치 없이 자연적인 음향적 수단, 즉 악기 본연의 울림을 통해 소리를 내는 상태나 특성**을 의미합니다, 즉, 앰프나 전자 장치의 활용의 증가로 어쿠스틱함이 줄어들고 그에 따라 음량은 커졌다고 해석할 수 있음

- **상위 5% 인기곡(popularity) 특성 시각화**
<img width="1244" height="791" alt="image" src="https://github.com/user-attachments/assets/e6855d88-6d39-46f2-aff2-70731c0c699b" />
<img width="537" height="301" alt="image" src="https://github.com/user-attachments/assets/948a96a5-2c5c-4ac1-97fd-c516e24dcb3d" />


- **상위 10위 아티스트**
<img width="1084" height="713" alt="image" src="https://github.com/user-attachments/assets/5674c8b0-83af-4ff8-a29b-5eaaaffb9e08" />



- **스케일링 전후의 특성 중요도**
<img width="809" height="525" alt="image" src="https://github.com/user-attachments/assets/b49c4375-3a86-4344-8d72-ca604b87c109" />

<img width="816" height="525" alt="image" src="https://github.com/user-attachments/assets/6961ecad-7ee3-4276-8648-5f08f94ffaad" />
전체 약 89만개 중 40만개를 추출하여 RandomForestRegressor 적용
- 특성 중요도 순위가 전반적으로 달라짐
- 특성마다 값의 단위/자릿수가 달라서 생기는 차이로 판단
    - ex) energy는 최대치가 1이지만 release_date는 2000대의 숫자가 존재
    
- 최근 아티스트들을 보면 유명인들과 콜라보를 하고 팔로워를 얻기 위해 SNS로 홍보하고 앨범 발매일을 홍보하는 것이 이미 이에 대한 분석을 통해 적절히 대응하고 있음을 알 수 있음

### 5. 데이터 정제
- **불필요한 컬럼 결정**

* streams: 스트리밍 횟수 - popularity와 겹치는 column, 결측치 과다(5,870/899,702)

* album_total_tracks: 앨범의 총 트랙 수 

* chart: 차트 정보

* available_markets: 서비스 가능 국가/지역

* region: 지역(나라)

* mode(삭제후 ML시 필요하면 사용) - 장/단조

* track_id: 트랙의 고유 ID

* album_name: 앨범 이름

* rank: 곡 순위 - 전체 column의 1%가 안되는 수치

* track_track_number: 앨범 내 트랙 번호

* time_signature: 박자 
  - tempo 겹치는 컬럼이고 정확히 무엇을 뜻하는지 모름
  - 차원의 저주 완화

* duration_ms: 곡의 길이 - 결측치 99.2%

* trend - 차트 내에서 순위 변화 - 분석에 불필요

* added_at - added_at이 row가 적고 비슷한 column인 album_release_date이 더 major하다고 판단.

df.drop(['streams', 'album_total_tracks', 'chart', 'available_markets', 'region', 'mode', 'track_id', 'album_name', 'track_track_number', 'rank', 'track_artists', 'duration_ms', 'trend', 'track_album_album', 'added_at', 'name', 'time_signature'], axis=1)


## 🔧 전처리 계획

### 6. 데이터 변환 및 피처 엔지니어링
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
