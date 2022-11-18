from fileinput import close
import busy
import curses
from curses import wrapper
import pandas as pd
import numpy as np
import mysql.connector
import emoji
import warnings
from mysql.connector import Error
warnings.filterwarnings('ignore')
#SET MYSQL
host ='HOST MYSQL'
user = 'USER'
passwd_mysql = 'pass'
#cardapio referencia(completo)
q1 = 'select ID_produto, Nome, Preco, Qtd from produtos order by ID_produto ASC'
#cardapio disponiveis completo
q2 = """select ID_produto, Nome, Preco, Qtd from produtos where Qtd > 0 and Situacao = 'Ativo' order by Preco ASC;"""
#cardapio bebidas
q3 = """select ID_produto, Nome, Preco, Qtd from produtos where Tipo = 'Bebida' and Qtd > 0 and Situacao = 'Ativo' order by Nome ASC;"""
#cardapio comidas
q4 = """select ID_produto, Nome, Preco, Qtd from produtos where Tipo = 'Comida' and Qtd > 0 and Situacao = 'Ativo' order by Nome ASC;"""
def salvar_mesa(obj, file):
    file = open(file, 'a')
    for i in obj.__dict__:
        if i == 'cardapio':
            continue
        else:
            item = str(obj.__dict__[i])
            file.writelines('{}\n'.format(item))    
    file.writelines('{}\n'.format('#'*30))
    file.close()
def importar_mesas(file, dict, lst):
    file = open(file, 'r')
    mesas = file.readlines()
    mesa = []
    for i in mesas:
        i = i.rstrip('\n')
        mesa.append(i)
        if len(mesa) == 6:
            for i in mesa:
                i.replace('','')
            mesa[3]=mesa[3].replace('[','')
            mesa[3]=mesa[3].replace(']','')
            mesa[3]=mesa[3].replace(' ','')
            mesa[3]=mesa[3].replace("'",'')
            mesa[3]=mesa[3].split(',') 
            if busy.check_titulo(str(mesa[1])) == False:
                    lst.append(str(mesa[1]))
                    busy.mesas_disponiveis.remove(str(mesa[1]))
                    dict['{}'.format(str(mesa[1]))] = busy.mesa(titulo=str(mesa[1]), responsavel=mesa[0],status=bool(mesa[2]),pago=mesa[3],conta=mesa[4])
                    mesa = []
            else:
                busy.militantes.append(str(mesa[1]))
                dict['{}'.format(str(mesa[1]))] = busy.mesa(titulo=str(mesa[1]), responsavel=mesa[0],status=bool(mesa[2]),pago=mesa[3],conta=mesa[4])
                mesa = []                   
def backup_mesas(dict, file):
    f = open(file, 'w')
    f.write('')
    f.close()
    for i in dict:
        salvar_mesa(dict[i], 'mesas.txt')
    return
def busy_table():
    table = busy.table_mesas(busy.mesas_ocupadas1, 'Mesas')
    clientes = []
    for i in busy.mesas_ocupadas1:
        clientes.append(busy.mesas_ocupadas['{}'.format(i)].responsavel)
    table['Cliente'] = clientes
    return table
def client_table():
    table = busy.table_mesas(busy.militantes, 'ID')
    clientes = []
    for i in busy.militantes:
        clientes.append(busy.mesas_ocupadas['{}'.format(i)].responsavel)
    table['Cliente'] = clientes
    return table
    return
def exibir_cardapio(q):
    try:
        con = mysql.connector.connect(host=host, database='bainema', user=user, password=passwd_mysql)
        cardapio = pd.read_sql(q, con = con)
        
        cardapio.rename(columns={'Nome': 'Item'}, inplace=True)    
    except Error as e:
        print(e)
    finally:
        if con.is_connected():
            con.close()
    return cardapio
