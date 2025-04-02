import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Gestion des Freelancers Intelcia")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Uploader un fichier CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Afficher un aperçu des données
    st.subheader("Aperçu des données")
    st.write(df.head())
    
    # Convertir les dates
    df['Date début contrat'] = pd.to_datetime(df['Date début contrat'])
    df['Date fin contrat'] = pd.to_datetime(df['Date fin contrat'])
    
    # Indicateurs clés
    total_freelancers = len(df)
    expired_contracts = len(df[df['Temps restant (jours)'] < 0])
    soon_expiring_contracts = len(df[df['Temps restant (jours)'] <= 30])
    avg_time_remaining = df[df['Temps restant (jours)'] > 0]['Temps restant (jours)'].mean()
    speciality_distribution = df['Spécialité IT'].value_counts()
    
    # Affichage des indicateurs
    st.subheader("Indicateurs clés")
    st.metric(label="Total Freelancers", value=total_freelancers)
    st.metric(label="Contrats Expirés", value=expired_contracts)
    st.metric(label="Contrats expirant < 30 jours", value=soon_expiring_contracts)
    st.metric(label="Moyenne Temps Restant (jours)", value=f"{avg_time_remaining:.1f}")
    
    # Graphique de répartition des spécialités
    st.subheader("Répartition des spécialités IT")
    fig = px.bar(x=speciality_distribution.index, y=speciality_distribution.values, labels={'x': 'Spécialité', 'y': 'Nombre de Freelancers'})
    st.plotly_chart(fig)
    
    # Alerte pour les contrats expirant bientôt
    if soon_expiring_contracts > 0:
        st.warning(f"Attention ! {soon_expiring_contracts} contrats expirent dans moins de 30 jours.")
        st.write(df[df['Temps restant (jours)'] <= 30])
    
    # Filtrage des données
    st.subheader("Recherche de Freelancers")
    search_term = st.text_input("Rechercher par nom ou spécialité")
    if search_term:
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
        st.write(filtered_df)
    
    # Export des données filtrées
    st.subheader("Exporter les données")
    if st.button("Télécharger les données filtrées"):
        filtered_df.to_csv("freelancers_filtered.csv", index=False)
        st.success("Données exportées avec succès !")
