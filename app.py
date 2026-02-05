import streamlit as st
import os
from supabase import create_client, Client
from datetime import datetime
import hashlib

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfiguration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
UPLOAD_PIN = os.getenv("UPLOAD_PIN", "")  # Optional: PIN für Upload-Schutz
BUCKET_NAME = "polterer-photos"

# Supabase Client
@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# Session State für PIN
if "pin_verified" not in st.session_state:
    st.session_state.pin_verified = False

# App Layout
st.set_page_config(
    page_title="Polterer Fotos 📸",
    page_icon="🎉",
    layout="wide"
)

st.title("🎉 Polterer Foto-Upload")
st.markdown("Lade deine Fotos vom Polterer hoch und schau dir die Galerie an!")

# PIN-Schutz (optional)
if UPLOAD_PIN and not st.session_state.pin_verified:
    with st.form("pin_form"):
        st.subheader("🔒 PIN eingeben")
        pin_input = st.text_input("PIN:", type="password")
        submit = st.form_submit_button("Weiter")
        
        if submit:
            if pin_input == UPLOAD_PIN:
                st.session_state.pin_verified = True
                st.rerun()
            else:
                st.error("❌ Falscher PIN!")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["📤 Upload", "🖼️ Galerie"])

with tab1:
    st.subheader("Fotos hochladen")
    
    # Uploader Name (optional)
    uploader_name = st.text_input("Dein Name (optional):", placeholder="z.B. Anna")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Wähle Fotos aus:",
        type=["jpg", "jpeg", "png", "heic", "heif"],
        accept_multiple_files=True,
        help="Du kannst mehrere Fotos gleichzeitig auswählen"
    )
    
    if uploaded_files:
        if st.button("🚀 Alle hochladen", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            success_count = 0
            total = len(uploaded_files)
            
            for idx, uploaded_file in enumerate(uploaded_files):
                try:
                    # Dateiname mit Timestamp für Eindeutigkeit
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_hash = hashlib.md5(uploaded_file.name.encode()).hexdigest()[:8]
                    filename = f"{timestamp}_{file_hash}_{uploaded_file.name}"
                    
                    # Metadata
                    metadata = {
                        "uploaded_at": datetime.now().isoformat(),
                        "original_name": uploaded_file.name,
                    }
                    if uploader_name:
                        metadata["uploader"] = uploader_name
                    
                    # Upload zu Supabase Storage
                    file_bytes = uploaded_file.read()
                    supabase.storage.from_(BUCKET_NAME).upload(
                        filename,
                        file_bytes,
                        {
                            "content-type": uploaded_file.type,
                            "x-upsert": "false"
                        }
                    )
                    
                    success_count += 1
                    status_text.text(f"✅ {uploaded_file.name} hochgeladen ({success_count}/{total})")
                    
                except Exception as e:
                    st.error(f"❌ Fehler bei {uploaded_file.name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / total)
            
            st.success(f"🎉 {success_count} von {total} Fotos erfolgreich hochgeladen!")
            st.balloons()

with tab2:
    st.subheader("Foto-Galerie")
    
    try:
        # Alle Dateien aus dem Bucket holen
        files = supabase.storage.from_(BUCKET_NAME).list()
        
        if not files:
            st.info("📭 Noch keine Fotos hochgeladen.")
        else:
            st.write(f"**{len(files)} Fotos**")
            
            # Grid Layout (3 Spalten)
            cols = st.columns(3)
            
            for idx, file in enumerate(files):
                with cols[idx % 3]:
                    # Public URL generieren
                    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file["name"])
                    
                    # Thumbnail anzeigen
                    st.image(public_url, use_container_width=True)
                    
                    # Dateiname und Download
                    st.caption(f"📷 {file['name']}")
                    st.markdown(f"[⬇️ Download]({public_url})")
    
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Galerie: {str(e)}")

# Footer
st.markdown("---")
st.markdown("💙 Gebaut mit Streamlit · Gespeichert in Supabase")
