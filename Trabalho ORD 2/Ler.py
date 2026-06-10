import struct
from Ordem import *
from Pagina import *

def LerPagina(rrn_pagina, arq):
    offset = rrn_pagina * struct.calcsize(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i') + struct.calcsize('i')
    arq.seek(offset)
    valoresBytes = arq.read(struct.calcsize(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i'))
    valores = struct.unpack(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i', valoresBytes)
    pagina_obj = Pagina()
    pagina_obj.quantidadeDeChaves = valores[0]
    pagina_obj.chaves = list(valores[1:ORDEM])
    pagina_obj.offsets = list(valores[ORDEM:ORDEM + ORDEM - 1])
    pagina_obj.filhos = list(valores[ORDEM + ORDEM - 1:])
    return pagina_obj

def lerRegistro(Arquivo) -> tuple[str, int]:
        tam_bytes = Arquivo.read(2)
        if len(tam_bytes) < 2:
            return '', 0
        
        tam = struct.unpack('h', tam_bytes)[0]
        if tam > 0:
            buffer = Arquivo.read(tam)
            return buffer.decode('utf-8', errors='replace'), tam