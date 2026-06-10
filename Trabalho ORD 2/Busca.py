import struct
from Ordem import *
from Ler import *
import Ler

def buscarJogo(Chave):
    with open("btree.dat", 'rb') as Arvore:
        resultado = [f'Busca pelo registro de chave "{Chave}"\n']
        rrn = struct.unpack('i', Arvore.read(struct.calcsize('i')))[0]
        achou, rrn, pos = BuscarNaArvore(int(Chave), rrn, Arvore)
        with open("games.dat", 'rb') as Games:
            if achou:
                pag = LerPagina(rrn, Arvore)
                offset = pag.offsets[pos]
                Games.seek(offset)
                registro, tam = lerRegistro(Games)
                resultado.append(f"{registro} ({tam} bytes - offset {offset})\n")
            else:
                resultado.append("O registro nao foi encontrado!\n")
    return "".join(resultado)

def BuscarNaPagina(chave_busca, pagina_obj):
    indice = 0
    while indice < pagina_obj.quantidadeDeChaves and chave_busca > pagina_obj.chaves[indice]:
        indice += 1
    
    if indice < pagina_obj.quantidadeDeChaves and chave_busca == pagina_obj.chaves[indice]:
        return True, indice
    else:
        return False, indice

def BuscarNaArvore(chave_busca, rrn_atual, Arquivo):
    if rrn_atual == NULO:
        return False, NULO, NULO
    else:
        pag = Ler.LerPagina(rrn_atual, Arquivo)
        achou, pos = BuscarNaPagina(chave_busca, pag)
        if achou:
            return True, rrn_atual, pos
        else:
            if pos < len(pag.filhos):
                return BuscarNaArvore(chave_busca, pag.filhos[pos], Arquivo)
            else:
                return False, NULO, NULO


