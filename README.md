# 🎭 Future Swap — Sistem Pendukung Keputusan Karir IT

> Sistem berbasis AI yang membantu kamu menemukan karir IT yang paling sesuai dengan minat dan kepribadianmu — lalu memvisualisasikannya lewat teknologi **Face Swap**.

---

## 📸 Preview

Aplikasi ini memiliki 3 fitur utama:
1. **Analisis Karir** — Kuis 10 pertanyaan berdasarkan metode SKKNI, hasilnya divisualisasikan dengan Radar Chart
2. **Transformasi Wajah** — Wajahmu akan "ditransformasi" ke profesi IT yang direkomendasikan menggunakan InsightFace
3. **Ensiklopedia IT** — Penjelasan mendalam tentang 10 profesi IT beserta proyeksi gaji 2026

---

## 🧠 Tech Stack

| Komponen | Teknologi |
|---|---|
| GUI | Python Tkinter |
| Model Klasifikasi | Scikit-Learn (Random Forest) |
| Face Swap Engine | InsightFace + ONNX Runtime |
| Visualisasi | Matplotlib |
| Image Processing | OpenCV, Pillow |

---

## 🗂️ Struktur Folder

```
future_swap/
├── app_gui.py              # Aplikasi utama (Tkinter GUI)
├── train_model.py          # Script training model ML
├── model_karir_it.pkl      # Model Random Forest terlatih
├── inswapper_128.onnx      # ⚠️ Model InsightFace (unduh terpisah)
├── requirements.txt
├── swap_assets/            # Foto referensi profesi IT (f & m)
│   ├── ai_engineer_f.jpg
│   ├── ai_engineer_m.jpg
│   └── ... (20 foto total)
└── templates/              # Gambar ilustrasi tiap bidang IT
    ├── ai.png
    ├── backend.png
    └── ... (10 gambar)
```

---

## ⚙️ Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/USERNAME/future-swap.git
cd future-swap
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download Model InsightFace (wajib)
File `inswapper_128.onnx` (528 MB) tidak disertakan di repo karena ukurannya besar.
Download di: [InsightFace Model Zoo](https://github.com/deepinsight/insightface/tree/master/model_zoo)

Letakkan file tersebut langsung di folder root project:
```
future_swap/
└── inswapper_128.onnx   ← letakkan di sini
```

### 4. Jalankan Aplikasi
```bash
python app_gui.py
```

---

## 📋 Profesi IT yang Didukung

| No | Profesi | Kode |
|---|---|---|
| 1 | AI Engineer | `ai` |
| 2 | Data Scientist | `data` |
| 3 | Cyber Security | `cyber` |
| 4 | UI/UX Designer | `uiux` |
| 5 | Frontend Developer | `frontend` |
| 6 | Backend Developer | `backend` |
| 7 | Mobile Developer | `mobile` |
| 8 | Game Developer | `game` |
| 9 | DevOps Engineer | `devops` |
| 10 | Database Administrator | `dba` |

---

## 📊 Estimasi Gaji Profesi IT 2026 (IDR/bulan)

| Profesi | Estimasi Gaji |
|---|---|
| AI Engineer | Rp 12.000.000 |
| Cyber Security | Rp 10.300.000 |
| DevOps Engineer | Rp 9.500.000 |
| Mobile Developer | Rp 8.000.000 |
| Database Administrator | Rp 7.200.000 |
| Backend Developer | Rp 7.000.000 |
| Data Scientist | Rp 7.500.000 |

---

## 👥 Tim Pengembang

> Project ini dikembangkan sebagai tugas akhir mata kuliah Data Science & Machine Learning.

---

## 📄 Lisensi

MIT License — bebas digunakan untuk keperluan edukasi.
