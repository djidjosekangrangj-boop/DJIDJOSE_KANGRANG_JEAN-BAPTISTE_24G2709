import streamlit as st

def creer_formulaire():
    st.write("### 📝 Saisie du Relevé")
    
    categories = [
        "Transport", "Construction & Habitat (Matériaux)", "Construction & Habitat (Mobilier)", 
        "Construction & Habitat (Électroménager)", "Biens de consommation (Alimentaire)", 
        "Biens de consommation (Hygiène)", "Habillement (Vêtements)", "Habillement (Chaussures)", 
        "Habillement (Accessoires)", "Bijoux & accessoires personnels", "Énergie & carburants", 
        "Technologie & électronique", "Outils & équipements", "Santé & pharmacie", "Services"
    ]
    
    categorie = st.selectbox("Catégorie du produit", categories)
    produit = st.text_input("Nom spécifique du produit", placeholder="Ex: Ciment, Moto, iPhone...")
    marche = st.text_input("Marché ou Enseigne", placeholder="Ex: Marché Central...")
    
    col1, col2 = st.columns(2)
    with col1:
        prix = st.number_input("Prix unitaire (FCFA)", min_value=0.0, format="%.2f", step=100.0)
        poids_volume = st.number_input("Poids/Volume (kg ou L)", min_value=0.1, format="%.2f", step=1.0, value=1.0)
    with col2:
        note_qualite = st.slider("Note de qualité", 1, 10, 5)
        origine = st.selectbox("Origine", ["Local", "Importé"])
    
    envoyer = st.form_submit_button("Vérifier les données")
    return envoyer, produit, marche, prix, categorie, poids_volume, note_qualite, origine