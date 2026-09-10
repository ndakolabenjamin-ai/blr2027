import streamlit as st
import random
import time

st.set_page_config(page_title="BLR 2027", page_icon="⚽", layout="wide")

# ============ SESSION ============
if "club" not in st.session_state:
    st.session_state.club = ""
    st.session_state.budget = 10000
    st.session_state.division = 1
    st.session_state.effectif = []
    st.session_state.page = "accueil"
    st.session_state.maillots = ("Rouge/Blanc", "Bleu marine", "Or/Noir")
    st.session_state.tactique = "4-3-3"
    st.session_state.mentalite = "Equilibre"
    # Match en cours
    st.session_state.match_actif = False
    st.session_state.match_minute = 0
    st.session_state.match_bm = 0
    st.session_state.match_ba = 0
    st.session_state.match_adv = ""
    st.session_state.match_note_adv = 60
    st.session_state.match_commentaire = ""
    st.session_state.match_buteur = ""
    st.session_state.match_fini = False

# ============ DONNEES ============
PRENOMS = ["Carlos","Luis","Ivan","Marco","Diego","Youssef","Karim","Andre","Luca","Pablo","Samir","Amine"]
NOMS = ["Silva","Garcia","Martin","Lopez","Diallo","Traore","Mendes","Costa","Rossi","Kovac","Petrov","Fernandes"]
POSTES = ["GB","DC","DD","DG","MC","MOC","AIG","AID","BU"]

def gen_joueur(note):
    return {
        "nom": random.choice(PRENOMS) + " " + random.choice(NOMS),
        "poste": random.choice(POSTES),
        "note": note + random.randint(-4, 4),
        "buts": 0
    }

DIVISIONS = {
    1: "DIVISION D'ACCUEIL",
    2: "4EME DIVISION",
    3: "3EME DIVISION",
    4: "2EME DIVISION",
    5: "1ERE DIVISION",
    6: "DIVISION D'ELITE"
}

ADVERSAIRES = ["FC Debutant","AS Novice","Club Amateur","Espoir FC","Jeune Equipe",
               "Academie SC","Rookie United","Sporting Quartier","Union Locale","Etoile Du Matin"]

TACTIQUES = ["4-4-2","4-3-3","5-3-2","4-2-3-1","3-5-2"]
MENTALITES = ["Defensive","Equilibre","Offensive"]

def note_equipe():
    if not st.session_state.effectif: return 50
    onze = sorted(st.session_state.effectif, key=lambda j: -j["note"])[:11]
    return int(sum(j["note"] for j in onze) / len(onze))

# ============ HEADER ============
st.title("⚽ BLR 2027")
st.caption("Ultimate Carrière — Match en direct")

# ============ PAGE ACCUEIL ============
if st.session_state.page == "accueil":
    st.header("🎮 Création de ton club")

    nom = st.text_input("Nom du club", value="FC Kinshasa")

    st.subheader("🎽 Maillots")
    c1, c2, c3 = st.columns(3)
    dom = c1.text_input("🏠 Domicile", value="Rouge/Blanc")
    ext = c2.text_input("✈️ Extérieur", value="Bleu marine")
    exc = c3.text_input("⭐ Exceptionnel", value="Or/Noir")

    if st.button("✅ Créer mon club", type="primary"):
        st.session_state.club = nom
        st.session_state.maillots = (dom, ext, exc)
        st.session_state.effectif = [gen_joueur(62) for _ in range(15)]
        st.session_state.page = "carriere"
        st.rerun()

