import streamlit as st

st.set_page_config(
    page_title="AuraBin",
    page_icon="✨",
    layout="wide"
)

import os
import random
import base64
import pandas as pd
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "metadata", "kiyafetler.csv")


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


df = load_data()

kategori_map = {
    "tshirt": "Üst",
    "gomlek": "Gömlek",
    "pantolon": "Pantolon",
    "etek": "Etek",
    "elbise": "Elbise",
    "ayakkabi": "Ayakkabı"
}

stil_map = {
    "spor": "spor",
    "bohemian": "bohem",
    "bohem": "bohem",
    "classic": "klasik",
    "klasik": "klasik"
}

df["stil_temiz"] = df["stil"].astype(str).str.strip().str.lower().map(stil_map)


def resmi_ac(kayit):
    klasor = os.path.join(DATA_DIR, str(kayit["kategori"]))
    beklenen = str(kayit["image_name"])

    tam_yol = os.path.join(klasor, beklenen)
    if os.path.exists(tam_yol):
        return Image.open(tam_yol)

    ana_ad = beklenen.split(".")[0].lower()

    if os.path.exists(klasor):
        for file in os.listdir(klasor):
            if file.lower().startswith(ana_ad):
                return Image.open(os.path.join(klasor, file))

    return None


def kombin_puani_hesapla(kombin_df):
    puan = 72

    if len(kombin_df) >= 2:
        puan += 8

    if "ayakkabi" in kombin_df["kategori"].astype(str).tolist():
        puan += 8

    if kombin_df["renk"].astype(str).nunique() <= len(kombin_df):
        puan += 6

    stil_seti = kombin_df["stil"].astype(str).nunique()
    if stil_seti == 1:
        puan += 6

    return min(puan, 100)


def kombinleri_getir(veri, stil, mevsim):
    uygun_df = veri[(veri["stil_temiz"] == stil) & (veri["mevsim"] == mevsim)]
    kombin_idleri = list(uygun_df["kombin_id"].dropna().unique())
    return uygun_df, kombin_idleri


