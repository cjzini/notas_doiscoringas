from dotenv import load_dotenv
import mysql.connector
import os
import streamlit as st

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

load_dotenv()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro na conexão com o banco de dados: {e}")
        return None