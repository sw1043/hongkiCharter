################################################################################
##                  pyinstaller --onefile hongkiCharter_pc.py                  ##
################################################################################
INFO_STR: str = """

*****************************************************
* hongkiCharter ver 1.1                             *
* first released at 2025-08-26                      *
* 제25회 정기공연 <나무는 서서 죽는다>를 준비하며   *
* by 리버액트 12기 손상원                           *
*****************************************************
"""
################################################################################
print(INFO_STR)

import sys, os
import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator
import requests
import io
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 
import json
import re

import math
plt.rc('font', family='Malgun Gothic')

print(' Program loaded...')

KST = ZoneInfo("Asia/Seoul")

def resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False):
        # .exe 폴더에 있는 conf.txt
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    # 개발 모드: 소스 파일 폴더
    return os.path.join(os.path.dirname(__file__), relative_path)

def load_conf(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        txt = f.read()

    # 1) 등호(=)를 콜론(:)으로 치환
    txt = re.sub(r'=\s*', ': ', txt)
    # 2) 전체를 중괄호로 감싸서 JSON 객체로 만들고
    txt = '{' + txt + '}'
    # 3) 마지막에 남은 불필요한 쉼표 제거
    txt = re.sub(r',\s*}', '}', txt)

    return json.loads(txt)

################################################################################

conf = load_conf(resource_path('conf.txt'))

current_play    = conf['current_play']
sheet_url       = conf['sheet_url']
gid             = conf['gid']
plays: dict     = conf['plays']
left_lim: int   = conf['left_lim']
right_lim: int  = conf['right_lim']
current_initial_day = datetime.strptime(plays[current_play]["initial_day"], "%Y-%m-%d").replace(tzinfo=KST)

left_dt = (current_initial_day - timedelta(days=left_lim)).replace(
    hour=0, minute=0, second=0, microsecond=0, tzinfo=None
)
right_dt = (current_initial_day + timedelta(days=right_lim)).replace(
    hour=0, minute=0, second=0, microsecond=0, tzinfo=None
)

print(" Configuration loaded...")

################################################################################
def dday_formatter(target_day):
    d_day = current_initial_day.replace(tzinfo=None)
    diff_in_days = (target_day - d_day).days

    if diff_in_days < -left_lim or diff_in_days > right_lim:
        return ""
    elif diff_in_days >= 0:
        return f"{diff_in_days + 1}일차"
    elif diff_in_days < 0:
        return f"D-{-diff_in_days}"
    else:
        return f"D+{diff_in_days-1}"
################################################################################

req_url:str     = f"{sheet_url}/export?gid={gid}&format=xlsx"
r               = requests.get(req_url)
data            = r.content
currentTime     = datetime.now(KST)
df_0: pd.DataFrame = pd.read_excel(io.BytesIO(data))

print(' Data loaded from Google Sheets...')

t_cols = [f"{title} timestp" for title in plays.keys()]
df_0[t_cols] = (df_0[t_cols]
    .apply(pd.to_datetime)
    .apply(lambda s: s.dt.tz_localize("Asia/Seoul"))
)

for title in plays.keys():
    date_gap = current_initial_day - datetime.strptime(plays[title]["initial_day"], "%Y-%m-%d").replace(tzinfo=KST)
    df_0[f"{title} adj_timestp"] = df_0[f"{title} timestp"] + date_gap

labels:list = list()
for title in plays.keys():
    labels.extend([title] * df_0[f"{title} adj_timestp"].notna().sum())

df_long:pd.DataFrame = pd.DataFrame({
    "adj_timestp": pd.concat([df_0[f"{title} adj_timestp"].dropna() for title in plays.keys()], ignore_index=True),
    "cmltv": pd.concat([df_0[f"{title} 누계"].dropna() for title in plays.keys()], ignore_index=True),
    "공연": labels
}).dropna(axis=0)
df_long['gap_from_initial'] = (df_long['adj_timestp'] - current_initial_day).dt.days
df_long['adj_timestp'] = (
    df_long['adj_timestp']
        .dt.tz_convert("Asia/Seoul")  # (혹시 다른 tz였다면)
        .dt.tz_localize(None)         # tz정보 제거
)

print(' Data transformed...')

#####################################################################################

plt.figure(figsize=(8, 6))

cp_dct = {title: plays[title]["color"] for title in plays.keys()}
sns.scatterplot(data=df_long, x="adj_timestp", y="cmltv",
                hue="공연", palette=cp_dct, s=25, alpha=0.5)

plt.gca().xaxis.set_major_locator(DayLocator())
# plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: dday_formatter(pd.to_datetime(x, unit='D')))) # type: ignore

ax = plt.gca()

def dday_tickfmt(x, pos):
    dt = mdates.num2date(x, tz=KST)           # matplotlib 내부 float -> datetime
    ts = pd.Timestamp(dt.date())      # 날짜만 취해 naive Timestamp로
    return dday_formatter(ts)

ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))  # 눈금: 24시간 간격
ax.xaxis.set_minor_locator(mdates.HourLocator(interval=12))  # 격자선: 12시간 간격
ax.xaxis.set_major_formatter(plt.FuncFormatter(dday_tickfmt)) # type: ignore

plt.grid(True, alpha=0.3, which='major')  
plt.grid(True, alpha=0.1, which='minor')  

ax.axvline(current_initial_day.replace(tzinfo=None), color='gray', linestyle='--', linewidth=1)     # type: ignore
current_naive = currentTime.replace(tzinfo=None)
ax.axvline(current_naive, color='firebrick', linestyle='--', linewidth=1, alpha=0.7)                # type: ignore

ax.set_xlim(left_dt, right_dt)                                                                      # type: ignore
ax.autoscale(False)
ax.margins(x=0)

plt.ylim(0, math.ceil(df_long['cmltv'].max()/100)*100)

plt.title(f"[{currentTime.strftime('%m/%d %H:%M')}] 공연별 예매 추이 비교")
plt.xlabel("")
plt.ylabel("")

print(' Plot generated.\n')
plt.savefig(resource_path(f"plots\\{current_play}at{currentTime.strftime('%Y%m%d_%H%M')}.png"), dpi=120)
plt.show()

input(" Press Enter to exit...")