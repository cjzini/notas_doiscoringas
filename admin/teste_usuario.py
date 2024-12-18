import streamlit as st
import services.database as db
import models.Usuario as usuario

def get_all_users():
    conn = db.get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = 'select * from usuarios'
        cursor.execute(sql)
        users = [(id, nome, email, papel) for (id, nome, email, papel) in cursor.fetchall()]
        conn.close()
        users.sort(key=lambda x:x[0])
        return users
    return []

st.write(get_all_users())