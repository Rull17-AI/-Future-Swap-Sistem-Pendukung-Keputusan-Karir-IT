import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Membuat Dataset
np.random.seed(42)
n_samples = 2000

data = {
    'ai': np.random.randint(1, 11, n_samples),
    'data': np.random.randint(1, 11, n_samples),
    'cyber': np.random.randint(1, 11, n_samples),
    'uiux': np.random.randint(1, 11, n_samples),
    'frontend': np.random.randint(1, 11, n_samples),
    'backend': np.random.randint(1, 11, n_samples),
    'mobile': np.random.randint(1, 11, n_samples),
    'game': np.random.randint(1, 11, n_samples),
    'devops': np.random.randint(1, 11, n_samples),
    'dba': np.random.randint(1, 11, n_samples)
}

df = pd.DataFrame(data)

# Logika Pendeteksi Label
# Aturannya dari tiap profesi memiliki spesialisasi sesuai urutan soal
def rule_engine(row): 
    # prioritas untuk skor tertinggi yang spesifik.
    if row['ai'] >= 9: return "AI Engineer"
    if row['cyber'] >= 9: return "Cyber Security"
    if row['data'] >= 9: return "Data Scientist"
    if row['uiux'] >= 9: return "UI/UX Designer"
    if row['game'] >= 9: return "Game Developer"
    if row['mobile'] >= 8: return "Mobile Developer"
    if row['frontend'] >= 8: return "Frontend Developer"
    if row['backend'] >= 8: return "Backend Developer"
    if row['devops'] >= 8: return "DevOps Engineer"
    if row['dba'] >= 8: return "Database Administrator"
    
    # Jika tidak ada yang menonjol, ambil nilai maksimal dari kolom
    return df.columns[np.argmax(row)] 

df['target'] = df.apply(rule_engine, axis=1)

# Training
X = df.drop('target', axis=1)
y = df['target']

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X, y)

# Ekspor Model
joblib.dump(model, 'model_karir_it.pkl')
print("--- SUKSES: Model Baru dengan 10 Fitur (SKKNI) telah dibuat! ---")