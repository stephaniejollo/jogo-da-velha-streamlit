import streamlit as st
import random

# Emojis para o jogador e o computador
JOGADOR = "❌"
COMPUTADOR = "⭕"

# Inicializar o estado do jogo
if "tabuleiro" not in st.session_state:
    st.session_state.tabuleiro = [""] * 9
    st.session_state.vencedor = None
    st.session_state.placar = {JOGADOR: 0, COMPUTADOR: 0, "Empate": 0}

# Função para verificar o vencedor
def verificar_vencedor(tab):
    combinacoes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for c in combinacoes:
        if tab[c[0]] == tab[c[1]] == tab[c[2]] and tab[c[0]] != "":
            return tab[c[0]]
    if "" not in tab:
        return "Empate"
    return None

# IA boba
def jogada_do_computador():
    tab = st.session_state.tabuleiro

    for i in range(9):
        if tab[i] == "":
            tab[i] = COMPUTADOR
            if verificar_vencedor(tab) == COMPUTADOR:
                return
            tab[i] = ""

    for i in range(9):
        if tab[i] == "":
            tab[i] = JOGADOR
            if verificar_vencedor(tab) == JOGADOR:
                tab[i] = COMPUTADOR
                return
            tab[i] = ""

    vazios = [i for i, v in enumerate(tab) if v == ""]
    if vazios:
        escolha = random.choice(vazios)
        tab[escolha] = COMPUTADOR

# Reiniciar
def resetar_jogo():
    st.session_state.tabuleiro = [""] * 9
    st.session_state.vencedor = None

# Título
st.title("🎯 Jogo da Velha - Você é o ❌")

# Ajuste de layout para dispositivos móveis
st.markdown("""
    <style>
    .stButton > button {
        height: 45px !important;
        font-size: 22px !important;
        padding: 4px 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.info("📱 Se estiver jogando no celular, **gire a tela para o modo horizontal** (paisagem) para uma melhor experiência.")
    
# Placar
st.markdown(f"""
**Placar**
- {JOGADOR} Jogador: {st.session_state.placar[JOGADOR]}
- {COMPUTADOR} Computador: {st.session_state.placar[COMPUTADOR]}
- 🤝 Empates: {st.session_state.placar["Empate"]}
""")

# Layout do tabuleiro (3x3 com st.columns)
for linha in range(3):
    cols = st.columns(3)
    for coluna in range(3):
        i = linha * 3 + coluna
        with cols[coluna]:
            btn_key = f"casa_{i}"
            if st.session_state.tabuleiro[i] == "":
                if st.button(" ", key=btn_key, use_container_width=True):
                    st.session_state.tabuleiro[i] = JOGADOR
                    vencedor = verificar_vencedor(st.session_state.tabuleiro)
                    if vencedor:
                        st.session_state.vencedor = vencedor
                        st.session_state.placar[vencedor] += 1
                    else:
                        jogada_do_computador()
                        vencedor = verificar_vencedor(st.session_state.tabuleiro)
                        if vencedor:
                            st.session_state.vencedor = vencedor
                            st.session_state.placar[vencedor] += 1
                    st.rerun()
            else:
                st.button(st.session_state.tabuleiro[i], key=btn_key, disabled=True, use_container_width=True)

# Mensagem final
if st.session_state.vencedor:
    if st.session_state.vencedor == JOGADOR:
        st.success(f"🎉 Jogador {JOGADOR} venceu!")
    elif st.session_state.vencedor == COMPUTADOR:
        st.error(f"💻 Computador {COMPUTADOR} venceu!")
    elif st.session_state.vencedor == "Empate":
        st.info("🤝 Deu empate!")

# Reiniciar e informações
col1, col2 = st.columns([1, 3])
with col1:
    st.button("🔄 Reiniciar Jogo", on_click=resetar_jogo)
with col2:
    with st.expander("ℹ️ Sobre o projeto"):
        st.markdown(
            "Esse jogo da velha foi desenvolvido em Python com Streamlit, com uma IA simples que responde automaticamente após a jogada do jogador.\n"
            "- Você joga como ❌ e o computador responde com ⭕.\n"
            "- A IA tenta ganhar, bloquear ou joga aleatoriamente.\n"
            "- Desenvolvido por **Stephanie Jollo**."
        )