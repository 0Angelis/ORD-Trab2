import sys
from Arvore import *
from Imprimir import *
from Operacao import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n=========================================")
        print("python main.py -c")
        print("python main.py -p")
        print("python main.py -e 'arquivo de operações'")  
        print("==========================================\n")
        sys.exit(1)
    elif sys.argv[1] == "-c":
        arvore()
        print("\n==============================")        
        print("Árvore montada com sucesso")
        print("==============================\n") 
    elif sys.argv[1] == "-p":
        ImprimirArvore()
        print("\n==========================================================")
        print("Arvore foi impressa no arquivo 'Saida.txt' com sucesso.")
        print("==========================================================\n")     
    elif sys.argv[1] == "-e" and len(sys.argv) == 3:
        Arquivo = sys.argv[2]
        Operaçao(Arquivo)
        print("\n===================================================================================")
        print(f"As operações do arquivo '{Arquivo}' foram realizadas com sucesso.")
        print("Foi criado um arquivo novo chamado 'operacoes.txt' mostrando o que foi realizado.")
        print("===================================================================================\n")
    else: 
        print("\n==========================================")
        print("Comando inválido.\nUtilize:")
        print("python main.py -c")
        print("python main.py -p")
        print("python main.py -e 'arquivo de operações'") 
        print("==========================================\n")
        sys.exit(1)
