# hongkiCharter

`hongkiCharter`은 Google Sheets를 활용해 리버액트 정기공연의 공연 일정과 예매 현황을 관리·시각화하는 작은 유틸리티입니다.

## 주요 기능

- `conf.txt`에서 설정 정보(공연, 날짜, 색상 등) 읽어오기  
- 지정된 Google Sheets 문서에서 일정 데이터 불러오기  
- 각 공연을 설정된 색상으로 강조 표시  
- `left_lim`/`right_lim`으로 달력 뷰의 좌우 범위 조정  

## 작동 예시

<img width="800" height="577" alt="Image" src="https://github.com/user-attachments/assets/f58764d2-336e-493c-8fed-10228b2a6fc9" />

- 마스킹된 이미지입니다. 

## 설정 방법

모든 설정은 프로젝트 최상위의 `conf.txt` 파일에서 관리합니다.

- `current_play`: 현재 추적 중인 공연 이름  
- `sheet_url`   : 사용할 Google Sheets 문서 URL  
- `gid`         : 해당 시트의 ID  
- `plays`       : 각 공연별 시작일(`initial_day`)과 표시 색상(`color`)  
- `left_lim`    : 달력 뷰의 왼쪽 한계  
- `right_lim`   : 달력 뷰의 오른쪽 한계  

### conf.txt 예시

```json
{
  "current_play": "나서죽",
  "sheet_url": "https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "gid": "1111111111",
  "plays": {
    "여사말":   { "initial_day": "2024-09-04", "color": "forestgreen" },
    "밤산책":   { "initial_day": "2025-03-06", "color": "royalblue"  },
    "나서죽":   { "initial_day": "2025-09-01", "color": "orangered"  }
  },
  "left_lim":  11,
  "right_lim":  3
}
```

## 사용 방법

1. Google Forms와 연동된 Google Sheets를 형식에 맞게 가공합니다. 이건 방법을 명확하게 작성하기 귀찮아서... 그냥 연락주세요. 금방 하고 한번만 해놓으면 됩니다. 
2. `hongkiCharter_pc.exe` 파일과 같은 폴더에 `conf.txt`라는 이름으로 Google Sheets URL, GID, 공연 정보 등을 지정합니다.  
3. `hongkiCharter_pc.exe` 파일을 더블클릭하여 실행하면 이전 정기공연과 시간에 따른 예매자 수 추이를 비교할 수 있습니다. 

## 정보

- 제작자: 손상원, 리버액트 12기
- 문의: s.son7651@gmail.com
- 라이선스: MIT
