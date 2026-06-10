import os
from Ordem import *
from Arvore import *
from Ler import *

def ImprimirArvore():
    with open("btree.dat", 'rb') as Arvore:
        with open("Saida.txt", 'w') as Saida:
            rrnRaiz = struct.unpack('i', Arvore.read(struct.calcsize('i')))[0]
            numPaginas = (os.path.getsize("btree.dat") - struct.calcsize('i')) // struct.calcsize(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i')
            for rrn in range(numPaginas):
                if rrn == rrnRaiz:
                    Saida.write("\n=================== Raiz ===================")
                
                pagina = LerPagina(rrn, Arvore)

                Saida.write(f"\nPagina {rrn}\n")
                Saida.write("Chaves: ")
                for i in range(ORDEM - 1):
                    if i < len(pagina.chaves) and pagina.chaves[i] != -1:
                        Saida.write(f"{pagina.chaves[i]} | ")
                    else:
                        Saida.write("-1 | ")
                Saida.write("\n")
                Saida.write("Offsets: ")
                for i in range(ORDEM - 1):
                    if i < len(pagina.offsets) and pagina.offsets[i] != -1:
                        Saida.write(f"{pagina.offsets[i]} | ")
                    else:
                        Saida.write("-1 | ")
                Saida.write("\n")
                Saida.write("Filhas: ")
                for filho in pagina.filhos:
                    Saida.write(f"{filho} | ")
                Saida.write("\n")
                if rrn == rrnRaiz:
                    Saida.write("============================================\n")


  