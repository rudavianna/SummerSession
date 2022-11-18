import curses
from curses import wrapper
from curses.textpad import Textbox
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import warnings
import emoji
warnings.filterwarnings('ignore')
#SET MYSQL
host ='HOST MYSQL'
user = 'USER'
passwd_mysql = 'pass'
def enter_is_terminate(x):
    if x in [10,459]:
        return 7
    if x in [49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 33, 64, 35, 36, 37,61, 94, 38, 42, 40, 41, 95, 43,96,530,460,458,463,464,
    46,44,47,92,124,63,465,62,60]:
        return 9
    else:
        return x      
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
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except mysql.connector.Error as e:
        input(e)
    finally:
        if con.is_connected():
            con.close()
def manage(stdscr):
    s = stdscr.getmaxyx()
    last_row =s[0] - 2
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLACK)
    blackout =curses.color_pair(11)
    magenblack = curses.color_pair(10)
    greenblack = curses.color_pair(9)
    whiteblack = curses.color_pair(7)
    blackred = curses.color_pair(5)
    blackblue = curses.color_pair(4)
    blackcyan = curses.color_pair(1)
    blackyellow = curses.color_pair(2)
    #Estoque
    q1 = """select ID_produto,Nome,Qtd,Preco,Situacao from produtos order by Qtd asc;"""
    q2 = """select ID_produto,Nome,Qtd,Preco,Situacao from produtos WHERE Tipo = 'Bebida' order by Qtd;"""
    q3 = """select ID_produto,Nome,Qtd,Preco,Situacao from produtos WHERE Tipo = 'Comida' order by Qtd ;"""
    q4 = """select ID_produto,Nome,Qtd,Preco,Situacao from produtos WHERE Qtd = 0 order by Nome;"""
    q5 = """update produtos Set Situacao = '{}' WHERE ID_produto = {}"""
    q6 = """update produtos Set Preco = '{}' WHERE ID_produto = {}"""
    q7 = """update produtos Set Qtd = '{}' WHERE ID_produto = {}"""
    q8 = """insert into produtos(Nome, Qtd, Tipo, Preco) values ('{}',{},'{}',{});"""
    def estrutura(valor=None):
        if valor == None:
            valor = 1
        stdscr.clear()
        stdscr.addstr(valor,0,emoji.emojize(':anchor: Pontal do Bainema:anchor:'),blackcyan|curses.A_BOLD)
        return
    def menu_principal():
        options=[emoji.emojize('Estoque :package:'), emoji.emojize('Vendas(em breve):heavy_dollar_sign:')]
        key = ''
        c = True
        while key not in [10,459]:
            curses.curs_set(0)
            estrutura(0)
            for i in options:
                if c  == True:
                    stdscr.addstr(2,1,'{}'.format(options[0]), whiteblack|curses.A_BOLD)
                    stdscr.addstr(4,1,'{}'.format(options[1]), blackout|curses.A_BOLD)
                else:
                    stdscr.addstr(2,1,'{}'.format(options[0]), blackout|curses.A_BOLD)
                    stdscr.addstr(4,1,'{}'.format(options[1]), whiteblack|curses.A_BOLD)
            stdscr.refresh()
            key = stdscr.getch()
            if key == 258:
                c = False
            if key == 259:
                c = True
            if key == 27:
                return None
        return c
    def menu_estoque():
        stdscr.clear()
        stdscr.refresh()
        s = stdscr.getmaxyx()
        options = [
        emoji.emojize(':package: Estoque Completo'),
        emoji.emojize(':tropical_drink: Estoque de Bebidas'),
        emoji.emojize(':shrimp: Estoque de Comida'),
        emoji.emojize(':pencil: Cadastrar Item'),
        emoji.emojize(':no_entry: Itens Esgotados'),]
        key = ''
        count = 0
        while key not in [10,459]:
            pos = 2
            estrutura(0)
            for id, i in enumerate(options):
                if id == count:
                    stdscr.addstr(pos,0,'{}'.format(i), whiteblack|curses.A_BOLD)
                    pos += 2
                if id != count:
                    stdscr.addstr(pos,0,'{}'.format(i), blackout|curses.A_BOLD)
                    pos +=2
            stdscr.refresh()
            key = stdscr.getch()
            if key == 258:
                count += 1
            if key == 259:
                count -= 1
            if key == 27:
                break
            if key in [10,459]:
                if count == 0:
                    return (q1, 'ESTOQUE COMPLETO')
                if count ==1:
                    return (q2, 'BEBIDAS')
                if count ==2:
                    return (q3, 'COMIDA') 
                if count ==3:
                    key2 = ''
                    options2 = [emoji.emojize(':green_salad: Comida'),
                    emoji.emojize(':bubble_tea: Bebida')
                    ]
                    count2 = 0
                    while key2 not in [10,459]:
                        stdscr.addstr(0,23,'{}'.format(emoji.emojize(':anchor: Selecione a Categoria')), blackblue|curses.A_BOLD)
                        pos = 2
                        for id, i in enumerate(options2):
                            if id == count2:
                                stdscr.addstr(pos,26,'{}'.format(i), whiteblack|curses.A_BOLD)
                                pos+=2
                            if id != count2:
                                stdscr.addstr(pos,26,'{}'.format(i), blackout|curses.A_BOLD)
                                pos+=2
                        stdscr.refresh()
                        key2 = stdscr.getch()
                        if key2 == 258:
                            count2 +=1
                        if key2== 259:
                            count2 -=1
                        if key2 == 27:
                            stdscr.clear()
                            stdscr.refresh()
                            key = ''
                            break
                        if count2 < 0:
                            count2 = 0
                        if count2 > 1:
                            count2 = 1
                        if key2 in [10,459]:
                            if count2 == 0:
                                tipo = 'Comida'
                            if count2 == 1:
                                tipo = 'Bebida'
                            stdscr.addstr(0,49,'{}'.format(emoji.emojize(':anchor: Digite o Nome do Item')), blackred|curses.A_BOLD)
                            win = curses.newwin(1,25,2,52)
                            box = Textbox(win)
                            stdscr.refresh()
                            curses.curs_set(1)
                            produto = box.edit(enter_is_terminate).title()
                            while produto == '':
                                win.clear()
                                stdscr.addstr(6,52,'Digite um Nome Valido {}'.format(produto), blackred)
                                stdscr.refresh()
                                produto = box.edit(enter_is_terminate).title()
                            curses.curs_set(0)
                            produto = produto.replace('\n','')
                            key3 = ''
                            count3 = 0
                            window =curses.newwin(4,25,0,75)
                            stdscr.nodelay(True)
                            while key3 not in [10,459]:
                                window.addstr(0,0,'{}'.format(emoji.emojize(':anchor: Selecione a Quantidade ')), magenblack)
                                window.addstr(2,3,'{}'.format(count3), magenblack|curses.A_BOLD)
                                stdscr.refresh()
                                window.refresh()
                                try:
                                    key3 = stdscr.getch()
                                except:
                                    key3 = None
                                if key3 == 258:
                                    count3 -= 1
                                if key3 == 259:
                                    count3 += 1
                                if key3 == 27:
                                    stdscr.nodelay(False)
                                    win.clear()
                                    win.refresh()
                                    window.clear()
                                    window.refresh()
                                    stdscr.refresh()
                                    key2 = ''
                                    break
                                if count3 < 0:
                                    count3 = 0
                                if key3 in [10,459]:
                                    qtd = count3
                                    key4 = ''
                                    window3 = curses.newwin(4,25,4,75)
                                    count4 = 0
                                    while key4 not in [10,459]:
                                        window3.addstr(0,0,'{}'.format(emoji.emojize(':anchor: Selecione o Preco ')), greenblack)
                                        window3.addstr(2,3,'R${}'.format(count4), greenblack|curses.A_BOLD)
                                        stdscr.refresh()
                                        window3.refresh()
                                        try:
                                            key4 = stdscr.getch()
                                        except:
                                            key4 =None
                                        if key4 == 258:
                                            count4 -= 0.5
                                        if key4 == 259:
                                            count4 += 0.5
                                        if key4 == 27:
                                            stdscr.nodelay(False)
                                            key3 = ''
                                            window3.clear()
                                            window3.refresh()
                                            stdscr.refresh()
                                            break
                                        if count4 < 0:
                                            count4 = 0
                                        if key4 in [10,459]:
                                            stdscr.nodelay(False)
                                            window3.clear()
                                            window3.refresh()
                                            key5 = ''
                                            count5 = 0
                                            windowconfirm = curses.newwin(4,21,10,75)
                                            while key5 not in [10,459]:
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,'{}'.format(emoji.emojize(':warning: Confirma Operacao?')), blackyellow)
                                                if count5 == 0:
                                                    windowconfirm.addstr(1,1,'{}'.format(emoji.emojize('Sim')), whiteblack|curses.A_BOLD)
                                                    windowconfirm.addstr(2,1,'{}'.format(emoji.emojize('Nao')), blackout|curses.A_BOLD)
                                                if count5 == 1:
                                                    windowconfirm.addstr(1,1,'{}'.format(emoji.emojize('Sim')), blackout|curses.A_BOLD)
                                                    windowconfirm.addstr(2,1,'{}'.format(emoji.emojize('Nao')), whiteblack|curses.A_BOLD)
                                                windowconfirm.refresh()
                                                key5 = stdscr.getch()
                                                if key5 == 258:
                                                    count5 +=1
                                                if key5 == 259:
                                                    count5 -=1
                                                if key5 == 27:
                                                    windowconfirm.clear()
                                                    windowconfirm.refresh()
                                                    key4 = ''
                                                    break
                                                if count5 > 1:
                                                    count5 = 0
                                                if count5 < 0:
                                                    count5 = 1
                                                if key5 in [10,459]:
                                                    if count5 == 0:    
                                                        preco = count4
                                                        exec_query(q8.format(produto,qtd,tipo,preco))
                                                        windowconfirm.clear()
                                                        windowconfirm.refresh()
                                                        windowconfirm.addstr(0,0,emoji.emojize(':check_mark_button:Produto Cadastrado'),greenblack|curses.A_BOLD)
                                                        windowconfirm.refresh()
                                                        stdscr.getch()
                                                        stdscr.clear()
                                                        stdscr.refresh()
                                                        key = ''
                                                    if count5 == 1:
                                                        windowconfirm.clear()
                                                        windowconfirm.refresh()
                                                        windowconfirm.addstr(0,0,emoji.emojize('Registro Cancelado:red_exclamation_mark:'),blackred|curses.A_BOLD)
                                                        windowconfirm.refresh()
                                                        stdscr.getch()
                                                        stdscr.clear()
                                                        stdscr.refresh()
                                                        key = ''
                if count ==4:
                    return q4, 'ITENS ESOTADOS'
            if count > 4:
                count =0
            if count < 0:
                count = 4
    def tabela_pad(tuple):
        if tuple == None:
            return False
        else:
            pass
        stdscr.clear()
        key = ''
        count =0
        while key not in [10,459]:
            tabela = get_tabela_mysql(tuple[0])
            if tabela.empty == True:
               stdscr.addstr(0,25,emoji.emojize('Nao ha Registros:red_exclamation_mark:'),blackred)
               stdscr.refresh()
               stdscr.getch()
               return None
            rows = tabela.values.tolist()
            posy = 3
            posx = 0
            estrutura(0)
            stdscr.addstr(2,(s[1]//2-10), '{}'.format(tuple[1]), whiteblack| curses.A_BOLD)
            for id, i in enumerate(rows):
                if posy == last_row -1:
                    posx = posx + 42
                    posy = 3
                if i[2] < 10:
                    color2 = blackred
                    color1 = blackred
                if i[2] > 40:
                    color2 = greenblack
                    color1 =greenblack
                if i[2] >=10 and i[2]<=40:
                    color1 = blackyellow
                    color2 = blackyellow
                if i[4] == 'Ativo':
                    i[4] = emoji.emojize(':small_blue_diamond:')
                    pass
                if i[4] == 'Inativo':
                    color2 = blackred
                    color1 = blackred
                    i[4] = emoji.emojize(':no_entry:')
                if posy <= last_row -1 and posx == 0:    
                    if id == count:
                        stdscr.addstr(posy,0,'{} {} R${} ({}) '.format(i[4],i[1],i[3],i[2]),color2| curses.A_BOLD| curses.A_REVERSE)
                        posy= posy +1
                    if id != count:
                        stdscr.addstr(posy,0,'{} {} R${} ({}) '.format(i[4],i[1],i[3],i[2]),color1| curses.A_BOLD)
                        posy= posy +1
                else:
                    if id == count:
                        stdscr.addstr(posy,posx,'{} {} R${} ({}) '.format(i[4],i[1],i[3],i[2]),color2| curses.A_BOLD|curses.A_REVERSE)
                        posy= posy +1
                    if id != count:
                        stdscr.addstr(posy,posx,'{} {} R${} ({}) '.format(i[4],i[1],i[3],i[2]),color1| curses.A_BOLD)
                        posy= posy +1
            stdscr.refresh()
            try:
                key = stdscr.getch()
            except:
                key = None
            if key == 258:
                count +=1
            if key == 259:
                count -=1
            if key == 261:
                count = count - last_row -4
            if key == 260:
                count = count + int(last_row - 4)
            if key == 32:
                if tabela.at[tabela.index[count], 'Situacao'] == 'Inativo':
                    exec_query(q5.format('Ativo',tabela.at[tabela.index[count],'ID_produto']))
                else:
                    exec_query(q5.format('Inativo',tabela.at[tabela.index[count],'ID_produto']))
            if key == 27:
                tabela_pad(menu_estoque())
                return None
            if key in [10,459]:
                options = [
                    'Alterar Quantidade',
                    'Alterar Preco'
                ]
                key2 = ''
                count2 = 0
                z = s[1] - 22
                while key2 not in [10,459]:
                    stdscr.addstr(0,z,'{}'.format(emoji.emojize(':anchor:Menu')), blackblue|curses.A_BOLD)
                    pos = 1
                    for id, i in enumerate(options):
                        if id != count2:
                            stdscr.addstr(pos,z,'{}'.format(i), blackout|curses.A_BOLD)
                            pos+=1
                        if id == count2:
                            stdscr.addstr(pos,z,'{}'.format(i), whiteblack|curses.A_BOLD)
                            pos+=1
                    stdscr.refresh()
                    key2 = stdscr.getch()
                    if key2 == 258:
                        count2 +=1
                    if key2 == 259:
                        count2 -=1
                    if key2 == 27:
                        key = ''
                        break
                    if count2 > 1:
                        count2 = 1
                    if count2 < 0:
                        count2 = 0
                    if key2 in [10,459]:
                        stdscr.refresh()
                        key3 = ''
                        preco = float(tabela.at[tabela.index[count], 'Preco'])
                        qtd = int(tabela.at[tabela.index[count], 'Qtd'])
                        nome = tabela.at[tabela.index[count], 'Nome']
                        window = curses.newwin(4,30,s[0]//4,s[1]-30)
                        if count2 == 1:
                            stdscr.nodelay(True)
                            while key3 not in [10,459]:
                                window.clear()
                                window.addstr(0,0,'{}'.format(emoji.emojize(':anchor: Selecione o Preco ')), magenblack|curses.A_BOLD)
                                window.addstr(2,0,'{}  R${}'.format(nome, preco), whiteblack|curses.A_BOLD)
                                window.refresh()
                                stdscr.refresh()
                                try:
                                    key3 = stdscr.getch()
                                except:
                                    key3 = None
                                if key3 == 258:
                                    preco -= 0.5
                                if key3 == 259:
                                    preco += 0.5
                                if key3 == 27:
                                    stdscr.nodelay(False)
                                    window.clear()
                                    window.refresh()
                                    key2 = ''
                                    break
                                if key3 in [10,459]:
                                    stdscr.nodelay(False)
                                    key5 = ''
                                    count5 = 0
                                    x =s[1] - 30
                                    y = (s[0]//4) + 5
                                    windowconfirm = curses.newwin(4,25,y,x)
                                    while key5 not in [10,459]:
                                        windowconfirm.clear()
                                        windowconfirm.refresh()
                                        windowconfirm.addstr(0,0,'{}'.format(emoji.emojize(':warning: Confirma Operacao?')), blackyellow)
                                        if count5 == 0:
                                            windowconfirm.addstr(1,0,'{}'.format(emoji.emojize('Sim')), whiteblack|curses.A_BOLD)
                                            windowconfirm.addstr(2,0,'{}'.format(emoji.emojize('Nao')), blackout|curses.A_BOLD)
                                        if count5 == 1:
                                            windowconfirm.addstr(1,0,'{}'.format(emoji.emojize('Sim')), blackout|curses.A_BOLD)
                                            windowconfirm.addstr(2,0,'{}'.format(emoji.emojize('Nao')), whiteblack|curses.A_BOLD)
                                        windowconfirm.refresh()
                                        key5 = stdscr.getch()
                                        if key5 == 258:
                                            count5 +=1
                                        if key5 == 259:
                                            count5 -=1
                                        if key5 == 27:
                                            windowconfirm.clear()
                                            windowconfirm.refresh()
                                            key = ''
                                            break
                                        if count5 > 1:
                                            count5 = 0
                                        if count5 < 0:
                                            count5 = 1
                                        if key5 in [10,459]:
                                            if count5 == 0:
                                                key2 = 10
                                                key = ''
                                                exec_query(q6.format(preco,tabela.at[tabela.index[count],'ID_produto']))
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,emoji.emojize(':check_mark_button: Operacao Concluida'), greenblack)
                                                windowconfirm.refresh()
                                                stdscr.getch()
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                break
                                            if count5 == 1:
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,emoji.emojize(':red_exclamation_mark: Operacao Cancelada'))
                                                windowconfirm.refresh()
                                                stdscr.getch()
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                break
                                if preco < 0:
                                    preco = 0
                        if count2 == 0:
                            stdscr.nodelay(True)
                            while key3 not in [10,459]:
                                window.clear()
                                window.addstr(1,0,'{}'.format(emoji.emojize(':anchor: Selecione a Quantidade ')), magenblack|curses.A_BOLD)
                                window.addstr(3,1,'{} {}'.format(nome, qtd), whiteblack|curses.A_BOLD)
                                window.refresh()
                                try:
                                    key3 = stdscr.getch() 
                                except:
                                    key3 = None
                                if key3 == 258:
                                    qtd = qtd - 1
                                if key3 == 259:
                                    qtd = qtd + 1
                                if key3 == 27:
                                    stdscr.nodelay(False)
                                    window.clear()
                                    window.refresh()
                                    key2 = ''
                                    break
                                if key3 in [10,459]:
                                    stdscr.nodelay(False)
                                    key5 = ''
                                    count5 = 0
                                    x =s[1] - 30
                                    y = (s[0]//4) + 5
                                    windowconfirm = curses.newwin(4,25,y,x)
                                    while key5 not in [10,459]:
                                        windowconfirm.clear()
                                        windowconfirm.refresh()
                                        windowconfirm.addstr(0,0,'{}'.format(emoji.emojize(':warning: Confirma Operacao?')), blackyellow)
                                        if count5 == 0:
                                            windowconfirm.addstr(1,0,'{}'.format(emoji.emojize('Sim')), whiteblack|curses.A_BOLD)
                                            windowconfirm.addstr(2,0,'{}'.format(emoji.emojize('Nao')), blackout|curses.A_BOLD)
                                        if count5 == 1:
                                            windowconfirm.addstr(1,0,'{}'.format(emoji.emojize('Sim')), blackout|curses.A_BOLD)
                                            windowconfirm.addstr(2,0,'{}'.format(emoji.emojize('Nao')), whiteblack|curses.A_BOLD)
                                        windowconfirm.refresh()
                                        key5 = stdscr.getch()
                                        if key5 == 258:
                                            count5 +=1
                                        if key5 == 259:
                                            count5 -=1
                                        if key5 == 27:
                                            windowconfirm.clear()
                                            windowconfirm.refresh()
                                            key = ''
                                            break
                                        if count5 > 1:
                                            count5 = 0
                                        if count5 < 0:
                                            count5 = 1
                                        if key5 in [10,459]:
                                            if count5 == 0:
                                                key2 = 10
                                                key = ''
                                                exec_query(q7.format(qtd,tabela.at[tabela.index[count],'ID_produto']))
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,emoji.emojize(':check_mark_button: Operacao Concluida'), greenblack)
                                                windowconfirm.refresh()
                                                stdscr.getch()
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                break
                                            if count5 == 1:
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,emoji.emojize(':red_exclamation_mark: Operacao Cancelada'))
                                                windowconfirm.refresh()
                                                stdscr.getch()
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                break
                                if qtd < 0:
                                    qtd = 0            
            if count > len(rows) -1:
                count = 0
            if count < 0:
                count = len(rows) -1
    while True:
        program = menu_principal()                                            
        if program == True:
            x = tabela_pad(menu_estoque())
            if x == None:
                continue
        else:
            return program       
wrapper(manage)

