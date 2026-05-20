import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import base64
from pathlib import Path

st.set_page_config(
    page_title="IT Career System Application - Future Swap",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background-color: #1e272e !important; color: white; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header, .stDeployButton,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Sembunyikan semua tombol bawaan streamlit kecuali yang kita butuhkan */
.stButton > button {
    background-color: #2f3542 !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: Arial, sans-serif !important;
    font-weight: 700 !important;
}

/* Tombol kembali */
.back-btn .stButton > button {
    background-color: #1e272e !important;
    color: white !important;
    padding: 5px 14px !important;
    font-size: 0.85rem !important;
    border: 1px solid #485460 !important;
}

/* Tombol jawaban kuis */
.quiz-opt .stButton > button {
    background-color: #2f3542 !important;
    color: white !important;
    padding: 12px !important;
    font-size: 1rem !important;
    width: 100% !important;
    text-align: center !important;
    margin: 2px 0 !important;
}
.quiz-opt .stButton > button:hover { background-color: #485460 !important; }

/* Tombol sidebar ensiklopedia */
.enc-btn .stButton > button {
    background-color: #2f3542 !important;
    color: #d2dae2 !important;
    text-align: left !important;
    padding: 10px 12px !important;
    font-size: 0.82rem !important;
    border-radius: 2px !important;
    margin: 2px 0 !important;
    width: 100% !important;
}
.enc-btn-active .stButton > button {
    background-color: #3c40c6 !important;
    color: white !important;
    text-align: left !important;
    padding: 10px 12px !important;
    font-size: 0.82rem !important;
    border-radius: 2px !important;
    margin: 2px 0 !important;
    width: 100% !important;
}

/* Tombol transformasi */
.swap-btn .stButton > button {
    background-color: #3c40c6 !important;
    color: white !important;
    padding: 14px 28px !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
}

/* Tombol ulangi */
.retry-btn .stButton > button {
    background-color: #2f3542 !important;
    color: white !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA
# ==========================================
NARRATIVE_KARIR = {
    "Frontend Developer": "Seorang Frontend Developer adalah arsitek visual dari sebuah aplikasi web. Mereka bertanggung jawab penuh untuk membangun bagian antarmuka yang berinteraksi langsung dengan pengguna (User Interface). Tugas utama mereka meliputi penerjemahan desain visual (mockup) dari tim UI/UX menjadi kode yang fungsional dan responsif di berbagai perangkat, baik desktop maupun mobile. Alur kerja mereka biasanya dimulai setelah desain disetujui, di mana mereka akan melakukan slicing desain menggunakan HTML, menyusun tata letak dengan CSS (seringkali menggunakan framework seperti Tailwind atau Bootstrap), dan menambahkan interaktivitas dinamis menggunakan JavaScript, terutama framework modern seperti React, Next.js, atau Vue.js. Selain kemampuan coding, seorang Frontend Developer juga harus memahami prinsip-prinsip SEO dasar, optimasi kecepatan loading halaman, dan memastikan aksesibilitas web bagi semua pengguna. Tools wajib mereka meliputi Git untuk version control, browser developer tools untuk debugging, dan pemahaman mendalam tentang Document Object Model (DOM).",
    "Backend Developer": "Backend Developer adalah tulang punggung dari sebuah aplikasi, mengelola semua logika, penyimpanan data, dan komunikasi antar sistem di balik layar yang tidak terlihat oleh pengguna. Peran mereka sangat krusial dalam memastikan aplikasi berjalan stabil, aman, dan efisien. Tugas mereka meliputi perancangan dan pengelolaan basis data (database), pengembangan Application Programming Interface (API) sebagai jembatan komunikasi dengan Frontend, serta implementasi sistem otentikasi dan otorisasi pengguna. Alur kerja mereka sering kali dimulai dengan merancang skema database (ERD), kemudian membangun logika bisnis utama menggunakan bahasa pemrograman seperti Python (FastAPI/Django), Node.js, PHP (Laravel), atau Go. Pemahaman tentang prinsip RESTful API, keamanan web dasar (seperti OWASP), dan konsep caching (misal dengan Redis) adalah kemampuan yang harus dimiliki.",
    "Data Scientist": "Data Scientist adalah seorang detektif data yang bertugas mengubah tumpukan data mentah yang kompleks menjadi wawasan bisnis yang strategis dan prediktif. Mereka menggabungkan kemampuan matematika, statistik, pemrograman, dan pengetahuan domain bisnis untuk memecahkan masalah yang rumit. Proses kerja mereka dimulai dengan pengumpulan data dari berbagai sumber, dilanjutkan dengan pembersihan data (data cleaning) agar layak dianalisis. Inti dari pekerjaan mereka adalah membangun model Machine Learning atau AI untuk melakukan prediksi masa depan atau klasifikasi otomatis, menggunakan library Python seperti Pandas, NumPy, Scikit-Learn, TensorFlow, atau PyTorch. Kemampuan riset, keingintahuan yang tinggi, dan pemahaman statistik yang kuat adalah modal utama seorang Data Scientist.",
    "Cyber Security": "Ahli Cyber Security adalah garda terdepan dalam melindungi aset digital, sistem jaringan, dan data sensitif perusahaan dari ancaman serangan siber. Tugas mereka meliputi pemantauan jaringan secara real-time untuk mendeteksi aktivitas mencurigakan, melakukan audit keamanan berkala, mengelola sistem pertahanan seperti firewall dan IPS, serta merespons insiden keamanan dengan cepat jika terjadi serangan. Alur kerja mereka sering kali melibatkan Vulnerability Assessment dan Penetration Testing (uji penetrasi) legal menggunakan tools seperti Kali Linux, Wireshark, Metasploit, dan Nmap. Pemahaman regulasi perlindungan data (seperti GDPR atau UU PDP) dan prinsip enkripsi data sangat krusial.",
    "UI/UX Designer": "UI/UX Designer adalah perancang pengalaman dan antarmuka pengguna, memastikan bahwa sebuah aplikasi tidak hanya terlihat indah (User Interface) tetapi juga mudah, nyaman, dan intuitif saat digunakan (User Experience). Proses kerja mereka berpusat pada Human-Centered Design, dimulai dengan riset pengguna (User Research) untuk memahami kebutuhan dan pain points pengguna target. Berdasarkan hasil riset, mereka menyusun User Journey, Arsitektur Informasi, dan wireframe aplikasi. Langkah selanjutnya adalah menciptakan desain visual High-Fidelity yang estetis menggunakan tools utama seperti Figma atau Adobe XD. Kemampuan empati, komunikasi, dan Design Thinking sangat krusial dalam peran ini.",
    "Mobile Developer": "Mobile Developer adalah spesialis yang bertanggung jawab untuk merancang, membangun, dan memelihara aplikasi yang berjalan pada perangkat bergerak seperti smartphone dan tablet. Tugas mereka meliputi implementasi desain antarmuka ke dalam platform mobile, optimasi performa aplikasi agar ringan dan hemat baterai, serta integrasi dengan berbagai layanan backend (API) dan fitur perangkat keras seperti GPS, kamera, atau notifikasi push. Alur kerja mereka dimulai dengan proses coding menggunakan bahasa pemrograman native seperti Kotlin/Java untuk Android dan Swift/Objective-C untuk iOS, atau menggunakan framework cross-platform modern seperti Flutter atau React Native.",
    "AI Engineer": "AI Engineer (Artificial Intelligence Engineer) adalah arsitek cerdas di balik pengembangan sistem kecerdasan buatan yang mampu belajar dan bertindak secara otomatis untuk memecahkan masalah yang kompleks. Mereka fokus pada penerapan praktis dari konsep Machine Learning dan Deep Learning ke dalam produk fungsional. Tugas utama mereka meliputi perancangan arsitektur model AI, pemilihan algoritma yang tepat, pemrosesan dan pelabelan data dalam jumlah besar untuk pelatihan model, serta integrasi model AI yang sudah terlatih ke dalam aplikasi utama melalui API. Pemahaman matematika lanjut (kalkulus, aljabar linier), konsep statistik, dan kemampuan pemrograman Python yang kuat sangat mutlak dibutuhkan.",
    "Game Developer": "Game Developer adalah pencipta pengalaman interaktif yang imersif dan menghibur dalam bentuk permainan digital di berbagai platform, mulai dari PC, konsol, hingga mobile. Tugas mereka meliputi implementasi logika permainan (gameplay mechanics), pengaturan sistem fisika (physics engine), integrasi aset visual dan audio, serta optimasi grafis agar game berjalan lancar. Alur kerja mereka biasanya dimulai dari konsep di Game Design Document, kemudian masuk ke tahap prototyping, dilanjutkan dengan pengembangan penuh menggunakan Game Engine utama seperti Unity (C#) atau Unreal Engine (C++). Mereka juga harus mampu mengelola aset 2D/3D dan melakukan playtesting secara ketat.",
    "DevOps Engineer": "DevOps Engineer adalah jembatan fungsional yang menghubungkan tim pengembangan perangkat lunak (Development) dengan tim operasional IT (Operations). Tujuan utama mereka adalah meningkatkan kecepatan dan kualitas proses pengiriman perangkat lunak melalui otomatisasi. Tugas mereka meliputi otomatisasi CI/CD pipeline, manajemen infrastruktur server, dan pemantauan performa aplikasi di lingkungan produksi menggunakan tools seperti Jenkins, GitLab CI, Terraform, Kubernetes, dan Docker di platform cloud seperti AWS, Azure, atau Google Cloud.",
    "Database Administrator": "Database Administrator (DBA) adalah penjaga integritas, keamanan, dan performa penyimpanan data perusahaan. Mereka bertanggung jawab penuh untuk memastikan bahwa basis data tersimpan aman, selalu tersedia, dan dapat diakses dengan cepat serta efisien. Tugas mereka meliputi perancangan skema database, manajemen hak akses pengguna, serta perencanaan backup dan recovery data secara berkala. Mereka bekerja dengan DBMS seperti MySQL, PostgreSQL, Oracle, SQL Server, atau MongoDB. Pemahaman mendalam tentang prinsip ACID, replikasi data, dan bahasa SQL sangat krusial."
}

LIST_PERTANYAAN = [
    ("AI",       "Apakah Anda tertarik melatih suatu mesin agar bisa melakukan prediksi otomatis berdasarkan data?"),
    ("DATA",     "Apakah Anda merasa puas ketika berhasil menemukan pola tersembunyi di balik kumpulan data yang rumit?"),
    ("CYBER",    "Seberapa besar rasa ingin tahu Anda untuk menguji celah keamanan pada sebuah sistem agar tidak dibobol?"),
    ("UIUX",     "Dalam membangun aplikasi, apakah fokus utama Anda adalah menciptakan tampilan yang indah dan nyaman?"),
    ("FRONTEND", "Apakah Anda lebih suka fokus pada bagian aplikasi yang berinteraksi langsung dengan pengguna?"),
    ("BACKEND",  "Apakah Anda lebih tertantang mengelola logika di balik layar dan integrasi database daripada tampilan?"),
    ("MOBILE",   "Apakah Anda tertarik mengembangkan aplikasi yang khusus dikembangkan untuk perangkat smartphone?"),
    ("GAME",     "Apakah Anda memiliki minat besar dalam merancang mekanika dunia virtual dan interaksi dalam sebuah permainan?"),
    ("DEVOPS",   "Apakah Anda tertarik mempelajari cara memastikan aplikasi tetap berjalan stabil di server meskipun diakses banyak orang?"),
    ("DBA",      "Apakah Anda tipe orang yang sangat teliti dalam menyusun struktur penyimpanan data agar rapi dan efisien?")
]

PILIHAN_JAWABAN = [("Sangat Tidak Suka", 2), ("Tidak Suka", 4), ("Biasa Saja", 6), ("Suka", 8), ("Sangat Suka", 10)]

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
    paths = ['model_karir_it.pkl', './model_karir_it.pkl',
             os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_karir_it.pkl')]
    for p in paths:
        if os.path.exists(p):
            try: return joblib.load(p)
            except: pass
    return None

model = load_model()

# ==========================================
# HELPER: image to base64
# ==========================================
def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            return f"data:image/{ext};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return None

def get_template_img(karir):
    base = KEY_MAP.get(karir, "ai")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "templates", f"{base}.png")
    return img_to_base64(path)

def get_swap_imgs(karir):
    base = KEY_MAP.get(karir, "ai")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    result = {'f': None, 'm': None}
    for gender, suffixes in [
        ('f', [f"{base}_f.jpg", f"{base}_engineer_f.jpg", f"{base}_developer_f.jpg", f"{base}_designer_f.jpg", f"{base}_administrator_f.jpg"]),
        ('m', [f"{base}_m.jpg", f"{base}_engineer_m.jpg", f"{base}_developer_m.jpg", f"{base}_designer_m.jpg", f"{base}_administrator_m.jpg"])
    ]:
        for s in suffixes:
            p = os.path.join(script_dir, "swap_assets", s)
            if os.path.exists(p):
                result[gender] = img_to_base64(p)
                break
    return result

# ==========================================
# SESSION STATE
# ==========================================
for k, v in {'page':'home','q_index':0,'answers':[],'result':None,'enc_selected':'AI Engineer'}.items():
    if k not in st.session_state: st.session_state[k] = v

# ==========================================
# RADAR CHART
# ==========================================
def draw_radar(values):
    labels = ["AI", "Data", "Cyber", "UIUX", "Front", "Back", "Mobile", "Game", "DevOps", "DBA"]
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    v = values + [values[0]]; a = angles + [angles[0]]
    fig = plt.figure(figsize=(5, 4), dpi=85, facecolor='#2f3542')
    ax = fig.add_subplot(111, polar=True, facecolor='#2f3542')
    ax.plot(a, v, color='#05c46b', linewidth=2)
    ax.fill(a, v, color='#05c46b', alpha=0.3)
    ax.set_thetagrids(np.degrees(angles), labels, color='white', fontsize=9)
    ax.set_ylim(0, 10); ax.set_yticklabels([])
    ax.tick_params(colors='white'); ax.grid(color='#485460', linewidth=0.8)
    ax.spines['polar'].set_color('#485460')
    plt.tight_layout(); return fig

# ==========================================
# HOME
# ==========================================
def page_home():
    st.markdown("""
    <div style="background:#2c3e50;padding:35px 0;text-align:center;margin-bottom:60px;">
        <span style="color:#0fbcf9;font-size:2rem;font-weight:900;letter-spacing:4px;font-family:Arial,sans-serif;">
            FUTURE SWAP
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Pakai HTML button dengan query param untuk navigasi
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;gap:12px;margin-top:20px;">
        <form action="" method="get" style="width:420px;">
            <button name="nav" value="quiz"
                style="width:100%;padding:18px;background:#05c46b;color:white;border:none;
                border-radius:3px;font-size:1rem;font-weight:700;letter-spacing:2px;
                font-family:Arial,sans-serif;cursor:pointer;">
                 ANALISIS KARIR
            </button>
        </form>
        <form action="" method="get" style="width:420px;">
            <button name="nav" value="encyclopedia"
                style="width:100%;padding:18px;background:#3c40c6;color:white;border:none;
                border-radius:3px;font-size:1rem;font-weight:700;letter-spacing:2px;
                font-family:Arial,sans-serif;cursor:pointer;">
                 EKSPLORASI BIDANG IT
            </button>
        </form>
        <form action="" method="get" style="width:420px;">
            <button name="nav" value="trends"
                style="width:100%;padding:18px;background:#f39c12;color:white;border:none;
                border-radius:3px;font-size:1rem;font-weight:700;letter-spacing:2px;
                font-family:Arial,sans-serif;cursor:pointer;">
                 TREN PASAR &amp; GAJI
            </button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    # Tangkap query param dari HTML form
    params = st.query_params
    if "nav" in params:
        nav = params["nav"]
        st.query_params.clear()
        if nav == "quiz":
            st.session_state.update({'page':'quiz','q_index':0,'answers':[]}); st.rerun()
        elif nav == "encyclopedia":
            st.session_state.page = 'encyclopedia'; st.rerun()
        elif nav == "trends":
            st.session_state.page = 'trends'; st.rerun()

# ==========================================
# KUIS
# ==========================================
def page_quiz():
    st.markdown('<div style="background:#05c46b;height:8px;width:100%;margin-bottom:5px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="bk_q"):
        st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    idx = st.session_state.q_index
    if idx < len(LIST_PERTANYAAN):
        _, teks = LIST_PERTANYAAN[idx]
        st.markdown("<br><br>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 3, 1])
        with col:
            st.markdown(f"""
            <p style="color:white;font-size:1.2rem;font-weight:bold;text-align:center;
               font-family:Arial,sans-serif;line-height:1.6;margin-bottom:25px;">{teks}</p>
            """, unsafe_allow_html=True)
            for label, value in PILIHAN_JAWABAN:
                st.markdown('<div class="quiz-opt">', unsafe_allow_html=True)
                if st.button(label, key=f"a_{idx}_{value}", use_container_width=True):
                    st.session_state.answers.append(value)
                    st.session_state.q_index += 1; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        page_result()

# ==========================================
# HASIL
# ==========================================
def page_result():
    if model is None:
        st.markdown('<div style="background:#3c40c6;height:8px;width:100%;margin-bottom:5px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ Kembali", key="bk_r_err"):
            st.session_state.page = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#c0392b;padding:20px;margin:20px;border-radius:6px;text-align:center;">
            <p style="color:white;font-size:1rem;margin:0;">
                ⚠️ Model <b>model_karir_it.pkl</b> tidak ditemukan di server.<br>
                Pastikan file sudah di-upload ke GitHub repository.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    feature_names = ['ai','data','cyber','uiux','frontend','backend','mobile','game','devops','dba']
    df_input = pd.DataFrame([st.session_state.answers], columns=feature_names)
    probs = model.predict_proba(df_input)[0]
    result = model.classes_[np.argmax(probs)]
    st.session_state.result = result

    st.markdown('<div style="background:#3c40c6;height:8px;width:100%;margin-bottom:5px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="bk_r"):
        st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:#0fbcf9;font-size:1.6rem;font-weight:900;text-align:center;
       letter-spacing:3px;font-family:Arial,sans-serif;margin:20px 0 10px 0;">
       REKOMENDASI: {result.upper()}
    </p>
    """, unsafe_allow_html=True)

    _, cb, _ = st.columns([2, 2, 2])
    with cb:
        st.markdown('<div class="swap-btn">', unsafe_allow_html=True)
        if st.button("✨ TRANSFORMASI WAJAH", key="bswap", use_container_width=True):
            st.session_state.page = 'swap'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, cc, _ = st.columns([1, 2, 1])
    with cc:
        st.markdown('<div style="background:#2f3542;padding:20px;border-radius:4px;">', unsafe_allow_html=True)
        fig = draw_radar(st.session_state.answers)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, cr, _ = st.columns([2, 1, 2])
    with cr:
        st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
        if st.button("🔄 Ulangi Kuis", key="retake", use_container_width=True):
            st.session_state.update({'q_index':0,'answers':[],'result':None,'page':'quiz'}); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SWAP
# ==========================================
def page_swap():
    result = st.session_state.result or "AI Engineer"
    st.markdown('<div style="background:#3c40c6;height:8px;width:100%;margin-bottom:5px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="bk_s"):
        st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:white;font-size:1.1rem;text-align:center;font-family:Arial,sans-serif;margin:15px 0;">
        Transformasi: {result}
    </p>
    <div style="background:#c0392b;border-radius:4px;padding:12px 20px;text-align:center;margin:0 auto 20px auto;max-width:600px;">
        <span style="color:white;font-weight:700;font-size:0.95rem;">
            ⚠️ Fitur Face Swap hanya tersedia di versi desktop (app_gui.py).<br>
            Jalankan app_gui.py di laptop untuk menggunakan fitur ini secara penuh.
        </span>
    </div>
    """, unsafe_allow_html=True)

    imgs = get_swap_imgs(result)
    img_f = imgs['f']; img_m = imgs['m']

    st.markdown("<p style='color:white;font-weight:700;text-align:center;margin:10px 0;'>Foto Referensi Profesi:</p>", unsafe_allow_html=True)

    f_tag = f'<img src="{img_f}" style="width:100%;border-radius:4px;"/><p style="color:#d2dae2;text-align:center;font-size:0.85rem;margin-top:5px;">👩 {result}</p>' if img_f else '<p style="color:#747d8c;text-align:center;">Foto tidak tersedia</p>'
    m_tag = f'<img src="{img_m}" style="width:100%;border-radius:4px;"/><p style="color:#d2dae2;text-align:center;font-size:0.85rem;margin-top:5px;">👨 {result}</p>' if img_m else '<p style="color:#747d8c;text-align:center;">Foto tidak tersedia</p>'

    st.markdown(f"""
    <div style="display:flex;gap:20px;justify-content:center;max-width:800px;margin:0 auto;">
        <div style="flex:1;">{f_tag}</div>
        <div style="flex:1;">{m_tag}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ENSIKLOPEDIA
# ==========================================
def page_encyclopedia():
    st.markdown("""
    <div style="background:#485460;padding:10px 20px;margin-bottom:10px;">
        <span style="color:white;font-weight:bold;font-size:1rem;letter-spacing:2px;font-family:Arial,sans-serif;">
            PERKEMBANGAN KARIR IT DIGITAL
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="bk_e"):
        st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_list, col_detail = st.columns([1, 3])

    with col_list:
        for i, nama in enumerate(NARRATIVE_KARIR.keys(), 1):
            is_active = st.session_state.enc_selected == nama
            css = "enc-btn-active" if is_active else "enc-btn"
            st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
            if st.button(f"{i:02d}. {nama.upper()}", key=f"e_{i}", use_container_width=True):
                st.session_state.enc_selected = nama; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col_detail:
        selected = st.session_state.enc_selected
        narrative = NARRATIVE_KARIR.get(selected, "")
        tmpl_b64 = get_template_img(selected)

        img_html = ""
        if tmpl_b64:
            img_html = f"""
            <div style="text-align:center;margin-bottom:15px;">
                <img src="{tmpl_b64}"
                     style="max-height:260px;max-width:100%;object-fit:cover;border-radius:4px;"/>
            </div>
            """

        st.markdown(f"""
        <div style="background:#2f3542;padding:20px;border:1px solid #485460;min-height:500px;border-radius:4px;">
            {img_html}
            <p style="color:white;font-size:0.95rem;line-height:1.8;font-family:Helvetica,Arial,sans-serif;
               text-align:justify;margin:0;">{narrative}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TREN GAJI
# ==========================================
def page_trends():
    st.markdown("""
    <div style="background:#f39c12;padding:10px 20px;margin-bottom:5px;">
        <span style="color:#1e272e;font-weight:bold;font-size:1rem;letter-spacing:2px;font-family:Arial,sans-serif;">
            PROYEKSI TREN GAJI &amp; PASAR IT 2026
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ Kembali", key="bk_t"):
        st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    profesi = ['Frontend','Backend','Data Sci','Cyber Sec','UI/UX','Mobile','AI Eng','Game Dev','DevOps','DBA']
    gaji    = [6.5, 7.0, 7.5, 10.3, 5.0, 8.0, 12.0, 6.0, 9.5, 7.2]
    colors  = ['#1abc9c','#3498db','#9b59b6','#e74c3c','#f1c40f','#e67e22','#2ecc71','#34495e','#7f8c8d','#d35400']

    fig, ax = plt.subplots(figsize=(9, 5), dpi=90, facecolor='#1e272e')
    ax.set_facecolor('#1e272e')
    bars = ax.barh(profesi, gaji, color=colors, edgecolor='white', linewidth=0.5)
    for bar in bars:
        w = bar.get_width()
        ax.text(w+0.5, bar.get_y()+bar.get_height()/2, f'{w}jt', va='center', color='white', fontweight='bold', fontsize=9)
    ax.set_title("Estimasi Gaji Bulanan 2026 (Juta IDR)", color="white", fontsize=13, pad=15, fontweight='bold')
    ax.tick_params(colors='white', labelsize=9)
    ax.set_xlim(0, 22)
    for spine in ax.spines.values(): spine.set_color('#485460')
    plt.tight_layout()

    _, cc, _ = st.columns([0.1, 4, 0.1])
    with cc:
        st.pyplot(fig, use_container_width=True)

    highest = profesi[gaji.index(max(gaji))]
    st.markdown(f"""
    <div style="background:#2f3542;padding:18px 22px;margin-top:10px;">
        <p style="color:#d2dae2;font-size:0.92rem;line-height:1.8;margin:0;">
            <b>ANALISIS PASAR 2026:</b><br>
            1. Dominasi AI: {highest} menjadi profesi paling mahal karena integrasi LLM di berbagai industri.<br>
            2. Keamanan Data: Cyber Security naik signifikan menyusul regulasi perlindungan data global.<br>
            3. Full-Stack Trend: Perusahaan mulai mengapresiasi tinggi developer yang menguasai DevOps & Backend.
        </p>
        <p style="color:#747d8c;font-size:0.78rem;font-style:italic;text-align:right;margin:8px 0 0 0;">
            Sumber: Platform Job & Salary Insights
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
page = st.session_state.page
if   page == 'home':         page_home()
elif page == 'quiz':         page_quiz()
elif page == 'swap':         page_swap()
elif page == 'encyclopedia': page_encyclopedia()
elif page == 'trends':       page_trends()
else:                        page_home()
