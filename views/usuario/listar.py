import streamlit as st
import controllers.UsuarioController as UsuarioController
import paginas.usuario.criar as PageCreateUsuario


def List():
    params = st.experimental_get_query_params()
    if params.get("id") is None:
        st.experimental_set_query_params()
        colms = st.columns((1, 2, 1, 2, 1, 1))
        campos = ['Nº', 'Nome', 'Email', 'Papel', 'Excluir', 'Alterar']
        for col, campo_nome in zip(colms, campos):
            col.write(campo_nome)

        for x, item in enumerate(UsuarioController.SelecionarTodos()):
            col1, col2, col3, col4, col5, col6 = st.columns((1, 2, 1, 2, 1, 1))
            col1.write(item.id)
            col2.write(item.nome)
            col3.write(item.email)
            col4.write(item.papel)
            button_space_excluir = col5.empty()
            on_click_excluir = button_space_excluir.button(
                'Excluir', 'btnExcluir' + str(item.id))
            button_space_alterar = col6.empty()
            on_click_alterar = button_space_alterar.button(
                'Alterar', 'btnAlterar' + str(item.id))

            if on_click_excluir:
                UsuarioController.Excluir(item.id)
                button_space_excluir.button(
                    'Excluído', 'btnExcluir' + str(item.id))
                st.experimental_rerun()
            if on_click_alterar:
                st.experimental_set_query_params(
                    id=[item.id]
                )
                st.experimental_rerun()
    else:
        on_click_voltar = st.button("Voltar")
        if on_click_voltar:
            st.experimental_set_query_params()
            st.experimental_rerun()
        PageCreateUsuario.Create()