import curses
from curses import wrapper
from curses.textpad import Textbox
import pandas as pd
import numpy as np
import emoji
import threading
import re
import data
import random
import busy
import newmenuindividual
import syncronyze
data.importar_mesas(file='mesas.txt',dict=busy.mesas_ocupadas,lst=busy.mesas_ocupadas1)
def enter_is_terminate(x):
    if x in [10,459]:
        return 7
    if x in [49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 33, 64, 35, 36, 37,61, 94, 38, 42, 40, 41, 95, 43,96,530,460,458,463,464,
    46,44,47,92,124,63,465,62,60]:
        return 9
    else:
        return x 
def menu_principal():
    def menu(stdscr):
        curses.start_color()
        curses. init_color(49,0,800,1000)
        curses.init_color(50,1000,444,300)
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(11,49, curses.COLOR_BLACK)
        curses.init_pair(12,50, curses.COLOR_BLACK)
        bluebaby = curses.color_pair(11)
        blackorange = curses.color_pair(12)
        grennblack = curses.color_pair(8)
        redblack= curses.color_pair(7)
        blackout =curses.color_pair(3)
        blackcyan = curses.color_pair(4)
        blackyellow = curses.color_pair(2)
        whiteblack = curses.color_pair(1)
        blackblue = curses.color_pair(5)    
        options =[
            emoji.emojize(':pencil: Nova Conta'),
            emoji.emojize(':page_with_curl: Acessar Contas'),
            emoji.emojize(':no_entry: Mesas Ocupadas'),
            emoji.emojize(':green_circle: Mesas Disponiveis'),
            emoji.emojize(':clipboard: Exibir Cardapio'),
            emoji.emojize(':stop_sign: Finalizar Sessao')
        ]
        count = 0
        key = ''
        def estrutura(valorx=None, valory=None):
            if valorx == None:
                valorx = 0
            if valory == None:
                valory = 1
            stdscr.addstr(valory,valorx,emoji.emojize(':sailboat: Pontal do Bainema'),blackblue|curses.A_BOLD)
            return 
        while key not in [10,459]:
            stdscr.clear()
            stdscr.refresh()
            estrutura(0,0)
            pos =2
            for id, i in enumerate(options):
                if id != count:
                    stdscr.addstr(pos,1,'{}'.format(i), blackout|curses.A_BOLD)
                    pos = pos +2
                if id == count:
                    stdscr.addstr(pos,0,'{}'.format(i), whiteblack|curses.A_BOLD)
                    pos = pos +2
            stdscr.refresh()
            key = stdscr.getch()
            if key == 258:
                count +=1
            if key == 259:
                count -=1
            if count > len(options)-1:
                count = 0
            if count < 0:
                count = len(options) -1
            if key in [10,459]:
                #Nova Conta
                if count == 0:
                    key2 = ''
                    count2 = 0
                    options2 = [emoji.emojize(':chair: Mesa'),emoji.emojize(':woman_dancing: Balcao')]
                    window = curses.newwin(5,22,0,23)
                    stdscr.refresh()
                    while key2 not in [10,459]:
                        stdscr.refresh()
                        pos = 2
                        window.addstr(0,0,emoji.emojize(':anchor: Selecione uma Opcao'),bluebaby)
                        for id, i in enumerate(options2):
                            if id == count2:
                                window.addstr(pos,0,'{}'.format(i), whiteblack|curses.A_BOLD)
                                pos +=2
                            if id != count2:
                                window.addstr(pos,0,'{}'.format(i), blackout|curses.A_BOLD)
                                pos +=2
                        window.refresh()
                        stdscr.refresh()
                        key2 = stdscr.getch()
                        if key2 == 258:
                            count2 +=1
                        if key2 == 259:
                            count2 -=1
                        if count2 > 1:
                            count2 =0
                        if count2 < 0:
                            count2 =1
                        if key2 == 27:
                            key = ''
                            window.clear()
                            window.refresh()
                            break
                        if key2 in [10,459]:
                            if count2 == 0:
                                key3 = ''
                                count3 = 0
                                df = busy.table_mesas(busy.mesas_disponiveis, 'Mesa')
                                rows = df.values.tolist()
                                window2 = curses.newwin((len(rows)+1)*2,25,0,46)
                                while key3 not in [10,459]:
                                    window2.clear()
                                    window2.refresh()
                                    window2.addstr(0,0,'{}'.format(emoji.emojize(':anchor: Selecione uma Mesa ')), blackcyan|curses.A_BOLD)
                                    posy = 2
                                    posx = 1
                                    for id, i in enumerate(rows):
                                        if id == count3:
                                            window2.addstr(posy,posx - 1,emoji.emojize(':small_blue_diamond:{}'.format(i[0])),blackyellow|curses.A_BOLD )
                                            posy +=2
                                        if id != count3:
                                            window2.addstr(posy,posx,emoji.emojize(':small_blue_diamond:{}'.format(i[0])),whiteblack|curses.A_BOLD )
                                            posy +=2
                                    window2.refresh()
                                    stdscr.refresh()
                                    key3 =stdscr.getch()
                                    if key3 == 258:
                                        count3 +=1
                                    if key3 == 259:
                                        count3 -=1
                                    if key3 == 27:
                                        key2 = ''
                                        window2.clear()
                                        window2.refresh()
                                        break
                                    if count3 < 0:
                                        count3 = len(rows) -1
                                    if count3 > len(rows) -1:
                                        count3 = 0
                                    if key3 in [10,459]:
                                        titulo = (df.at[df.index[count3], 'Mesa'])
                                        stdscr.addstr(0,68,'{}'.format(emoji.emojize(':anchor: Digite o Nome do Cliente')), blackorange)
                                        win = curses.newwin(1,25,2,72)
                                        box = Textbox(win)
                                        stdscr.refresh()
                                        nome = box.edit(enter_is_terminate).title()
                                        while nome == '':
                                            win.clear()
                                            stdscr.addstr(3,72,'Digite um Nome Valido', redblack)
                                            stdscr.refresh()
                                            nome = box.edit(enter_is_terminate).title()
                                        nome = nome.replace('\n','')
                                        nome.replace(' ','')
                                        key4 = ''
                                        count4 = 0
                                        while key4 not in [10,459]:
                                            window3 = curses.newwin(4,22,5,69)
                                            if count4 == 0:
                                                window3.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                                window3.addstr(1,3,emoji.emojize('Sim'),whiteblack|curses.A_BOLD)
                                                window3.addstr(2,3,emoji.emojize('Nao'),blackout|curses.A_BOLD)
                                            if count4 == 1:
                                                window3.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                                window3.addstr(1,3,emoji.emojize('Sim'),blackout|curses.A_BOLD)
                                                window3.addstr(2,3,emoji.emojize('Nao'),whiteblack|curses.A_BOLD)
                                            window3.refresh()
                                            key4 = stdscr.getch()
                                            if key4 == 258:
                                                count4 +=1
                                            if key4 == 259:
                                                count4 -=1
                                            if count4 < 0:
                                                count4 = 1
                                            if count4 > 1:
                                                count4 = 0
                                            if key4 == 27:
                                                window3.clear()
                                                window3.refresh()
                                                key2 = ''
                                                break
                                            if key4 in [10,459]:
                                                if count4 == 0:
                                                    busy.mesas_disponiveis.remove(titulo)
                                                    busy.mesas_ocupadas1.append(titulo)
                                                    busy.mesas_ocupadas['{}'.format(titulo)] = busy.mesa(titulo=titulo, responsavel=nome, pago=[0,0,0],status=False)
                                                    data.backup_mesas(dict=busy.mesas_ocupadas,file='mesas.txt')
                                                    window3.clear()
                                                    window3.refresh()
                                                    def relacionar(id):
                                                        _key_venda = 'fk_ID_venda_{}'.format(id)
                                                        _key_produto = 'fk_ID_produto_{}'.format(id)
                                                        _table = 'conta{}'.format(id)
                                                        q7 = """CALL relacionar_produtos('{}','{}');""".format(_table, _key_produto)
                                                        q8 = """CALL relacionar_venda('{}','{}');""".format(_table, _key_venda)
                                                        data.exec_query(q7)
                                                        data.exec_query(q8)
                                                        return    
                                                    threading.Thread(target=relacionar, args=(busy.mesas_ocupadas['{}'.format(titulo)].conta,)).start()
                                                    window3.addstr(0,3,'Operacao Concluida',grennblack|curses.A_BOLD)
                                                    if syncronyze.Status == True:
                                                        syncronyze.devices_allert()
                                                    window3.refresh()
                                                    stdscr.getch()
                                                    stdscr.clear()
                                                    key = ''
                                                if count4 == 1:
                                                    stdscr.clear()
                                                    key = ''
                            if count2 == 1:
                                stdscr.addstr(0,47,'{}'.format(emoji.emojize(':anchor: Digite o Nome do Cliente')), blackorange)
                                win = curses.newwin(1,25,2,50)
                                box = Textbox(win)
                                stdscr.refresh()
                                nome = box.edit(enter_is_terminate).title()
                                while nome == '':
                                    win.clear()
                                    stdscr.addstr(4,50,'Digite um Nome Valido', redblack)
                                    stdscr.refresh()
                                    nome = box.edit(enter_is_terminate).title()
                                nome = nome.replace('\n','')
                                titulo = str(random.randint(1,999))
                                while titulo in busy.militantes:
                                    titulo = str(random.randint(1,999))
                                count5 = 0
                                key5 = ''
                                while key5 not in [10,459]:
                                    window4 = curses.newwin(4,22,7,49)
                                    if count5 == 0:
                                        window4.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                        window4.addstr(1,3,emoji.emojize('Sim'),whiteblack|curses.A_BOLD)
                                        window4.addstr(2,3,emoji.emojize('Nao'),blackout|curses.A_BOLD)
                                    if count5 == 1:
                                        window4.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                        window4.addstr(1,3,emoji.emojize('Sim'),blackout|curses.A_BOLD)
                                        window4.addstr(2,3,emoji.emojize('Nao'),whiteblack|curses.A_BOLD)
                                    window4.refresh()
                                    key5 = stdscr.getch()
                                    if key5 == 27:
                                        window4.clear()
                                        window4.refresh()
                                        key2 = ''
                                        break
                                    if key5 == 258:
                                        count5 -=1
                                    if key5 == 259:
                                        count5 += 1
                                    if count5 < 0:
                                        count5 = 1
                                    if count5 > 1:
                                        count5 = 0
                                    if key5 in [10,459]:
                                        if count5 == 0:
                                            busy.militantes.append(titulo)
                                            busy.mesas_ocupadas['{}'.format(titulo)] = busy.mesa(titulo=titulo, responsavel=nome, pago=[0,0,0],status=False)
                                            data.backup_mesas(busy.mesas_ocupadas, 'mesas.txt')
                                            window4.clear()
                                            window4.refresh()
                                            def relacionar(id):
                                                _key_venda = 'fk_ID_venda_{}'.format(id)
                                                _key_produto = 'fk_ID_produto_{}'.format(id)
                                                _table = 'conta{}'.format(id)
                                                q7 = """CALL relacionar_produtos('{}','{}');""".format(_table, _key_produto)
                                                q8 = """CALL relacionar_venda('{}','{}');""".format(_table, _key_venda)
                                                data.exec_query(q7)
                                                data.exec_query(q8)
                                                return    
                                            threading.Thread(target=relacionar, args=(busy.mesas_ocupadas['{}'.format(titulo)].conta,)).start()
                                            window4.addstr(0,3,'Operacao Concluida',grennblack|curses.A_BOLD)
                                            if syncronyze.Status == True:
                                                syncronyze.devices_allert()
                                            window4.refresh()
                                            stdscr.getch()
                                            stdscr.clear()
                                            key = ''
                                        if count5 == 1:
                                            key = ''                                        
                #Acessar Conta
                if count == 1:
                    key2 = ''
                    count2 = 0
                    options2 = [emoji.emojize(':chair: Mesa'),emoji.emojize(':woman_dancing: Balcao')]
                    while key2 not in [10,459]:
                        window = curses.newwin(5,21,0,22)
                        stdscr.refresh()
                        pos = 2
                        window.addstr(0,0,emoji.emojize(':anchor: Selecione uma Opcao'),bluebaby)
                        for id, i in enumerate(options2):
                            if id == count2:
                                window.addstr(pos,0,'{}'.format(i), whiteblack|curses.A_BOLD)
                                pos +=2
                            if id != count2:
                                window.addstr(pos,0,'{}'.format(i), blackout|curses.A_BOLD)
                                pos +=2
                        window.refresh()
                        stdscr.refresh()
                        key2 = stdscr.getch()
                        if key2 == 258:
                            count2 +=1
                        if key2 == 259:
                            count2 -=1
                        if count2 > 1:
                            count2 =0
                        if count2 < 0:
                            count2 =1
                        if key2 == 27:
                            key = ''
                            window.clear()
                            window.refresh()
                            break
                        if key2 in [10,459]:
                            #MESA
                            if count2 == 0:
                                if len(busy.mesas_ocupadas1) == 0:
                                    stdscr.addstr(7,21,emoji.emojize(':warning:Todas as Mesas Estao Livres'),grennblack|curses.A_BOLD)
                                    stdscr.getch()
                                    key = ''
                                    break
                                else:
                                    df = data.busy_table()
                                    rows = df.values.tolist()
                                    key3 = ''
                                    count3 = 0
                                    x = (len(rows)+2) * 2
                                    if x < 2:
                                        x = 2
                                    window = curses.newwin(x,50,0,45)
                                    stdscr.refresh()
                                    while key3 not in [10,459]:
                                        window.clear()
                                        window.addstr(0,0,emoji.emojize(':anchor: Selecione a Mesa '), blackorange)
                                        pos = 2
                                        for id, i in enumerate(rows):
                                            if id == count3:
                                                nome = busy.mesas_ocupadas[i[0]].responsavel.replace(' ','')
                                                nome = re.sub(r"(\w)([A-Z])", r"\1 \2", nome)
                                                window.addstr(pos,0,emoji.emojize(':small_orange_diamond:{}({})'.format(i[0],nome)), whiteblack|curses.A_BOLD)
                                                pos += 1
                                            if id != count3:
                                                nome = busy.mesas_ocupadas[i[0]].responsavel.replace(' ','')
                                                nome = re.sub(r"(\w)([A-Z])", r"\1 \2", nome)
                                                window.addstr(pos,1,emoji.emojize(':small_orange_diamond:{}({})'.format(i[0],nome)), blackout|curses.A_BOLD)
                                                pos += 1
                                        window.refresh()
                                        key3 = stdscr.getch()
                                        if key3 == 258:
                                            count3 += 1
                                        if key3 == 259:
                                            count3 -= 1
                                        if count3 < 0:
                                            count3 = len(rows) -1
                                        if count3 > len(rows) -1:
                                            count3 = 0
                                        if key3 == 27:
                                            window.clear()
                                            window.refresh()
                                            stdscr.refresh()
                                            key2 = ''
                                            break
                                        if key3 in [10,459]:
                                            newmenuindividual.menuindividual(busy.mesas_ocupadas['{}'.format(df.at[df.index[count3], 'Mesas'])])
                                            wrapper(menu)
                                            return
                            #BALCAO
                            if count2 == 1:
                                if len(busy.militantes) == 0:
                                    stdscr.addstr(7,21,emoji.emojize(':warning:Nao Ha Contas Cadastradas!'),redblack)
                                    stdscr.getch()
                                    key = ''
                                    break
                                else:
                                    key3 = ''
                                    count3 = 0
                                    df = data.client_table()
                                    rows = df.values.tolist()
                                    x = (len(rows)+2) * 2
                                    if x < 2:
                                        x = 2
                                    window = curses.newwin(x,25,0,45)
                                    stdscr.refresh()
                                    while key3 not in [10,459]:
                                        window.clear()
                                        window.addstr(0,0,emoji.emojize(':anchor: Selecione o Cliente '),blackorange)
                                        pos = 2
                                        for id, i in enumerate(rows):
                                            if id != count3:
                                                window.addstr(pos,1,emoji.emojize(':small_orange_diamond:{}'.format(i[1])),blackout|curses.A_BOLD)
                                                pos += 1
                                            if id == count3:
                                                window.addstr(pos,0,emoji.emojize(':small_orange_diamond:{}'.format(i[1])),whiteblack|curses.A_BOLD)
                                                pos += 1
                                        window.refresh()
                                        key3 = stdscr.getch()
                                        if key3 == 27:
                                            window.clear()
                                            window.refresh()
                                            key2 = ''
                                            break
                                        if key3 == 258:
                                            count3 += 1
                                        if key3 == 259:
                                            count3 -= 1
                                        if count3 > len(rows) - 1:
                                            count3 = 0
                                        if count3 < 0:
                                            count3 = len(rows) -1
                                        if key3 in [10,459]:
                                            newmenuindividual.menuindividual(busy.mesas_ocupadas['{}'.format(df.at[df.index[count3], 'ID'])])
                                            wrapper(menu)
                                            return
                #Show mesas ocupadas
                if count == 2:
                    df = busy.table_mesas(busy.mesas_ocupadas1, 'Mesa')
                    rows = df.values.tolist()
                    if len(busy.mesas_ocupadas1) == 0:
                        stdscr.addstr(0,23,emoji.emojize(':green_heart: Todas as Mesas estao Livres. '),grennblack|curses.A_BOLD)
                        stdscr.getch()
                        stdscr.clear()
                        key = ''
                    else:
                        x = (len(rows)+2)*2
                        if x < 2:
                            x = 2
                        pos = 2
                        mesas = curses.newwin(x,25,0,25)
                        stdscr.refresh()
                        mesas.addstr(0,0,emoji.emojize('Mesas Ocupadas :no_entry:'),whiteblack|curses.A_BOLD)
                        for id, i in enumerate(rows):
                            mesas.addstr(pos,0,'{}'.format(i[0]), redblack|curses.A_BOLD)
                            pos += 2
                        mesas.refresh()
                        stdscr.refresh()
                        stdscr.getch()
                        key = ''
                #show mesas disponiveis
                if count == 3:
                    df = busy.table_mesas(busy.mesas_disponiveis, 'Mesa')
                    rows = df.values.tolist()
                    if len(busy.mesas_disponiveis) == 0:
                        stdscr.addstr(14,0,emoji.emojize(':warning: Todas as Mesas estao Ocupadas. '),redblack)
                        stdscr.getch()
                        stdscr.clear()
                        key = ''
                    else:
                        x = (len(rows)+1)*2
                        if x < 2:
                            x = 2
                        pos = 2
                        mesas = curses.newwin(x,20,0,25)
                        stdscr.refresh()
                        mesas.addstr(0,0,emoji.emojize('Mesas Livres :green_heart:'),blackyellow|curses.A_BOLD)
                        for id, i in enumerate(rows):
                            mesas.addstr(pos,0,'{}'.format(i[0]), grennblack)
                            pos += 2
                        mesas.refresh()
                        stdscr.refresh()
                        stdscr.getch()
                        key = ''
                #show cardapios
                if count == 4:
                    s = stdscr.getmaxyx()
                    last_row = s[0] - 1
                    count2 = 0
                    key2 = ''
                    options2 = [emoji.emojize(':crab: Para Comer'),
                    emoji.emojize(':tropical_drink: Para Beber'),
                    emoji.emojize(':clipboard: Cardapio Completo')]
                    window = curses.newwin(8,26,0,21)
                    while key2 not in [10,459]:
                        window.clear()
                        window.addstr(0,0,emoji.emojize(':anchor: Selecione uma Categoria'),bluebaby)
                        pos = 2
                        for id, i in enumerate(options2):
                            if count2 == id:
                                window.addstr(pos,0,'{}'.format(i), whiteblack|curses.A_BOLD)
                                pos = pos + 2
                            else:
                                window.addstr(pos,1,'{}'.format(i), blackout| curses.A_BOLD)
                                pos = pos + 2
                        window.refresh()
                        stdscr.refresh()
                        key2 = stdscr.getch()
                        if key2 == 258:
                            count2 = count2 + 1
                        elif key2 == 259:
                            count2 = count2- 1
                        elif key2 == 27:
                            key = ''
                            break
                        if count2 > 2:
                            count2 = 0
                        if count2 < 0:
                            count2 = 2
                        if key2 == 10:
                            if count2 == 0:
                                df = data.exibir_cardapio(data.q4)
                            if count2 == 1:
                                df = data.exibir_cardapio(data.q3)
                            if count2 == 2:
                                df = data.exibir_cardapio(data.q2)
                            rows = df.values.tolist()
                            if df.empty == True:
                                key = ''
                                break
                            posy = int(1)
                            posx = int(47)
                            stdscr.addstr(0,62,emoji.emojize(':bright_button: Pontal do Bainema :bright_button: '),blackorange)
                            for id ,i in enumerate(rows):
                                if posy == last_row:
                                    posx = posx + 26
                                    posy = 1
                                if posy <= last_row -1 and posx == 0:
                                    stdscr.addstr(posy,posx,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), whiteblack)
                                    stdscr.addstr(posy, posx+20,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), grennblack)
                                    posy = posy + 1       
                                else:
                                    stdscr.addstr(posy,posx,emoji.emojize(':small_orange_diamond:{}'.format(i[1])), whiteblack)
                                    stdscr.addstr(posy, posx+20,emoji.emojize(':heavy_dollar_sign:{}'.format(i[2])), grennblack)
                                    posy = posy + 1       
                            stdscr.refresh()
                            stdscr.getch()
                            key = ''
    wrapper(menu)
    return
if syncronyze.Status == True:
    threading.Thread(target=syncronyze.maquina_listen).start()
menu_principal()














