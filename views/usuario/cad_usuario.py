import streamlit as st
import time
import controllers.UsuarioController as UsuarioController
import models.Usuario as usuario
from streamlit_option_menu import option_menu

def exibir_usuarios():
    usuarios = UsuarioController.SelecionarTodos()

    colms = st.columns((1, 2, 2, 1, 1, 1))
    campos = ['Nº', 'Nome', 'Email', 'Papel', 'Alterar', 'Excluir']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)
    for x, item in enumerate(usuarios):
        col1, col2, col3, col4, col5, col6 = st.columns((1, 2, 2, 1, 1, 1))
        col1.write(item.id)
        col2.write(item.nome)
        col3.write(item.email)
        col4.write(item.papel)
        btn_alterar = col5.empty()
        on_click_alterar = btn_alterar.button(
            '✏️', 'btnAlterar' + str(item.id), 'Alterar')
        btn_excluir = col6.empty()
        on_click_excluir = btn_excluir.button(
            '❌', 'btnExcluir' + str(item.id), 'Excluir')
        

        if on_click_excluir:
            if UsuarioController.Excluir(item):
                st.success("Usuário excluído com sucesso!")
                time.sleep(2)
                st.rerun()
        if on_click_alterar:
            abrir_dialogo_edicao(item)

@st.dialog("Editar Usuário")
def abrir_dialogo_edicao(usuario):
    with st.form(key=f"edit_form_{usuario.id}"):
        usuario.nome = st.text_input("Nome", value=usuario.nome)
        usuario.email = st.text_input("Email", value=usuario.email)
        usuario.papel = st.text_input("Papel", value=usuario.papel)
        btn_atualizar = st.form_submit_button("Atualizar")
        if btn_atualizar:
            UsuarioController.Alterar(usuario)
            st.success("Usuário atualizado com sucesso!")
            time.sleep(2)
            st.rerun()

def inserir_usuario():
    with st.form("inserir_usuario"):
        usuario.nome = st.text_input("Nome")
        usuario.email = st.text_input("Email")
        usuario.papel = st.text_input("Papel")
        btn_inserir = st.form_submit_button("Inserir Usuário")
        if btn_inserir:
            UsuarioController.Incluir(usuario)
            st.success("Usuário inserido com sucesso!")
            time.sleep(2)
            st.rerun()

def Listar():
    # Custom CSS to embed FontAwesome - https://fontawesome.com/how-to-use/on-the-web/with-st-streamlit
    # Colocando esse custom CSS é possível colocar icones nos botoes
    st.markdown("""
    <style>
    .btn-custom {
        font-family: 'FontAwesome';
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Gerenciamento de Usuários")
    
    menu = ["Listar", "Inserir"]
    choice = option_menu(None, menu, 
        icons=['list', 'plus-circle'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    
    if choice == "Listar":
        exibir_usuarios()
    elif choice == "Inserir":
        inserir_usuario()

# Executar a função Listar() diretamente
Listar()