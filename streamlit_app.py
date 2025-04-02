import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Configuration de la page
st.set_page_config(page_title="Gestion des Freelancers Intelcia", layout="wide")

# Affichage des logos
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
with top_col1:
    st.image("https://ibb.co/tTQpxD4h", width=150)
with top_col3:
    st.image("https://ibb.co/XxQF3t7J", width=150)

# Style CSS pour améliorer l'apparence
st.markdown("""
    <style>
        .main {background: linear-gradient(to right, #1e3c72, #2a5298); color: white;}
        h1 {color: #ffffff; text-align: center;}
        .stMetric {background: #1e3c72; padding: 10px; border-radius: 10px; 
                   box-shadow: 0px 4px 6px rgba(255, 255, 255, 0.2); color: white;}
        .stButton>button {background-color: #2a5298; color: white; border-radius: 5px;}
        .stTextInput>div>div>input {background-color: #ffffff; color: #000000; border-radius: 5px;}
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
    
    # Afficher un aperçu des données
    st.subheader("🔍 Aperçu des données")
    st.write(df.head())
    
    # Convertir les dates
    df['Date début contrat'] = pd.to_datetime(df['Date début contrat'])
    df['Date fin contrat'] = pd.to_datetime(df['Date fin contrat'])
    
    # Calculer les indicateurs
    total_freelancers = len(df)
    expired_contracts = len(df[df['Temps restant (jours)'] < 0])
    soon_expiring_contracts = len(df[df['Temps restant (jours)'] <= 30])
    avg_time_remaining = df[df['Temps restant (jours)'] > 0]['Temps restant (jours)'].mean()
    speciality_distribution = df['Spécialité IT'].value_counts()
    
    # Affichage des indicateurs avec animations
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="👥 Total Freelancers", value=total_freelancers)
    with col2:
        st.metric(label="❌ Contrats Expirés", value=expired_contracts)
    with col3:
        st.metric(label="⏳ Contrats < 30 jours", value=soon_expiring_contracts)
    with col4:
        st.metric(label="📅 Moyenne Temps Restant", value=f"{avg_time_remaining:.1f} jours")
    
    # Graphique de répartition des spécialités
    st.subheader("📊 Répartition des spécialités IT")
    fig = px.bar(x=speciality_distribution.index, y=speciality_distribution.values,
                 labels={'x': 'Spécialité', 'y': 'Nombre de Freelancers'},
                 color=speciality_distribution.index, color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig, use_container_width=True)
    
    # Graphique de répartition des contrats actifs/expirés
    st.subheader("📊 Contrats Actifs vs Expirés")
    contracts_status = pd.DataFrame({
        "Statut": ["Actifs", "Expirés"],
        "Nombre": [total_freelancers - expired_contracts, expired_contracts]
    })
    fig2 = px.pie(contracts_status, names='Statut', values='Nombre', color='Statut',
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Alerte pour les contrats expirant bientôt
    if soon_expiring_contracts > 0:
        st.warning(f"⚠️ {soon_expiring_contracts} contrats expirent dans moins de 30 jours.")
        st.write(df[df['Temps restant (jours)'] <= 30])
    
    # Filtrage des données
    st.subheader("🔎 Recherche de Freelancers")
    search_term = st.text_input("Rechercher par nom ou spécialité")
    if search_term:
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
        st.write(filtered_df)
    
    # Export des données filtrées
    st.subheader("📂 Exporter les données")
    if st.button("💾 Télécharger les données filtrées"):
        filtered_df.to_csv("freelancers_filtered.csv", index=False)
        st.success("✅ Données exportées avec succès !")
