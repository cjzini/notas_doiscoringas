import streamlit as st
import time
import os
from helpers.buscanf import Buscanf
from helpers.trataarquivos import Trataarquivos
from helpers.trataxml import Trataxml

st.title("Notas de Combustível")

#Definir as duas colunas que serão usadas para dividir os campos de dados
col1, col2 = st.columns(2)
# Windows
#pasta = os.getcwd() + '\\xml'
# Linux
pasta = os.getcwd() + '/xml'
trataxml = Trataxml(pasta)
trataarquivos = Trataarquivos(pasta)

with col1:
    data_i = st.date_input('Data Inicial', format='DD/MM/YYYY')
    data_ini = data_i.strftime('%d/%m/%Y')
    dia_ini, mes_ini, ano_ini = data_i.strftime('%d'), data_i.strftime('%m'), data_i.strftime('%Y')
with col2:
    data_f = st.date_input('Data Final', format='DD/MM/YYYY')
    data_fim = data_f.strftime('%d/%m/%Y')
    dia_fim, mes_fim, ano_fim = data_f.strftime('%d'), data_f.strftime('%m'), data_f.strftime('%Y')

nome_arquivo = f'NFComb_{dia_ini}{mes_ini}{ano_ini}_{dia_fim}{mes_fim}{ano_fim}.csv'

btn_processar = st.button('Processar')
if btn_processar:
    with st.spinner('Processando Notas...'):
        trataarquivos.deletar_arquivos()
        buscanf = Buscanf(pasta, data_ini, data_fim)
        buscanf.pegarNotas()
        if not trataarquivos.extrair_arquivos():
            st.error("Não foram encontradas notas no período informado.")
            time.sleep(2)
            st.rerun()
        trataxml.extrair_xmls()
        trataxml.grava_supabase()
        #st.write(trataxml.dados_nota)
        dados_csv = trataxml.grava_csv()
        # Botão de download	
        st.download_button(
            label='Download do Arquivo CSV', 
            data=dados_csv, 
            file_name=nome_arquivo, 
            mime='text/csv'
        )