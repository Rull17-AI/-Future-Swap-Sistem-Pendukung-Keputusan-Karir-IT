import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="IT Career System Application - Future Swap",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Arial:wght@400;700&display=swap');

/* Reset & Background */
.stApp { background-color: #1e272e; color: white; }
section[data-testid="stSidebar"] { display: none; }
div[data-testid="stDecoration"] { display: none; }
header { background-color: #1e272e !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* Header Bar */
.header-bar {
    background-color: #2c3e50;
    padding: 28px 0 28px 0;
    text-align: center;
    margin-bottom: 0;
}
.header-title {
    color: #0fbcf9;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 4px;
    font-family: Arial, sans-serif;
    margin: 0;
}

/* Top bar halaman */
.topbar-green  { background:#05c46b; padding:10px 15px; display:flex; align-items:center; margin-bottom:0; }
.topbar-blue   { background:#3c40c6; padding:10px 15px; display:flex; align-items:center; margin-bottom:0; }
.topbar-gray   { background:#485460; padding:10px 15px; display:flex; align-items:center; margin-bottom:0; }
.topbar-orange { background:#f39c12; padding:10px 15px; display:flex; align-items:center; margin-bottom:0; }
.topbar-title  { color: white; font-weight: bold; font-size: 1rem; letter-spacing: 2px; margin-left: 10px; }
.topbar-title-dark { color: #1e272e; font-weight: bold; font-size: 1rem; letter-spacing: 2px; margin-left: 10px; }

/* Tombol menu utama */
.stButton > button {
    width: 100%;
    padding: 18px 0 !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    border: none !important;
    border-radius: 4px !important;
    color: white !important;
    cursor: pointer;
    font-family: Arial, sans-serif;
}
div[data-testid="column"]:nth-child(1) .stButton > button { background-color: #05c46b !important; }
div[data-testid="column"]:nth-child(2) .stButton > button { background-color: #3c40c6 !important; }
div[data-testid="column"]:nth-child(3) .stButton > button { background-color: #f39c12 !important; }

/* Tombol kuis */
.quiz-btn > button {
    background-color: #2f3542 !important;
    color: white !important;
    width: 100% !important;
    padding: 12px !important;
    border: none !important;
    border-radius: 4px !important;
    font-size: 1rem !important;
    text-align: center !important;
    margin: 3px 0 !important;
}
.quiz-btn > button:hover { background-color: #485460 !important; }

/* Tombol kembali */
.btn-back > button {
    background-color: #1e272e !important;
    color: white !important;
    border: none !important;
    padding: 6px 16px !important;
    font-size: 0.9rem !important;
}

/* Teks pertanyaan */
.question-text {
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    text-align: center;
    padding: 30px 20px;
    font-family: Arial, sans-serif;
}

/* Hasil rekomendasi */
.result-title {
    color: #0fbcf9;
    font-size: 1.5rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: 3px;
    padding: 20px 0 10px 0;
    font-family: Arial, sans-serif;
}

/* Tombol transformasi wajah */
.btn-swap > button {
    background-color: #3c40c6 !important;
    color: white !important;
    padding: 14px 28px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 4px !important;
    letter-spacing: 1px !important;
}

/* Sidebar ensiklopedia */
.sidebar-btn > button {
    background-color: #2f3542 !important;
    color: #d2dae2 !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 10px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 2px !important;
    margin: 2px 0 !important;
}
.sidebar-btn-active > button {
    background-color: #3c40c6 !important;
    color: white !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 10px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 2px !important;
    margin: 2px 0 !important;
}

/* Detail panel ensiklopedia */
.detail-panel {
    background-color: #2f3542;
    padding: 15px;
    min-height: 500px;
    border: 1px solid #485460;
}
.narasi-text {
    color: white;
    font-size: 0.95rem;
    line-height: 1.8;
    font-family: Helvetica, Arial, sans-serif;
    text-align: justify;
    padding: 10px;
}

/* Insight box tren */
.insight-box {
    background-color: #2f3542;
    padding: 18px 22px;
    margin-top: 10px;
}
.insight-text { color: #d2dae2; font-size: 0.92rem; line-height: 1.8; }
.source-text { color: #747d8c; font-size: 0.78rem; font-style: italic; text-align: right; margin-top: 8px; }

/* Sembunyikan elemen bawaan streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA
# ==========================================
NARRATIVE_KARIR = {
    "Frontend Developer": "Seorang Frontend Developer adalah arsitek visual dari sebuah aplikasi web. Mereka bertanggung jawab penuh untuk membangun bagian antarmuka yang berinteraksi langsung dengan pengguna (User Interface). Tugas utama mereka meliputi penerjemahan desain visual (mockup) dari tim UI/UX menjadi kode yang fungsional dan responsif di berbagai perangkat, baik desktop maupun mobile. Alur kerja mereka biasanya dimulai setelah desain disetujui, di mana mereka akan melakukan slicing desain menggunakan HTML, menyusun tata letak dengan CSS (seringkali menggunakan framework seperti Tailwind atau Bootstrap), dan menambahkan interaktivitas dinamis menggunakan JavaScript, terutama framework modern seperti React, Next.js, atau Vue.js. Selain kemampuan coding, seorang Frontend Developer juga harus memahami prinsip-prinsip SEO dasar, optimasi kecepatan loading halaman, dan memastikan aksesibilitas web bagi semua pengguna. Tools wajib mereka meliputi Git untuk version control, browser developer tools untuk debugging, dan pemahaman mendalam tentang Document Object Model (DOM).",
    "Backend Developer": "Backend Developer adalah tulang punggung dari sebuah aplikasi, mengelola semua logika, penyimpanan data, dan komunikasi antar sistem di balik layar yang tidak terlihat oleh pengguna. Peran mereka sangat krusial dalam memastikan aplikasi berjalan stabil, aman, dan efisien. Tugas mereka meliputi perancangan dan pengelolaan basis data (database), pengembangan Application Programming Interface (API) sebagai jembatan komunikasi dengan Frontend, serta implementasi sistem otentikasi dan otorisasi pengguna. Alur kerja mereka sering kali dimulai dengan merancang skema database (ERD), kemudian membangun logika bisnis utama menggunakan bahasa pemrograman seperti Python (FastAPI/Django), Node.js, PHP (Laravel), atau Go. Mereka juga bertanggung jawab atas optimasi query database agar akses data berlangsung cepat, serta melakukan deployment dan pemeliharaan aplikasi di server (sering kali menggunakan Docker dan Cloud Services seperti AWS atau Google Cloud). Pemahaman tentang prinsip RESTful API, keamanan web dasar (seperti OWASP), dan konsep caching (misal dengan Redis) adalah kemampuan yang harus dimiliki.",
    "Data Scientist": "Data Scientist adalah seorang detektif data yang bertugas mengubah tumpukan data mentah yang kompleks menjadi wawasan bisnis yang strategis dan prediktif. Mereka menggabungkan kemampuan matematika, statistik, pemrograman, dan pengetahuan domain bisnis untuk memecahkan masalah yang rumit. Proses kerja mereka dimulai dengan pengumpulan data dari berbagai sumber (database, file log, API), dilanjutkan dengan pembersihan data (data cleaning) agar layak dianalisis. Langkah selanjutnya adalah Exploratory Data Analysis (EDA) untuk menemukan pola, tren, dan korelasi yang menarik. Inti dari pekerjaan mereka adalah membangun model Machine Learning atau AI untuk melakukan prediksi masa depan atau klasifikasi otomatis, menggunakan library Python seperti Pandas, NumPy, Scikit-Learn, TensorFlow, atau PyTorch. Mereka juga harus mampu mengomunikasikan hasil temuan mereka yang teknis menjadi cerita yang mudah dipahami oleh pemangku kepentingan (stakeholders) melalui visualisasi data yang menarik menggunakan tools seperti PowerBI, Tableau, atau matplotlib. Kemampuan riset, keingintahuan yang tinggi, dan pemahaman statistik yang kuat adalah modal utama seorang Data Scientist.",
    "Cyber Security": "Ahli Cyber Security adalah garda terdepan dalam melindungi aset digital, sistem jaringan, dan data sensitif perusahaan dari ancaman serangan siber, pencurian data, dan peretasan oleh pihak yang tidak bertanggung jawab. Peran mereka sangat vital di era digital ini untuk menjaga kepercayaan pengguna dan integritas data. Tugas mereka meliputi pemantauan jaringan secara real-time untuk mendeteksi aktivitas mencurigakan, melakukan audit keamanan berkala, mengelola sistem pertahanan seperti firewall dan IPS, serta merespons insiden keamanan dengan cepat jika terjadi serangan. Alur kerja mereka sering kali melibatkan Vulnerability Assessment untuk menemukan celah keamanan, dilanjutkan dengan Penetration Testing (uji penetrasi) legal untuk mensimulasikan serangan nyata dan menguji kekuatan sistem. Mereka menggunakan berbagai tools spesialis seperti Kali Linux, Wireshark, Metasploit, dan Nmap. Selain kemampuan teknis tentang jaringan dan sistem operasi, seorang ahli Cyber Security juga harus memahami regulasi perlindungan data (seperti GDPR atau UU PDP) dan prinsip-prinsip enkripsi data (kriptografi).",
    "UI/UX Designer": "UI/UX Designer adalah perancang pengalaman dan antarmuka pengguna, memastikan bahwa sebuah aplikasi tidak hanya terlihat indah (User Interface) tetapi juga mudah, nyaman, dan intuitif saat digunakan (User Experience). Peran mereka menjembatani kebutuhan bisnis dengan kenyamanan pengguna akhir. Proses kerja mereka berpusat pada manusia (Human-Centered Design), dimulai dengan riset pengguna (User Research) untuk memahami kebutuhan, perilaku, dan poin masalah (pain points) pengguna target. Berdasarkan hasil riset, mereka menyusun User Journey, Arsitektur Informasi, dan wireframe (kerangka kasar) aplikasi. Langkah selanjutnya adalah menciptakan desain visual High-Fidelity yang estetis, termasuk pemilihan warna, tipografi, ikon, dan tata letak, menggunakan tools utama seperti Figma atau Adobe XD. Mereka juga membangun prototype interaktif untuk mensimulasikan alur aplikasi dan melakukan Usability Testing untuk mendapatkan masukan langsung dari pengguna guna melakukan perbaikan desain secara iteratif sebelum diserahkan ke tim developer. Kemampuan empati, komunikasi, dan Design Thinking sangat krusial dalam peran ini.",
    "Mobile Developer": "Mobile Developer adalah spesialis yang bertanggung jawab untuk merancang, membangun, dan memelihara aplikasi yang berjalan pada perangkat bergerak seperti smartphone dan tablet. Di tengah tren penggunaan perangkat mobile yang dominan, peran ini sangat dicari oleh industri. Tugas mereka meliputi implementasi desain antarmuka ke dalam platform mobile, optimasi performa aplikasi agar ringan dan hemat baterai, serta integrasi dengan berbagai layanan backend (API) dan fitur perangkat keras seperti GPS, kamera, atau notifikasi push. Alur kerja mereka dimulai dari pemahaman arsitektur aplikasi mobile, dilanjutkan dengan proses coding menggunakan bahasa pemrograman native seperti Kotlin/Java untuk Android dan Swift/Objective-C untuk iOS, atau menggunakan framework cross-platform modern seperti Flutter atau React Native. Setelah tahap pengembangan dan testing, mereka juga bertanggung jawab atas proses rilis aplikasi ke toko aplikasi resmi seperti Google Play Store dan Apple App Store, serta melakukan pemeliharaan dan update berkala berdasarkan feedback pengguna.",
    "AI Engineer": "AI Engineer (Artificial Intelligence Engineer) adalah arsitek cerdas di balik pengembangan sistem kecerdasan buatan yang mampu belajar dan bertindak secara otomatis untuk memecahkan masalah yang kompleks. Mereka fokus pada penerapan praktis dari konsep Machine Learning dan Deep Learning ke dalam produk fungsional. Tugas utama mereka meliputi perancangan arsitektur model AI, pemilihan algoritma yang tepat, pemrosesan dan pelabelan data dalam jumlah besar untuk pelatihan model, serta integrasi model AI yang sudah terlatih ke dalam aplikasi utama melalui API. Alur kerja mereka melibatkan siklus definisi masalah, persiapan data, pelatihan model (model training), hyperparameter tuning untuk optimasi akurasi, hingga deployment model di lingkungan produksi. Mereka bekerja sangat erat dengan library dan framework seperti TensorFlow, PyTorch, Keras, dan OpenCV untuk aplikasi Computer Vision atau Hugging Face untuk Natural Language Processing (NLP). Pemahaman matematika lanjut (kalkulus, aljabar linier), konsep statistik, dan kemampuan pemrograman Python yang kuat sangat mutlak dibutuhkan.",
    "Game Developer": "Game Developer adalah pencipta pengalaman interaktif yang imersif dan menghibur dalam bentuk permainan digital di berbagai platform, mulai dari PC, konsol, hingga mobile. Peran mereka menggabungkan kreativitas seni dengan logika pemrograman yang rumit. Tugas mereka sangat bervariasi, meliputi implementasi logika permainan (gameplay mechanics), pengaturan sistem fisika (physics engine), integrasi aset visual dan audio, serta optimasi grafis agar game berjalan lancar. Alur kerja mereka biasanya dimulai dari konsep di Game Design Document, kemudian masuk ke tahap prototyping untuk menguji ide utama, dilanjutkan dengan pengembangan penuh menggunakan Game Engine utama seperti Unity (menggunakan C#) atau Unreal Engine (menggunakan C++). Mereka juga harus mampu mengelola aset 2D/3D (menggunakan tools seperti Blender atau Maya), membangun kecerdasan buatan (AI) untuk karakter non-pemain (NPC), dan melakukan uji coba (playtesting) secara ketat untuk menemukan bug serta menyempurnakan pengalaman bermain.",
    "DevOps Engineer": "DevOps Engineer adalah jembatan fungsional yang menghubungkan tim pengembangan perangkat lunak (Development) dengan tim operasional IT (Operations). Tujuan utama mereka adalah meningkatkan kecepatan, efisiensi, dan kualitas proses pengiriman perangkat lunak (software delivery) melalui otomatisasi dan kolaborasi budaya. Tugas mereka meliputi otomatisasi siklus integrasi dan pengiriman kode (Continuous Integration/Continuous Deployment - CI/CD), manajemen infrastruktur server, dan pemantauan performa aplikasi di lingkungan produksi. Alur kerja mereka berfokus pada pembangunan pipeline otomatis menggunakan tools seperti Jenkins, GitLab CI, atau GitHub Actions. Mereka juga mengelola infrastruktur server menggunakan prinsip Infrastructure as Code (IaC) dengan tools seperti Terraform atau Ansible, serta mengatur skalabilitas dan orkestrasi aplikasi (seringkali menggunakan Kubernetes dan Docker) di platform cloud seperti AWS, Azure, atau Google Cloud. Kemampuan pemecahan masalah yang cepat, pemahaman mendalam tentang Linux, jaringan, dan keamanan jaringan sangat dibutuhkan.",
    "Database Administrator": "Database Administrator (DBA) adalah penjaga integritas, keamanan, dan performa penyimpanan data perusahaan. Mereka bertanggung jawab penuh untuk memastikan bahwa basis data (database) tersimpan aman, selalu tersedia saat dibutuhkan, dan dapat diakses dengan cepat serta efisien. Tugas mereka meliputi perancangan skema database, konfigurasi dan instalasi server database, manajemen hak akses pengguna, serta perencanaan dan pelaksanaan backup dan recovery data secara berkala untuk mencegah kehilangan data akibat kegagalan sistem. Alur kerja mereka melibatkan pemantauan performa database secara real-time, melakukan optimasi struktur tabel dan query SQL (performance tuning), serta menerapkan patch keamanan terkini. Mereka bekerja keras dengan sistem manajemen basis data (DBMS) terkemuka seperti MySQL, PostgreSQL, Oracle, SQL Server, atau NoSQL database seperti MongoDB. Pemahaman mendalam tentang prinsip ACID, replikasi data, keamanan data tingkat lanjut, dan bahasa SQL sangat krusial dalam peran ini."
}

LIST_PERTANYAAN = [
    ("AI", "Apakah Anda tertarik melatih suatu mesin agar bisa melakukan prediksi otomatis berdasarkan data?"),
    ("DATA", "Apakah Anda merasa puas ketika berhasil menemukan pola tersembunyi di balik kumpulan data yang rumit?"),
    ("CYBER", "Seberapa besar rasa ingin tahu Anda untuk menguji celah keamanan pada sebuah sistem agar tidak dibobol?"),
    ("UIUX", "Dalam membangun aplikasi, apakah fokus utama Anda adalah menciptakan tampilan yang indah dan nyaman?"),
    ("FRONTEND", "Apakah Anda lebih suka fokus pada bagian aplikasi yang berinteraksi langsung dengan pengguna?"),
    ("BACKEND", "Apakah Anda lebih tertantang mengelola logika di balik layar dan integrasi database daripada tampilan?"),
    ("MOBILE", "Apakah Anda tertarik mengembangkan aplikasi yang khusus dikembangkan untuk perangkat smartphone (Android/iOS)?"),
    ("GAME", "Apakah Anda memiliki minat besar dalam merancang mekanika dunia virtual dan interaksi dalam sebuah permainan?"),
    ("DEVOPS", "Apakah Anda tertarik mempelajari cara memastikan aplikasi tetap berjalan stabil di server meskipun diakses banyak orang?"),
    ("DBA", "Apakah Anda tipe orang yang sangat teliti dalam menyusun struktur penyimpanan data agar rapi dan efisien?")
]

PILIHAN_JAWABAN = [
    ("Sangat Tidak Suka", 2),
    ("Tidak Suka", 4),
    ("Biasa Saja", 6),
    ("Suka", 8),
    ("Sangat Suka", 10)
]

KEY_MAP = {
    "Frontend Developer": "frontend", "Backend Developer": "backend",
    "Data Scientist": "data_science", "Cyber Security": "cyber_security",
    "UI/UX Designer": "uiux", "Mobile Developer": "mobile",
    "AI Engineer": "ai", "Game Developer": "game",
    "DevOps Engineer": "devops", "Database Administrator": "dba"
}

# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    try:
        return joblib.load('model_karir_it.pkl')
    except:
        return None

model = load_model()

# ==========================================
# SESSION STATE
# ==========================================
for key, val in {
    'page': 'home', 'q_index': 0, 'answers': [],
    'result': None, 'enc_selected': 'AI Engineer'
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ==========================================
# RADAR CHART
# ==========================================
def draw_radar(values):
    labels = ["AI", "Data", "Cyber", "UIUX", "Front", "Back", "Mobile", "Game", "DevOps", "DBA"]
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    v = values + [values[0]]
    a = angles + [angles[0]]

    fig = plt.figure(figsize=(5, 4), dpi=85, facecolor='#2f3542')
    ax = fig.add_subplot(111, polar=True, facecolor='#2f3542')
    ax.plot(a, v, color='#05c46b', linewidth=2)
    ax.fill(a, v, color='#05c46b', alpha=0.3)
    ax.set_thetagrids(np.degrees(angles), labels, color='white', fontsize=9)
    ax.set_ylim(0, 10)
    ax.tick_params(colors='white')
    ax.grid(color='#485460', linewidth=0.8)
    ax.spines['polar'].set_color('#485460')
    ax.set_yticklabels([])
    plt.tight_layout()
    return fig

# ==========================================
# HALAMAN HOME
# ==========================================
def page_home():
    st.markdown('<div class="header-bar"><p class="header-title">FUTURE SWAP</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="quiz-btn">', unsafe_allow_html=True)
        if st.button("  ANALISIS KARIR", key="btn_analisis", use_container_width=True):
            st.session_state.page = 'quiz'
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("  EKSPLORASI BIDANG IT", key="btn_eksplorasi", use_container_width=True):
            st.session_state.page = 'encyclopedia'
            st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("  TREN PASAR & GAJI", key="btn_tren", use_container_width=True):
            st.session_state.page = 'trends'
            st.rerun()

    # Override warna tombol menu
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] .stButton:nth-child(1) button { background-color: #05c46b !important; }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] .stButton:nth-child(3) button { background-color: #3c40c6 !important; }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] .stButton:nth-child(5) button { background-color: #f39c12 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# HALAMAN KUIS
# ==========================================
def page_quiz():
    st.markdown('<div class="topbar-green"><span style="color:white;font-size:0.9rem">⬅ Kembali</span></div>', unsafe_allow_html=True)
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅ Kembali", key="back_quiz"):
            st.session_state.page = 'home'
            st.rerun()

    idx = st.session_state.q_index

    if idx < len(LIST_PERTANYAAN):
        _, teks = LIST_PERTANYAAN[idx]

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_mid, col_r = st.columns([1, 3, 1])
        with col_mid:
            st.markdown(f'<div class="question-text">{teks}</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            for label, value in PILIHAN_JAWABAN:
                if st.button(label, key=f"ans_{idx}_{value}", use_container_width=True):
                    st.session_state.answers.append(value)
                    st.session_state.q_index += 1
                    st.rerun()
    else:
        show_result()

# ==========================================
# HALAMAN HASIL
# ==========================================
def show_result():
    if model is None:
        st.error("Model tidak ditemukan!")
        return

    feature_names = ['ai', 'data', 'cyber', 'uiux', 'frontend', 'backend', 'mobile', 'game', 'devops', 'dba']
    df_input = pd.DataFrame([st.session_state.answers], columns=feature_names)
    probs = model.predict_proba(df_input)[0]
    result = model.classes_[np.argmax(probs)]
    st.session_state.result = result

    st.markdown('<div class="topbar-blue"></div>', unsafe_allow_html=True)
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅ Kembali", key="back_result"):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="result-title">REKOMENDASI: {result.upper()}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_btn, col_r = st.columns([2, 2, 2])
    with col_btn:
        if st.button("✨ TRANSFORMASI WAJAH", key="btn_swap", use_container_width=True):
            st.session_state.page = 'swap'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_chart, col_r = st.columns([1, 3, 1])
    with col_chart:
        st.markdown('<div style="background:#2f3542; padding:20px; border-radius:4px">', unsafe_allow_html=True)
        fig = draw_radar(st.session_state.answers)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l2, col_btn2, col_r2 = st.columns([2, 2, 2])
    with col_btn2:
        if st.button("🔄 Ulangi Kuis", key="retake", use_container_width=True):
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.session_state.result = None
            st.session_state.page = 'quiz'
            st.rerun()

# ==========================================
# HALAMAN SWAP
# ==========================================
def page_swap():
    result = st.session_state.result or "AI Engineer"

    st.markdown('<div class="topbar-blue"></div>', unsafe_allow_html=True)
    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅ Kembali", key="back_swap"):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p style="color:white; font-size:1.1rem; text-align:center; font-family:Arial">Transformasi: {result}</p>', unsafe_allow_html=True)

    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        uploaded = st.file_uploader("PILIH FOTO WAJAH ANDA", type=["jpg", "jpeg", "png"], key="face_upload",
                                     label_visibility="collapsed")

        st.markdown("""
        <style>
        div[data-testid="stFileUploader"] > label { display: none; }
        div[data-testid="stFileUploader"] section {
            background-color: #05c46b !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 14px !important;
            text-align: center;
        }
        div[data-testid="stFileUploader"] section span { color: white !important; font-weight: bold; font-size: 1rem; }
        div[data-testid="stFileUploader"] section svg { display: none; }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div style="background:#2f3542; min-height:350px; display:flex; align-items:center; justify-content:center; margin-top:10px; padding:10px;">', unsafe_allow_html=True)

        if uploaded:
            from PIL import Image
            img = Image.open(uploaded)
            st.image(img, use_container_width=True)
            st.info("ℹ️ Fitur face swap memerlukan InsightFace yang hanya tersedia di versi desktop (app_gui.py). Gambar referensi profesi ditampilkan di bawah.")

            base = KEY_MAP.get(result, "ai")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            col_f, col_m = st.columns(2)
            for suffix_list, col, label in [
                ([f"{base}_f.jpg", f"{base}_engineer_f.jpg", f"{base}_developer_f.jpg", f"{base}_designer_f.jpg", f"{base}_administrator_f.jpg"], col_f, "Perempuan"),
                ([f"{base}_m.jpg", f"{base}_engineer_m.jpg", f"{base}_developer_m.jpg", f"{base}_designer_m.jpg", f"{base}_administrator_m.jpg"], col_m, "Laki-laki")
            ]:
                with col:
                    for s in suffix_list:
                        p = os.path.join(script_dir, "swap_assets", s)
                        if os.path.exists(p):
                            st.image(p, caption=f"{result} ({label})", use_container_width=True)
                            break
        else:
            st.markdown('<p style="color:#747d8c; text-align:center; padding:120px 0; font-style:italic;">Upload foto untuk memulai transformasi</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN ENSIKLOPEDIA
# ==========================================
def page_encyclopedia():
    st.markdown('<div class="topbar-gray"><span class="topbar-title">PERKEMBANGAN KARIR IT DIGITAL</span></div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅ Kembali", key="back_enc"):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    profesi_list = list(NARRATIVE_KARIR.keys())
    col_sidebar, col_detail = st.columns([1, 3])

    with col_sidebar:
        for i, nama in enumerate(profesi_list, 1):
            is_active = st.session_state.enc_selected == nama
            css_class = "sidebar-btn-active" if is_active else "sidebar-btn"
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(f"{i:02d}. {nama.upper()}", key=f"enc_{i}", use_container_width=True):
                st.session_state.enc_selected = nama
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col_detail:
        selected = st.session_state.enc_selected
        narrative = NARRATIVE_KARIR.get(selected, "")
        base = KEY_MAP.get(selected, "ai")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tmpl_path = os.path.join(script_dir, "templates", f"{base}.png")

        st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
        if os.path.exists(tmpl_path):
            col_img_l, col_img_c, col_img_r = st.columns([1, 3, 1])
            with col_img_c:
                st.image(tmpl_path, use_container_width=True)
        st.markdown(f'<div class="narasi-text">{narrative}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN TREN GAJI
# ==========================================
def page_trends():
    st.markdown('<div class="topbar-orange"><span class="topbar-title-dark">PROYEKSI TREN GAJI & PASAR IT 2026</span></div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 8])
    with col_back:
        if st.button("⬅ Kembali", key="back_trend"):
            st.session_state.page = 'home'
            st.rerun()

    profesi = ['Frontend', 'Backend', 'Data Sci', 'Cyber Sec', 'UI/UX', 'Mobile', 'AI Eng', 'Game Dev', 'DevOps', 'DBA']
    gaji    = [6.5, 7.0, 7.5, 10.3, 5.0, 8.0, 12.0, 6.0, 9.5, 7.2]
    colors  = ['#1abc9c','#3498db','#9b59b6','#e74c3c','#f1c40f','#e67e22','#2ecc71','#34495e','#7f8c8d','#d35400']

    fig, ax = plt.subplots(figsize=(9, 5), dpi=90, facecolor='#1e272e')
    ax.set_facecolor('#1e272e')
    bars = ax.barh(profesi, gaji, color=colors, edgecolor='white', linewidth=0.5)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2,
                f'{w}jt', va='center', color='white', fontweight='bold', fontsize=9)
    ax.set_title("Estimasi Gaji Bulanan 2026 (Juta IDR)", color="white", fontsize=13, pad=15, fontweight='bold')
    ax.tick_params(colors='white', labelsize=9)
    ax.set_xlim(0, 22)
    for spine in ax.spines.values():
        spine.set_color('#485460')
    plt.tight_layout()

    col_l, col_chart, col_r = st.columns([0.2, 4, 0.2])
    with col_chart:
        st.pyplot(fig, use_container_width=True)

    highest_job = profesi[gaji.index(max(gaji))]
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-text">
            <b>ANALISIS PASAR 2026:</b><br>
            1. Dominasi AI: {highest_job} menjadi profesi paling mahal karena integrasi LLM di berbagai industri.<br>
            2. Keamanan Data: Cyber Security naik signifikan menyusul regulasi perlindungan data global.<br>
            3. Full-Stack Trend: Perusahaan mulai mengapresiasi tinggi developer yang menguasai DevOps & Backend.
        </div>
        <div class="source-text">Sumber: Platform Job & Salary Insights</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if st.session_state.page == 'home':
    page_home()
elif st.session_state.page == 'quiz':
    page_quiz()
elif st.session_state.page == 'quiz_result':
    show_result()
elif st.session_state.page == 'swap':
    page_swap()
elif st.session_state.page == 'encyclopedia':
    page_encyclopedia()
elif st.session_state.page == 'trends':
    page_trends()
else:
    page_home()
