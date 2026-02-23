import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Portal Transparansi Musholla At Taqwa")

st.title("🕌 Portal Transparansi Musholla At Taqwa")
st.write("Sistem Transparansi Keuangan Publik")

# Scope akses
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Ambil credentials dari Streamlit Secrets
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)

client = gspread.authorize(credentials)

SPREADSHEET_ID = "1XTX9i9WHtGm6KkOfa01MpJuKYBODZXfH8-Z1FpF6BZo"

spreadsheet = client.open_by_key(SPREADSHEET_ID)

kas_masuk_sheet = spreadsheet.worksheet("kas_masuk")
data_kas_masuk = pd.DataFrame(kas_masuk_sheet.get_all_records())

st.subheader("Data Kas Masuk")
st.dataframe(data_kas_masuk)
