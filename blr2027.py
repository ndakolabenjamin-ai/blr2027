import streamlit as st
import random

st.set_page_config(page_title="BLR 2027", page_icon="⚽", layout="wide")

if "club" not in st.session_state:
    st.session_state.club = ""
    st.session_state.budget = 10000
    st.session_state.division = 1
    st.session_state.effectif = []
    st.session_state.page = "accueil"
    st.session_state.maillots = ("Rouge/Blanc", "Bleu marine", "Or/Noir")

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

st.title("⚽ BLR 2027")
st.caption("Ultimate Carrière")

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

elif st.session_state.page == "carriere":
    st.subheader(f"⚽ {st.session_state.club}")
    st.write(f"**{DIVISIONS[st.session_state.division]}**")

    c1, c2 = st.columns(2)
    c1.metric("💰 Budget", f"{st.session_state.budget} €")
    c2.metric("👥 Joueurs", len(st.session_state.effectif))

    st.divider()

    tab1, tab2, tab3 = st.tabs(["⚽ Jouer", "👥 Effectif", "🎽 Maillots"])

    with tab1:
        if st.button("🎮 Jouer un match", type="primary"):
            adv = random.choice(ADVERSAIRES)
            bm = random.randint(0, 5)
            ba = random.randint(0, 3)

            if bm > ba:
                st.session_state.budget += 500
                st.success(f"🎉 {st.session_state.club} {bm} - {ba} {adv} — VICTOIRE !")
            elif bm == ba:
                st.info(f"🤝 {st.session_state.club} {bm} - {ba} {adv} — NUL")
            else:
                st.error(f"😢 {st.session_state.club} {bm} - {ba} {adv} — DÉFAITE")

        if st.button("📅 Jouer 8 matchs"):
            v, n, d = 0, 0, 0
            for i in range(8):
                bm = random.randint(0, 5)
                ba = random.randint(0, 3)
                if bm > ba: v += 1
                elif bm == ba: n += 1
                else: d += 1
            st.session_state.budget += v * 500
            st.write(f"**Bilan : {v}V {n}N {d}D**")
            if v >= 5:
                st.balloons()
                st.success("🏆 Promotion !")

    with tab2:
        for j in sorted(st.session_state.effectif, key=lambda x: -x["note"]):
            st.write(f"**{j['poste']}** — {j['nom']} — Note **{j['note']}**")

    with tab3:
        d, e, x = st.session_state.maillots
        st.write(f"🏠 **Domicile** : {d}")
        st.write(f"✈️ **Extérieur** : {e}")
        st.write(f"⭐ **Exceptionnel** : {x}")

    st.divider()
    if st.button("🚪 Menu principal"):
        st.session_state.page = "accueil"
        st.rerun()
