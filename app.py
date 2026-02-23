import streamlit as st
import pandas as pd
import gspread
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="Portal Musholla At Taqwa", layout="wide")

# ======================================================
# 🎨 THEME HIJAU NU ELEGAN
# ======================================================

st.markdown("""
<style>

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

.main {
    background-color: #F3F8F4;
    animation: fadeIn 0.8s ease-in;
}

h1, h2, h3 {
    color: #0B6623;
    font-weight: 700;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0B6623;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Metric Card */
[data-testid="stMetric"] {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    border-left: 6px solid #1B8A3C;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.05);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 15px;
    padding: 10px;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ======================================================
# 🔐 GOOGLE SHEET CONNECTION
# ======================================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)

client = gspread.authorize(creds)

SPREADSHEET_ID = "1XTX9i9WHtGm6KkOfa01MpJuKYBODZXfH8-Z1FpF6BZo"
spreadsheet = client.open_by_key(SPREADSHEET_ID)

sheet_masuk = spreadsheet.worksheet("kas_masuk")
sheet_keluar = spreadsheet.worksheet("kas_keluar")
sheet_kegiatan = spreadsheet.worksheet("kegiatan")

data_masuk = pd.DataFrame(sheet_masuk.get_all_records())
data_keluar = pd.DataFrame(sheet_keluar.get_all_records())
data_kegiatan = pd.DataFrame(sheet_kegiatan.get_all_records())

# ======================================================
# 💰 PERHITUNGAN SALDO
# ======================================================

total_masuk = data_masuk["Jumlah"].sum() if not data_masuk.empty else 0
total_keluar = data_keluar["Jumlah"].sum() if not data_keluar.empty else 0
saldo = total_masuk - total_keluar

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ======================================================
# 📌 SIDEBAR
# ======================================================

st.sidebar.image("logo_nu.png", width=80)
st.sidebar.title("Musholla At Taqwa")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "Profil Musholla",
        "Manajemen Keuangan",
        "Jadwal Kegiatan",
        "Struktur Organisasi / DKM",
        "Dokumentasi",
    ],
)

# ======================================================
# 🏠 PROFIL
# ======================================================

if menu == "Profil Musholla":

    col1, col2, col3 = st.columns([1,1,4])

    with col1:
        st.image("logo_nu.png", width=90)

    with col2:
        st.image("logo_musholla.png", width=90)

    with col3:
        st.title("🕌 Musholla At Taqwa")
        st.subheader("Pusat Ibadah & Kegiatan Keislaman Masyarakat")

    st.image("https://images.unsplash.com/photo-1509228468518-180dd4864904",
             use_container_width=True)

    st.markdown("""
    Musholla At Taqwa berdiri sebagai pusat ibadah, dakwah, dan kegiatan sosial masyarakat.

    📍 **Alamat:**  
    Jl. Contoh No. 123, Desa Contoh, Kecamatan Contoh.

    🌍 **Koordinat:**  
    -6.200000 , 106.816666
    """)

    st.map(pd.DataFrame({
        "lat": [-6.200000],
        "lon": [106.816666]
    }))

# ======================================================
# 💰 KEUANGAN
# ======================================================

elif menu == "Manajemen Keuangan":

    st.title("💰 Transparansi Keuangan")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Kas Masuk", rupiah(total_masuk))
    col2.metric("Total Kas Keluar", rupiah(total_keluar))
    col3.metric("Saldo Saat Ini", rupiah(saldo))

    st.divider()

    # Grafik Kas Masuk Bulanan
    if not data_masuk.empty:
        data_masuk["Tanggal"] = pd.to_datetime(data_masuk["Tanggal"])
        data_masuk["Bulan"] = data_masuk["Tanggal"].dt.to_period("M")
        bulanan = data_masuk.groupby("Bulan")["Jumlah"].sum()

        plt.figure()
        bulanan.plot(kind="bar")
        plt.title("Kas Masuk per Bulan")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    st.subheader("📥 Kas Masuk")
    st.dataframe(data_masuk, use_container_width=True)

    st.subheader("📤 Kas Keluar")
    st.dataframe(data_keluar, use_container_width=True)

# ======================================================
# 📅 KEGIATAN
# ======================================================

elif menu == "Jadwal Kegiatan":

    st.title("📅 Jadwal Kegiatan")

    if not data_kegiatan.empty:
        st.dataframe(data_kegiatan, use_container_width=True)
    else:
        st.info("Belum ada kegiatan tercatat.")

# ======================================================
# 👥 STRUKTUR
# ======================================================

elif menu == "Struktur Organisasi / DKM":

    st.title("👥 Struktur Organisasi DKM")

    st.markdown("""
    **Ketua DKM:** Ahmad  
    **Sekretaris:** Budi  
    **Bendahara 1:** Rahmat  
    **Bendahara 2:** Siti  

    ### Seksi:
    - Dakwah  
    - Humas  
    - Pembangunan  
    - Sosial  
    """)

    st.info("AD/ART dapat ditambahkan dalam format PDF.")

# ======================================================
# 📷 DOKUMENTASI
# ======================================================

elif menu == "Dokumentasi":

    st.title("📷 Dokumentasi Kegiatan")

    st.image("https://images.unsplash.com/photo-1584556812952-905ffd0c611a",
             caption="Kegiatan Pengajian")

    st.image("https://images.unsplash.com/photo-1591604466107-ec97de577aff",
             caption="Kegiatan Sosial")

# ======================================================
# 🕒 FOOTER
# ======================================================

st.divider()
now = datetime.now().strftime("%d %B %Y - %H:%M WIB")
st.caption(f"Terakhir diperbarui: {now}")
st.caption("Dikelola oleh DKM Musholla At Taqwa • Transparansi adalah Amanah")
