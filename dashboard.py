import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 8px;
            padding: 12px 16px;
        }
        button[data-baseweb="tab"] { font-size: 14px; font-weight: 500; }
    </style>
    """,
    unsafe_allow_html=True
)

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.family": "sans-serif", "axes.edgecolor": "#d1d5db"})

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_ORDER = ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]
DEMAND_ORDER = ["Low Demand", "Medium Demand", "High Demand"]
PALETTE_2 = ["#93c5fd", "#1d4ed8"]


# ==========================================
# MEMUAT DATA
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, "bike_sharing_clean.csv"))
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["demand_category"] = pd.cut(
        df["cnt"],
        bins=[0, 3000, 6000, float("inf")],
        labels=DEMAND_ORDER
    )
    df["season_weather"] = df["season_name"] + " - " + df["weather_name"]
    return df


df = load_data()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Filter")

    min_date = df["dteday"].min().date()
    max_date = df["dteday"].max().date()
    selected_date_range = st.date_input(
        "Rentang Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(selected_date_range, (list, tuple)) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date, end_date = min_date, max_date

    year_options = sorted(df["year"].unique())
    selected_year = st.multiselect("Tahun", options=year_options, default=year_options)

    season_options = [s for s in SEASON_ORDER if s in df["season_name"].unique()]
    selected_season = st.multiselect("Musim", options=season_options, default=season_options)

    weather_options = [w for w in WEATHER_ORDER if w in df["weather_name"].unique()]
    selected_weather = st.multiselect("Kondisi Cuaca", options=weather_options, default=weather_options)

fdf = df[
    (df["dteday"].dt.date >= start_date)
    & (df["dteday"].dt.date <= end_date)
    & (df["year"].isin(selected_year))
    & (df["season_name"].isin(selected_season))
    & (df["weather_name"].isin(selected_weather))
]

# ==========================================
# HEADER & METRIK
# ==========================================
st.title("Bike Sharing Dashboard")
st.caption("Analisis penyewaan sepeda harian periode 2011–2012: pengaruh musim, cuaca, dan jenis pengguna.")

if fdf.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan sesuaikan pilihan di sidebar.")
    st.stop()

total_rentals = int(fdf["cnt"].sum())
total_registered = int(fdf["registered"].sum())
total_casual = int(fdf["casual"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Penyewaan", f"{total_rentals:,}")
c2.metric("Rata-rata Harian", f"{fdf['cnt'].mean():,.0f}")
c3.metric("Registered", f"{total_registered:,}", f"{total_registered / total_rentals * 100:.1f}%")
c4.metric("Casual", f"{total_casual:,}", f"{total_casual / total_rentals * 100:.1f}%")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "Pengaruh Musim & Cuaca",
    "Analisis Jenis Pengguna",
    "Analisis Lanjutan",
    "Data & Kesimpulan"
])


def bar_with_labels(data, x, y, title, xlabel, ylabel, order=None, figsize=(6, 4)):
    fig, ax = plt.subplots(figsize=figsize, dpi=100)
    bars = sns.barplot(
        data=data, x=x, y=y, hue=x, legend=False,
        palette="Blues_r", order=order, ax=ax
    )
    ax.bar_label(bars.containers[0], fmt="%.0f", padding=3, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_ylim(0, data[y].max() * 1.15)
    plt.tight_layout()
    return fig


# ----------------------------------------------------
# TAB 1: PENGARUH MUSIM & CUACA 
# ----------------------------------------------------
with tab1:
    st.subheader("Perbedaan rata-rata penyewaan berdasarkan musim dan kondisi cuaca")

    season_summary = (
        fdf.groupby("season_name")["cnt"].mean().reset_index().sort_values("cnt", ascending=False)
    )
    weather_summary = (
        fdf.groupby("weather_name")["cnt"].mean().reset_index().sort_values("cnt", ascending=False)
    )

    col_s, col_w = st.columns(2)
    with col_s:
        fig = bar_with_labels(
            season_summary, "season_name", "cnt",
            "Rata-rata Penyewaan per Musim", "Musim", "Rata-rata Penyewaan / Hari"
        )
        st.pyplot(fig)
        plt.close(fig)
    with col_w:
        fig = bar_with_labels(
            weather_summary, "weather_name", "cnt",
            "Rata-rata Penyewaan per Kondisi Cuaca", "Kondisi Cuaca", "Rata-rata Penyewaan / Hari"
        )
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("##### Kombinasi Musim dan Cuaca")
    combo_pivot = fdf.pivot_table(
        index="season_name", columns="weather_name", values="cnt", aggfunc="mean"
    )
    combo_pivot = combo_pivot.reindex(
        index=[s for s in SEASON_ORDER if s in combo_pivot.index],
        columns=[w for w in WEATHER_ORDER if w in combo_pivot.columns]
    )
    fig, ax = plt.subplots(figsize=(9, 3.8), dpi=100)
    sns.heatmap(combo_pivot, annot=True, fmt=".0f", cmap="Blues", linewidths=0.5, ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Musim")
    ax.set_title("Rata-rata Penyewaan per Kombinasi Musim dan Cuaca", fontsize=11, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Tabel statistik per musim dan cuaca"):
        st.dataframe(
            fdf.groupby("season_name")["cnt"].agg(["mean", "sum", "min", "max"])
            .round(2).sort_values("mean", ascending=False),
            use_container_width=True
        )
        st.dataframe(
            fdf.groupby("weather_name")["cnt"].agg(["mean", "sum", "min", "max"])
            .round(2).sort_values("mean", ascending=False),
            use_container_width=True
        )

    top_s, low_s = season_summary.iloc[0], season_summary.iloc[-1]
    top_w, low_w = weather_summary.iloc[0], weather_summary.iloc[-1]
    st.info(
        f"Musim **{top_s['season_name']}** memiliki rata-rata penyewaan tertinggi ({top_s['cnt']:,.0f}), "
        f"sedangkan **{low_s['season_name']}** terendah ({low_s['cnt']:,.0f}). "
        f"Cuaca **{top_w['weather_name']}** tertinggi ({top_w['cnt']:,.0f}) dan "
        f"**{low_w['weather_name']}** terendah ({low_w['cnt']:,.0f})."
    )

# ----------------------------------------------------
# TAB 2: ANALISIS JENIS PENGGUNA
# ----------------------------------------------------
with tab2:
    st.subheader("Perbedaan pengguna casual dan registered: hari kerja vs hari non-kerja")

    col_a, col_b = st.columns(2)

    with col_a:
        avg_wd = fdf.groupby("workingday_name")[["casual", "registered"]].mean().reset_index()
        avg_melt = avg_wd.melt(
            id_vars="workingday_name", var_name="Tipe Pengguna", value_name="Rata-rata"
        )
        fig, ax = plt.subplots(figsize=(6.5, 4), dpi=100)
        sns.barplot(
            data=avg_melt, x="workingday_name", y="Rata-rata",
            hue="Tipe Pengguna", palette=PALETTE_2, ax=ax
        )
        for c in ax.containers:
            ax.bar_label(c, fmt="%.0f", padding=3, fontsize=9)
        ax.set_title("Rata-rata Pengguna per Jenis Hari", fontsize=11, fontweight="bold")
        ax.set_xlabel("Jenis Hari")
        ax.set_ylabel("Rata-rata Pengguna / Hari")
        ax.set_ylim(0, avg_melt["Rata-rata"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_b:
        tot_wd = fdf.groupby("workingday_name")[["casual", "registered"]].sum().reset_index()
        tot_melt = tot_wd.melt(
            id_vars="workingday_name", var_name="Tipe Pengguna", value_name="Total"
        )
        fig, ax = plt.subplots(figsize=(6.5, 4), dpi=100)
        sns.barplot(
            data=tot_melt, x="workingday_name", y="Total",
            hue="Tipe Pengguna", palette=PALETTE_2, ax=ax
        )
        for c in ax.containers:
            ax.bar_label(c, fmt="%.0f", padding=3, fontsize=8)
        ax.set_title("Total Pengguna per Jenis Hari", fontsize=11, fontweight="bold")
        ax.set_xlabel("Jenis Hari")
        ax.set_ylabel("Total Pengguna")
        ax.set_ylim(0, tot_melt["Total"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    col_c, col_d = st.columns(2)

    with col_c:
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.pie(
            [total_casual, total_registered],
            labels=["Casual", "Registered"],
            autopct="%1.1f%%", startangle=90, colors=PALETTE_2,
            wedgeprops={"width": 0.45, "edgecolor": "white"}
        )
        ax.set_title("Kontribusi Jenis Pengguna", fontsize=11, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_d:
        year_avg = fdf.groupby("year")[["casual", "registered"]].mean().reset_index()
        year_melt = year_avg.melt(
            id_vars="year", var_name="Tipe Pengguna", value_name="Rata-rata"
        )
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        sns.barplot(
            data=year_melt, x="year", y="Rata-rata",
            hue="Tipe Pengguna", palette=PALETTE_2, ax=ax
        )
        for c in ax.containers:
            ax.bar_label(c, fmt="%.0f", padding=3, fontsize=9)
        ax.set_title("Rata-rata Pengguna per Tahun", fontsize=11, fontweight="bold")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Rata-rata Pengguna / Hari")
        ax.set_ylim(0, year_melt["Rata-rata"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    avg_idx = avg_wd.set_index("workingday_name")
    if {"Working Day", "Non-Working Day"}.issubset(avg_idx.index):
        st.info(
            f"Pengguna **casual** rata-rata {avg_idx.loc['Non-Working Day', 'casual']:,.0f} pada hari non-kerja "
            f"vs {avg_idx.loc['Working Day', 'casual']:,.0f} pada hari kerja. "
            f"Pengguna **registered** rata-rata {avg_idx.loc['Working Day', 'registered']:,.0f} pada hari kerja "
            f"vs {avg_idx.loc['Non-Working Day', 'registered']:,.0f} pada hari non-kerja."
        )

# ----------------------------------------------------
# TAB 3: ANALISIS LANJUTAN
# ----------------------------------------------------
with tab3:
    st.subheader("Korelasi faktor cuaca dengan jumlah penyewaan")

    corr = fdf[["temp", "hum", "windspeed", "cnt"]].corr()
    col_h, col_sc = st.columns(2)

    with col_h:
        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=100)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
        ax.set_title("Korelasi Variabel Cuaca dengan cnt", fontsize=11, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_sc:
        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=100)
        sns.regplot(
            data=fdf, x="temp", y="cnt",
            scatter_kws={"alpha": 0.4, "color": "#93c5fd"},
            line_kws={"color": "#1d4ed8"}, ax=ax
        )
        ax.set_title("Suhu vs Jumlah Penyewaan", fontsize=11, fontweight="bold")
        ax.set_xlabel("Suhu (ternormalisasi)")
        ax.set_ylabel("Jumlah Penyewaan")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.caption("Korelasi menunjukkan keterkaitan antarvariabel, bukan hubungan sebab-akibat.")

    st.markdown("---")
    st.subheader("Segmentasi tingkat permintaan")
    st.caption("Low Demand: ≤ 3.000 | Medium Demand: 3.001–6.000 | High Demand: > 6.000 penyewaan per hari")

    demand_counts = (
        fdf["demand_category"].value_counts().reindex(DEMAND_ORDER).fillna(0).reset_index()
    )
    demand_counts.columns = ["Kategori", "Jumlah Hari"]

    col_d1, col_d2 = st.columns([1, 2])
    with col_d1:
        fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=100)
        bars = sns.barplot(
            data=demand_counts, x="Kategori", y="Jumlah Hari",
            hue="Kategori", legend=False, palette="Blues", ax=ax
        )
        ax.bar_label(bars.containers[0], fmt="%.0f", padding=3, fontsize=9)
        ax.set_title("Jumlah Hari per Kategori", fontsize=11, fontweight="bold")
        ax.set_xlabel("")
        plt.xticks(rotation=15)
        ax.set_ylim(0, demand_counts["Jumlah Hari"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_d2:
        demand_pivot = pd.crosstab(fdf["season_weather"], fdf["demand_category"])
        demand_pivot = demand_pivot.reindex(columns=DEMAND_ORDER, fill_value=0)
        fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)
        demand_pivot.plot(
            kind="bar", stacked=True, ax=ax,
            color=["#bfdbfe", "#60a5fa", "#1d4ed8"]
        )
        ax.set_title("Distribusi Kategori Permintaan per Musim dan Cuaca", fontsize=11, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("Jumlah Hari")
        plt.xticks(rotation=45, ha="right")
        ax.legend(title="Kategori")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ----------------------------------------------------
# TAB 4: DATA & KESIMPULAN
# ----------------------------------------------------
with tab4:
    st.subheader("Data Terfilter")
    preview_cols = [
        "dteday", "season_name", "weather_name", "workingday_name",
        "temp", "hum", "windspeed", "casual", "registered", "cnt", "demand_category"
    ]
    st.dataframe(fdf[preview_cols], use_container_width=True, hide_index=True)
    st.download_button(
        "Unduh Data (CSV)",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="bike_sharing_filtered.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("Kesimpulan")
    st.caption("Berdasarkan seluruh data periode 2011–2012.")

    k1, k2 = st.columns(2)
    with k1:
        st.markdown(
            """
            **Pertanyaan 1 – Musim dan cuaca**
            - Rata-rata penyewaan tertinggi pada musim **Fall** (5.644), disusul Summer (4.992), Winter (4.728), dan terendah **Spring** (2.604).
            - Cuaca **Clear** tertinggi (4.877), Mist/Cloudy (4.036), dan **Light Rain/Snow** terendah (1.803).
            - Kombinasi **Fall + Clear** menghasilkan rata-rata tertinggi (5.878).

            **Analisis korelasi**
            - Suhu berkorelasi positif cukup kuat dengan penyewaan (0,63).
            - Kelembapan (-0,10) dan kecepatan angin (-0,23) berkorelasi negatif lemah.
            """
        )
    with k2:
        st.markdown(
            """
            **Pertanyaan 2 – Jenis pengguna**
            - **Registered** mendominasi: 2.672.662 penyewaan (81,17%) vs **Casual** 620.017 (18,83%).
            - Casual lebih tinggi pada hari non-kerja (1.371 vs 607), registered lebih tinggi pada hari kerja (3.978 vs 2.959).
            - Rata-rata penyewaan meningkat dari 3.406 (2011) menjadi 5.600 (2012).

            **Segmentasi permintaan**
            - Medium Demand terbanyak (379 hari), High Demand 180 hari, Low Demand 172 hari.
            - High Demand paling sering pada **Fall + Clear** (61 hari); Low Demand paling sering pada **Spring + Clear** (65 hari).
            """
        )

    st.subheader("Rekomendasi")
    st.markdown(
        """
        1. Tingkatkan kesiapan armada pada musim Fall dan Summer saat cuaca cerah; sesuaikan jumlah armada pada musim Spring.
        2. Prioritaskan ketersediaan sepeda bagi pengguna registered pada hari kerja, dan arahkan promosi kepada pengguna casual pada hari non-kerja.
        3. Gunakan data suhu, kelembapan, dan kecepatan angin sebagai pendukung perkiraan permintaan.
        4. Pantau kategori permintaan secara berkala, terutama periode Low Demand pada musim Spring.
        """
    )

st.markdown("---")
st.caption("Data Analysis Project. Sumber Data : Bike Sharing Dataset.")
