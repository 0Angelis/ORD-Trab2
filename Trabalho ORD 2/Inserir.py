import os
import struct
from Busca import *
from Ler import *
from Ordem import *
from Pagina import *
import Busca
import Pagina
import Ler

def rrnNovo(Arquivo):
    Arquivo.seek(0, os.SEEK_END)
    offset = Arquivo.tell()
    return ((offset - struct.calcsize('i')) // struct.calcsize(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i'))


def InsereNaPagina(chave_inserir, offset_inserir, filho_direito, pagina_obj):
    if pagina_obj.quantidadeDeChaves == ORDEM - 1:
        pagina_obj.chaves.append(NULO)
        pagina_obj.offsets.append(NULO)
        pagina_obj.filhos.append(NULO)
    i = pagina_obj.quantidadeDeChaves

    while i > 0 and chave_inserir < pagina_obj.chaves[i - 1]:
        pagina_obj.chaves[i] = pagina_obj.chaves[i - 1]
        pagina_obj.offsets[i] = pagina_obj.offsets[i - 1]
        pagina_obj.filhos[i + 1] = pagina_obj.filhos[i]
        i -= 1
    pagina_obj.chaves[i] = chave_inserir
    pagina_obj.offsets[i] = offset_inserir
    pagina_obj.filhos[i + 1] = filho_direito
    pagina_obj.quantidadeDeChaves += 1


def SepararPagina(chave_dividir, offset_dividir, filho_direito, paginaBase, arq):
    InsereNaPagina(chave_dividir, offset_dividir, filho_direito, paginaBase)
    meio = ORDEM // 2
    chave_promocao = paginaBase.chaves[meio]
    offset_promocao = paginaBase.offsets[meio]
    filhoDireitoNovo = rrnNovo(arq)
    Pagina_atual = Pagina.Pagina()
    Pagina_atual.quantidadeDeChaves = meio
    chaves = paginaBase.chaves[:meio] + [NULO] * (ORDEM - 1 - len(paginaBase.chaves[:meio]))
    Pagina_atual.chaves = chaves
    offsets = paginaBase.offsets[:meio] + [NULO] * (ORDEM - 1 - len(paginaBase.offsets[:meio]))
    Pagina_atual.offsets = offsets
    filhos = paginaBase.filhos[:meio + 1] + [NULO] * (ORDEM - len(paginaBase.filhos[:meio + 1]))
    Pagina_atual.filhos = filhos
    nova_pagina = Pagina.Pagina()
    nova_pagina.quantidadeDeChaves = ORDEM - meio - 1
    chaves_novas = paginaBase.chaves[meio + 1:] + [NULO] * (ORDEM - 1 - len(paginaBase.chaves[meio + 1:]))
    nova_pagina.chaves = chaves_novas
    offsets_novos = paginaBase.offsets[meio + 1:] + [NULO] * (ORDEM - 1 - len(paginaBase.offsets[meio + 1:]))
    nova_pagina.offsets = offsets_novos
    filhos_novos = paginaBase.filhos[meio + 1:] + [NULO] * (ORDEM - len(paginaBase.filhos[meio + 1:]))
    nova_pagina.filhos = filhos_novos
    return chave_promocao, offset_promocao, filhoDireitoNovo, Pagina_atual, nova_pagina


def InserirNaArvore(chave_inserir, offset_inserir, rrn_atual, Arquivo):
    if rrn_atual == NULO:
        chave_promocao = chave_inserir
        offset_promocao = offset_inserir
        filhoDireitoNovo = NULO
        return chave_promocao, offset_promocao, filhoDireitoNovo, True
    else:
        pag = Ler.LerPagina(rrn_atual, Arquivo)
        achou, pos = Busca.BuscarNaPagina(chave_inserir, pag)
    if achou:
        raise KeyError("Chave duplicada")

    chave_promocao, offset_promocao, filhoDireitoNovo, promocao = InserirNaArvore(chave_inserir, offset_inserir, pag.filhos[pos], Arquivo)

    if not promocao:
        return NULO, NULO, NULO, False
    else:
        if pag.quantidadeDeChaves < ORDEM - 1:
            InsereNaPagina(chave_promocao, offset_promocao, filhoDireitoNovo, pag)
            Pagina.SalvarPagina(rrn_atual, pag, Arquivo)
            return NULO, NULO, NULO, False
        else:
            chave_promocao, offset_promocao, filhoDireitoNovo, Pagina_atual, pag_nova = SepararPagina(chave_promocao, offset_promocao, filhoDireitoNovo, pag, Arquivo)
            Pagina.SalvarPagina(rrn_atual, Pagina_atual, Arquivo)
            Pagina.SalvarPagina(filhoDireitoNovo, pag_nova, Arquivo)
            return chave_promocao, offset_promocao, filhoDireitoNovo, True


def InserirJogo(registro):       
    Chave = int(registro.split('|')[0])
    resultado = [f'Insercao do registro de chave "{Chave}"\n']
    with open("btree.dat", 'rb') as Arvore:
        rrnRaiz = struct.unpack('i', Arvore.read(struct.calcsize('i')))[0]
        achou, _, _ = Busca.BuscarNaArvore(Chave, rrnRaiz, Arvore)
        if achou:
            resultado.append(f"Erro: chave {Chave} ja existente!\n")
            return "".join(resultado)
    with open("games.dat", 'ab') as Games:
        offset = Games.tell()
        tam = len(registro)
        Games.write(struct.pack('h', tam))
        Games.write(registro.encode('utf-8'))
    with open("btree.dat", 'r+b') as Arvore:
        novaChave, novoOffset, filhoDireito, promo = InserirNaArvore(Chave, offset, rrnRaiz, Arvore)
        if promo:
            PaginaNova = Pagina()
            PaginaNova.chaves[0] = novaChave
            PaginaNova.offsets[0] = novoOffset
            PaginaNova.filhos[0] = rrnRaiz
            PaginaNova.filhos[1] = filhoDireito
            PaginaNova.quantidadeDeChaves = 1
            rrnRaiz = rrnNovo(Arvore)
            Pagina.SalvarPagina(rrnRaiz, PaginaNova, Arvore)
    resultado.append(f"{registro} ({tam} bytes - offset {offset})\n")
    return "".join(resultado)
