import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="172.26.171.193",
            user="admin",
            password="killer66",
            database="twojokers"
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Create user
def create_user(name, email):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(query, (name, email))
            conn.commit()
            st.success("User created successfully!")
        except Error as e:
            st.error(f"Error creating user: {e}")
        finally:
            cursor.close()
            conn.close()

# Read users
def read_users():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        except Error as e:
            st.error(f"Error fetching users: {e}")
        finally:
            cursor.close()
            conn.close()
    return []

# Update user
def update_user(user_id, name, email):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
            cursor.execute(query, (name, email, user_id))
            conn.commit()
            st.success("User updated successfully!")
        except Error as e:
            st.error(f"Error updating user: {e}")
        finally:
            cursor.close()
            conn.close()

# Delete user
def delete_user(user_id):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            st.success("User deleted successfully!")
        except Error as e:
            st.error(f"Error deleting user: {e}")
        finally:
            cursor.close()
            conn.close()

# Streamlit app
st.title("User Management")

with st.container():
    st.subheader("Registered Users")
    users = read_users()
    for user in users:
        col_info, col_edit, col_delete = st.columns([3, 1, 1])
        with col_info:
            st.write(f"{user['name']} - {user['email']}")
        with col_edit:
            if st.button("Edit", key=f"edit_{user['id']}"):
                with st.form(key=f"edit_form_{user['id']}"):
                    st.subheader("Edit User")
                    edit_name = st.text_input("Name", value=user['name'])
                    edit_email = st.text_input("Email", value=user['email'])
                    if st.form_submit_button("Update"):
                        update_user(user['id'], edit_name, edit_email)
                        st.success("User updated successfully!")
                        st.experimental_rerun()
        with col_delete:
            if st.button("Delete", key=f"delete_{user['id']}"):
                if st.confirm("Are you sure you want to delete this user?"):
                    delete_user(user['id'])
                    st.success("User deleted successfully!")
                    st.experimental_rerun()

with st.form(key="new_user_form"):
    st.subheader("Register New User")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email")
    if st.form_submit_button("Register"):
        create_user(name, email)
        st.experimental_rerun()
