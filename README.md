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
| 2-2 | 데이터 시각화 | 김종민, 배상준 | 9/18-9/22 | 데이터 시각화자료 |
| **3** | **데이터 정제 및 전처리** | | | |
| 3-1 | 담당 컬럼별 데이터 Standardscale/MinMaxscale 비교 | 전체 팀 | 9/19 | 데이터 처리 방법 |
| **4** | **그 외** | | | |
| 5-1 |  함수 모듈화 | 이인재 | 9/19-9/20 | 코드 |
| 5-2 | 리드미 작성 | 마한성 | 9/20-9/22 | 리드미 파일 |


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
다양한 시대(1900년대~2023년도)와 장르를 아우르는 포괄적인 데이터

* 풍부한 분석 변수

33개의 다양한 컬럼으로 다각도 분석 가능
음악적 특성 (tempo, energy, danceability, valence 등)부터 메타데띔
    - 이 구간에 해당하는 BPM을 가진 장르는 팝, 힙합, EDM이 다수.


> **시대별 음악의 특성 변화**
<img width="1165" height="713" alt="image" src="https://github.com/user-attachments/assets/d5fad843-33ae-4904-99e7-e91167b3d13d" />

<img width="1165" height="713" alt="image" src="https://github.com/user-attachments/assets/c6baa8b4-69a0-403f-92b4-2277d25ad60a" />

* 1920년대 key와 tempo의 급격한 상승
    - 미국 흑인사회를 중심으로 재즈음악의 급성장 - 재즈 시대(Jazz Age)
    - 1차 세계대전 이후 미국이 세계 강대국으로 호황을 누리던 황금기 - 광란의 20년대(Roaring 20s)
    - 복잡한 멜로디와 빠른 템포를 가진 신나는 곡
* 1940년대 부근에 급격한 감소 - loudness, tempo
    - 2차 세계대전의 영향일 가능성
    - 전쟁으로 인해 기존의 밴드 음악에서 감성적인 발라드 음악이 유행
* 1960년대 이후부터 loudness, tempo 상승
    - 록(Rock) 음악의 유행으로 강렬한 에너지와 빠른 비트가 대중문화를 지배
* 1990년대 이후 가사에 비속어 포함 급증
    - 스트리밍 서비스 등장: 방송국에서 틀어주는 검열된(Censored) 음악에서 자기가 직접 찾아듣는 시대
    - 갱스터 랩 & 힙합의 유행: 기성세대에 대한 반항과 강렬한 사회적 메세지를 담는 기조
* `loudness`(음량)와 `acousticness`(어쿠스틱함) 반비례 관계 -어쿠스틱함이란 **앰프나 전자 장치 없이 자연적인 음향적 수단, 즉 악기 본연의 울림을 통해 소리를 내는 상태나 특성**을 의미합니다, 즉, 앰프나 전자 장치의 활용의 증가로 어쿠스틱함이 줄어들고 그에 따라 음량은 커졌다고 해석할 수 있음

> **상위 5% 인기곡(popularity) 특성 시각화**
<img width="1244" height="791" alt="image" src="https://github.com/user-attachments/assets/e6855d88-6d39-46f2-aff2-70731c0c699b" />
<center>
 <img width="455" height="470" alt="image" src="https://github.com/user-attachments/assets/09a98a7c-e8c4-4340-9196-c4eae1d9f71f" />
</center>

> **시대별 장르의 트렌드 및 상위 5% 장르 트렌드**
<img width="630" height="470" alt="image" src="https://github.com/user-attachments/assets/c8c6ae36-35b1-4a6b-b0b6-390b9e4da741" />


- 2010년대에 Pop의 인기가 급격히 올라갔고 2020년대에도 여전히 인기가 있지만 다른 장르들도 관심도가 올라간 것을 알 수 있음
  
<img width="630" height="470" alt="image" src="https://github.com/user-attachments/assets/9c8e9224-e84f-4438-84ff-5099208e724a" />

- 전체 트렌드 추이와 상위 인기곡 트렌드 추이가 모양이 유사
 - 90년대엔 전체 표본에서는 Classical 장르가 많았으나 상위 인기곡은 Rock이 지배함
 - 90년대에 유행했던 클래식과 현대음악을 조합하는 형태인 Classical Crossover의 영향으로 보임
 → 한국에서는 ‘팝페라’라는 단어로 알려짐

> **상위 10위 아티스트**
<img width="1084" height="713" alt="image" src="https://github.com/user-attachments/assets/5674c8b0-83af-4ff8-a29b-5eaaaffb9e08" />


> **스타 파워와 인기도 상관관계**
<img width="1489" height="593" alt="image" src="https://github.com/user-attachments/assets/89a5d9cd-bd88-40fa-824e-a443b2da3549" />

아티스트의 인기(스타 파워)와 곡 자체의 인기는 항상 비례할까?

- 해당 값들은 각 아티스트의 곡별 인기도를 나타냄
  
- 아티스트의 명성도는 인기도와 대체로 비례함
- 팔로워 수와 인기도는 명확한 관계가 보이지 않음
    - 곡 자체의 인기와 아티스트에 대한 팬심은 별개인듯
    - 가수의 팬이 아니라도 노래는 얼마든지 들을 수 있음
    - 팔로우가 많다고 노래가 인기 있는 것은 아님




### 5. 데이터 정제
> **불필요한 컬럼 결정**

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

1. Feature importance 확인을 통한 학습시킬 최종 컬럼 선정
2. 시대별 음악적 선호도 분석을 통한 유행할 음악 예측



## 🛠️ 사용 기술

- **언어**: Python
- **라이브러리**: pandas, numpy, matplotlib, seaborn
- **환경**: Jupyter Notebook





---

*이 프로젝트는 시대별 음악 트렌드 변화를 데이터 과학적 방법론으로 분석하는 것을 목표로 합니다.*
