import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from formulaire import creer_formulaire
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score# 1. CONFIGURATION
st.set_page_config(page_title="EcoSnap Universal", layout="wide")

# 2. STYLE CSS (Boutons Grands, Colorés et Alignés)
st.markdown(
    """
    <style>
    /* Changement de la couleur de fond globale pour éviter le tout blanc */
    .stApp {
        background-color: #f0f4f8;
    }
    
    /* Amélioration des boutons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: bold !important;
        transition: all 0.3s ease;
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        color: #1f2937;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #3b82f6;
        color: #3b82f6;
    }
    .main-title { text-align: center; color: #1E3A8A; font-size: 40px; font-weight: bold; margin-bottom: 0px; padding-bottom: 0px; }
    
    /* Style pour le message de bienvenue */
    .welcome-msg {
        text-align: center;
        font-size: 28px;
        font-weight: 600;
        background: -webkit-linear-gradient(45deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0px;
        margin-bottom: 30px;
        padding-top: 10px;
    }
    
    .interpretation-box { padding: 15px; border-radius: 10px; background-color: #F0F9FF; border-left: 5px solid #3B82F6; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. GESTION DES DONNÉES
FICHIER_DATA = "base_expert.csv"
def charger_donnees():
    cols = ['Produit', 'Marché', 'Prix', 'Catégorie', 'Poids_Volume', 'Note_Qualite', 'Origine']
    if os.path.exists(FICHIER_DATA):
        try:
            df = pd.read_csv(FICHIER_DATA)
            for c in cols:
                if c not in df.columns:
                    if c == 'Poids_Volume': df[c] = 1.0
                    elif c == 'Note_Qualite': df[c] = 5
                    elif c == 'Origine': df[c] = "Local"
            return df[cols]
        except:
            return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)

if 'data' not in st.session_state:
    st.session_state.data = charger_donnees()

st.markdown('<p class="main-title">📸 EcoSnap Universal</p>', unsafe_allow_html=True)
st.markdown('<p class="welcome-msg">Bienvenue sur EcoSnap ! / Welcome to EcoSnap!</p>', unsafe_allow_html=True)

col_form, col_dash = st.columns([1, 2], gap="large")

with col_form:
    st.markdown("### 📥 Saisie")
    with st.form("mon_formulaire"):
        valider, p, m, v, cat, poids, note, orig = creer_formulaire()
    if valider and p and m:
        st.session_state.en_cours = {"Produit": p, "Marché": m, "Prix": v, "Catégorie": cat, "Poids_Volume": poids, "Note_Qualite": note, "Origine": orig}
    if "en_cours" in st.session_state:
        if st.button("💾 CONFIRMER L'AJOUT", use_container_width=True):
            nl = pd.DataFrame([st.session_state.en_cours])
            st.session_state.data = pd.concat([st.session_state.data, nl], ignore_index=True)
            st.session_state.data.to_csv(FICHIER_DATA, index=False)
            del st.session_state.en_cours
            st.rerun()

with col_dash:
    if 'page' not in st.session_state:
        st.session_state.page = "menu"

    st.markdown("### 📊 Tableau de Bord")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📍 RÉPARTITION\nMARCHÉS", use_container_width=True, type="primary"): st.session_state.page = "rep"; st.rerun()
        if st.button("🔄 COMPARATIF\nPRIX", use_container_width=True, type="primary"): st.session_state.page = "comp"; st.rerun()
    with c2:
        if st.button("📊 ANALYSE PAR\nCATÉGORIE", use_container_width=True, type="primary"): st.session_state.page = "cat"; st.rerun()
        if st.button("🛠️ MAINTENANCE\nBASE", use_container_width=True, type="primary"): st.session_state.page = "stats"; st.rerun()
    
    if st.button("🧠 INTELLIGENCE ARTIFICIELLE (TP)", use_container_width=True, type="primary"): st.session_state.page = "ml"; st.rerun()

    # Navigation et affichage des pages
    if st.session_state.page == "menu":
        if st.session_state.data.empty:
            st.info("Aucune donnée enregistrée. Veuillez utiliser le formulaire de gauche pour commencer.")
        else:
            st.success("Données disponibles. Sélectionnez une analyse ci-dessus.")
    else:
        if st.session_state.data.empty:
            st.warning("Aucune donnée enregistrée. Veuillez utiliser le formulaire de gauche.")
            if st.button("⬅️ RETOUR AU MENU"): 
                st.session_state.page = "menu"
                st.rerun()
        else:
            if st.button("⬅️ RETOUR AU MENU"): 
                st.session_state.page = "menu"
                st.rerun()

            # --- PAGE RÉPARTITION AVEC % ---
            if st.session_state.page == "rep":
                st.write("#### 📍 Analyse des parts de marché (%)")
                fig = px.pie(st.session_state.data, names='Marché', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)

                # Calcul des pourcentages pour l'interprétation
                stats = st.session_state.data['Marché'].value_counts(normalize=True) * 100
                top_m = stats.idxmax()
                st.markdown(f"""
                <div class="interpretation-box">
                    <b>Interprétation des données :</b><br>
                    Le marché de <b>{top_m}</b> domine la collecte avec <b>{stats.max():.1f}%</b> des relevés effectués. 
                </div>
                """, unsafe_allow_html=True)

            # --- PAGE CATÉGORIE ---
            elif st.session_state.page == "cat":
                st.write("#### 📊 Coût moyen par Catégorie")
                df_cat = st.session_state.data.groupby('Catégorie')['Prix'].mean().reset_index()
                st.plotly_chart(px.bar(df_cat, x='Catégorie', y='Prix', color='Catégorie', text_auto='.2s'), use_container_width=True)

            # --- PAGE COMPARATIF ---
            elif st.session_state.page == "comp":
                st.write("#### 🔄 Comparaison des meilleures offres")
                for prod in st.session_state.data['Produit'].unique():
                    df_p = st.session_state.data[st.session_state.data['Produit'] == prod]
                    if len(df_p) > 1:
                        m_min = df_p.loc[df_p['Prix'].idxmin()]
                        st.success(f"📦 **{prod}** : Moins cher à **{m_min['Marché']}** ({m_min['Prix']:.0f} FCFA)")

            # --- PAGE MAINTENANCE (NETTOYAGE) ---
            elif st.session_state.page == "stats":
                st.write("#### 🛠️ Maintenance de la Base de Données")
                st.dataframe(st.session_state.data, use_container_width=True)
                st.markdown("---")
                
                st.write("##### 🗑️ Supprimer une entrée spécifique")
                # Création d'un dictionnaire pour lier le texte affiché à l'index réel de la ligne
                options = {f"Ligne {i+1} : {row['Produit']} ({row['Marché']} - {row['Prix']} FCFA)": i for i, row in st.session_state.data.iterrows()}
                
                if options:
                    choix = st.selectbox("Sélectionnez l'enregistrement à supprimer :", list(options.keys()))
                    if st.button("🗑️ Supprimer cette entrée"):
                        idx = options[choix]
                        st.session_state.data = st.session_state.data.drop(idx).reset_index(drop=True)
                        st.session_state.data.to_csv(FICHIER_DATA, index=False)
                        st.success("Entrée supprimée avec succès !")
                        st.rerun()
                
                st.markdown("---")
                st.write("##### ⚠️ Zone de danger et Tests")
                if st.button("🎲 GÉNÉRER DES DONNÉES DE TEST (100 LIGNES)", key="btn_gen"):
                    import random
                    import string
                    categories_list = ["Transport", "Construction", "Alimentaire", "Technologie"]
                    nouveaux_produits = []
                    for _ in range(100):
                        nouveaux_produits.append({
                            "Produit": "Prod_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)),
                            "Marché": random.choice(["Marché Central", "Marché Mokolo", "Marché Mboppi"]),
                            "Prix": random.randint(10, 500) * 100.0,
                            "Catégorie": random.choice(categories_list),
                            "Poids_Volume": round(random.uniform(0.5, 50.0), 2),
                            "Note_Qualite": random.randint(1, 10),
                            "Origine": random.choice(["Local", "Importé"])
                        })
                    df_gen = pd.DataFrame(nouveaux_produits)
                    st.session_state.data = pd.concat([st.session_state.data, df_gen], ignore_index=True)
                    st.session_state.data.to_csv(FICHIER_DATA, index=False)
                    st.success("100 produits de test générés !")
                    st.rerun()

                # Le bouton est réduit car on a enlevé use_container_width=True
                if st.button("🔥 VIDER TOUTE LA BASE", key="btn_clean_final"):
                    if os.path.exists(FICHIER_DATA):
                        os.remove(FICHIER_DATA)
                    st.session_state.data = pd.DataFrame(columns=['Produit', 'Marché', 'Prix', 'Catégorie', 'Poids_Volume', 'Note_Qualite', 'Origine'])
                    st.success("La base a été réinitialisée !")
                    st.rerun()

            # --- PAGE MACHINE LEARNING (TP) ---
            elif st.session_state.page == "ml":
                st.markdown("### 🧠 Machine Learning (TP INF 232 EC2)")
                st.info("Cette section présente les 5 exigences du TP d'Analyse de Données.")
                
                df_ml = st.session_state.data.copy()
                # Conversion en numérique pour être sûr
                df_ml['Prix'] = pd.to_numeric(df_ml['Prix'], errors='coerce')
                df_ml['Note_Qualite'] = pd.to_numeric(df_ml['Note_Qualite'], errors='coerce')
                df_ml['Poids_Volume'] = pd.to_numeric(df_ml['Poids_Volume'], errors='coerce')
                df_ml = df_ml.dropna(subset=['Prix', 'Note_Qualite', 'Poids_Volume'])
                
                if len(df_ml) < 10:
                    st.warning("⚠️ Pas assez de données pour entraîner les modèles. Veuillez aller dans 'Maintenance Base' et générer des données de test.")
                else:
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "1. Régression Simple", 
                        "2. Régression Multiple", 
                        "3. PCA", 
                        "4. Classif. Supervisée", 
                        "5. Clustering (K-Means)"
                    ])
                    
                    # 1. Régression Linéaire Simple
                    with tab1:
                        st.subheader("1. Régression Linéaire Simple (Prix ~ Qualité)")
                        X_simple = df_ml[['Note_Qualite']]
                        y = df_ml['Prix']
                        model_simple = LinearRegression()
                        model_simple.fit(X_simple, y)
                        
                        fig1 = px.scatter(df_ml, x='Note_Qualite', y='Prix', title="Relation entre Qualité et Prix")
                        # Ligne de régression
                        preds = model_simple.predict(X_simple)
                        fig1.add_traces(go.Scatter(x=df_ml['Note_Qualite'], y=preds, mode='lines', name='Régression', line=dict(color='red')))
                        st.plotly_chart(fig1, use_container_width=True)
                        st.write(f"**Coefficient :** {model_simple.coef_[0]:.2f}")
                        
                    # 2. Régression Linéaire Multiple
                    with tab2:
                        st.subheader("2. Régression Linéaire Multiple (Prix ~ Qualité + Poids)")
                        X_mult = df_ml[['Note_Qualite', 'Poids_Volume']]
                        model_mult = LinearRegression()
                        model_mult.fit(X_mult, y)
                        
                        st.write("**Équation du modèle :**")
                        st.latex(f"Prix = {model_mult.intercept_:.2f} + {model_mult.coef_[0]:.2f} \\times Qualité + {model_mult.coef_[1]:.2f} \\times Poids")
                        
                        # Graphique des prédictions vs réels
                        preds_mult = model_mult.predict(X_mult)
                        fig2 = px.scatter(x=y, y=preds_mult, labels={'x': 'Prix Réel', 'y': 'Prix Prédit'}, title="Prédictions vs Réalité")
                        fig2.add_shape(type="line", x0=y.min(), y0=y.min(), x1=y.max(), y1=y.max(), line=dict(color='red', dash='dash'))
                        st.plotly_chart(fig2, use_container_width=True)

                    # 3. PCA
                    with tab3:
                        st.subheader("3. Réduction de Dimensionnalité (PCA)")
                        features = ['Prix', 'Note_Qualite', 'Poids_Volume']
                        X_pca = df_ml[features]
                        
                        # Gérer le cas où l'écart-type est 0 (colonne constante) pour éviter les NaNs
                        std_dev = X_pca.std().replace(0, 1)
                        X_pca_norm = ((X_pca - X_pca.mean()) / std_dev).fillna(0)
                        
                        pca = PCA(n_components=2)
                        components = pca.fit_transform(X_pca_norm)
                        
                        df_pca = pd.DataFrame(data=components, columns=['CP1', 'CP2'])
                        df_pca['Origine'] = df_ml['Origine'].values
                        
                        fig3 = px.scatter(df_pca, x='CP1', y='CP2', color='Origine', title="Visualisation PCA (2D)")
                        st.plotly_chart(fig3, use_container_width=True)
                        st.write(f"**Variance expliquée :** {pca.explained_variance_ratio_[0]*100:.1f}% (CP1) et {pca.explained_variance_ratio_[1]*100:.1f}% (CP2)")

                    # 4. Classification Supervisée
                    with tab4:
                        st.subheader("4. Classification Supervisée (Prédire l'Origine)")
                        X_cls = df_ml[['Prix', 'Note_Qualite', 'Poids_Volume']]
                        y_cls = df_ml['Origine']
                        
                        if len(y_cls.unique()) > 1:
                            X_train, X_test, y_train, y_test = train_test_split(X_cls, y_cls, test_size=0.3, random_state=42)
                            clf = RandomForestClassifier(random_state=42)
                            clf.fit(X_train, y_train)
                            y_pred = clf.predict(X_test)
                            acc = accuracy_score(y_test, y_pred)
                            
                            st.success(f"**Précision du modèle (Random Forest) :** {acc*100:.2f}%")
                            
                            importances = pd.DataFrame({'Feature': X_cls.columns, 'Importance': clf.feature_importances_})
                            fig4 = px.bar(importances, x='Feature', y='Importance', title="Importance des variables pour l'Origine")
                            st.plotly_chart(fig4, use_container_width=True)
                        else:
                            st.warning("Toutes les données ont la même Origine. Impossible d'entraîner le classifieur.")

                    # 5. Clustering (K-Means)
                    with tab5:
                        st.subheader("5. Classification Non-Supervisée (K-Means)")
                        k = st.slider("Nombre de clusters (K)", 2, 5, 3)
                        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                        df_ml['Cluster'] = kmeans.fit_predict(X_pca_norm)
                        
                        fig5 = px.scatter(df_ml, x='Poids_Volume', y='Prix', color=df_ml['Cluster'].astype(str), title="Clusters de Produits (K-Means)")
                        st.plotly_chart(fig5, use_container_width=True)
                        st.write("L'algorithme a automatiquement regroupé les produits en segments selon leurs caractéristiques.")