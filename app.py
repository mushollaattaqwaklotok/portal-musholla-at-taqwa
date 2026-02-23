import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="Portal Musholla At Taqwa", layout="wide")

# ==============================
# 🔐 KONEKSI GOOGLE SHEET
# ==============================

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

# ==============================
# 💰 HITUNG SALDO
# ==============================

total_masuk = data_masuk["Jumlah"].sum() if not data_masuk.empty else 0
total_keluar = data_keluar["Jumlah"].sum() if not data_keluar.empty else 0
saldo = total_masuk - total_keluar

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ==============================
# 📌 SIDEBAR MENU
# ==============================

st.sidebar.title("🕌 Musholla At Taqwa")

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

# ==============================
# 🏠 PROFIL MUSHOLLA
# ==============================

if menu == "Profil Musholla":

    st.title("📖 Profil Musholla At Taqwa")

    st.markdown("""
    Musholla At Taqwa didirikan sebagai pusat ibadah dan kegiatan keislaman masyarakat.
    
    **Alamat:**
    Jl. Contoh No. 123, Desa Contoh, Kecamatan Contoh, Kabupaten Contoh.
    
    **Koordinat Lokasi:**
    - Latitude: -6.200000
    - Longitude: 106.816666
    """)

    st.map(pd.DataFrame({
        "lat": [-6.200000],
        "lon": [106.816666]
    }))

# ==============================
# 💰 MANAJEMEN KEUANGAN
# ==============================

elif menu == "Manajemen Keuangan":

    st.title("💰 Transparansi Keuangan")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Kas Masuk", rupiah(total_masuk))
    col2.metric("Total Kas Keluar", rupiah(total_keluar))
    col3.metric("Saldo Saat Ini", rupiah(saldo))

    st.divider()

    st.subheader("📥 Data Kas Masuk")
    st.dataframe(data_masuk, use_container_width=True)

    st.subheader("📤 Data Kas Keluar")
    st.dataframe(data_keluar, use_container_width=True)

# ==============================
# 📅 JADWAL KEGIATAN
# ==============================

elif menu == "Jadwal Kegiatan":

    st.title("📅 Kegiatan Musholla")

    if not data_kegiatan.empty:
        st.dataframe(data_kegiatan, use_container_width=True)
    else:
        st.info("Belum ada kegiatan yang tercatat.")

# ==============================
# 👥 STRUKTUR ORGANISASI
# ==============================

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

    st.subheader("📜 AD/ART")
    st.info("Dokumen AD/ART dapat diunggah dalam bentuk PDF ke repositori atau ditampilkan di sini.")

# ==============================
# 📷 DOKUMENTASI
# ==============================

elif menu == "Dokumentasi":

    st.title("📷 Dokumentasi Kegiatan")

    st.info("Upload foto kegiatan ke folder repository atau integrasikan dengan Google Drive.")

    # Contoh jika mau pakai gambar lokal:
    # st.image("foto1.jpg", caption="Kegiatan Pengajian")

# ==============================
# 🕒 FOOTER
# ==============================

st.divider()
now = datetime.now().strftime("%d %B %Y - %H:%M WIB")
st.caption(f"Terakhir diperbarui: {now}")
st.caption("Dikelola oleh DKM Musholla At Taqwa")
