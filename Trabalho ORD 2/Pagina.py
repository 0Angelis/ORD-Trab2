import struct
from Ordem import *

class Pagina:
    def __init__(self, quantidadeDeChaves=0) -> None:
        self.quantidadeDeChaves: int = quantidadeDeChaves
        self.chaves: list = [NULO] * (ORDEM - 1)
        self.offsets: list = [NULO] * (ORDEM - 1)
        self.filhos: list = [NULO] * ORDEM


def SalvarPagina(rrn_pagina, pagina_obj, arquivo):
    offset = rrn_pagina * struct.calcsize(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i') + struct.calcsize('i')
    arquivo.seek(offset)
    valores = [pagina_obj.quantidadeDeChaves] + pagina_obj.chaves + pagina_obj.offsets + pagina_obj.filhos
    valoresBytes = struct.pack(f'i{ORDEM - 1}i{ORDEM - 1}i{ORDEM}i', *valores)
    arquivo.write(valoresBytes)