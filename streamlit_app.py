import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Configuration de la page
st.set_page_config(page_title="Gestion des Freelancers Intelcia", layout="wide")

# Style CSS
st.markdown("""
    <style>
        .main {background: linear-gradient(to right, #1e3c72, #2a5298); color: white;}
        h1 {color: #ffffff; text-align: center;}
        .stButton>button {background-color: #2a5298; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Titre animé
st.title("🚀 Gestion des Freelancers Intelcia")

# Upload du fichier CSV
uploaded_file = st.file_uploader("📂 Uploader un fichier CSV", type=["csv"])
if uploaded_file:
    with st.spinner('📊 Chargement des données...'):
        time.sleep(1)
        df = pd.read_csv(uploaded_file)
    
    # Convertir les dates
    df['Date début contrat'] = pd.to_datetime(df['Date début contrat'])
    df['Date fin contrat'] = pd.to_datetime(df['Date fin contrat'])
    df['Temps restant (jours)'] = (df['Date fin contrat'] - pd.Timestamp.today()).dt.days
    
    # Afficher un aperçu des données
    st.subheader("🔍 Aperçu des données")
    st.write(df.head())
    
    # Identifier les contrats expirant bientôt
    soon_expiring_df = df[df['Temps restant (jours)'] <= 30]
    
    # Bouton de renouvellement
    if not soon_expiring_df.empty:
        st.subheader("🔄 Renouvellement des contrats")
        st.warning(f"⚠️ {len(soon_expiring_df)} contrats expirent dans moins de 30 jours.")
        st.write(soon_expiring_df)
        
        renewal_days = st.number_input("Durée du renouvellement (jours)", min_value=1, max_value=365, value=30)
        if st.button("🔄 Renouveler les contrats"):
            df.loc[df['Temps restant (jours)'] <= 30, 'Date fin contrat'] += pd.to_timedelta(renewal_days, unit='D')
            df['Temps restant (jours)'] = (df['Date fin contrat'] - pd.Timestamp.today()).dt.days
            df.to_csv("freelancers_updated.csv", index=False)
            st.success("✅ Contrats renouvelés avec succès !")
            st.write(df[df['Temps restant (jours)'] <= 30])
    
    # Affichage des statistiques
    st.subheader("📊 Statistiques des contrats")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Freelancers", len(df))
    col2.metric("❌ Contrats Expirés", len(df[df['Temps restant (jours)'] < 0]))
    col3.metric("⏳ Contrats < 30 jours", len(soon_expiring_df))
    
    # Export des données mises à jour
    if st.button("💾 Télécharger les données mises à jour"):
        df.to_csv("freelancers_updated.csv", index=False)
        st.success("✅ Données mises à jour exportées avec succès !")
