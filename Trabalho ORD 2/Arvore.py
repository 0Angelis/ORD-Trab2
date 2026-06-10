import struct
import Inserir
import Ler
import Pagina 

def CriarArvore():
    Arvore = open('btree.dat', 'wb+')
    rrnRaiz = 0
    Arvore.write(struct.pack('i', rrnRaiz))
    Pagina.SalvarPagina(rrnRaiz, Pagina.Pagina(), Arvore)
    return Arvore, rrnRaiz

def FecharArvore(rrnRaiz, Arquivo):
    Arquivo.seek(0)
    Arquivo.write(struct.pack('i', rrnRaiz))
    Arquivo.close()

def arvore():
    with open("games.dat", 'rb') as Games:
        Arvore, rrnRaiz = CriarArvore()
        numRegistros = struct.unpack('i', Games.read(struct.calcsize('i')))[0]
        reg, tam = Ler.lerRegistro(Games)
        Chave = reg.split('|')[0]
        Chave = int(Chave)
        offset = 4
        contador = 0
        while contador < numRegistros:
            novaChave, novoOffset, filhoDireito, promo = Inserir.InserirNaArvore(Chave, offset, rrnRaiz, Arvore)
            if promo:
                novaPagina = Pagina.Pagina()
                novaPagina.chaves[0] = novaChave
                novaPagina.offsets[0] = novoOffset
                novaPagina.filhos[0] = rrnRaiz
                novaPagina.filhos[1] = filhoDireito
                novaPagina.quantidadeDeChaves = 1
                rrnRaiz = Inserir.rrnNovo(Arvore)
                Pagina.SalvarPagina(rrnRaiz, novaPagina, Arvore)
            contador += 1
            offset += tam + 2
            reg, tam = Ler.lerRegistro(Games)
            if not(reg == '' and tam == 0):
                Chave = int(reg.split('|')[0])
        FecharArvore(rrnRaiz, Arvore)