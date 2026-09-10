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
    # Match
    st.session_state.match_actif = False
    st.session_state.match_minute = 0
    st.session_state.match_bm = 0
    st.session_state.match_ba = 0
    st.session_state.match_adv = ""
    st.session_state.match_note_adv = 60
    st.session_state.match_commentaire = ""
    st.session_state.match_possession = "milieu"
    st.session_state.match_zone = 50  # position de la balle sur le terrain (0-100)
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

# ============ TERRAIN ASCII ============
def dessiner_terrain(zone_balle):
    """Dessine le terrain avec les joueurs et la balle
    zone_balle : 0 (but adverse) a 100 (notre but)
    """
    # position de la balle sur 60 caracteres
    pos = int(zone_balle / 100 * 40) + 10
    pos = max(10, min(50, pos))

    lignes = []
    lignes.append("   ╔" + "═" * 52 + "╗")
    lignes.append("   ║" + " " * 52 + "║  🥅 ADVERSE")

    # Ligne 1 : defense adverse
    l1 = list(" " * 52)
    for x in [8, 22, 38, 46]:
        l1[x] = "✕"
    l1[pos] = "⚽"
    lignes.append("   ║" + "".join(l1) + "║")

    # Ligne 2 : milieu adverse
    l2 = list(" " * 52)
    for x in [12, 26, 34, 44]:
        l2[x] = "✕"
    lignes.append("   ║" + "".join(l2) + "║")

    lignes.append("   ║" + " " * 52 + "║")

    # Ligne 3 : milieu terrain
    l3 = list(" " * 52)
    for x in [15, 24, 28, 36]:
        l3[x] = "●"
    lignes.append("   ║" + "".join(l3) + "║  ⚔️  DUEL")

    lignes.append("   ║" + " " * 52 + "║")

    # Ligne 4 : milieu
    l4 = list(" " * 52)
    for x in [14, 20, 30, 40]:
        l4[x] = "●"
    lignes.append("   ║" + "".join(l4) + "║")

    # Ligne 5 : defense
    l5 = list(" " * 52)
    for x in [10, 20, 32, 42]:
        l5[x] = "●"
    lignes.append("   ║" + "".join(l5) + "║")

    lignes.append("   ║" + " " * 52 + "║  🥅 NOTRE BUT")
    lignes.append("   ╚" + "═" * 52 + "╝")

    return "\n".join(lignes)

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

    # SCORE EN GROS
    c1, c2, c3 = st.columns([3, 2, 3])
    c1.markdown(f"<h2 style='text-align:center;color:red'>{st.session_state.club}</h2>", unsafe_allow_html=True)
    c2.markdown(f"<h1 style='text-align:center'>{st.session_state.match_bm} - {st.session_state.match_ba}</h1>", unsafe_allow_html=True)
    c3.markdown(f"<h2 style='text-align:center;color:blue'>{st.session_state.match_adv}</h2>", unsafe_allow_html=True)

    # CHRONO
    minute = st.session_state.match_minute
    st.progress(minute / 90, text=f"⏱️ {minute}' / 90'")

    # INFOS
    c1, c2, c3 = st.columns(3)
    c1.write(f"🎽 {st.session_state.maillots[0]}")
    c2.write(f"⚙️ {st.session_state.tactique}")
    c3.write(f"🧠 {st.session_state.mentalite}")

    st.divider()

    # TERRAIN
    st.markdown("### 🏟️ Terrain")
    st.code(dessiner_terrain(st.session_state.match_zone), language=None)

    # COMMENTAIRE
    if st.session_state.match_commentaire:
        st.info(f"💬 {st.session_state.match_commentaire}")

    # MATCH FINI ?
    if st.session_state.match_fini or minute >= 90:
        if st.session_state.match_bm > st.session_state.match_ba:
            st.balloons()
            st.success(f"🎉 VICTOIRE ! {st.session_state.match_bm} - {st.session_state.match_ba}")
            st.session_state.budget += 500
        elif st.session_state.match_bm == st.session_state.match_ba:
            st.info(f"🤝 NUL {st.session_state.match_bm} - {st.session_state.match_ba}")
            st.session_state.budget += 200
        else:
            st.error(f"😢 DÉFAITE {st.session_state.match_bm} - {st.session_state.match_ba}")

        if st.button("🏠 Retour au menu", type="primary"):
            st.session_state.page = "carriere"
            st.session_state.match_actif = False
            st.rerun()

    else:
        # BOUTONS D'ACTION
        st.markdown("### 🎮 Tes actions")

        c1, c2, c3 = st.columns(3)
        with c1:
            tirer = st.button("⚽ TIRER", use_container_width=True, type="primary")
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

        # IMPORTANT : Le match avance TOUT SEUL (simulation)
        # On avance de quelques minutes automatiquement
        st.session_state.match_minute += 1
        if st.session_state.match_minute >= 90:
            st.session_state.match_minute = 90
            st.session_state.match_fini = True

        # Action adverse automatique (le match continue sans toi)
        if random.randint(1, 100) < 15:
            st.session_state.match_ba += 1
            st.session_state.match_commentaire = f"😢 {st.session_state.match_minute}' — {st.session_state.match_adv} marque !"

        # Traitement de l'action utilisateur
        action = None
        if tirer: action = "tirer"
        elif passer: action = "passer"
        elif dribbler: action = "dribbler"
        elif defendre: action = "defendre"
        elif centrer: action = "centrer"
        elif passe_dec: action = "passe_dec"

        if action:
            tact_bonus = {"4-4-2":0, "4-3-3":8, "5-3-2":-5, "4-2-3-1":5, "3-5-2":6}
            ment_bonus = {"Defensive":-5, "Equilibre":0, "Offensive":10}
            bonus = tact_bonus.get(st.session_state.tactique, 0) + ment_bonus.get(st.session_state.mentalite, 0)
            diff = (note_equipe() - st.session_state.match_note_adv) + bonus

            if action == "tirer":
                if random.randint(1, 100) < 40 + diff:
                    st.session_state.match_bm += 1
                    buteur = random.choice(st.session_state.effectif)["nom"]
                    st.session_state.match_commentaire = f"⚽ {minute}' — BUT !!! {buteur} marque ! 🎉"
                    st.session_state.match_zone = 0
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Tir raté par le gardien..."
                    st.session_state.match_zone = 20

            elif action == "passer":
                if random.randint(1, 100) < 70 + diff:
                    st.session_state.match_commentaire = f"✅ {minute}' — Belle passe en profondeur..."
                    st.session_state.match_zone = min(80, st.session_state.match_zone + 10)
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Passe interceptée..."
                    st.session_state.match_zone = 50

            elif action == "dribbler":
                if random.randint(1, 100) < 50 + diff:
                    st.session_state.match_commentaire = f"🏃 {minute}' — Dribble réussi !"
                    st.session_state.match_zone = max(10, st.session_state.match_zone - 15)
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Perte de balle..."
                    st.session_state.match_zone = 50

            elif action == "defendre":
                if random.randint(1, 100) < 60 + diff:
                    st.session_state.match_commentaire = f"🛡️ {minute}' — Bon tacle !"
                    st.session_state.match_zone = 70
                else:
                    st.session_state.match_commentaire = f"⚠️ {minute}' — Faute..."
                    st.session_state.match_zone = 60

            elif action == "centrer":
                if random.randint(1, 100) < 45 + diff:
                    st.session_state.match_commentaire = f"🎪 {minute}' — Centre dangereux !"
                    st.session_state.match_zone = 15
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Centre capté..."
                    st.session_state.match_zone = 30

            elif action == "passe_dec":
                if random.randint(1, 100) < 35 + diff:
                    st.session_state.match_bm += 1
                    st.session_state.match_commentaire = f"🎁 {minute}' — PASSE DÉCISIVE ! But ! 🎉"
                    st.session_state.match_zone = 0
                else:
                    st.session_state.match_commentaire = f"❌ {minute}' — Passe décisive ratée..."
                    st.session_state.match_zone = 40

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

    with tab1:
        st.subheader("Match")
        st.write("Choisis ton adversaire et lance le match !")

        if st.button("🎮 Commencer un match", type="primary"):
            adv = random.choice(ADVERSAIRES)
            st.session_state.match_adv = adv
            st.session_state.match_note_adv = 58 + (st.session_state.division - 1) * 5 + random.randint(-3, 3)
            st.session_state.match_bm = 0
            st.session_state.match_ba = 0
            st.session_state.match_minute = 0
            st.session_state.match_zone = 50
            st.session_state.match_commentaire = f"⚽ Le match commence ! {st.session_state.club} vs {adv}"
            st.session_state.match_fini = False
            st.session_state.match_actif = True
            st.session_state.page = "match"
            st.rerun()

    with tab2:
        for j in sorted(st.session_state.effectif, key=lambda x: -x["note"]):
            st.write(f"**{j['poste']}** — {j['nom']} — Note **{j['note']}**")

    with tab3:
        d, e, x = st.session_state.maillots
        st.write(f"🏠 **Domicile** : {d}")
        st.write(f"✈️ **Extérieur** : {e}")
        st.write(f"⭐ **Exceptionnel** : {x}")

    with tab4:
        st.subheader("⚙️ Tactique")
        st.session_state.tactique = st.selectbox("Formation", TACTIQUES,
            index=TACTIQUES.index(st.session_state.tactique))
        st.session_state.mentalite = st.selectbox("Mentalité", MENTALITES,
            index=MENTALITES.index(st.session_state.mentalite))
        st.info("🏃 **Offensive** = +10% chance de marquer\n\n🛡️ **Défensive** = meilleure défense")

    st.divider()
    if st.button("🚪 Menu principal"):
        st.session_state.page = "accueil"
        st.rerun()
