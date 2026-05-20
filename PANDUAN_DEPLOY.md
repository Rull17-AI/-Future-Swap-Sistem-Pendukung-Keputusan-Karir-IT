# 📘 PANDUAN DEPLOY — Future Swap Project

---

## ═══════════════════════════════
## FASE 1: UPLOAD KE GITHUB
## ═══════════════════════════════

### A. Persiapan (Lakukan Sekali)

1. Daftar/login di https://github.com
2. Install Git: https://git-scm.com/downloads
3. Buka terminal/CMD, konfigurasi identitas:
   ```
   git config --global user.name "Nama Kamu"
   git config --global user.email "email@kamu.com"
   ```

---

### B. Buat Repository Baru di GitHub

1. Klik tombol **"New"** (hijau) di GitHub
2. Isi:
   - Repository name: `future-swap`
   - Description: `Sistem Pendukung Keputusan Karir IT Berbasis Visual Future Face Swap`
   - Pilih: **Public**
   - Jangan centang apapun (README/gitignore)
3. Klik **"Create repository"**
4. **Salin URL** repository (contoh: `https://github.com/username/future-swap.git`)

---

### C. Upload File ke GitHub

Buka terminal/CMD di folder project kamu, lalu jalankan perintah berikut **satu per satu**:

```bash
# 1. Inisialisasi Git
git init

# 2. Tambahkan semua file (KECUALI yang ada di .gitignore)
git add .

# 3. Commit pertama
git commit -m "Initial commit: Future Swap IT Career System"

# 4. Hubungkan ke GitHub (ganti URL dengan milikmu)
git remote add origin https://github.com/USERNAME/future-swap.git

# 5. Push ke GitHub
git branch -M main
git push -u origin main
```

---

### D. Cara Upload File ONNX yang 528MB

File `inswapper_128.onnx` terlalu besar untuk GitHub biasa.
**Solusi: tambahkan instruksi download di README** (sudah dibuatkan).

Atau gunakan **Git LFS** (opsional, perlu install terpisah):
```bash
git lfs install
git lfs track "*.onnx"
git add .gitattributes
git add inswapper_128.onnx
git commit -m "Add ONNX model via LFS"
git push
```

---

## ═══════════════════════════════
## FASE 2: KONVERSI KE WEB (STREAMLIT)
## ═══════════════════════════════

### Kenapa Perlu Dikonversi?

Aplikasi saat ini pakai **Tkinter** (desktop only).
Untuk bisa diakses online, harus diubah ke **Streamlit** (web-based Python).

---

### Cara Deploy ke Streamlit Cloud (Gratis)

1. Buka https://streamlit.io/cloud
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository `future-swap`
5. Set **Main file path**: `app_streamlit.py`
6. Klik **Deploy**

URL akan jadi: `https://username-future-swap.streamlit.app`

---

### Catatan Penting untuk Streamlit

- File ONNX 528MB **tidak bisa** di-host di Streamlit Cloud free tier (limit 1GB RAM)
- **Solusi**: Fitur face swap bisa dinonaktifkan dulu, fokus ke fitur kuis + radar chart + ensiklopedia
- Model `.pkl` 19.4MB = **aman**, bisa langsung dipakai

---

## ═══════════════════════════════
## RINGKASAN FILE YANG DIBUTUHKAN
## ═══════════════════════════════

Setelah semua selesai, struktur GitHub kamu akan jadi:

```
future-swap/
├── app_gui.py              ✅ Upload
├── app_streamlit.py        ✅ Upload (versi web — akan dibuatkan)
├── train_model.py          ✅ Upload
├── model_karir_it.pkl      ✅ Upload (19.4MB, masih aman)
├── requirements.txt        ✅ Sudah dibuatkan
├── .gitignore              ✅ Sudah dibuatkan
├── README.md               ✅ Sudah dibuatkan
├── swap_assets/            ✅ Upload semua isinya
├── templates/              ✅ Upload semua isinya
└── inswapper_128.onnx      ⚠️ SKIP — terlalu besar, instruksi download di README
```
