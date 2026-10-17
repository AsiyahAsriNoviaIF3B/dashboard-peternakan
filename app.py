import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Data Peternakan",
    page_icon="🐄",
    layout="wide",
)

sns.set_theme(style="whitegrid")


@st.cache_data
def buat_data(jumlah=600):
    """Membuat data contoh/simulasi untuk demonstrasi dashboard.

    Data ini bukan data peternakan riil. Ganti fungsi ini atau unggah CSV
    milik sendiri saat data asli sudah tersedia.
    """
    rng = np.random.default_rng(42)
    jenis_list = np.array(["Sapi Perah", "Kambing Perah", "Ayam Petelur"])
    jenis = rng.choice(jenis_list, size=jumlah, p=[0.35, 0.25, 0.40])
    umur = np.where(
        jenis == "Ayam Petelur",
        rng.integers(4, 30, size=jumlah),
        np.where(jenis == "Sapi Perah", rng.integers(12, 120, size=jumlah), rng.integers(6, 84, size=jumlah)),
    )
    jk = rng.choice(["Jantan", "Betina"], size=jumlah, p=[0.28, 0.72])

    berat = np.empty(jumlah, dtype=float)
    m_sapi = jenis == "Sapi Perah"
    m_kambing = jenis == "Kambing Perah"
    m_ayam = jenis == "Ayam Petelur"
    berat[m_sapi] = rng.normal(450, 75, m_sapi.sum())
    berat[m_kambing] = rng.normal(38, 10, m_kambing.sum())
    berat[m_ayam] = rng.normal(1.8, 0.35, m_ayam.sum())
    berat = np.clip(berat, 0.5, None).round(1)

    kesehatan = rng.choice(["Sehat", "Perlu Pemantauan", "Sakit"], size=jumlah, p=[0.78, 0.16, 0.06])
    vaksin = rng.choice(["Sudah", "Belum"], size=jumlah, p=[0.84, 0.16])
    farm = rng.choice(["Farm A", "Farm B", "Farm C", "Farm D"], size=jumlah)

    pakan = np.empty(jumlah, dtype=float)
    pakan[m_sapi] = rng.normal(12, 3, m_sapi.sum())
    pakan[m_kambing] = rng.normal(2.2, 0.7, m_kambing.sum())
    pakan[m_ayam] = rng.normal(0.12, 0.03, m_ayam.sum())
    pakan = np.clip(pakan, 0.02, None).round(2)

    susu = np.zeros(jumlah, dtype=float)
    susu[m_sapi] = np.clip(rng.normal(14, 4, m_sapi.sum()), 0, None)
    susu[m_kambing] = np.clip(rng.normal(1.5, 0.5, m_kambing.sum()), 0, None)
    telur = np.zeros(jumlah, dtype=float)
    telur[m_ayam] = np.clip(rng.normal(0.82, 0.15, m_ayam.sum()), 0, 1).round(2)

    biaya_pakan = pakan * np.where(m_sapi, 3500, np.where(m_kambing, 3000, 9000)) * 30
    pendapatan = (susu * np.where(m_sapi, 18000, 16000) * 30) + (telur * 1900 * 30)
    biaya_operasional = biaya_pakan + rng.uniform(50000, 250000, size=jumlah)

    return pd.DataFrame({
        "ID Ternak": [f"TRN-{i:04d}" for i in range(1, jumlah + 1)],
        "Jenis Ternak": jenis,
        "Umur (bulan)": umur,
        "Jenis Kelamin": jk,
        "Berat (kg)": berat,
        "Status Kesehatan": kesehatan,
        "Status Vaksinasi": vaksin,
        "Lokasi Farm": farm,
        "Konsumsi Pakan (kg/hari)": pakan,
        "Produksi Susu (liter/hari)": susu.round(2),
        "Produksi Telur (butir/ekor/hari)": telur,
        "Estimasi Biaya Bulanan (Rp)": biaya_operasional.round(0).astype(int),
        "Estimasi Pendapatan Bulanan (Rp)": pendapatan.round(0).astype(int),
    })


df = buat_data()

st.title("🐄 Dashboard Visualisasi Data Peternakan")
st.markdown(
    "Dashboard interaktif untuk memantau populasi ternak, kesehatan, konsumsi pakan, "
    "produksi, dan estimasi finansial."
)
st.warning(
    "Catatan akademik: data di dashboard ini adalah **data simulasi untuk praktikum**, bukan "
    "data peternakan riil. Gunakan data lapangan/CSV asli untuk analisis faktual."
)

# Sidebar: kontrol/filter dashboard
st.sidebar.header("Filter Data")
pilihan_jenis = st.sidebar.multiselect(
    "Jenis ternak",
    options=sorted(df["Jenis Ternak"].unique()),
    default=sorted(df["Jenis Ternak"].unique()),
)
pilihan_farm = st.sidebar.multiselect(
    "Lokasi farm",
    options=sorted(df["Lokasi Farm"].unique()),
    default=sorted(df["Lokasi Farm"].unique()),
)
pilihan_kesehatan = st.sidebar.multiselect(
    "Status kesehatan",
    options=sorted(df["Status Kesehatan"].unique()),
    default=sorted(df["Status Kesehatan"].unique()),
)

