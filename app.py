import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="Portal Transparansi Musholla At Taqwa", layout="wide")

st.title("🕌 Portal Transparansi Musholla At Taqwa")
st.caption("Sistem Transparansi Keuangan Publik")

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
# 💰 HITUNG TOTAL
# ==============================

total_masuk = data_masuk["Jumlah"].sum() if not data_masuk.empty else 0
total_keluar = data_keluar["Jumlah"].sum() if not data_keluar.empty else 0
saldo = total_masuk - total_keluar

def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

# ==============================
# 📊 RINGKASAN KEUANGAN
# ==============================

st.markdown("## 💰 Ringkasan Keuangan")

col1, col2, col3 = st.columns(3)

col1.metric("Total Kas Masuk", rupiah(total_masuk))
col2.metric("Total Kas Keluar", rupiah(total_keluar))
col3.metric("Saldo Saat Ini", rupiah(saldo))

st.divider()

# ==============================
# 📥 DATA KAS MASUK
# ==============================

st.subheader("📥 Data Kas Masuk")
if not data_masuk.empty:
    st.dataframe(data_masuk, use_container_width=True)
else:
    st.info("Belum ada data kas masuk.")

# ==============================
# 📤 DATA KAS KELUAR
# ==============================

st.subheader("📤 Data Kas Keluar")
if not data_keluar.empty:
    st.dataframe(data_keluar, use_container_width=True)
else:
    st.info("Belum ada data kas keluar.")

# ==============================
# 📅 KEGIATAN MUSHOLLA
# ==============================

st.subheader("📅 Kegiatan Musholla")
if not data_kegiatan.empty:
    st.dataframe(data_kegiatan, use_container_width=True)
else:
    st.info("Belum ada data kegiatan.")

st.divider()

# ==============================
# 🕒 UPDATE TERAKHIR
# ==============================

now = datetime.now().strftime("%d %B %Y - %H:%M WIB")
st.caption(f"Terakhir diperbarui: {now}")
