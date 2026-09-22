import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("최근 1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 요약 데이터를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 세로막대(|) 기호로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # 개봉일(여덟 자리 숫자)을 실제 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    return df


df = load_data()

st.divider()

# ------------------------------------------------------------
# 구역 1. 장르별 영화 편수
# ------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)
fig_genre.update_layout(legend_title_text="장르")

st.plotly_chart(fig_genre, use_container_width=True)

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 구역 2. (다음 그래프를 위한 자리)
# ------------------------------------------------------------
st.header("2. ")

st.info("다음 그래프가 이 구역에 추가될 예정입니다.")

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")