filtered = df[
    df["Jenis Ternak"].isin(pilihan_jenis)
    & df["Lokasi Farm"].isin(pilihan_farm)
    & df["Status Kesehatan"].isin(pilihan_kesehatan)
].copy()

if filtered.empty:
    st.info("Tidak ada data yang sesuai dengan filter. Silakan ubah pilihan di sidebar.")
    st.stop()

# KPI
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Ternak", f"{len(filtered):,}")
k2.metric("Berat Rata-rata", f"{filtered['Berat (kg)'].mean():,.1f} kg")
k3.metric("Perlu Perhatian", f"{filtered['Status Kesehatan'].isin(['Perlu Pemantauan', 'Sakit']).sum():,}")
cakupan_vaksin = (filtered["Status Vaksinasi"].eq("Sudah").mean() * 100)
k4.metric("Cakupan Vaksinasi", f"{cakupan_vaksin:.1f}%")

st.divider()

# Grafik distribusi populasi dan kesehatan
kol1, kol2 = st.columns(2)
with kol1:
    st.subheader("1. Distribusi Populasi Ternak")
    distribusi = filtered["Jenis Ternak"].value_counts()
    fig_pie, ax_pie = plt.subplots(figsize=(6, 4))
    ax_pie.pie(distribusi.values, labels=distribusi.index, autopct="%1.1f%%", startangle=90)
    ax_pie.set_title("Proporsi berdasarkan jenis ternak")
    st.pyplot(fig_pie, use_container_width=True)
    plt.close(fig_pie)

with kol2:
    st.subheader("2. Kondisi Kesehatan Hewan")
    sehat_data = (
        filtered.groupby(["Jenis Ternak", "Status Kesehatan"])
        .size().reset_index(name="Jumlah")
    )
    fig_health, ax_health = plt.subplots(figsize=(7, 4))
    sns.barplot(data=sehat_data, x="Jenis Ternak", y="Jumlah", hue="Status Kesehatan", ax=ax_health)
    ax_health.set_title("Status kesehatan per jenis ternak")
    ax_health.set_xlabel("Jenis ternak")
    ax_health.set_ylabel("Jumlah hewan")
    ax_health.tick_params(axis="x", rotation=10)
    st.pyplot(fig_health, use_container_width=True)
    plt.close(fig_health)

# Grafik hubungan dan konsumsi pakan
kol3, kol4 = st.columns(2)
with kol3:
    st.subheader("3. Hubungan Umur dan Berat")
    fig_scatter, ax_scatter = plt.subplots(figsize=(7, 4))
    sns.scatterplot(
        data=filtered,
        x="Umur (bulan)",
        y="Berat (kg)",
        hue="Jenis Ternak",
        alpha=0.7,
        ax=ax_scatter,
    )
    ax_scatter.set_title("Sebaran umur terhadap berat ternak")
    st.pyplot(fig_scatter, use_container_width=True)
    plt.close(fig_scatter)

with kol4:
    st.subheader("4. Rata-rata Konsumsi Pakan")
    pakan_data = filtered.groupby("Jenis Ternak", as_index=False)["Konsumsi Pakan (kg/hari)"].mean()
    fig_feed, ax_feed = plt.subplots(figsize=(7, 4))
    sns.barplot(data=pakan_data, x="Jenis Ternak", y="Konsumsi Pakan (kg/hari)", ax=ax_feed)
    ax_feed.set_title("Rata-rata konsumsi pakan per ekor")
    ax_feed.set_xlabel("Jenis ternak")
    ax_feed.set_ylabel("Kg per hari")
    ax_feed.tick_params(axis="x", rotation=10)
    st.pyplot(fig_feed, use_container_width=True)
    plt.close(fig_feed)

st.divider()
st.subheader("5. Matriks Korelasi Variabel Numerik")
variabel_numerik = [
    "Umur (bulan)", "Berat (kg)", "Konsumsi Pakan (kg/hari)",
    "Produksi Susu (liter/hari)", "Produksi Telur (butir/ekor/hari)",
    "Estimasi Biaya Bulanan (Rp)", "Estimasi Pendapatan Bulanan (Rp)",
]
fig_corr, ax_corr = plt.subplots(figsize=(11, 6))
sns.heatmap(filtered[variabel_numerik].corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", ax=ax_corr)
ax_corr.set_title("Korelasi antarvariabel numerik")
st.pyplot(fig_corr, use_container_width=True)
plt.close(fig_corr)
st.caption("Korelasi menunjukkan hubungan statistik antarvariabel dan tidak otomatis membuktikan sebab-akibat.")

# Tabel, ekspor data
st.divider()
st.subheader("6. Data Ternak")
with st.expander("Tampilkan tabel data sesuai filter"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="Unduh data hasil filter (CSV)",
    data=csv,
    file_name="data_peternakan_terfilter.csv",
    mime="text/csv",
)

st.caption("Praktikum Visualisasi Data | Python, Pandas, NumPy, Matplotlib, Seaborn, dan Streamlit")