# ============ PAGE MATCH EN DIRECT ============
elif st.session_state.page == "match":

    # Header du match
    st.markdown(f"### ⚽ {st.session_state.club} vs {st.session_state.match_adv}")

    # Score
    c1, c2, c3 = st.columns([2, 1, 2])
    c1.markdown(f"<h1 style='text-align:center'>{st.session_state.club}</h1>", unsafe_allow_html=True)
    c2.markdown(f"<h1 style='text-align:center'>{st.session_state.match_bm} - {st.session_state.match_ba}</h1>", unsafe_allow_html=True)
    c3.markdown(f"<h1 style='text-align:center'>{st.session_state.match_adv}</h1>", unsafe_allow_html=True)

    # Chrono + barre de progression
    minute = st.session_state.match_minute
    pct = int(minute / 90 * 100)
    st.progress(pct / 100, text=f"⏱️ {minute}' / 90'  ({pct}%)")

    # Info tactique et maillot
    c1, c2, c3 = st.columns(3)
    c1.write(f"🎽 **Maillot** : {st.session_state.maillots[0]}")
    c2.write(f"⚙️ **Tactique** : {st.session_state.tactique}")
    c3.write(f"🧠 **Mentalité** : {st.session_state.mentalite}")

    st.divider()

    # Commentaire
    if st.session_state.match_commentaire:
        st.info(st.session_state.match_commentaire)

    # Match fini ?
    if st.session_state.match_fini or minute >= 90:
        st.balloons() if st.session_state.match_bm > st.session_state.match_ba else None

        if st.session_state.match_bm > st.session_state.match_ba:
            st.success(f"🎉 VICTOIRE ! {st.session_state.club} {st.session_state.match_bm} - {st.session_state.match_ba} {st.session_state.match_adv}")
            st.session_state.budget += 500
        elif st.session_state.match_bm == st.session_state.match_ba:
            st.info(f"🤝 MATCH NUL {st.session_state.match_bm} - {st.session_state.match_ba}")
            st.session_state.budget += 200
        else:
            st.error(f"😢 DÉFAITE {st.session_state.match_bm} - {st.session_state.match_ba}")

        if st.button("🏠 Retour au menu"):
            st.session_state.page = "carriere"
            st.session_state.match_actif = False
            st.rerun()

    else:
        # Boutons d'action
        st.subheader("🎮 Choisis ton action")

        c1, c2, c3 = st.columns(3)
        with c1:
            tirer = st.button("⚽ TIRER", use_container_width=True)
        with c2:
            passer = st.button("🎯 PASSER", use_container_width=True)
        with c3:
            dribbler = st.button("🏃 DRIBBLER", use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            defendre = st.button("🛡️ DÉFENDRE", use_container_width=True)
        with c2:
            centrer = st.button("🎪 CENTRER", use_container_width=True)
        with c3:
            passe_dec = st.button("🎁 PASSE DÉC.", use_container_width=True)

        st.divider()

        # Traitement de l'action
        action = None
        if tirer: action = "tirer"
        elif passer: action = "passer"
        elif dribbler: action = "dribbler"
        elif defendre: action = "defendre"
        elif centrer: action = "centrer"
        elif passe_dec: action = "passe_dec"

        if action:
            # Avancer le temps
            st.session_state.match_minute += random.randint(5, 12)
            if st.session_state.match_minute > 90:
                st.session_state.match_minute = 90

            minute = st.session_state.match_minute

            # Note équipe + tactique influence
            tact_bonus = {"4-4-2":0, "4-3-3":5, "5-3-2":-5, "4-2-3-1":3, "3-5-2":4}
            ment_bonus = {"Defensive":-5, "Equilibre":0, "Offensive":8}
            bonus = tact_bonus.get(st.session_state.tactique, 0) + ment_bonus.get(st.session_state.mentalite, 0)
            diff = (note_equipe() - st.session_state.match_note_adv) + bonus

            # Résultat selon l'action
            if action == "tirer":
                if random.randint(1, 100) < 40 + diff:
                    st.session_state.match_bm += 1
                    buteur = random.choice(st.session_state.effectif)["nom"]
                    st.session_state.match_commentaire = f"⚽ {minute}' — BUT !!! {buteur} marque pour {st.session_state.club} ! 🎉"
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Tir raté..."

            elif action == "passer":
                if random.randint(1, 100) < 70 + diff:
                    st.session_state.match_commentaire = f"✅ {minute}' — Belle passe..."
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Passe interceptée..."

            elif action == "dribbler":
                if random.randint(1, 100) < 50 + diff:
                    st.session_state.match_commentaire = f"🏃 {minute}' — Dribble réussi ! L'adversaire est éliminé !"
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Perte de balle..."

            elif action == "defendre":
                if random.randint(1, 100) < 60 + diff:
                    st.session_state.match_commentaire = f"🛡️ {minute}' — Bon tacle, ballon récupéré !"
                else:
                    st.session_state.match_commentaire = f"⚠️ {minute}' — Faute commise..."

            elif action == "centrer":
                if random.randint(1, 100) < 45 + diff:
                    st.session_state.match_commentaire = f"🎪 {minute}' — Centre dangereux dans la surface !"
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Centre capté par le gardien..."

            elif action == "passe_dec":
                if random.randint(1, 100) < 35 + diff:
                    st.session_state.match_bm += 1
                    st.session_state.match_commentaire = f"🎁 {minute}' — PASSE DÉCISIVE ! But marqué ! 🎉"
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Passe décisive ratée..."

            # Action adversaire (probabilité)
            if random.randint(1, 100) < 20 + (st.session_state.match_note_adv - note_equipe()) // 3:
                st.session_state.match_ba += 1
                st.session_state.match_commentaire += f"\n\n😢 {minute}' — {st.session_state.match_adv} marque..."

            # Fin du match ?
            if st.session_state.match_minute >= 90:
                st.session_state.match_fini = True

            st.rerun()

# ============ PAGE CARRIERE ============
elif st.session_state.page == "carriere":
    st.subheader(f"⚽ {st.session_state.club}")
    st.write(f"**{DIVISIONS[st.session_state.division]}**")

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Budget", f"{st.session_state.budget} €")
    c2.metric("👥 Joueurs", len(st.session_state.effectif))
    c3.metric("📊 Note équipe", note_equipe())

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["⚽ Jouer", "👥 Effectif", "🎽 Maillots", "⚙️ Tactique"])

    # --- JOUER ---
    with tab1:
        st.subheader("Match amical ou championnat")

        if st.button("🎮 Commencer un match", type="primary"):
            adv = random.choice(ADVERSAIRES)
            st.session_state.match_adv = adv
            st.session_state.match_note_adv = 58 + (st.session_state.division - 1) * 5 + random.randint(-3, 3)
            st.session_state.match_bm = 0
            st.session_state.match_ba = 0
            st.session_state.match_minute = 0
            st.session_state.match_commentaire = f"⚽ Le match commence ! {st.session_state.club} vs {adv}"
            st.session_state.match_fini = False
            st.session_state.match_actif = True
            st.session_state.page = "match"
            st.rerun()

    # --- EFFECTIF ---
    with tab2:
        for j in sorted(st.session_state.effectif, key=lambda x: -x["note"]):
            st.write(f"**{j['poste']}** — {j['nom']} — Note **{j['note']}**")

    # --- MAILLOTS ---
    with tab3:
        d, e, x = st.session_state.maillots
        st.write(f"🏠 **Domicile** : {d}")
        st.write(f"✈️ **Extérieur** : {e}")
        st.write(f"⭐ **Exceptionnel** : {x}")

    # --- TACTIQUE ---
    with tab4:
        st.subheader("⚙️ Tactique")
        st.session_state.tactique = st.selectbox("Formation", TACTIQUES,
            index=TACTIQUES.index(st.session_state.tactique))
        st.session_state.mentalite = st.selectbox("Mentalité", MENTALITES,
            index=MENTALITES.index(st.session_state.mentalite))

        st.info(f"""
        **Impact tactique :**
        - 🏃 Offensive → +8% chance de marquer
        - 🛡️ Défensive → -5% chance mais meilleure défense
        - ⚽ 4-3-3 → +5% attaque
        - 🎯 4-2-3-1 → +3% milieu
        """)

    st.divider()
    if st.button("🚪 Menu principal"):
        st.session_state.page = "accueil"
        st.rerun()
