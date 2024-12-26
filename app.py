from PIL import Image
import streamlit as st
import services.supabase_client as supabase_client

im = Image.open("images/favicon.png")
st.set_page_config(
    page_title="Dois Coringas",
    page_icon=im,
)

supabase = supabase_client.get_supabase_connection()

# Inicialização das variáveis de sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

# Função para criar arquivo de usuários se não existir
def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = response.user
        st.session_state.logged_in = True
        st.session_state.role = 'admin'
        return True
    except Exception as e:
        st.error(f"Erro no login: {str(e)}")
        return False

def logout_user():
    supabase.auth.sign_out()
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# Interface de login
def login_page():
    st.title("Login")  
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if login_user(email, password):
                st.success("Login realizado com sucesso!")
                st.rerun()

# Interface principal após o login
def main_page():
    role = st.session_state.role
    notas_comb = st.Page(
        "views/notas_comb.py",
        title="Notas de Combustível",
        icon=":material/local_gas_station:",
        default=(role == "integ"),
    )

    #respond_2 = st.Page(
    #    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
    #)

    # admin = st.Page(
    #     #"admin/cad_usuario.py",
    #     #PageListarUsuario.Listar(),
    #     #"admin/teste_usuario.py",
    #     "views/usuario/cad_usuario.py",
    #     title="Cadastro de Usuário",
    #     icon=":material/person_add:",
    #     default=(role == "admin"),
    # )
    # admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")
    # if Page_cliente == 'Consultar':
    #     PageListCliente.List()

    # if Page_cliente == 'Incluir':
    #     st.experimental_set_query_params()
    #     PageCreateCliente.Create()
    settings = st.Page("settings.py", title="Configuração", icon=":material/settings:")
    logout_page = st.Page(logout_user, title="Sair", icon=":material/logout:")

    user_pages = [notas_comb]
    #admin_pages = [admin]
    account_pages = [settings, logout_page]

    #st.title("Integração Dois Coringas")
    st.logo("images/logo_2coringas.png")

    page_dict = {}
    if st.session_state.role in ["integ", "admin"]:
        page_dict["Integrações"] = user_pages
    #if st.session_state.role == "admin":
    #    page_dict["Cadastros"] = admin_pages

    if len(page_dict) > 0:
        pg = st.navigation(page_dict | {"Conta": account_pages})
    else:
        pg = st.navigation([st.Page(login_page)])

    pg.run()

# Fluxo principal da aplicação
if st.session_state.logged_in:
    main_page()
else:
    login_page()