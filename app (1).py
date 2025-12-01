import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# LOAD DATA
# ==========================
data = pd.read_csv("data_bersih.csv", sep=";",decimal=",")
df = pd.DataFrame(data)

st.title("📊 Dashboard Analisis Antropometri Anak")
st.markdown("---")


# ========================================================
# 1. CARD RINGKASAN
# ========================================================
st.header("1. Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jumlah Observasi", len(df))

with col2:
    st.metric("Rata-rata Tinggi Badan", round(df["J02B"].mean(), 2))

with col3:
    st.metric("Rata-rata Berat Badan Sekarang", round(df["J01C"].mean(), 2))

with col4:
    st.metric("Rata-rata Berat Badan Lahir", round(df["I05A"].mean(), 2))


st.markdown("---")


# ========================================================
# 2. DISTRIBUSI TINGGI & BERAT BADAN (DENGAN FILTER)
# ========================================================
st.header("2. Distribusi Tinggi & Berat Badan")

gender_filter = st.selectbox(
    "Pilih Jenis Kelamin",
    options=["Semua", "Laki-laki (1)", "Perempuan (2)"]
)

min_rt, max_rt = st.slider(
    "Filter Banyak Anggota Rumah Tangga (B3R1)",
    int(df["B3R1"].min()), int(df["B3R1"].max()),
    (int(df["B3R1"].min()), int(df["B3R1"].max()))
)

df_filtered = df.copy()

if gender_filter == "Laki-laki (1)":
    df_filtered = df_filtered[df_filtered["B4K4"] == 1]
elif gender_filter == "Perempuan (2)":
    df_filtered = df_filtered[df_filtered["B4K4"] == 2]

df_filtered = df_filtered[
    (df_filtered["B3R1"] >= min_rt) & (df_filtered["B3R1"] <= max_rt)
]

col5, col6 = st.columns(2)
with col5:
    fig1 = px.histogram(df_filtered, x="J02B", title="Distribusi Tinggi Badan (J02B)")
    st.plotly_chart(fig1)

with col6:
    fig2 = px.histogram(df_filtered, x="J01C", title="Distribusi Berat Badan Sekarang (J01C)")
    st.plotly_chart(fig2)


st.markdown("---")


# ========================================================
# 3. PERBANDINGAN LAKI-LAKI VS PEREMPUAN
# ========================================================
st.header("3. Perbandingan Antar Jenis Kelamin")

metric = st.selectbox(
    "Pilih Metrik",
    ["Tinggi Badan (J02B)", "Berat Badan Sekarang (J01C)", "Berat Badan Lahir (I05A)"]
)

col_map = {
    "Tinggi Badan (J02B)": "J02B",
    "Berat Badan Sekarang (J01C)": "J01C",
    "Berat Badan Lahir (I05A)": "I05A"
}

selected_col = col_map[metric]

fig_bar = px.bar(
    df,
    x="B4K4",
    y=selected_col,
    color="B4K4",
    barmode="group",
    title=f"Rata-rata {metric} Berdasarkan Jenis Kelamin"
)
st.plotly_chart(fig_bar)

fig_box = px.box(
    df,
    x="B4K4",
    y=selected_col,
    color="B4K4",
    title=f"Boxplot {metric} Berdasarkan Jenis Kelamin"
)
st.plotly_chart(fig_box)


st.markdown("---")


# ========================================================
# 4. PENGARUH BANYAK ANGGOTA RUMAH TANGGA
# ========================================================
st.header("4. Pengaruh Banyak Anggota Rumah Tangga (B3R1)")

df_grouped = df.groupby("B3R1")[["J02B", "J01C"]].mean().reset_index()

fig_line = px.line(
    df_grouped,
    x="B3R1",
    y="J02B",
    title="Hubungan Banyak Anggota RT vs Rata-rata Tinggi Badan"
)
st.plotly_chart(fig_line)

fig_line2 = px.line(
    df_grouped,
    x="B3R1",
    y="J01C",
    title="Hubungan Banyak Anggota RT vs Rata-rata Berat Badan"
)
st.plotly_chart(fig_line2)


st.markdown("---")


# ========================================================
# 5. KORELASI BERAT LAHIR VS BERAT SEKARANG
# ========================================================
st.header("5. Korelasi Berat Badan Lahir vs Berat Sekarang")

fig_scatter = px.scatter(
    df,
    x="I05A",
    y="J01C",
    color="B4K4",
    trendline="ols",
    title="Scatter Plot Berat Lahir (I05A) vs Berat Sekarang (J01C)"
)
st.plotly_chart(fig_scatter)

