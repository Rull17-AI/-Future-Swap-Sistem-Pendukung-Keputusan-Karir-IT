import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import os
import cv2

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Future Swap — IT Career System",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS KUSTOM
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }
    .main { background-color: #1e272e; }
    .stApp { background-color: #1e272e; color: white; }

    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        color: #0fbcf9;
        text-align: center;
        letter-spacing: 6px;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        text-align: center;
        color: #747d8c;
        font-size: 1rem;
        letter-spacing: 2px;
        margin-bottom: 2rem;
    }
    .menu-card {
        background: linear-gradient(135deg, #2f3542, #3d4a56);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        border: 1px solid #485460;
        transition: all 0.3s;
        margin: 0.5rem;
    }
    .result-box {
        background: linear-gradient(135deg, #0a3d62, #1e3799);
        border-left: 5px solid #0fbcf9;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
    }
    .result-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.6rem;
        color: #0fbcf9;
        letter-spacing: 3px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3c40c6, #2980b9);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 1px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4a4fcf, #3498db);
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(63,116,198,0.4);
    }
    .question-card {
        background: #2f3542;
        border-radius: 16px;
        padding: 2rem;
        border-left: 4px solid #05c46b;
        margin: 1rem 0;
    }
    .career-tag {
        background: #3c40c6;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }
    div[data-testid="stRadio"] label {
        background: #2f3542;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 0.2rem;
        display: block;
        color: white;
        border: 1px solid #485460;
    }
    div[data-testid="stRadio"] label:hover {
        background: #3c40c6;
        border-color: #0fbcf9;
    }
    .salary-badge {
        background: linear-gradient(135deg, #05c46b, #0be881);
        color: #1e272e;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA
# ==========================================
NARRATIVE_KARIR = {
    "Frontend Developer": (
        "Seorang Frontend Developer adalah arsitek visual dari sebuah aplikasi web. "
        "Mereka bertanggung jawab membangun antarmuka yang berinteraksi langsung dengan pengguna. "
        "Tugas utama meliputi penerjemahan desain dari tim UI/UX menjadi kode fungsional menggunakan "
        "HTML, CSS, dan JavaScript (React, Next.js, Vue.js). Tools wajib: Git, browser DevTools, "
        "pemahaman mendalam tentang DOM dan SEO.",
        "💻", "#1abc9c", "Rp 6.500.000"
    ),
    "Backend Developer": (
        "Backend Developer adalah tulang punggung aplikasi, mengelola logika bisnis, penyimpanan data, "
        "dan komunikasi antar sistem di balik layar. Mereka merancang database, membangun REST API, "
        "dan mengimplementasi sistem autentikasi menggunakan Python (FastAPI/Django), Node.js, "
        "PHP (Laravel), atau Go. Pemahaman ACID, Docker, dan keamanan web sangat krusial.",
        "⚙️", "#3498db", "Rp 7.000.000"
    ),
    "Data Scientist": (
        "Data Scientist adalah detektif data yang mengubah data mentah menjadi wawasan bisnis strategis. "
        "Mereka menggabungkan matematika, statistik, dan pemrograman untuk membangun model ML/AI "
        "menggunakan Pandas, NumPy, Scikit-Learn, TensorFlow, atau PyTorch. Kemampuan komunikasi "
        "hasil analisis kepada stakeholders melalui visualisasi data (PowerBI, Tableau) sangat penting.",
        "📊", "#9b59b6", "Rp 7.500.000"
    ),
    "Cyber Security": (
        "Ahli Cyber Security adalah garda terdepan melindungi sistem dan data dari ancaman siber. "
        "Tugas meliputi pemantauan jaringan, vulnerability assessment, dan penetration testing "
        "menggunakan Kali Linux, Wireshark, Metasploit, dan Nmap. Pemahaman regulasi GDPR/UU PDP "
        "dan kriptografi wajib dimiliki.",
        "🔐", "#e74c3c", "Rp 10.300.000"
    ),
    "UI/UX Designer": (
        "UI/UX Designer merancang pengalaman dan antarmuka yang tidak hanya indah tapi juga intuitif. "
        "Proses berpusat pada Human-Centered Design: riset pengguna, user journey, wireframe, "
        "hingga prototype interaktif menggunakan Figma atau Adobe XD. Kemampuan empati dan "
        "Design Thinking sangat krusial.",
        "🎨", "#f1c40f", "Rp 5.000.000"
    ),
    "Mobile Developer": (
        "Mobile Developer membangun aplikasi untuk smartphone dan tablet. Menggunakan Kotlin/Java "
        "(Android), Swift/Objective-C (iOS), atau framework cross-platform seperti Flutter/React Native. "
        "Bertanggung jawab atas optimasi performa, integrasi fitur hardware (GPS, kamera), "
        "dan rilis ke Google Play Store / App Store.",
        "📱", "#e67e22", "Rp 8.000.000"
    ),
    "AI Engineer": (
        "AI Engineer merancang dan mengimplementasikan sistem kecerdasan buatan ke dalam produk fungsional. "
        "Fokus pada siklus: definisi masalah → persiapan data → training model → deployment. "
        "Bekerja dengan TensorFlow, PyTorch, OpenCV, dan Hugging Face. Matematika lanjut "
        "(kalkulus, aljabar linier) dan Python yang kuat adalah modal utama.",
        "🤖", "#2ecc71", "Rp 12.000.000"
    ),
    "Game Developer": (
        "Game Developer menciptakan pengalaman interaktif menggunakan Unity (C#) atau Unreal Engine (C++). "
        "Tugas meliputi implementasi gameplay mechanics, physics engine, integrasi aset visual/audio, "
        "dan AI untuk NPC. Bekerja dengan Blender atau Maya untuk aset 3D, "
        "serta melakukan playtesting ketat.",
        "🎮", "#34495e", "Rp 6.000.000"
    ),
    "DevOps Engineer": (
        "DevOps Engineer menghubungkan tim Development dan Operations untuk mempercepat software delivery. "
        "Fokus pada CI/CD pipeline (Jenkins, GitHub Actions), Infrastructure as Code (Terraform, Ansible), "
        "dan orkestrasi container (Kubernetes, Docker) di platform cloud AWS/Azure/GCP. "
        "Kemampuan Linux, jaringan, dan problem-solving cepat sangat dibutuhkan.",
        "🔧", "#7f8c8d", "Rp 9.500.000"
    ),
    "Database Administrator": (
        "DBA bertanggung jawab atas integritas, keamanan, dan performa database perusahaan. "
        "Tugas: perancangan skema, manajemen hak akses, backup/recovery, dan performance tuning. "
        "Bekerja dengan MySQL, PostgreSQL, Oracle, SQL Server, atau MongoDB. "
        "Pemahaman mendalam tentang prinsip ACID dan replikasi data sangat krusial.",
        "🗄️", "#d35400", "Rp 7.200.000"
    )
}

LIST_PERTANYAAN = [
    ("ai", "Apakah Anda tertarik melatih suatu mesin agar bisa melakukan prediksi otomatis berdasarkan data?"),
    ("data", "Apakah Anda merasa puas ketika berhasil menemukan pola tersembunyi di balik kumpulan data yang rumit?"),
    ("cyber", "Seberapa besar rasa ingin tahu Anda untuk menguji celah keamanan pada sebuah sistem?"),
    ("uiux", "Dalam membangun aplikasi, apakah fokus utama Anda adalah menciptakan tampilan yang indah dan nyaman?"),
    ("frontend", "Apakah Anda lebih suka fokus pada bagian aplikasi yang berinteraksi langsung dengan pengguna?"),
    ("backend", "Apakah Anda lebih tertantang mengelola logika di balik layar dan integrasi database?"),
    ("mobile", "Apakah Anda tertarik mengembangkan aplikasi khusus untuk perangkat smartphone?"),
    ("game", "Apakah Anda memiliki minat besar dalam merancang mekanika dunia virtual dalam sebuah permainan?"),
    ("devops", "Apakah Anda tertarik memastikan aplikasi tetap stabil di server meski diakses banyak orang?"),
    ("dba", "Apakah Anda tipe orang yang sangat teliti dalam menyusun struktur penyimpanan data?")
]

PILIHAN_JAWABAN = {
    "Sangat Tidak Suka": 2,
    "Tidak Suka": 4,
    "Biasa Saja": 6,
    "Suka": 8,
    "Sangat Suka": 10
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
# FUNGSI RADAR CHART
# ==========================================
def draw_radar(values, label_result):
    labels = ["AI", "Data", "Cyber", "UI/UX", "Frontend", "Backend", "Mobile", "Game", "DevOps", "DBA"]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), facecolor='#2f3542')
    ax.set_facecolor('#2f3542')

    ax.plot(angles, values_plot, color='#05c46b', linewidth=2.5, linestyle='solid')
    ax.fill(angles, values_plot, color='#05c46b', alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white', size=10, fontweight='bold')
    ax.set_yticklabels([])
    ax.set_ylim(0, 10)
    ax.grid(color='#485460', linewidth=0.8)
    ax.spines['polar'].set_color('#485460')

    plt.title(f"Profil Minat: {label_result}", color='#0fbcf9', size=12, pad=20, fontweight='bold')
    plt.tight_layout()
    return fig

# ==========================================
# SESSION STATE
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'result' not in st.session_state:
    st.session_state.result = None

# ==========================================
# HALAMAN: HOME
# ==========================================
def page_home():
    st.markdown('<div class="hero-title">⚡ FUTURE SWAP</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">SISTEM PENDUKUNG KEPUTUSAN KARIR IT • BERBASIS VISUAL FACE SWAP</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="menu-card">
            <div style="font-size:3rem">🎯</div>
            <div style="font-size:1.2rem; font-weight:700; color:#05c46b; margin:0.5rem 0">ANALISIS KARIR</div>
            <div style="color:#747d8c; font-size:0.9rem">Kuis 10 pertanyaan SKKNI untuk menemukan karir IT terbaikmu</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Mulai Analisis", key="btn_quiz"):
            st.session_state.page = 'quiz'
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.rerun()

    with col2:
        st.markdown("""
        <div class="menu-card">
            <div style="font-size:3rem">📚</div>
            <div style="font-size:1.2rem; font-weight:700; color:#3c40c6; margin:0.5rem 0">ENSIKLOPEDIA IT</div>
            <div style="color:#747d8c; font-size:0.9rem">Eksplorasi mendalam 10 profesi IT dan roadmap karirnya</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Eksplorasi", key="btn_enc"):
            st.session_state.page = 'encyclopedia'
            st.rerun()

    with col3:
        st.markdown("""
        <div class="menu-card">
            <div style="font-size:3rem">📈</div>
            <div style="font-size:1.2rem; font-weight:700; color:#f39c12; margin:0.5rem 0">TREN & GAJI</div>
            <div style="color:#747d8c; font-size:0.9rem">Proyeksi gaji dan tren pasar IT Indonesia 2026</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Lihat Tren", key="btn_trend"):
            st.session_state.page = 'trends'
            st.rerun()

# ==========================================
# HALAMAN: QUIZ
# ==========================================
def page_quiz():
    if st.button("⬅ Kembali ke Menu", key="back_quiz"):
        st.session_state.page = 'home'
        st.rerun()

    idx = st.session_state.q_index
    total = len(LIST_PERTANYAAN)

    if idx < total:
        progress = idx / total
        st.progress(progress, text=f"Pertanyaan {idx + 1} dari {total}")

        _, teks = LIST_PERTANYAAN[idx]

        st.markdown(f"""
        <div class="question-card">
            <div style="color:#747d8c; font-size:0.85rem; font-weight:600; letter-spacing:2px; margin-bottom:0.5rem">
                PERTANYAAN {idx + 1}/{total}
            </div>
            <div style="font-size:1.2rem; font-weight:600; color:white; line-height:1.6">
                {teks}
            </div>
        </div>
        """, unsafe_allow_html=True)

        jawaban = st.radio(
            "Pilih jawaban:",
            options=list(PILIHAN_JAWABAN.keys()),
            key=f"q_{idx}",
            label_visibility="collapsed"
        )

        col_a, col_b = st.columns([3, 1])
        with col_b:
            if st.button("Lanjut ➡", key=f"next_{idx}"):
                st.session_state.answers.append(PILIHAN_JAWABAN[jawaban])
                st.session_state.q_index += 1
                st.rerun()
    else:
        # Proses hasil
        if model is None:
            st.error("❌ Model tidak ditemukan! Pastikan file `model_karir_it.pkl` ada di folder project.")
            return

        feature_names = ['ai', 'data', 'cyber', 'uiux', 'frontend', 'backend', 'mobile', 'game', 'devops', 'dba']
        df_input = pd.DataFrame([st.session_state.answers], columns=feature_names)
        probs = model.predict_proba(df_input)[0]
        result = model.classes_[np.argmax(probs)]
        st.session_state.result = result

        emoji, _, accent, salary = NARRATIVE_KARIR.get(result, ("💼", "", "#0fbcf9", ""))

        st.markdown(f"""
        <div class="result-box">
            <div style="color:#747d8c; font-size:0.8rem; letter-spacing:2px">REKOMENDASI KARIR TERBAIK UNTUKMU</div>
            <div class="result-title">{emoji} {result.upper()}</div>
            <div style="margin-top:0.8rem">
                <span class="salary-badge">💰 Est. Gaji {salary}/bulan</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            fig = draw_radar(st.session_state.answers, result)
            st.pyplot(fig)

        with col_r2:
            # Top 3 karir
            st.markdown("**🏆 Top 3 Karir Rekomendasi:**")
            top3_idx = np.argsort(probs)[::-1][:3]
            for rank, i in enumerate(top3_idx, 1):
                karir = model.classes_[i]
                persen = probs[i] * 100
                st.markdown(f"""
                <div style="background:#2f3542; border-radius:10px; padding:0.8rem 1rem; margin:0.5rem 0; border-left: 3px solid {'#0fbcf9' if rank==1 else '#485460'}">
                    <span style="color:#747d8c">#{rank}</span>
                    <span style="color:white; font-weight:600; margin-left:0.5rem">{karir}</span>
                    <span style="float:right; color:#05c46b; font-weight:700">{persen:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Swap foto
        st.markdown("### 🎭 Lihat Seperti Apa Kamu Sebagai Seorang " + result)
        st.info("💡 **Fitur Face Swap** tersedia di versi desktop (app_gui.py) karena membutuhkan file model InsightFace 528MB yang tidak dapat di-host di web gratis.")

        col_swap1, col_swap2 = st.columns(2)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_map = {
            "Frontend Developer": "frontend", "Backend Developer": "backend",
            "Data Scientist": "data_science", "Cyber Security": "cyber_security",
            "UI/UX Designer": "uiux", "Mobile Developer": "mobile",
            "AI Engineer": "ai", "Game Developer": "game",
            "DevOps Engineer": "devops", "Database Administrator": "dba"
        }
        base = key_map.get(result, "ai")

        with col_swap1:
            img_path_f = os.path.join(script_dir, "swap_assets", f"{base}_engineer_f.jpg" if "engineer" in base else f"{base}_f.jpg")
            # Coba berbagai nama file
            for suffix in [f"{base}_f.jpg", f"{base}_engineer_f.jpg", f"{base}_developer_f.jpg",
                           f"{base}_designer_f.jpg", f"{base}_administrator_f.jpg"]:
                p = os.path.join(script_dir, "swap_assets", suffix)
                if os.path.exists(p):
                    st.image(p, caption=f"👩 {result} (Perempuan)", use_container_width=True)
                    break

        with col_swap2:
            for suffix in [f"{base}_m.jpg", f"{base}_engineer_m.jpg", f"{base}_developer_m.jpg",
                           f"{base}_designer_m.jpg", f"{base}_administrator_m.jpg"]:
                p = os.path.join(script_dir, "swap_assets", suffix)
                if os.path.exists(p):
                    st.image(p, caption=f"👨 {result} (Laki-laki)", use_container_width=True)
                    break

        if st.button("🔄 Ulangi Kuis", key="retake"):
            st.session_state.q_index = 0
            st.session_state.answers = []
            st.session_state.result = None
            st.rerun()

# ==========================================
# HALAMAN: ENSIKLOPEDIA
# ==========================================
def page_encyclopedia():
    if st.button("⬅ Kembali ke Menu", key="back_enc"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("## 📚 Ensiklopedia Profesi IT")

    profesi_list = list(NARRATIVE_KARIR.keys())
    selected = st.selectbox("Pilih Profesi IT:", profesi_list, key="enc_select")

    if selected:
        narasi, emoji, color, salary = NARRATIVE_KARIR[selected]

        col_img, col_info = st.columns([1, 2])

        with col_img:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            key_map = {
                "Frontend Developer": "frontend", "Backend Developer": "backend",
                "Data Scientist": "data_science", "Cyber Security": "cyber_security",
                "UI/UX Designer": "uiux", "Mobile Developer": "mobile",
                "AI Engineer": "ai", "Game Developer": "game",
                "DevOps Engineer": "devops", "Database Administrator": "dba"
            }
            base = key_map.get(selected, "ai")
            tmpl_path = os.path.join(script_dir, "templates", f"{base}.png")
            if os.path.exists(tmpl_path):
                st.image(tmpl_path, use_container_width=True)
            else:
                st.markdown(f"<div style='font-size:5rem; text-align:center'>{emoji}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#2f3542; border-radius:12px; padding:1rem; text-align:center; margin-top:1rem">
                <div style="color:#747d8c; font-size:0.8rem">ESTIMASI GAJI 2026</div>
                <div style="color:#05c46b; font-size:1.4rem; font-weight:700; margin-top:0.3rem">{salary}</div>
                <div style="color:#747d8c; font-size:0.8rem">per bulan</div>
            </div>
            """, unsafe_allow_html=True)

        with col_info:
            st.markdown(f"### {emoji} {selected}")
            st.markdown(f"<div style='background:#2f3542; border-radius:12px; padding:1.5rem; line-height:1.8; color:#d2dae2'>{narasi}</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN: TREN GAJI
# ==========================================
def page_trends():
    if st.button("⬅ Kembali ke Menu", key="back_trend"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("## 📈 Proyeksi Tren Gaji & Pasar IT 2026")

    profesi = ['Frontend', 'Backend', 'Data Sci', 'Cyber Sec', 'UI/UX', 'Mobile', 'AI Eng', 'Game Dev', 'DevOps', 'DBA']
    gaji = [6.5, 7.0, 7.5, 10.3, 5.0, 8.0, 12.0, 6.0, 9.5, 7.2]
    colors = ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f1c40f', '#e67e22', '#2ecc71', '#34495e', '#7f8c8d', '#d35400']

    fig, ax = plt.subplots(figsize=(10, 6), dpi=90, facecolor='#1e272e')
    ax.set_facecolor('#1e272e')
    bars = ax.barh(profesi, gaji, color=colors, edgecolor='#2f3542', linewidth=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
                f'Rp {width}jt', va='center', color='white', fontweight='bold', fontsize=10)

    ax.set_title("Estimasi Gaji Bulanan 2026 (Juta IDR)", color="white", fontsize=14, pad=15, fontweight='bold')
    ax.tick_params(colors='white', labelsize=11)
    ax.set_xlim(0, 18)
    for spine in ax.spines.values():
        spine.set_color('#485460')
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#2f3542; border-radius:12px; padding:1.2rem; border-left:4px solid #2ecc71">
            <div style="color:#2ecc71; font-weight:700">🤖 Dominasi AI</div>
            <div style="color:#d2dae2; font-size:0.9rem; margin-top:0.5rem">AI Engineer menjadi profesi paling mahal karena integrasi LLM di berbagai industri.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#2f3542; border-radius:12px; padding:1.2rem; border-left:4px solid #e74c3c">
            <div style="color:#e74c3c; font-weight:700">🔐 Keamanan Data</div>
            <div style="color:#d2dae2; font-size:0.9rem; margin-top:0.5rem">Cyber Security naik signifikan menyusul regulasi perlindungan data global & UU PDP.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#2f3542; border-radius:12px; padding:1.2rem; border-left:4px solid #3498db">
            <div style="color:#3498db; font-weight:700">⚙️ DevOps Trend</div>
            <div style="color:#d2dae2; font-size:0.9rem; margin-top:0.5rem">Perusahaan semakin mengapresiasi developer yang menguasai DevOps & cloud infrastructure.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:right; color:#747d8c; font-size:0.8rem; font-style:italic'>Sumber: Platform Job & Salary Insights Indonesia 2026</div>", unsafe_allow_html=True)

# ==========================================
# ROUTING
# ==========================================
if st.session_state.page == 'home':
    page_home()
elif st.session_state.page == 'quiz':
    page_quiz()
elif st.session_state.page == 'encyclopedia':
    page_encyclopedia()
elif st.session_state.page == 'trends':
    page_trends()
