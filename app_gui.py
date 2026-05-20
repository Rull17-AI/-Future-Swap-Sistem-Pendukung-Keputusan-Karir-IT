import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os
import cv2
import threading
import insightface
from insightface.app import FaceAnalysis

# Load Model Prediksi Karir
try:
    model = joblib.load('model_karir_it.pkl')
except:
    print("Error: Model 'model_karir_it.pkl' tidak ditemukan!")

# Inisialisasi Model Face Swap (InsightFace)
try:
    print("Sedang memuat mesin Face Swap... Mohon tunggu...")
    app_face = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    app_face.prepare(ctx_id=0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False)
    print("Mesin Face Swap SIAP!")
except Exception as e:
    print(f"Peringatan: Gagal memuat mesin swap. Detail: {e}")
    swapper = None

# ==========================================
# 2. DATA ENSIKLOPEDIA
# ==========================================
NARRATIVE_KARIR = {
    "Frontend Developer": 
        "Seorang Frontend Developer adalah arsitek visual dari sebuah aplikasi web. Mereka bertanggung jawab penuh untuk membangun bagian antarmuka yang berinteraksi langsung dengan pengguna (User Interface). Tugas utama mereka meliputi penerjemahan desain visual (mockup) dari tim UI/UX menjadi kode yang fungsional dan responsif di berbagai perangkat, baik desktop maupun mobile. Alur kerja mereka biasanya dimulai setelah desain disetujui, di mana mereka akan melakukan slicing desain menggunakan HTML, menyusun tata letak dengan CSS (seringkali menggunakan framework seperti Tailwind atau Bootstrap), dan menambahkan interaktivitas dinamis menggunakan JavaScript, terutama framework modern seperti React, Next.js, atau Vue.js. Selain kemampuan coding, seorang Frontend Developer juga harus memahami prinsip-prinsip SEO dasar, optimasi kecepatan loading halaman, dan memastikan aksesibilitas web bagi semua pengguna. Tools wajib mereka meliputi Git untuk version control, browser developer tools untuk debugging, dan pemahaman mendalam tentang Document Object Model (DOM).",

    "Backend Developer": 
        "Backend Developer adalah tulang punggung dari sebuah aplikasi, mengelola semua logika, penyimpanan data, dan komunikasi antar sistem di balik layar yang tidak terlihat oleh pengguna. Peran mereka sangat krusial dalam memastikan aplikasi berjalan stabil, aman, dan efisien. Tugas mereka meliputi perancangan dan pengelolaan basis data (database), pengembangan Application Programming Interface (API) sebagai jembatan komunikasi dengan Frontend, serta implementasi sistem otentikasi dan otorisasi pengguna. Alur kerja mereka sering kali dimulai dengan merancang skema database (ERD), kemudian membangun logika bisnis utama menggunakan bahasa pemrograman seperti Python (FastAPI/Django), Node.js, PHP (Laravel), atau Go. Mereka juga bertanggung jawab atas optimasi query database agar akses data berlangsung cepat, serta melakukan deployment dan pemeliharaan aplikasi di server (sering kali menggunakan Docker dan Cloud Services seperti AWS atau Google Cloud). Pemahaman tentang prinsip RESTful API, keamanan web dasar (seperti OWASP), dan konsep caching (misal dengan Redis) adalah kemampuan yang harus dimiliki.",

    "Data Scientist": 
        "Data Scientist adalah seorang detektif data yang bertugas mengubah tumpukan data mentah yang kompleks menjadi wawasan bisnis yang strategis dan prediktif. Mereka menggabungkan kemampuan matematika, statistik, pemrograman, dan pengetahuan domain bisnis untuk memecahkan masalah yang rumit. Proses kerja mereka dimulai dengan pengumpulan data dari berbagai sumber (database, file log, API), dilanjutkan dengan pembersihan data (data cleaning) agar layak dianalisis. Langkah selanjutnya adalah Exploratory Data Analysis (EDA) untuk menemukan pola, tren, dan korelasi yang menarik. Inti dari pekerjaan mereka adalah membangun model Machine Learning atau AI untuk melakukan prediksi masa depan atau klasifikasi otomatis, menggunakan library Python seperti Pandas, NumPy, Scikit-Learn, TensorFlow, atau PyTorch. Mereka juga harus mampu mengomunikasikan hasil temuan mereka yang teknis menjadi cerita yang mudah dipahami oleh pemangku kepentingan (stakeholders) melalui visualisasi data yang menarik menggunakan tools seperti PowerBI, Tableau, atau matplotlib. Kemampuan riset, keingintahuan yang tinggi, dan pemahaman statistik yang kuat adalah modal utama seorang Data Scientist.",

    "Cyber Security": 
        "Ahli Cyber Security adalah garda terdepan dalam melindungi aset digital, sistem jaringan, dan data sensitif perusahaan dari ancaman serangan siber, pencurian data, dan peretasan oleh pihak yang tidak bertanggung jawab. Peran mereka sangat vital di era digital ini untuk menjaga kepercayaan pengguna dan integritas data. Tugas mereka meliputi pemantauan jaringan secara real-time untuk mendeteksi aktivitas mencurigakan, melakukan audit keamanan berkala, mengelola sistem pertahanan seperti firewall dan IPS, serta merespons insiden keamanan dengan cepat jika terjadi serangan. Alur kerja mereka sering kali melibatkan Vulnerability Assessment untuk menemukan celah keamanan, dilanjutkan dengan Penetration Testing (uji penetrasi) legal untuk mensimulasikan serangan nyata dan menguji kekuatan sistem. Mereka menggunakan berbagai tools spesialis seperti Kali Linux, Wireshark, Metasploit, dan Nmap. Selain kemampuan teknis tentang jaringan dan sistem operasi, seorang ahli Cyber Security juga harus memahami regulasi perlindungan data (seperti GDPR atau UU PDP) dan prinsip-prinsip enkripsi data (kriptografi).",

    "UI/UX Designer": 
        "UI/UX Designer adalah perancang pengalaman dan antarmuka pengguna, memastikan bahwa sebuah aplikasi tidak hanya terlihat indah (User Interface) tetapi juga mudah, nyaman, dan intuitif saat digunakan (User Experience). Peran mereka menjembatani kebutuhan bisnis dengan kenyamanan pengguna akhir. Proses kerja mereka berpusat pada manusia (Human-Centered Design), dimulai dengan riset pengguna (User Research) untuk memahami kebutuhan, perilaku, dan poin masalah (pain points) pengguna target. Berdasarkan hasil riset, mereka menyusun User Journey, Arsitektur Informasi, dan wireframe (kerangka kasar) aplikasi. Langkah selanjutnya adalah menciptakan desain visual High-Fidelity yang estetis, termasuk pemilihan warna, tipografi, ikon, dan tata letak, menggunakan tools utama seperti Figma atau Adobe XD. Mereka juga membangun prototype interaktif untuk mensimulasikan alur aplikasi dan melakukan Usability Testing untuk mendapatkan masukan langsung dari pengguna guna melakukan perbaikan desain secara iteratif sebelum diserahkan ke tim developer. Kemampuan empati, komunikasi, dan Design Thinking sangat krusial dalam peran ini.",

    "Mobile Developer": 
        "Mobile Developer adalah spesialis yang bertanggung jawab untuk merancang, membangun, dan memelihara aplikasi yang berjalan pada perangkat bergerak seperti smartphone dan tablet. Di tengah tren penggunaan perangkat mobile yang dominan, peran ini sangat dicari oleh industri. Tugas mereka meliputi implementasi desain antarmuka ke dalam platform mobile, optimasi performa aplikasi agar ringan dan hemat baterai, serta integrasi dengan berbagai layanan backend (API) dan fitur perangkat keras seperti GPS, kamera, atau notifikasi push. Alur kerja mereka dimulai dari pemahaman arsitektur aplikasi mobile, dilanjutkan dengan proses coding menggunakan bahasa pemrograman native seperti Kotlin/Java untuk Android dan Swift/Objective-C untuk iOS, atau menggunakan framework cross-platform modern seperti Flutter atau React Native. Setelah tahap pengembangan dan testing, mereka juga bertanggung jawab atas proses rilis aplikasi ke toko aplikasi resmi seperti Google Play Store dan Apple App Store, serta melakukan pemeliharaan dan update berkala berdasarkan feedback pengguna.",

    "AI Engineer": 
        "AI Engineer (Artificial Intelligence Engineer) adalah arsitek cerdas di balik pengembangan sistem kecerdasan buatan yang mampu belajar dan bertindak secara otomatis untuk memecahkan masalah yang kompleks. Mereka fokus pada penerapan praktis dari konsep Machine Learning dan Deep Learning ke dalam produk fungsional. Tugas utama mereka meliputi perancangan arsitektur model AI, pemilihan algoritma yang tepat, pemrosesan dan pelabelan data dalam jumlah besar untuk pelatihan model, serta integrasi model AI yang sudah terlatih ke dalam aplikasi utama melalui API. Alur kerja mereka melibatkan siklus definisi masalah, persiapan data, pelatihan model (model training), hyperparameter tuning untuk optimasi akurasi, hingga deployment model di lingkungan produksi. Mereka bekerja sangat erat dengan library dan framework seperti TensorFlow, PyTorch, Keras, dan OpenCV untuk aplikasi Computer Vision atau Hugging Face untuk Natural Language Processing (NLP). Pemahaman matematika lanjut (kalkulus, aljabar linier), konsep statistik, dan kemampuan pemrograman Python yang kuat sangat mutlak dibutuhkan.",

    "Game Developer": 
        "Game Developer adalah pencipta pengalaman interaktif yang imersif dan menghibur dalam bentuk permainan digital di berbagai platform, mulai dari PC, konsol, hingga mobile. Peran mereka menggabungkan kreativitas seni dengan logika pemrograman yang rumit. Tugas mereka sangat bervariasi, meliputi implementasi logika permainan (gameplay mechanics), pengaturan sistem fisika (physics engine), integrasi aset visual dan audio, serta optimasi grafis agar game berjalan lancar. Alur kerja mereka biasanya dimulai dari konsep di Game Design Document, kemudian masuk ke tahap *prototyping* untuk menguji ide utama, dilanjutkan dengan pengembangan penuh menggunakan Game Engine utama seperti Unity (menggunakan C#) atau Unreal Engine (menggunakan C++). Mereka juga harus mampu mengelola aset 2D/3D (menggunakan tools seperti Blender atau Maya), membangun kecerdasan buatan (AI) untuk karakter non-pemain (NPC), dan melakukan uji coba (playtesting) secara ketat untuk menemukan bug serta menyempurnakan pengalaman bermain ( polishing).",

    "DevOps Engineer": 
        "DevOps Engineer adalah jembatan fungsional yang menghubungkan tim pengembangan perangkat lunak (Development) dengan tim operasional IT (Operations). Tujuan utama mereka adalah meningkatkan kecepatan, efisiensi, dan kualitas proses pengiriman perangkat lunak (software delivery) melalui otomatisasi dan kolaborasi budaya. Tugas mereka meliputi otomatisasi siklus integrasi dan pengiriman kode (Continuous Integration/Continuous Deployment - CI/CD), manajemen infrastruktur server, dan pemantauan performa aplikasi di lingkungan produksi. Alur kerja mereka berfokus pada pembangunan pipeline otomatis menggunakan tools seperti Jenkins, GitLab CI, atau GitHub Actions. Mereka juga mengelola infrastruktur server menggunakan prinsip Infrastructure as Code (IaC) dengan tools seperti Terraform atau Ansible, serta mengatur skalabilitas dan orkestrasi aplikasi (seringkali menggunakan Kubernetes dan Docker) di platform cloud seperti AWS, Azure, atau Google Cloud. Kemampuan pemecahan masalah yang cepat, pemahaman mendalam tentang Linux, jaringan, dan keamanan jaringan sangat dibutuhkan.",

    "Database Administrator": 
        "Database Administrator (DBA) adalah penjaga integritas, keamanan, dan performa penyimpanan data perusahaan. Mereka bertanggung jawab penuh untuk memastikan bahwa basis data (database) tersimpan aman, selalu tersedia saat dibutuhkan, dan dapat diakses dengan cepat serta efisien. Tugas mereka meliputi perancangan skema database, konfigurasi dan instalasi server database, manajemen hak akses pengguna, serta perencanaan dan pelaksanaan backup dan recovery data secara berkala untuk mencegah kehilangan data akibat kegagalan sistem. Alur kerja mereka melibatkan pemantauan performa database secara real-time, melakukan optimasi struktur tabel dan query SQL (performance tuning), serta menerapkan patch keamanan terkini. Mereka bekerja keras dengan sistem manajemen basis data (DBMS) terkemuka seperti MySQL, PostgreSQL, Oracle, SQL Server, atau NoSQL database seperti MongoDB. Pemahaman mendalam tentang prinsip ACID, replikasi data, keamanan data tingkat lanjut, dan bahasa SQL sangat krusial dalam peran ini."
}

class CareerExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Career System Application - Future Swap")
        self.root.geometry("900x800")
        self.root.configure(bg="#1e272e")
        self.main_container = tk.Frame(self.root, bg="#1e272e")
        self.main_container.pack(fill="both", expand=True)
        self.user_photo_path = None
        self.last_prediction = None
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        header = tk.Frame(self.main_container, bg="#2c3e50", height=120)
        header.pack(fill="x")
        
        tk.Label(header, text="FUTURE SWAP", fg="#0fbcf9", bg="#2c3e50", 
                font=("Arial", 26, "bold")).pack(pady=40)
        
        menu_frame = tk.Frame(self.main_container, bg="#1e272e")
        menu_frame.pack(pady=50)

        def create_btn(txt, col, cmd):
            tk.Button(menu_frame, text=txt, bg=col, fg="white", width=35, pady=15, 
                    relief="flat", font=("Arial", 11, "bold"), cursor="hand2", command=cmd).pack(pady=10)

        create_btn(" ANALISIS KARIR", "#05c46b", self.show_ai_feature)
        create_btn(" EKSPLORASI BIDANG IT", "#3c40c6", self.show_encyclopedia)
        create_btn(" TREN PASAR & GAJI", "#f39c12", self.show_trends)

    # FITUR ANALISIS PERTANYAAN: Berdasarkan Metode RIASEC dan SKKNI
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

    def show_ai_feature(self):
        self.clear_screen()
        self.current_q_index = 0
        self.user_answers = []
        top_bar = tk.Frame(self.main_container, bg="#05c46b")
        top_bar.pack(fill="x")
        tk.Button(top_bar, text=" ⬅  Kembali", bg="#1e272e", fg="white", bd=0, command=self.show_main_menu).pack(side="left", padx=10, pady=10)
        
        self.quiz_container = tk.Frame(self.main_container, bg="#1e272e")
        self.quiz_container.pack(fill="both", expand=True, pady=50)
        self.display_question()

    def display_question(self):
        for widget in self.quiz_container.winfo_children(): widget.destroy()
        if self.current_q_index < len(self.LIST_PERTANYAAN):
            _, teks = self.LIST_PERTANYAAN[self.current_q_index]
            tk.Label(self.quiz_container, text=teks, bg="#1e272e", fg="white", font=("Arial", 14, "bold"), wraplength=600).pack(pady=30)
            opsi = [("Sangat Tidak Suka", 2), ("Tidak Suka", 4), ("Biasa Saja", 6), ("Suka", 8), ("Sangat Suka", 10)]
            for text, value in opsi:
                tk.Button(self.quiz_container, text=text, width=30, pady=8, bg="#2f3542", fg="white", command=lambda v=value: self.next_question(v)).pack(pady=5)
        else:
            self.run_ai_logic()

    def next_question(self, value):
        self.user_answers.append(value)
        self.current_q_index += 1
        self.display_question()

    def run_ai_logic(self):
        try:
            print(f"Jumlah jawaban: {len(self.user_answers)}") 
            
            feature_names = ['ai', 'data', 'cyber', 'uiux', 'frontend', 'backend', 'mobile', 'game', 'devops', 'dba']
            df_input = pd.DataFrame([self.user_answers], columns=feature_names)
            probs = model.predict_proba(df_input)[0]
            res = model.classes_[np.argmax(probs)]
            self.last_prediction = res
            for widget in self.quiz_container.winfo_children(): 
                widget.destroy()

            # Tampilan Hasil
            tk.Label(self.quiz_container, text=f"REKOMENDASI: {res.upper()}", 
                    bg="#1e272e", fg="#0fbcf9", font=("Arial", 18, "bold")).pack(pady=20)
            
            tk.Button(self.quiz_container, text=" ✨ TRANSFORMASI WAJAH", bg="#3c40c6", fg="white",
                    pady=12, padx=25, font=("Arial", 11, "bold"), 
                    command=self.show_ai_swap_screen).pack(pady=10)
            
            # Tampilan Gambar Radar Chart
            self.res_frame = tk.Frame(self.quiz_container, bg="#2f3542")
            self.res_frame.pack(fill="both", expand=True, padx=40)
            self.draw_radar(self.user_answers)
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"LOG ERROR DETAIL: {error_msg}")
            messagebox.showerror("Error Logika", f"Terjadi kesalahan saat analisis: {e}")
            self.show_main_menu()

    def draw_radar(self, values):
        labels = ["AI", "Data", "Cyber", "UIUX", "Front", "Back", "Mobile", "Game", "DevOps", "DBA"]
        fig = plt.figure(figsize=(4, 3), dpi=85, facecolor='#2f3542')
        ax = fig.add_subplot(111, polar=True, facecolor='#2f3542')
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        v = values + [values[0]]; a = angles + [angles[0]]
        ax.plot(a, v, color='#05c46b', linewidth=2)
        ax.fill(a, v, color='#05c46b', alpha=0.3)
        ax.set_thetagrids(np.degrees(angles), labels)
        canvas = FigureCanvasTkAgg(fig, master=self.res_frame)
        canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- LOGIKA INSIGHTFACE (FITUR SWAP) ---
    def show_ai_swap_screen(self):
        self.clear_screen()
        top_bar = tk.Frame(self.main_container, bg="#3c40c6"); top_bar.pack(fill="x")
        tk.Button(top_bar, text=" ⬅  Kembali", bg="#1e272e", fg="white", bd=0, command=self.show_main_menu).pack(side="left", padx=10, pady=10)
        
        frame = tk.Frame(self.main_container, bg="#1e272e"); frame.pack(fill="both", expand=True, pady=20)
        tk.Label(frame, text=f"Transformasi: {self.last_prediction}", fg="white", bg="#1e272e", font=("Arial", 14)).pack()
        
        btn_pick = tk.Button(frame, text="PILIH FOTO WAJAH ANDA", bg="#05c46b", fg="white", pady=15, command=self.process_ai_swap)
        btn_pick.pack(pady=20)
        
        self.display_area = tk.Frame(frame, bg="#2f3542", width=500, height=400); self.display_area.pack()
        self.display_area.pack_propagate(False)

    def process_ai_swap(self):
        path_user = filedialog.askopenfilename()
        if not path_user: return
        
        # Menambahkan Indikator Loading
        for w in self.display_area.winfo_children(): w.destroy()
        self.loading_label = tk.Label(self.display_area, text="⌛ Sedang Memproses...\nMohon Tunggu Sebentar", 
                                    fg="#f1c40f", bg="#2f3542", font=("Arial", 12, "bold"))
        self.loading_label.pack(expand=True)
        
        thread = threading.Thread(target=self.run_heavy_ai_logic, args=(path_user,))
        self.progress = ttk.Progressbar(self.display_area, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start(10)
        thread.start()

    def run_heavy_ai_logic(self, path_user):
        try:
            # 1. Membaca foto user
            img_u = cv2.imread(path_user)
            if img_u is None:
                self.root.after(0, lambda: messagebox.showerror("Error", "Gagal membaca file foto user, Pastikan foto wajah jelas dan detail."))
                return

            face_u = app_face.get(img_u)

            if len(face_u) == 0:
                self.root.after(0, lambda: self.loading_label.config(text="❌ Wajah tidak terdeteksi!"))
                return

            # 2. DETEKSI GENDER
            gender_code = face_u[0].gender
            gender_suffix = "m" if gender_code == 1 else "f"
            
            # 3. Path Template
            clean = self.last_prediction.lower().replace(" ", "_").replace("/", "")
            template_filename = f"{clean}_{gender_suffix}.png"
            
            base_path = os.path.dirname(os.path.abspath(__file__))
            path_template = os.path.join(base_path, "swap_assets", template_filename)

            print(f"DEBUG: Mencari template -> {path_template}")

            if not os.path.exists(path_template):
                self.root.after(0, lambda t=template_filename: messagebox.showerror("Error", f"File template tidak ditemukan:\n{t}"))
                return

            # 4. Eksekusi Swap
            img_t = cv2.imread(path_template)
            face_t = app_face.get(img_t)
            
            if len(face_t) > 0:
                # Proses Swap
                res_img = swapper.get(img_t, face_t[0], face_u[0], paste_back=True)
                res_rgb = cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB)
                res_pil = Image.fromarray(res_rgb)
                res_pil.thumbnail((480, 380))
                
                # Tampilkan hasil
                self.root.after(0, lambda img=res_pil: self.show_final_result(img))
            else:
                self.root.after(0, lambda: self.loading_label.config(text="❌ Wajah di template tidak terbaca!"))

        except Exception:
            import traceback
            err = traceback.format_exc().splitlines()[-1]
            print(f"LOG ERROR: {err}")
            
            self.root.after(0, lambda: messagebox.showerror("Error AI", "Terjadi kendala pada deteksi wajah. Pastikan foto jelas."))

    def show_final_result(self, res_pil):
        # Tampilan image hasil akhir
        self.final_tk = ImageTk.PhotoImage(res_pil)
        for w in self.display_area.winfo_children(): w.destroy()
        tk.Label(self.display_area, image=self.final_tk, bg="#2f3542").pack(expand=True)
        messagebox.showinfo("Berhasil", "FaceSwap Sukses!")

    # ==========================================
    # MENU 2: ENSIKLOPEDIA (EKSPLORASI IT)
    # ==========================================
    def show_encyclopedia(self):
        self.clear_screen()
        
        top_bar = tk.Frame(self.main_container, bg="#485460")
        top_bar.pack(fill="x")
        tk.Button(top_bar, text="⬅ Kembali", bg="#1e272e", fg="white", bd=0, command=self.show_main_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_bar, text="PERKEMBANGAN KARIR IT DIGITAL", bg="#485460", fg="white", font=("Arial", 14, "bold")).pack(side="left", padx=25)

        self.split_frame = tk.Frame(self.main_container, bg="#1e272e")
        self.split_frame.pack(fill="both", expand=True, padx=15, pady=20)

        list_container = tk.Frame(self.split_frame, bg="#1e272e", width=280) # Ubah dari 250 ke 280
        list_container.pack(side="left", fill="y", padx=(0, 15))
        list_container.pack_propagate(False)

        canvas_list = tk.Canvas(list_container, bg="#1e272e", highlightthickness=0)
        scrollbar_list = ttk.Scrollbar(list_container, orient="vertical", command=canvas_list.yview)
        self.scrollable_list_frame = tk.Frame(canvas_list, bg="#1e272e")

        self.scrollable_list_frame.bind("<Configure>", lambda e: canvas_list.configure(scrollregion=canvas_list.bbox("all")))
        canvas_list.create_window((0, 0), window=self.scrollable_list_frame, anchor="nw")
        canvas_list.configure(yscrollcommand=scrollbar_list.set)

        canvas_list.pack(side="left", fill="both", expand=True)
        scrollbar_list.pack(side="right", fill="y")

        for i, (nama, _) in enumerate(NARRATIVE_KARIR.items(), 1):
            nomor = f"{i:02d}. "
            btn = tk.Button(self.scrollable_list_frame, text=f"{nomor}{nama.upper()}", 
                            font=("Arial", 9, "bold"), fg="#d2dae2", bg="#2f3542", 
                            width=28, pady=10, relief="flat", anchor="w", padx=10, cursor="hand2")
            btn.pack(pady=4, fill="x")
            
            def make_cmd(n=nama, b=btn):
                return lambda: self.select_career(n, b)
            btn.config(command=make_cmd())
            
            def on_enter(e, b=btn): 
                if b['bg'] != "#3c40c6": b.config(bg="#485460")
            def on_leave(e, b=btn): 
                if b['bg'] != "#3c40c6": b.config(bg="#2f3542")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        self.career_buttons = self.scrollable_list_frame.winfo_children()

        # Panel Detail (Image + Narasi)
        self.detail_panel = tk.Frame(self.split_frame, bg="#2f3542", bd=1, relief="solid")
        self.detail_panel.pack(side="left", fill="both", expand=True)

        # Area Gambar (Top Right)
        self.image_container = tk.Frame(self.detail_panel, bg="#2f3542", height=250)
        self.image_container.pack(fill="x", padx=10, pady=10)
        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(self.image_container, text="[ Pilih Profesi untuk Melihat Gambar ]", 
                                    bg="#2f3542", fg="#747d8c", font=("Arial", 10, "italic"))
        self.image_label.pack(fill="both", expand=True)

        # Area Teks Narasi (Bottom Right)
        text_container = tk.Frame(self.detail_panel, bg="#2f3542")
        text_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar Teks Narasi
        scrollbar_txt = ttk.Scrollbar(text_container)
        scrollbar_txt.pack(side="right", fill="y")

        self.narasi_text = tk.Text(text_container, wrap="word", font=("Helvetica", 11), 
                                bg="#2f3542", fg="white", bd=0, padx=10, pady=10,
                                yscrollcommand=scrollbar_txt.set, spacing2=5)
        self.narasi_text.pack(side="left", fill="both", expand=True)
        scrollbar_txt.config(command=self.narasi_text.yview)
        
        # Teks Awalan
        self.narasi_text.insert("1.0", "Silakan pilih salah satu profesi di sebelah kiri untuk melihat penjelasan deskriptif yang komprehensif.")
        self.narasi_text.config(state="disabled")

    def select_career(self, name, clicked_btn):
        for btn in self.career_buttons:
            if isinstance(btn, tk.Button): btn.config(bg="#2f3542")
        clicked_btn.config(bg="#3c40c6")

        narrative = NARRATIVE_KARIR[name]

        self.narasi_text.config(state="normal")
        self.narasi_text.delete("1.0", tk.END)
        self.narasi_text.insert("1.0", narrative)
        self.narasi_text.config(state="disabled")

        self.update_image(name)

    def update_image(self, name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        clean_name = name.lower()
        if "." in clean_name:
            clean_name = clean_name.split(".", 1)[1].strip()
        
        clean_name = clean_name.replace(" ", "_").replace("/", "").replace("-", "_")

        base_image_filenames = {
            "frontend_developer": "frontend",
            "backend_developer": "backend",
            "data_scientist": "data_science",
            "cyber_security": "cyber_security",
            "uiux_designer": "uiux",
            "mobile_developer": "mobile",
            "ai_engineer": "ai",
            "game_developer": "game",
            "devops_engineer": "devops",
            "database_administrator": "dba"
        }
        
        base_name = base_image_filenames.get(clean_name)
        
        if base_name:
            filename = f"{base_name}.png"
            image_path = os.path.join(script_dir, "templates", filename)
            
            try:
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img.thumbnail((450, 250)) 
                    self.img_tk = ImageTk.PhotoImage(img)
                    self.image_label.config(image=self.img_tk, text="")
                else:
                    self.image_label.config(image="", text=f"File Tidak Ada:\n{filename}")
            except Exception as e:
                self.image_label.config(image="", text=f"Gagal Load Gambar: {e}")

    # ==========================================
    # MENU 3: TREN GAJI
    # ==========================================
    def show_trends(self):
        self.clear_screen()
        
        top_bar = tk.Frame(self.main_container, bg="#f39c12")
        top_bar.pack(fill="x")
        tk.Button(top_bar, text="⬅ Kembali", bg="#1e272e", fg="white", bd=0, padx=15, 
                command=self.show_main_menu, cursor="hand2").pack(side="left", padx=10, pady=10)
        tk.Label(top_bar, text="PROYEKSI TREN GAJI & PASAR IT 2026", bg="#f39c12", fg="#1e272e", 
                font=("Arial", 12, "bold")).pack(side="left", padx=20)

        content_container = tk.Frame(self.main_container, bg="#1e272e")
        content_container.pack(fill="both", expand=True, padx=20)

        # --- DATA PROYEKSI GAJI KARIR 2026 ---
        profesi = ['Frontend', 'Backend', 'Data Sci', 'Cyber Sec', 'UI/UX', 'Mobile', 'AI Eng', 'Game Dev', 'DevOps', 'DBA']
        gaji = [6.5, 7.0, 7.5, 10.3, 5.0, 8.0, 12.0, 6.0, 9.5, 7.2]
        
        colors = ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f1c40f', '#e67e22', '#2ecc71', '#34495e', '#7f8c8d', '#d35400']

        # Menambahkan Grafik
        fig, ax = plt.subplots(figsize=(7, 5), dpi=90, facecolor='#1e272e')
        ax.set_facecolor('#1e272e')
        
        bars = ax.barh(profesi, gaji, color=colors, edgecolor='white', linewidth=0.5)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{width}jt', va='center', color='white', fontweight='bold', fontsize=9)

        ax.set_title("Estimasi Gaji Bulanan 2026 (Juta IDR)", color="white", fontsize=13, pad=15, fontweight='bold')
        ax.tick_params(colors='white', labelsize=9)
        ax.set_xlim(0, 22)
        
        for spine in ax.spines.values():
            spine.set_color('#485460')
        
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=content_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- PANEL INSIGHT ---
        insight_frame = tk.Frame(self.main_container, bg="#2f3542", padx=20, pady=15)
        insight_frame.pack(fill="x", side="bottom", padx=20, pady=20)
        
        highest_job = profesi[gaji.index(max(gaji))]
        
        insight_text = (
            f"ANALISIS PASAR 2026:\n"
            f"1. Dominasi AI: {highest_job} menjadi profesi paling mahal karena integrasi LLM di berbagai industri.\n"
            f"2. Keamanan Data: Cyber Security naik signifikan menyusul regulasi perlindungan data global.\n"
            f"3. Full-Stack Trend: Perusahaan mulai mengapresiasi tinggi developer yang menguasai DevOps & Backend."
        )
        
        lbl_insight = tk.Label(insight_frame, text=insight_text, bg="#2f3542", fg="#d2dae2", 
                            justify="left", font=("Arial", 10), wraplength=800)
        lbl_insight.pack(anchor="w")

        # --- CATATAN SUMBER DATA ---
        lbl_source = tk.Label(insight_frame, text="Sumber: Platform Job & Salary Insights", 
                            bg="#2f3542", fg="#747d8c",
                            font=("Arial", 8, "italic"))
        lbl_source.pack(anchor="e", pady=(10, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = CareerExpertSystem(root)
    root.mainloop()