import streamlit as st
import json

st.title("📦 BIENVENUS A AGENCE OKAPI UVIRA")

# Charger les colis
try:
    with open("registre_colis.json", "r", encoding="utf-8") as f:
        colis_list = json.load(f)
except FileNotFoundError:
    colis_list = []

# === MENU PRINCIPAL ===
menu = st.sidebar.radio(
    "MENU PRINCIPAL",
    ["Accueil", "Enregistrer un envoi", "Afficher les colis reçus", "Livrer un colis", "Quitter"]
)

# === ACCUEIL ===
if menu == "Accueil":
    st.header("🏠 Accueil")
    st.write("Bienvenue dans l’application OKAPI UVIRA.")
    st.write("Choisissez une option dans le menu à gauche pour commencer.")

# === ENREGISTRER UN ENVOI ===
elif menu == "Enregistrer un envoi":
    st.header("📝 Nouvel envoi")
    expediteur_nom = st.text_input("Nom expéditeur")
    expediteur_prenom = st.text_input("Prénom expéditeur")
    expediteur_carte = st.text_input("Carte expéditeur (10 chiffres)")
    destinataire_nom = st.text_input("Nom destinataire")
    destinataire_prenom = st.text_input("Prénom destinataire")
    destinataire_carte = st.text_input("Carte destinataire (10 chiffres)")
    code = st.text_input("Code colis (10 chiffres)")
    carte_electeur = st.text_input("Carte électeur")
    poids = st.number_input("Poids (kg)", min_value=0)
    valeur = st.number_input("Valeur déclarée", min_value=0)
    tarif = st.number_input("Tarif", min_value=0)
    depart = st.text_input("Ville départ")
    arrivee = st.text_input("Ville arrivée")

    if st.button("✅ Enregistrer"):
        if not (expediteur_carte.isdigit() and len(expediteur_carte) == 10):
            st.error("Carte expéditeur invalide")
        elif not (destinataire_carte.isdigit() and len(destinataire_carte) == 10):
            st.error("Carte destinataire invalide")
        elif not (code.isdigit() and len(code) == 10):
            st.error("Code colis invalide")
        elif not carte_electeur.isdigit():
            st.error("Carte électeur invalide")
        else:
            colis = {
                "code": code,
                "carte_electeur": carte_electeur,
                "poids": poids,
                "valeur": valeur,
                "tarif": tarif,
                "depart": depart,
                "arrivee": arrivee,
                "expediteur": f"{expediteur_nom} {expediteur_prenom}",
                "destinataire": f"{destinataire_nom} {destinataire_prenom}"
            }
            colis_list.append(colis)
            with open("registre_colis.json", "w", encoding="utf-8") as f:
                json.dump(colis_list, f, ensure_ascii=False, indent=4)
            st.success(f"Colis {code} enregistré avec succès !")

# === AFFICHER LES COLIS ===
elif menu == "Afficher les colis reçus":
    st.header("📋 Liste des colis reçus")
    if not colis_list:
        st.info("Aucun colis enregistré.")
    else:
        for i, colis in enumerate(colis_list, start=1):
            st.subheader(f"Colis {i}")
            st.write(colis)

# === LIVRER UN COLIS ===
elif menu == "Livrer un colis":
    st.header("🚚 Livraison")
    code_livraison = st.text_input("Code du colis")
    collecteur_nom = st.text_input("Nom collecteur")
    collecteur_prenom = st.text_input("Prénom collecteur")
    collecteur_carte = st.text_input("Carte collecteur")

    if st.button("✅ Livrer"):
        colis_trouve = next((c for c in colis_list if c["code"] == code_livraison), None)
        if not colis_trouve:
            st.error(f"Colis {code_livraison} introuvable.")
        elif not collecteur_nom or not collecteur_prenom or not collecteur_carte:
            st.error("Informations collecteur incomplètes.")
        else:
            colis_list.remove(colis_trouve)
            with open("registre_colis.json", "w", encoding="utf-8") as f:
                json.dump(colis_list, f, ensure_ascii=False, indent=4)
            st.success(f"Colis {code_livraison} livré et retiré de la liste.")

# === QUITTER ===
elif menu == "Quitter":
    st.header("👋 Fin du programme")
    st.write(f"Nombre total de colis enregistrés : {len(colis_list)}")
    st.info("Merci d’avoir utilisé l’application OKAPI UVIRA.")