def add_item_conta(id):
    conta = id
    def add_menu(stdscr):
        curses.start_color()
        curses.init_color(46,1000,444,300)
        s = stdscr.getmaxyx()
        last_row = s[0] - 1
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(5,46, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        greenblack = curses.color_pair(7)
        whitegreen = curses.color_pair(6)
        blackout =curses.color_pair(3)
        whitered = curses.color_pair(4)
        blackyellow = curses.color_pair(2)
        blackred = curses.color_pair(1)
        blackorange = curses.color_pair(5)
        def estrutura(valor=None):
            if valor == None:
                valor = 1
            stdscr.addstr(valor,0,emoji.emojize(':bright_button: Pontal do Bainema :bright_button: '),blackorange)
            return
        count = 0
        key = ''
        option = [emoji.emojize(':crab: Para Comer'),
        emoji.emojize(':tropical_drink: Para Beber'),
        emoji.emojize(':clipboard: Cardapio Completo')]
        while True:
            while key not in [10,459]:
                stdscr.clear()
                stdscr.refresh()
                estrutura(0)
                pos = 2
                for id, i in enumerate(option):
                    if count == id:
                        stdscr.addstr(pos,0,'{}'.format(i),blackred|curses.A_BOLD)
                        pos = pos + 2
                    else:
                        stdscr.addstr(pos,1,'{}'.format(i), blackout| curses.A_BOLD)
                        pos = pos + 2
                stdscr.refresh()
                key = stdscr.getch()
                if key == 258:
                    count = count + 1
                elif key == 259:
                    count = count- 1
                elif key == 27:
                    return
                if count > 2:
                    count = 0
                if count < 0:
                    count = 2
            if count == 0:
                df = exibir_cardapio(q4)
            if count == 1:
                df = exibir_cardapio(q3)
            if count == 2:
                df = exibir_cardapio(q2)
            maxid = int(df.index.max())
            count = 0
            key2 = ''
            while key2 not in [10,459]:
                posy = int(2)
                posx = int(0)
                stdscr.clear()
                estrutura(0)
                for id ,i in enumerate(df.values):
                    if posy == last_row:
                        posx = posx + 27
                        posy = 2
                    if posy <= last_row -1 and posx == 0:
                        if count == id:
                            stdscr.addstr(posy,posx,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), blackyellow|curses.A_BOLD)
                            stdscr.addstr(posy,posx+20,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), blackyellow|curses.A_BOLD)
                            posy = posy + 1
                        else:
                            stdscr.addstr(posy,posx+1,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), blackout|curses.A_BOLD)
                            stdscr.addstr(posy,posx+21,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), blackout|curses.A_BOLD)
                            posy = posy + 1
                    else:
                        if count == id:
                            stdscr.addstr(posy,posx,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), blackyellow|curses.A_BOLD)
                            stdscr.addstr(posy,posx+20,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), blackyellow|curses.A_BOLD)
                            posy = posy + 1
                        else:
                            stdscr.addstr(posy,posx+1,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), blackout|curses.A_BOLD)
                            stdscr.addstr(posy,posx+21,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), blackout|curses.A_BOLD)
                            posy = posy + 1
                stdscr.refresh()
                key2 = stdscr.getch()
                if key2 in [10,459]:
                    count2= 0
                    key3 = ''
                    while key3 not in [10,459]:
                        if count2 < 0:
                            count2 = 0
                        window = curses.newwin(4,25,0,s[1]-25)
                        window.addstr(1,0,'{}'.format(emoji.emojize(':anchor: Selecione Quantidade')), blackyellow|curses.A_BOLD)
                        window.addstr(3,0,'{}'.format(count2), blackyellow| curses.A_BOLD|curses.A_REVERSE)
                        window.refresh()
                        stdscr.refresh()
                        key3 = stdscr.getch()
                        if key3 == 258:
                            count2 = count2 -1
                        if key3 == 259:
                            count2 =count2 + 1
                        if key3 in [10,459]:
                            count3 = 0
                            key4 = ''
                            while key4 not in [10,459]:
                                window3 = curses.newwin(4,22,6,s[1]-25)
                                if count3 == 0:
                                    window3.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                    window3.addstr(1,3,emoji.emojize('Sim'),whitegreen|curses.A_REVERSE)
                                    window3.addstr(2,3,emoji.emojize('Nao'),blackout|curses.A_BOLD)
                                if count3 == 1:
                                    window3.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                    window3.addstr(1,3,emoji.emojize('Sim'),blackout|curses.A_BOLD)
                                    window3.addstr(2,3,emoji.emojize('Nao'),whitered|curses.A_REVERSE)
                                window3.refresh()
                                key4 = stdscr.getch()
                                if key4 == 27:
                                    window3.clear()
                                    window3.refresh()
                                    key3 = ''
                                    break
                                if key4 == 258:
                                    count3 -=1
                                if key4 == 259:
                                    count3 += 1
                                if count3 < 0:
                                    count3 = 1
                                if count3 > 1:
                                    count3 = 0
                                if key4 in [10,459]:
                                    if count3 == 0:
                                        idproduto = int(df.at[df.index[count], 'ID_produto'])
                                        preco = df.at[df.index[count], 'Preco']
                                        if check_if_exists_in_account(conta=conta,idproduto=idproduto) == True:
                                            q = """INSERT INTO conta{}(ID_produto,Qtd,PrecoVendido) VALUES({},{},{})""".format(conta,idproduto,count2,preco)
                                        else:
                                            q = """update conta{} set Qtd = Qtd + {} WHERE ID_produto = {};""".format(conta,count2,idproduto)
                                        qe = """update produtos set Qtd = Qtd - {} WHERE ID_produto = {};""".format(count2,idproduto)
                                        exec_query(q)
                                        exec_query(qe)
                                        window3.clear()
                                        window.refresh()
                                        window3.addstr(0,3,'Operacao Concluida',greenblack|curses.A_BOLD)
                                        window3.refresh()
                                        stdscr.getch()
                                        key = ''
                                        break
                                    elif count3 ==1:
                                        return
                        if key3 == 27:
                            window.clear()
                            window.refresh()
                            key2 = ''
                            stdscr.refresh()
                            break
                        if count2 >= df.at[df.index[count], 'Qtd']:
                            count2 =  df.at[df.index[count], 'Qtd']
                if key2 == 258:
                    count = count + 1
                elif key2 == 259:
                    count = count- 1
                if key2 == 27:
                    key = ''
                    count = 0
                    break 
                if key2 == 261:
                    count = count + last_row -2
                if key2 == 260 :
                    count = count - int(last_row - 2)
                if count > maxid:
                    count = 0
                if count < 0:
                    count = maxid
    wrapper(add_menu)
    return
def get_tabela_mysql(q):
    try:
        con = mysql.connector.connect(host=host, database='bainema', user=user, password=passwd_mysql)
        con.commit()
        tabela = pd.read_sql(q, con = con)
    except Error as e:
        print(e)
    finally:
        if con.is_connected():
            con.close()
    return tabela
def exec_query(query):
    try:
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        con.commit()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except mysql.connector.Error:
        return True
    finally:
        if con.is_connected():
            con.close()
            return  False
def check_if_exists_in_account(conta, idproduto):
    q = """SELECT Qtd from conta{} WHERE ID_produto = {};""".format(conta,idproduto)
    try:    
        con = mysql.connector.connect(host=host, database='bainema',user=user, password=passwd_mysql)
        cursor= con.cursor()
        con.commit()
        cursor.execute(q)
        id = cursor.fetchone()
        id = id[0]
        con.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        if con.is_connected():
            con.close()
            if id == None:
                return True
            else:
                return False
