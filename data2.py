import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import data
#HOST
host ='HOST MYSQL'
user = 'USER'
passwd_mysql = 'pass'
def ID_venda():
    try:    
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor= con.cursor()
        cursor.execute("select MAX(ID_venda) from venda;")
        id = cursor.fetchone()
        id = id[0]
        con.commit()
    except mysql.connector.Error as e:
        pass
    finally:
        if con.is_connected():
            con.close()
            if id == None:
                return 0
            else:
                return id
def ID_Produto(nome):
    n = """'{}'""".format(nome)
    q = """select ID_produto from produtos where Nome = {};""".format(n)
    try:    
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor= con.cursor()
        cursor.execute(q)
        x = cursor.fetchone()
    except mysql.connector.Error as e:
        input(e)
    finally:
        if con.is_connected():
            con.close()
    return x[0]
def criar_conta(nome, id):
#inserir venda
    data1 = datetime.today().strftime('%Y-%m-%d')
    data2 = data1.replace('-','')
    q5 ="""insert into venda(Nome,Data_venda,Tipo,Total,Total_pago,Dinheiro,Cartao,Pix) values ('{}',{},{},{},{},{},{},{});""".format(nome,data2,"""'Aberto'""",0,0,0,0,0)
#criar tabela da conta
    q6 = """create table conta{}(
        ID_venda smallint,
        Dinheiro decimal(5,2),
        Cartao decimal(5,2),
        Pix decimal(5,2),
        ID_produto smallint,
        Qtd smallint unsigned,
        PrecoVendido decimal(5,2));""".format(id)
    q9 = """insert into conta{}(ID_venda,Dinheiro,Pix,Cartao) values({},{},{},{});""".format(id,id,0,0,0)
    try:
        querys = [q5,q6,q9]
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor = con.cursor(buffered=True)
        for i in querys:
            cursor.execute(i)
        con.commit()
    except mysql.connector.Error:
        pass
    finally:
        if con.is_connected():
            con.close()
            return
def preencher_conta(idconta=str,idproduto=int,qtd=int,preco=float):
    q9 = """INSERT INTO conta{}(ID_produto,Qtd,PrecoVendido) VALUES ({},{},{});""".format(str(idconta),str(idproduto),str(qtd),str(preco))
    data.exec_query(q9)
def check_qtd(q,valor):
    try:    
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor= con.cursor()
        cursor.execute(q)
        id = cursor.fetchone()
        id = id[0]
        con.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        if con.is_connected():
            con.close()
    if id - valor < 0:
        return True, id
    else:
        return False, id
def get_pagamentos(id):
    query = """select Dinheiro,Cartao,Pix from conta{} WHERE ID_venda ={};""".format(id,id)
    try:
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor= con.cursor()
        cursor.execute(query)
        id = cursor.fetchone()
        con.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        if con.is_connected():
            con.close()
    return id