def background_image_base64():
    aday_klasorler = ["elbise", "gomlek", "tshirt"]
    aday_dosyalar = []

    for klasor in aday_klasorler:
        klasor_yolu = os.path.join(DATA_DIR, klasor)
        if os.path.exists(klasor_yolu):
            for f in os.listdir(klasor_yolu):
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    aday_dosyalar.append(os.path.join(klasor_yolu, f))

    if not aday_dosyalar:
        return None

    secilen = random.choice(aday_dosyalar)

    with open(secilen, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


bg_base64 = background_image_base64()

if bg_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(255,255,255,0.94), rgba(255,255,255,0.94)),
                url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}

        .hero {{
            background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
            padding: 28px 32px;
            border-radius: 24px;
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.22);
        }}

        .hero-title {{
            font-size: 44px;
            font-weight: 800;
            margin: 0;
        }}

        .hero-sub {{
            font-size: 18px;
            margin-top: 8px;
            opacity: 0.96;
        }}

        .main-box {{
            background: rgba(255,255,255,0.92);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }}

        .score-box {{
            background: #fdf2f8;
            color: #be185d;
            padding: 12px 18px;
            border-radius: 14px;
            font-size: 18px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 14px;
            border: 1px solid #f9a8d4;
        }}

        .section-title {{
            font-size: 26px;
            font-weight: 700;
            margin-top: 8px;
            margin-bottom: 10px;
            color: #1f2937;
        }}

        .alt-box {{
            background: rgba(255,255,255,0.95);
            border: 1px solid #f5d0fe;
            border-radius: 18px;
            padding: 12px;
            margin-bottom: 10px;
        }}

        .small-note {{
            color: #374151;
            font-size: 14px;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #faf5ff 0%, #fdf2f8 100%);
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {{
            color: #4c1d95 !important;
            font-weight: 600;
        }}

        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            border: 2px solid #d8b4fe !important;
            border-radius: 14px !important;
        }}

        div[data-baseweb="select"] > div:hover {{
            border: 2px solid #ec4899 !important;
        }}

        .stButton > button {{
            background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
        }}

        .stButton > button:hover {{
            background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">✨ AuraBin</div>
        <div class="hero-sub">Tarzına uygun akıllı kombin öneri sistemi</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("## Kombin Filtreleri")

stil_listesi = ["spor", "bohem", "klasik"]
mevsim_listesi = ["yaz", "ilkbahar", "sonbahar"]

stil = st.sidebar.selectbox("Tarz seç", stil_listesi)
mevsim = st.sidebar.selectbox("Mevsim seç", mevsim_listesi)

col_btn1, col_btn2 = st.sidebar.columns(2)
oner_buton = col_btn1.button("Kombin Öner", use_container_width=True)
yenile_buton = col_btn2.button("Yenile", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("AuraBin seçtiğin filtreye göre uygun kombinleri gösterir.")

uygun_df, kombin_idleri = kombinleri_getir(df, stil, mevsim)

if "secilen_kombin_id" not in st.session_state:
    st.session_state["secilen_kombin_id"] = None

if oner_buton or yenile_buton:
    if len(kombin_idleri) == 0:
        st.session_state["secilen_kombin_id"] = None
    else:
        onceki = st.session_state["secilen_kombin_id"]
        adaylar = [k for k in kombin_idleri if k != onceki]
        if len(adaylar) == 0:
            adaylar = kombin_idleri
        st.session_state["secilen_kombin_id"] = random.choice(adaylar)

if st.session_state["secilen_kombin_id"] is None:
    if oner_buton or yenile_buton:
        st.warning("Bu tarz ve mevsim için uygun kombin bulunamadı.")
    else:
        st.info("Soldan tarz ve mevsim seçip kombin öner butonuna bas.")
else:
    secilen_id = st.session_state["secilen_kombin_id"]
    kombin_df = uygun_df[uygun_df["kombin_id"] == secilen_id]
    puan = kombin_puani_hesapla(kombin_df)

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Önerilen Kombin</div>', unsafe_allow_html=True)
    st.markdown(f"### Kombin #{secilen_id}")
    st.markdown(f'<div class="score-box">Uyum Puanı: %{puan}</div>', unsafe_allow_html=True)

    kolonlar = st.columns(len(kombin_df))

    for i, (_, satir) in enumerate(kombin_df.iterrows()):
        with kolonlar[i]:
            st.markdown(f"#### {kategori_map.get(satir['kategori'], satir['kategori'])}")
            img = resmi_ac(satir)
            if img is not None:
                st.image(img, use_container_width=True)
            else:
                st.warning("Görsel bulunamadı.")
            st.write(f"**Renk:** {satir['renk']}")
            st.write(f"**Tarz:** {stil}")
            st.write(f"**Kalıp:** {satir['kalip']}")
            st.write(f"**Mevsim:** {satir['mevsim']}")

    st.markdown("---")
    st.markdown('<div class="section-title">Alternatif Kombinler</div>', unsafe_allow_html=True)

    alternatif_idler = [k for k in kombin_idleri if k != secilen_id][:3]

    if len(alternatif_idler) == 0:
        st.info("Bu filtre için başka alternatif kombin yok.")
    else:
        alt_cols = st.columns(len(alternatif_idler))

        for i, kid in enumerate(alternatif_idler):
            alt_df = uygun_df[uygun_df["kombin_id"] == kid]
            alt_puan = kombin_puani_hesapla(alt_df)

            with alt_cols[i]:
                st.markdown(
                    f"""
                    <div class="alt-box">
                        <b>Kombin #{kid}</b><br>
                        Uyum Puanı: %{alt_puan}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                ilk_satir = alt_df.iloc[0]
                img = resmi_ac(ilk_satir)
                if img is not None:
                    st.image(img, use_container_width=True)

    st.markdown(
        '<p class="small-note">AuraBin seçtiğin filtreye göre en uygun kombinlerden birini ve alternatiflerini gösterdi.</p>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)