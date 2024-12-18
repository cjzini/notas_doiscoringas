import os
import shutil
import zipfile

class Trataarquivos:
    def __init__(self, pasta):
        self.pasta = pasta
        self.criar_pasta(pasta)

    def criar_pasta(self, pasta):
        try:
            # Verifica se o diretório existe, e se não existir, cria o diretório
            os.makedirs(pasta, exist_ok=True)
        except PermissionError:
            print("Você não tem permissão para criar ou acessar este diretório.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def extrair_arquivos(self):
        arquivo = os.listdir(self.pasta)
        # print (arquivo[0])
        caminho = os.path.join(self.pasta, arquivo[0])
        with zipfile.ZipFile(caminho, 'r') as zip:
            # Extraia todos os arquivos do arquivo ZIP para o diretório atual
            zip.extractall(self.pasta)
            # deletar o arquivo .zip original
        os.remove(caminho)


    def deletar_arquivos(self):
        for arquivo in os.listdir(self.pasta):
            caminho = os.path.join(self.pasta, arquivo)
            try:
                if os.path.isfile(caminho) or os.path.islink(caminho):
                    os.unlink(caminho)
                elif os.path.isdir(caminho):
                    shutil.rmtree(caminho)
            except Exception as e:
                print('Falha ao deletar %s. Motivo: %s' % (caminho, e))
         