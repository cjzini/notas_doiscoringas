import streamlit as st
import time
from helpers.buscanf import Buscanf
from helpers.trataarquivos import Trataarquivos
from helpers.trataxml import Trataxml

st.title("Notas de Combustível")

#Definir as duas colunas que serão usadas para dividir os campos de dados
col1, col2 = st.columns(2)
pasta = 'C:\\Temp\\XML'
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

# with col1:
#     #st.subheader("Filtros:")
#     #pasta = st.text_input('Diretório de trabalho', value='C:\\Temp\\XML')
#     trataxml = Trataxml(pasta)
#     #st.write(trataxml.motoristas)
#     #st.write(trataxml.placas)
#     # Scan the folder with files.
#     #file_paths = []
#     #if os.path.isdir(folder_path):
#     #    for fn in os.listdir(folder_path):
#     #        fp = f'{folder_path}\{fn}'
#     #        if os.path.isfile(fp):
#     #            file_paths.append(fp)

#     # Select file from scanned folder.
#     #selected_file = st.selectbox('Selecionar arquivo', options=file_paths)
#     #st.write(f'Arquivo selecionado: {selected_file}')
#     btn_processar = st.button('Processar')
#     if btn_processar:
#          with st.spinner('Gerando Arquivo...'):
#             #trataxml.extrair_codigo_ncm()
#             trataxml.extrair_xmls()
#             st.write(trataxml.dados_nota)
#             st.write(pasta)
#             #trataxml.grava_csv()
#             #st.success("Arquivo gerado!")
#             #df_notas = pd.DataFrame.from_dict(trataxml.extrair_xmls(), orient='index', columns=['num_nfe', 'data', 'ncm', 'cod_despesa', 'placa', 'teste1', 'teste2','teste3'])
#             #st.dataframe(df_notas)

# with col2:
#     #st.subheader("Resultados:")
#     data_nf = st.date_input('Data da NF', format='DD/MM/YYYY')
#     data_nf = data_nf.strftime('%d/%m/%Y') 
#     btn_getnotas = st.button('Baixar Notas')
#     if btn_getnotas:
#         with st.spinner('Processando Notas...'):
#             trataarquivos = Trataarquivos(pasta)
#             trataarquivos.deletar_arquivos()
#             buscanf = Buscanf(pasta, data_nf)
#             buscanf.pegarNotas()
#             trataarquivos.extrair_arquivos()
#             st.success("Pronto!")
#             #st.write(data_nf)