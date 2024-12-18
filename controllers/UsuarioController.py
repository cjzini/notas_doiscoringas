import services.database as db
import models.Usuario as usuario
import streamlit as st

def Incluir(usuario):
    conn = db.get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, papel) VALUES (%s, %s, %s)", (usuario.nome, usuario.email, usuario.papel,))
        conn.commit()
        conn.close()
    
# def SelecionarById(id):
#     db.cursor.execute("SELECT * FROM usuario WHERE ID = ?", id)
#     userList = []
#     for row in db.cursor.fetchall():
#         userList.append(usuario.Usuario(row[0], row[1],row[2], row[3]))
#     return userList[0]

def Alterar(usuario):
    conn = db.get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nome = %s, email = %s, papel = %s WHERE id = %s"
        val = (usuario.nome, usuario.email, usuario.papel, usuario.id)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        return True
    else:
        return False

def Excluir(usuario):
    conn = db.get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        val = (usuario.id,)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        return True
#@st.cache_data(show_spinner="Carregando...")
def SelecionarTodos():
    conn = db.get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = 'SELECT * FROM usuarios'
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            users.append(usuario.Usuario(row[0], row[1], row[2], row[3]))
        # users = [(id, nome, email, papel) for (id, nome, email, papel) in cursor.fetchall()]
        conn.close()
        return users
    return []