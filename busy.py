from time import sleep
import pandas as pd
import numpy as np
import data
import data2
mesas_disponiveis = ['Xaxado', 'Maxixe', 'Afoxe', 'Funk', 'Blues', 'Rock', 'Reggae', 'Chorinho', 'Samba', 'Frevo', 'Pop', 'Forro']
mesas_ocupadas1 = []
mesas_ocupadas = {}
comandas = {}
militantes = []
produtos = {}
produtos_disponiveis = {}
def isfloat(valor):
    try:
        float(valor)
        return True
    except:
        return False
def table_mesas(lst, str):
    table = pd.DataFrame()
    table[str] = lst
    return table
def check_titulo(str):
    try:
        int(str)
        return True
    except:
        return False
def def_tipo_transacao(tuple=list):
    count = 0
    tipo = ''
    for i in tuple:
        if i == 0:
            count = count +1
        else:
            continue
    if count == 2:
        if tuple[0] != 0:
            tipo="""'Dinheiro'"""
            return tipo
        if tuple[1] != 0:
            tipo="""'Cartao'"""
            return tipo
        if tuple[2] != 0 :
            print('Pix')
            tipo = """'Pix'"""
            return tipo
    else:
        tipo = """'Splitted'"""
        return tipo
class comanda:
    def __init__(self,itens=None):
        self.itens = itens
        self.itens = {}
        self.dfbar = pd.DataFrame(columns=['Qtd.', 'Item'])
        self.dfcozinha = pd.DataFrame(columns=['Qtd.','Item'])
        pass
    def gerar_comanda(self):
        index = 1
        sleep(2)
        for i in self.itens:
            q = """select Tipo from produtos where Nome = '{}'""".format(i)
            tipo = data2.check_preco(q)
            if tipo == 'Bebida':
                self.dfbar.at[index, 'Qtd.'] = int(self.itens['{}'.format(i)])
                self.dfbar.at[index, 'Item'] = str(i)
                index = index + 1
            else:
                self.dfcozinha.at[index, 'Qtd.'] = int(self.itens['{}'.format(i)])
                self.dfcozinha.at[index, 'Item'] = str(i)
                index = index + 1
        return
    def imprimir_comanda(self):
        if self.dfbar.empty:
            pass
        else:
            dfbar = self.dfbar.to_string(index=False)
            print('='*26)
            print('PB - BAR')
            print('='*26)
            input("{}\n\n\n\nImprimir Comanda?(y/n)\n".format(dfbar))
        if self.dfcozinha.empty:
            pass
        else:
            dfcozinha = self.dfcozinha.to_string(index=False)
            print('='*26)
            print('PB - COZINHA')
            print('='*26)
            input("{}\n\n\n\nImprimir Comanda?(y/n)\n".format(dfcozinha))
class mesa:
    def __init__(self, titulo, responsavel, conta=None,pago=None, status=None):
        self.responsavel = responsavel
        self.titulo = titulo
        self.cardapio = data.exibir_cardapio(data.q1)
        self.status = status
        self.pago= pago
        self.pago[0] = float(self.pago[0])
        self.pago[1] = float(self.pago[1])
        self.pago[2] = float(self.pago[2])
        if conta == None:
            self.conta = data2.ID_venda() + 1
            data2.criar_conta(id=self.conta, nome=self.responsavel)
        else:
            self.conta = conta    
    def adicionar_conta(self):
        data.add_item_conta(id=self.conta)
        return
