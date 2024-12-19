import services.supabase_client as supabase_client
import streamlit as st

def VerificarCpf(placa):
    conn = supabase_client.get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = """SELECT m.cpf FROM caminhoes c, motoristas m
                 WHERE c.motorista = m.id
                 AND (%s IN (c.placa, c.reboque, c.reboque2))
                 LIMIT 1"""
        val = (placa,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return False
#@st.cache_data(show_spinner="Carregando...")
def CarregarMotoristas():
    supabase = supabase_client.get_supabase_connection()
    if supabase:
        result = supabase.table("veiculos").select("motoristas(cpf), placa, reboque, reboque2, despesa, obs").execute().data
        return result

def InserirAbastecimentos(lista_abastecimentos):
    supabase = supabase_client.get_supabase_connection()
    if supabase:
        for abastecimento in lista_abastecimentos:
            # O 'documento', 'data' e 'placa_veiculo' são os campos que serão usados para identificar o abastecimento - no caso na ordem 0, 1 e 2
            result = supabase.table("abastecimentos").select("id").eq("documento", abastecimento[0]).eq("data", abastecimento[1]).eq("placa_veiculo", abastecimento[2]).eq("quantidade", abastecimento[6]).execute().data
            if not result or len(result) == 0:  # Se o registro não existir, insere
                supabase.table("abastecimentos").insert({
                    "documento": abastecimento[0],
                    "data": abastecimento[1],
                    "placa_veiculo": abastecimento[2],
                    "codigo_despesa": abastecimento[3],
                    "descricao_despesa": abastecimento[4],
                    "cnpj_fornecedor": abastecimento[5],
                    "quantidade": float(abastecimento[6].replace(',', '.')),
                    "valor_unitario": float(abastecimento[7].replace(',', '.')),
                    "valor_total": float(abastecimento[8].replace(',', '.')),
                    "tipo_pagamento": abastecimento[9],
                    "previsao_pagamento": abastecimento[10],
                    "hodometro": abastecimento[11],
                    "horimetro": abastecimento[12],
                    "descontar_comissao": abastecimento[13],
                    "abastecimento_completo": abastecimento[14],
                    "observacao": abastecimento[15],
                    "cpf_motorista": abastecimento[16]
                }).execute()
