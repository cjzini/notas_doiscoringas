import os
import csv
import io
import xml.etree.ElementTree as ET

import controllers.NotaController as NotaController
from datetime import datetime

class Trataxml:
    def __init__(self, pasta):
        self.pasta = pasta
        self.arquivos = []
        self.dados_nota = []
        self.placas = []
        self.motoristas = NotaController.CarregarMotoristas()
        self.carrega_placas()

    # Função para extrair as placas da lista self.motoristas
    def carrega_placas(self):
        for motorista in self.motoristas:
            self.placas.append(motorista['placa'])
            if motorista['reboque'] is not None:
                self.placas.append(motorista['reboque'])
            if motorista['reboque2'] is not None:
                self.placas.append(motorista['reboque2'])

    def extrair_codigo_ncm(self):
        #dic_codigos = {}
        # Percorrer cada arquivo
        for arquivo in self.arquivos:
            caminho = os.path.join(self.pasta, arquivo) # Caminho para os arquivo da NF
            tree = ET.parse(caminho) # Cria a arvore do XML
            root = tree.getroot()
            nsNFE = {"ns": "http://www.portalfiscal.inf.br/nfe"}
            # Percorre todos os itens de cada item de produto
            items = root.findall('ns:NFe/ns:infNFe/ns:det', nsNFE)
            for item in items:
                #print(item.attrib['nItem'])
                cod_ncm = int(item.find('ns:prod/ns:NCM', nsNFE).text)
                desc_prod = item.find('ns:prod/ns:xProd', nsNFE).text
                print(cod_ncm, desc_prod)

    def grava_csv(self):
        # Cria um buffer de memória
        buffer = io.StringIO()
        data = self.dados_nota[0][1]
        data = data.replace('/', '-')
        writer = csv.writer(buffer, delimiter=';')
        # Escreve os cabeçalhos
        writer.writerow(['DOCUMENTO', 'DATA', 'PLACA_VEICULO', 'CODIGO_DESPESA', 'DESCRICAO_DESPESA', 'CNPJ_FORNECEDOR', 'QUANTIDADE', 'VALOR_UNITARIO', 'VALOR_TOTAL', 'TIPO_PAGAMENTO', 'PREVISAO_PAGAMENTO', 'HODOMETRO', 'HORIMETRO', 'DESCONTAR_COMISSAO', 'ABASTECIMENTO_COMPLETO', 'OBSERVACAO', 'CPF_MOTORISTA'])
        # Escreve os dados
        writer.writerows(self.dados_nota)
        # Retorna o conteúdo do buffer
        return buffer.getvalue()

    def grava_supabase(self):
        NotaController.InserirAbastecimentos(self.dados_nota)

    def extrair_xmls(self):
        itens_combustivel = []
        self.arquivos = os.listdir(self.pasta)
        for arquivo in self.arquivos:
            caminho = os.path.join(self.pasta, arquivo) # Caminho para o arquivo da NF
            tree = ET.parse(caminho) # Cria a arvore do XML
            root = tree.getroot()
            nsNFE = {"ns": "http://www.portalfiscal.inf.br/nfe"}
            # Numero da NF
            num_nfe = root.find('ns:NFe/ns:infNFe/ns:ide/ns:nNF', nsNFE).text
            # CNPJ do Emissor
            cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFE).text
            if cnpj == '04956492000144' or cnpj == '81632093001736': # Se o CNPJ for da Maximport (ARLA Estoque) ou AGRICOPEL então não precisa ser tratado
                continue
            # data da NF
            data = root.find('ns:NFe/ns:infNFe/ns:ide/ns:dhEmi', nsNFE).text
            data = data[0:10]
            data = datetime.strptime(data, '%Y-%m-%d').date()
            data = data.strftime('%d/%m/%Y')
            #Valor total da NFe
            #total_nfe = float(root.find('ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF', nsNFE).text)
            # Percorre todos os itens de cada item de produto
            items = root.findall('ns:NFe/ns:infNFe/ns:det', nsNFE)
            #qtd_itens = len(items)
            # Percorre todos os itens
            for item in items:
                observacao = ''
                # Codigo NCM
                cod_ncm = int(item.find('ns:prod/ns:NCM', nsNFE).text)
                # itens_nfe.append(str(cod_ncm))
                # Codigo da despesa
                cod_despesa = self.retorna_tipo_despesa(cod_ncm)
                # Extrair informações do campo infComplementares tratando a exceção pois a tag infCpl pode não existir no xml     
                try:
                    obs = root.find('ns:NFe/ns:infNFe/ns:infAdic/ns:infCpl', nsNFE).text
                except AttributeError:
                    obs = 'Sem placa'
                # Retorna o número da placa
                placa = self.retorna_placa(obs)
                if placa == 'BBI0059': # No cadastro dos postos ainda está a placa antiga, alterando assim para a nova
                    placa = 'BBI0A59'
                # Quantidade
                qtd_item = float(item.find('ns:prod/ns:qCom', nsNFE).text)
                # Valor unitario
                vlr_unit = round(float(item.find('ns:prod/ns:vUnCom', nsNFE).text),2)
                # Valor produto
                vlr_prod = float(item.find('ns:prod/ns:vProd', nsNFE).text)
                # Valor desconto
                vlr_desc = 0.0
                if item.find('ns:prod/ns:vDesc', nsNFE) is not None: # Se existir a tag vDesc, faz o calculo do desconto no valor do produto e atualiza o valor unitario
                    vlr_desc = float(item.find('ns:prod/ns:vDesc', nsNFE).text)
                if vlr_desc > 0.0:
                    vlr_prod = round((vlr_prod - vlr_desc), 2)
                    vlr_unit = round((vlr_prod / qtd_item), 2)
                
                if cod_despesa == 28 or cod_despesa == 273 or cod_despesa == 298: # Se o Código da despesa for 28 - DIESEL, 273 - ARLA, ou 298 - ABASTECIMENTO
                    cons_motorista = self.retorna_cpf_motorista(placa)
                    if cons_motorista[1] == 'AAA0000':
                        observacao = 'Placa informada na NF: ' + placa
                    # consulta_motorista: [0] - CPF do motorista, [1] - placa, [2] - SE reboque, [3] - SE despesa, [4] - observação
                    if cons_motorista[3]: # Verifica se é despesa
                        cons_motorista[1] = 'AAA0000'
                        observacao = cons_motorista[4] + ' - Placa informada na NF: ' + placa
                        if cons_motorista[0] == '000.000.000-00':
                            cpf_motorista = ''
                        else:
                            cpf_motorista = cons_motorista[0]
                    else:
                        cpf_motorista = cons_motorista[0]
                    placa = cons_motorista[1] 
                    if cons_motorista[2]: # Verifica se a placa é reboque
                        cod_despesa = 367 # Caso seja reboque, o Código da despesa é 367 de MAÇARICO                    
                    itens_combustivel.append(str(num_nfe))     # Número do documento de despesa
                    itens_combustivel.append(str(data))        # Data da despesa
                    itens_combustivel.append(str(placa))       # Placa
                    itens_combustivel.append(str(cod_despesa)) # Código da despesa
                    itens_combustivel.append("")               # Descrição da despesa (em branco)
                    itens_combustivel.append(str(cnpj))        # CNPJ do Fornecedor
                    qtd_item = "{:,.2f}".format(qtd_item).replace('.', ',')
                    itens_combustivel.append(qtd_item)         # Quantidade
                    vlr_unit = "{:,.2f}".format(vlr_unit).replace('.', ',')
                    itens_combustivel.append(str(vlr_unit))    # Valor unitário
                    vlr_prod = "{:.2f}".format(vlr_prod).replace('.', ',')
                    itens_combustivel.append(str(vlr_prod))    # Valor Total
                    itens_combustivel.append("")               # Tipo do Pagamento (em branco)
                    itens_combustivel.append("")               # Previsão do Pagamento (em branco)
                    itens_combustivel.append("")               # Hodometro (em branco)
                    itens_combustivel.append("")               # Horimetro (em branco)
                    itens_combustivel.append("")               # Descontar Comissão (em branco)
                    itens_combustivel.append("")               # Abastecimento Completo (em branco)
                    itens_combustivel.append(observacao)               # Observação
                    itens_combustivel.append(str(cpf_motorista)) # CPF do Motorista
                    self.dados_nota.append(itens_combustivel)
                    itens_combustivel = []     
        #return self.dados_nota

    # Retorna o número da placa contido no campo infComplementares
    def retorna_placa(self, obs):
        obs = obs.upper()
        obs = obs.replace('-', '')
        for placa in self.placas:
            if placa in obs:
                return placa
        placa = self.caca_placa(obs)
        return placa

    def caca_placa(self, obs):
        obs = obs.upper()
        #procura pela substring "PLACA:" ou "PLACA " armazenada na obs e retorna a posição inicial encontrada
        posicao = obs.find("PLACA:")
        if posicao == -1:
            posicao = obs.find("PLACA ")
        if posicao != -1:
            subs = obs[posicao+6:posicao+15]
            subs = subs.replace('-', '')
            subs = subs.replace(' ', '')
            # Se o tamanho de subs for maior que 7 caracteres, exclui o último caractere (se houver), deixando apenas os 7 primeiros
            if len(subs) > 7:
                subs = subs[0:7]
            return subs
        return 'SEMPLAC'
        #print('Posição inicial da substring \"{0}\" no Texto = {1}'.format(subs,posicao))
    
    # Retorna o cpf do motorista através da placa contida no campo infComplementares
    def retorna_cpf_motorista(self, placa):
        for motorista in self.motoristas:
            # Verifica se a placa principal corresponde
            if motorista['placa'] == placa:
                return [motorista['motoristas']['cpf'], placa, False, motorista.get('despesa'), motorista.get('obs')]
            
            # Verifica se a placa do reboque corresponde
            if motorista.get('reboque') == placa:
                return [motorista['motoristas']['cpf'], placa, True, motorista.get('despesa'), motorista.get('obs')]
            
            # Verifica se a placa do reboque2 corresponde
            if motorista.get('reboque2') == placa:
                return [motorista['motoristas']['cpf'], placa, True, motorista.get('despesa'), motorista.get('obs')]
        
        # Caso nenhuma placa seja encontrada, retorna o CPF padrão
        return ['', 'AAA0000', False, False, None] # Se a placa não foi encontrada na listagem armazenada no BD, retorna placa DESPESAS GERAIS

    # Retorna o número da placa contido no campo infComplementares
    def retorna_motorista_obs(self, obs):
        obs = obs.upper()
        #procura pela substring "MOTORISTA:" armazenada na obs e retorna a posição inicial encontrada
        subs = "MOTORISTA:"
        posicao = obs.find(subs)
        if posicao == -1:
            return 'SEM MOTORISTA'
        subs = obs[posicao+11:posicao+32]
        return subs
    
    # Retorna o código da despesa para o Bsoft a partir da descricão do item
    def retorna_tipo_despesa(self, cod_ncm):
        match cod_ncm:
            case 27101259: # Código NCM para Gasolina Comum
                return 298 # Código da Despesa para Abastecimento no Bsoft
            case 27101921: # Código NCM para Diesel
                #Fazer a distinção de S10 e S500
                # S10 despesa 298 e S500 despesa 367
                return 28 # Código da Despesa para DIESEL no Bsoft
            case 31021010: # Código NCM para ARLA 31021010
                return 273 # Código da Despesa para Arla no Bsoft
            case 1104:
                return 4
        return 0