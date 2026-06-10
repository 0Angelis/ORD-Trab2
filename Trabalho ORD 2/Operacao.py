from Inserir import *
from Busca import *

def Operaçao(Arquivo):
    with open(Arquivo, "r") as arquivo, open("operacoes.txt", "w") as saida:
        linhas = arquivo.readlines()
        tamLinha = len(linhas)
        i = 0
        while i < tamLinha:
            linha = linhas[i].strip()
            if linha:
                operacao = linha[0]
                if len(linha.split()) > 1:
                    Chave = linha.split()[1]
                    Chave = Chave.split(sep='|')[0]
                    if operacao == "b":
                        resultado = Busca.buscarJogo(Chave)
                        saida.write(resultado + "\n")  
                    elif operacao == "i":
                        indiceEspaco = linha.index(' ')
                        registro = linha[indiceEspaco + 1:]
                        resultado = InserirJogo(registro)
                        saida.write(resultado + "\n")  
                    else:
                        saida.write(f"Operação '{operacao}' não reconhecida.\n\n")  
                else:
                    saida.write(f"Linha mal formatada ou faltando chave: {linha}\n\n")  
            i += 1