
import streamlit as st
import random

# Emojis para o jogador e o computador
JOGADOR = "❌"
COMPUTADOR = "⭕"

# 🔧 Estilo personalizado para melhorar visual no celular
st.markdown("""
    <style>
    .stButton button {
        height: 60px !important;
        font-size: 30px !important;
    }
    @media (max-width: 768px) {
        div[data-testid="column"] {
            display: inline-block;
            width: 33.33% !important;
            padding: 4px;
            vertical-align: top;
        }
    }
    </style>
""", unsafe_allow_html=True)

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

# IA boba: tenta ganhar, bloquear ou aleatório
def jogada_do_computador():
    tab = st.session_state.tabuleiro

    # Verificar se pode ganhar
    for i in range(9):
        if tab[i] == "":
            tab[i] = COMPUTADOR
            if verificar_vencedor(tab) == COMPUTADOR:
                return
            tab[i] = ""

    # Verificar se pode bloquear o jogador
    for i in range(9):
        if tab[i] == "":
            tab[i] = JOGADOR
            if verificar_vencedor(tab) == JOGADOR:
                tab[i] = COMPUTADOR
                return
            tab[i] = ""

    # Escolher aleatoriamente
    vazios = [i for i, v in enumerate(tab) if v == ""]
    if vazios:
        escolha = random.choice(vazios)
        tab[escolha] = COMPUTADOR

# Função para reiniciar o jogo
def resetar_jogo():
    st.session_state.tabuleiro = [""] * 9
    st.session_state.vencedor = None

# Título e placar
st.title("🎯 Jogo da Velha - Você é o ❌")
st.markdown(f"""
**Placar**
- {JOGADOR} Jogador: {st.session_state.placar[JOGADOR]}
- {COMPUTADOR} Computador: {st.session_state.placar[COMPUTADOR]}
- 🤝 Empates: {st.session_state.placar["Empate"]}
""")

# Tabuleiro com layout forçado 3x3 via HTML e botões separados
st.markdown("""
<style>
.tabela {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    max-width: 300px;
    margin: auto;
}
.botao-jogo button {
    width: 100%;
    height: 60px;
    font-size: 32px;
}
</style>
<div class="tabela">
""", unsafe_allow_html=True)

for idx in range(9):
    btn_key = f"casa_{idx}"
    col_html = f'<div class="botao-jogo">{idx}</div>'
    if st.session_state.tabuleiro[idx] == "":
        if st.button(" ", key=btn_key):
            st.session_state.tabuleiro[idx] = JOGADOR
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
        st.button(st.session_state.tabuleiro[idx], key=btn_key, disabled=True)

st.markdown("</div>", unsafe_allow_html=True)

# Mensagem final com destaque
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
        st.markdown("""
        Esse jogo da velha foi desenvolvido em Python com Streamlit, com uma IA simples que responde automaticamente após a jogada do jogador.

        - Você joga como ❌ e o computador responde com ⭕  
        - A IA tenta ganhar, bloquear ou joga aleatoriamente  
        - Desenvolvido por **Stephanie Jollo**
        """)
