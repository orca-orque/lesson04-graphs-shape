import streamlit as st
import pandas as pd
import numpy as np
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
# 구역 2. 장르 안의 영화별 총 관객 (트리맵)
# ------------------------------------------------------------
st.header("2. 장르 안의 영화별 총 관객")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>"
)
fig_treemap.update_layout(margin=dict(t=30, l=10, r=10, b=10))

st.plotly_chart(fig_treemap, use_container_width=True)

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 구역 3. 총 관객수 분포 (히스토그램)
# ------------------------------------------------------------
st.header("3. 총 관객수 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=20,
)
fig_hist.update_traces(
    hovertemplate="구간: %{x}<br>편수: %{y}편<extra></extra>"
)
fig_hist.update_layout(
    xaxis_title="총 관객수",
    yaxis_title="영화 편수",
    bargap=0.05,
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 많은 영화가 몰려 있는 구간 계산
counts, bin_edges = np.histogram(df["total_audi"], bins=20)
top_bin_idx = counts.argmax()
bin_low, bin_high = bin_edges[top_bin_idx], bin_edges[top_bin_idx + 1]

# 총 관객이 가장 많은 영화
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"대부분의 영화는 총 관객 **{bin_low:,.0f}명 ~ {bin_high:,.0f}명** 구간에 몰려 있고, "
    f"총 관객이 가장 많은 영화는 **{top_movie['movieNm']}**"
    f"({top_movie['total_audi']:,.0f}명)입니다."
)

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 구역 4. 개봉일 스크린수와 총 관객의 관계 (산점도)
# ------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}<br>총 관객: %{y:,}명<extra></extra>"
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수",
    legend_title_text="장르",
)

st.plotly_chart(fig_scatter, use_container_width=True)

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 구역 5. (다음 그래프를 위한 자리)
# ------------------------------------------------------------
st.header("5. ")

st.info("다음 그래프가 이 구역에 추가될 예정입니다.")

with st.container(border=True):
    st.markdown("**이 그래프로 알 수 있는 것:** ")
