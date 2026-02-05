# 🎉 Polterer Foto-Upload App

Eine einfache Streamlit-Web-App zum Hochladen und Anzeigen von Fotos vom Polterer. Gespeichert in Supabase Storage.

## Features

- 📤 **Multi-File-Upload**: Mehrere Fotos gleichzeitig hochladen
- 🔒 **PIN-Schutz**: Optionaler PIN zum Schutz vor unerwünschten Uploads
- 🖼️ **Galerie**: Alle hochgeladenen Fotos anzeigen
- ⬇️ **Download**: Jedes Foto einzeln herunterladen
- 👤 **Uploader-Name**: Optional Name beim Upload angeben

## Supabase Setup

### 1. Storage Bucket erstellen

1. Gehe zu deinem [Supabase Dashboard](https://app.supabase.com)
2. Wähle dein Projekt aus
3. Navigiere zu **Storage** (linkes Menü)
4. Klicke auf **New bucket**
5. Name: `polterer-photos`
6. **Public bucket**: ✅ **JA** (damit Fotos in der Galerie angezeigt werden können)
7. Klicke **Create bucket**

### 2. API Keys holen

1. Im Supabase Dashboard: **Settings** → **API**
2. Kopiere:
   - **Project URL** (z.B. `https://xyz.supabase.co`)
   - **anon/public key** (unter "Project API keys")

## Lokale Installation & Test

```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. .env Datei erstellen
cp .env.example .env

# 3. .env mit deinen Werten füllen:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-public-key
# UPLOAD_PIN=1234  (optional)

# 4. App starten
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## Cloud Deployment (Streamlit Community Cloud)

### Option 1: Streamlit Community Cloud (empfohlen, kostenlos)

1. **GitHub Repository erstellen**:
   - Pushe den Code in ein GitHub Repo (privat oder öffentlich)

2. **Streamlit Cloud**:
   - Gehe zu [share.streamlit.io](https://share.streamlit.io)
   - Klicke **New app**
   - Verbinde dein GitHub-Konto
   - Wähle dein Repository aus
   - Main file path: `app.py`
   - **Advanced settings** → **Secrets**:
     ```toml
     SUPABASE_URL = "https://your-project.supabase.co"
     SUPABASE_KEY = "your-anon-public-key"
     UPLOAD_PIN = "1234"
     ```
   - Klicke **Deploy**

3. **Fertig!** Deine App ist jetzt unter `https://your-app-name.streamlit.app` erreichbar.

### Option 2: Railway (kostenlos, aber Credit Card erforderlich)

1. Gehe zu [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. Wähle dein Repository
4. Füge Environment Variables hinzu (wie oben)
5. Deploy!

### Option 3: Render (kostenlos)

1. Gehe zu [render.com](https://render.com)
2. **New** → **Web Service**
3. Verbinde GitHub Repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Füge Environment Variables hinzu
7. Deploy!

## Sicherheit

- **PIN**: Wenn du einen `UPLOAD_PIN` setzt, müssen Benutzer diesen eingeben, bevor sie hochladen können.
- **Supabase anon key**: Die anon/public key ist sicher für Client-seitige Apps. Stelle sicher, dass dein Storage Bucket public ist, damit die Galerie funktioniert.

## Support

Bei Fragen: Frag Molty! 🦀
