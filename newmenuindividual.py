import busy
import data
import data2
import curses
from curses import wrapper
from curses.textpad import Textbox
import emoji      
def menuindividual(mesa=object):
    def menu(stdscr):
        curses.start_color()
        curses.init_color(45,0,1000,450)
        curses.init_color(46,1000,444,300)
        curses.init_color(30,424,360,820)
        curses. init_color(40,0,800,1000)
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(8, 45, curses.COLOR_BLACK)
        curses.init_pair(9,curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(10,curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(11,curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(12,46, curses.COLOR_BLACK)
        curses.init_pair(13,30, curses.COLOR_BLACK)
        curses.init_pair(14,40, curses.COLOR_BLACK)
        bluebaby = curses.color_pair(14)
        roxobaby = curses.color_pair(13)
        blackorange = curses.color_pair(12)
        whitered = curses.color_pair(10)
        whitegreen = curses.color_pair(9)
        grennblack = curses.color_pair(11)
        newgreen = curses.color_pair(8)
        redblack= curses.color_pair(7)
        blackout =curses.color_pair(3)
        blackcyan = curses.color_pair(4)
        blackyellow = curses.color_pair(2)
        whiteblack = curses.color_pair(1)
        stdscr.clear()
        def estrutura(valorx=None, valory=None):
            if valorx == None:
                valorx = 0
            if valory == None:
                valory = 1
            stdscr.addstr(valory,valorx,emoji.emojize(':page_with_curl: {}'.format(mesa.responsavel)),blackcyan|curses.A_BOLD)
            return
        s = stdscr.getmaxyx()
        x = s[1]//4
        options = [emoji.emojize(':fountain_pen: Adicionar Item '),emoji.emojize(':red_exclamation_mark: Remover Item '),emoji.emojize(':currency_exchange: Pagamento'),emoji.emojize(':person_running: Retornar')]
        key = ''
        count = 0
        while key not in [10,459]:
            stdscr.clear()
            estrutura(0,0)
            pos = 2
            for id,i in enumerate(options):
                if id == count:
                    stdscr.addstr(pos,0,'{}'.format(i),whiteblack|curses.A_BOLD)
                    pos +=2
                if id !=count:
                    stdscr.addstr(pos,1,'{}'.format(i),blackout|curses.A_BOLD)     
                    pos +=2
            stdscr.refresh()
            key = stdscr.getch()
            if key == 258:
                count +=1
            if key == 259:
                count -=1
            if key == 27:
                stdscr.clear()
                return
            if count < 0:
                count = len(options) -1
            if count > len(options) - 1:
                count = 0
            if key in [10,459]:
                #ADICIONAR ITEM
                if count == 0:
                    mesa.adicionar_conta()
                    wrapper(menu)
                #REMOVER ITEM
                if count == 1:
                    key2 = ''
                    count2 = 0    
                    q1 ="""select produtos.Nome,conta{}.Qtd,conta{}.PrecoVendido from conta{} inner join produtos on conta{}.ID_produto = produtos.ID_produto ORDER BY Preco;""".format(str(mesa.conta),str(mesa.conta),str(mesa.conta),str(mesa.conta))
                    conta = data.get_tabela_mysql(q=q1)
                    rows = conta.values.tolist()
                    while key2 not in [10,459]:
                        pos = 3
                        window = curses.newwin(len(rows)+5,43,0,38)
                        window.clear()
                        window.refresh()
                        size = window.getmaxyx()
                        posx = size[1]//2 - len(mesa.responsavel)
                        window.addstr(0,posx,emoji.emojize(':anchor: {}'.format(mesa.responsavel)))
                        window.addstr(2,0,'QTD   ITEM            PRECO(UN) VALOR TOTAL')
                        total = 0
                        for id, i in enumerate(rows):
                            if id != count2:
                                window.addstr(pos,0,'{}'.format(i[1]),blackout|curses.A_BOLD)
                                window.addstr(pos,3,'{}'.format(i[0]),blackout|curses.A_BOLD)
                                window.addstr(pos,22,'R${}'.format(i[2]),blackout|curses.A_BOLD)
                                window.addstr(pos,32,'R${}'.format(i[2]*i[1]),blackout|curses.A_BOLD)
                                pos += 1
                                total = total + i[2]*i[1]
                            if id == count2:
                                window.addstr(pos,0,'{}'.format(i[1]),redblack|curses.A_BOLD)
                                window.addstr(pos,3,'{}'.format(i[0]),redblack|curses.A_BOLD)
                                window.addstr(pos,22,'R${}'.format(i[2]),redblack|curses.A_BOLD)
                                window.addstr(pos,32,'R${}'.format(i[2]*i[1]),redblack|curses.A_BOLD)
                                pos += 1
                                total = total +float(i[2])*int(i[1]) 
                        window.addstr(pos+1,0,'Total R${}'.format(total))
                        window.refresh()
                        stdscr.refresh()
                        if conta.empty == True:
                                stdscr.getch()
                                window.clear()
                                window.refresh()
                                key = ''
                                break
                        key2 =stdscr.getch()
                        if key2  == 27:
                            key = ''
                            break
                        if key2 == 258:
                            count2 += 1
                        if key2 == 259:
                            count2 -= 1
                        if count2 > len(rows) - 1:
                            count2 = 0
                        if count2 < 0:
                            count2 = len(rows) -1
                        if key2 in [10,459]:
                            count3 = 0
                            qtd = conta.at[conta.index[count2],'Qtd']
                            key3 = ''
                            window2 = curses.newwin(3,23,12,37)
                            stdscr.refresh()
                            while key3 not in [10,459]:
                                window2.clear()
                                window2.refresh
                                window2.addstr(0,0,emoji.emojize(':anchor: Selecione Quantidade '),blackyellow|curses.A_BOLD)
                                window2.addstr(2,3,'{}'.format(count3),blackyellow|curses.A_BOLD|curses.A_REVERSE)
                                window2.refresh()
                                key3 = stdscr.getch()
                                if key3 == 258:
                                    count3 -=1
                                if key3 == 259:
                                    count3 +=1
                                if key3 == 27:
                                    window2.clear()
                                    window2.refresh()
                                    key2 = ''
                                    break
                                if count3 < 0:
                                    count3 = 0
                                if count3 > qtd:
                                    count3 = qtd
                                if key3 in [10,459]:
                                    count4 = 0
                                    key4 = ''
                                    while key4 not in [10,459]:
                                        window3 = curses.newwin(4,22,16,37)
                                        if count4 == 0:
                                            window3.addstr(0,0,emoji.emojize(':warning: Confirmar Operacao?'),blackyellow)
                                            window3.addstr(1,3,emoji.emojize('Sim'),whitegreen|curses.A_REVERSE)
                                            window3.addstr(2,3,emoji.emojize('Nao'),blackout|curses.A_BOLD)
                                        if count4 == 1:
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
                                            count4 -=1
                                        if key4 == 259:
                                            count4 += 1
                                        if count4 < 0:
                                            count4 = 1
                                        if count4 > 1:
                                            count4 = 0
                                        if key4 in [10,459]:
                                            if count4 == 0:
                                                nome = conta.at[conta.index[count2],'Nome']
                                                id_protudo = data2.ID_Produto(nome=nome)
                                                q1 = """update produtos set Qtd = Qtd +{} WHERE ID_produto = {};""".format(count3,id_protudo)
                                                q2 = """update conta{} set Qtd = Qtd -{} WHERE ID_produto = {};""".format(mesa.conta,count3,id_protudo)
                                                data.exec_query(q1)
                                                data.exec_query(q2)
                                                window3.clear()
                                                window3.refresh()
                                                window3.addstr(0,3,'Operacao concluida',grennblack|curses.A_BOLD)
                                                window3.refresh()
                                                stdscr.getch()
                                                stdscr.clear()
                                                wrapper(menu)
                                            if count4 == 1:
                                                return         
                #ACESSAR CONTA            
                if count == 2:
                    key2 = ''  
                    q1 ="""select produtos.Nome,conta{}.Qtd,conta{}.PrecoVendido from conta{} inner join produtos on conta{}.ID_produto = produtos.ID_produto ORDER BY Preco;""".format(str(mesa.conta),str(mesa.conta),str(mesa.conta),str(mesa.conta))
                    conta = data.get_tabela_mysql(q=q1)
                    pagamentos_history = data2.get_pagamentos(id=str(mesa.conta))
                    din = float(pagamentos_history[0])
                    card = float(pagamentos_history[1])
                    pix = float(pagamentos_history[2])
                    rows2 = conta.values.tolist()
                    valores = []
                    for i in rows2:
                        valores.append(i[1]*i[2])
                    conta['Valores'] = valores
                    rows2 = conta.values.tolist()
                    count2 = 0
                    while key2 not in [10,459]:
                        total_pago = din + card + pix
                        pos = 3
                        windowpagamento = curses.newwin(7,24,0,71)
                        windowpagamento.addstr(0,4,emoji.emojize(':money_bag: PAGAMENTOS'))
                        windowpagamento.addstr(2,0,emoji.emojize(':dollar_banknote: Dinheiro'),blackout|curses.A_BOLD)
                        windowpagamento.addstr(3,0,emoji.emojize(':credit_card: Cartao'),blackout|curses.A_BOLD)
                        windowpagamento.addstr(4,0,emoji.emojize(':coin: Pix'),blackout|curses.A_BOLD) 
                        windowpagamento.addstr(2,15,'R${}'.format(din),grennblack|curses.A_BOLD)
                        windowpagamento.addstr(3,15,'R${}'.format(card),grennblack|curses.A_BOLD)
                        windowpagamento.addstr(4,15,'R${}'.format(pix),grennblack|curses.A_BOLD)
                        windowpagamento.addstr(5,0,'Pago R${}'.format(total_pago),roxobaby)
                        windowconta = curses.newwin(len(rows2)+5,49,0,20)
                        windowconta.addstr(0,22,emoji.emojize('CONTA'))
                        windowconta.addstr(2,0,'   ITEM             QTD   PRECO(UN) VALOR TOTAL')
                        total2 = 0
                        for id,i in enumerate(rows2):
                            windowconta.addstr(pos,0,emoji.emojize(':small_orange_diamond:{}'.format(str(i[0]))),blackout|curses.A_BOLD)
                            windowconta.addstr(pos,21,'{}'.format(int(i[1])),blackout|curses.A_BOLD)
                            windowconta.addstr(pos,26,'R${}'.format(float(i[2])),blackout|curses.A_BOLD)
                            windowconta.addstr(pos,38,'R${}'.format(float(i[3])),blackout|curses.A_BOLD)
                            pos +=1
                            total2 = total2 + i[3]
                        saldo = float(total2) - float(total_pago)
                        windowconta.addstr(pos,2,'Total R${}'.format(total2),newgreen)
                        windowpagamento.addstr(6,0,'Saldo R${}'.format(saldo),redblack)
                        windowoptions = curses.newwin(4,22,8,69)
                        windowoptions.clear()
                        windowoptions.refresh()
                        option = [emoji.emojize(':small_blue_diamond:Pagamento'),emoji.emojize(':small_blue_diamond:Fechar Conta'),emoji.emojize(':small_blue_diamond:Retornar')]
                        windowoptions.addstr(0,0,emoji.emojize(':anchor: Selecione uma Opcao '),bluebaby)
                        pos = 1
                        for id, i in enumerate(option):
                            if id == count2:
                                windowoptions.addstr(pos,0,'{}'.format(i),whiteblack|curses.A_BOLD)
                                pos += 1
                            if id != count2:
                                windowoptions.addstr(pos,1,'{}'.format(i),blackout|curses.A_BOLD)
                                pos += 1
                        windowoptions.refresh()
                        windowpagamento.refresh()
                        windowconta.refresh()
                        key2 = stdscr.getch()
                        if key2 == 27:
                            key = ''
                            stdscr.clear()
                            break
                        if key2 == 258:
                            count2+=1
                        if key2 == 259:
                            count2 -=1
                        if count2 < 0:
                            count2 = 2
                        if count2 > 2:
                            count2 = 0
                        if key2 in [10,459]:
                            #Pagamento Parcial
                            if count2 == 0:
                                if saldo <= 0:
                                    windowoptions.clear()
                                    windowoptions.refresh()
                                    windowalert = curses.newwin(2,22,9,69)
                                    windowalert.addstr(0,0,emoji.emojize(':warning: O saldo esta zerado'),redblack)
                                    windowalert.refresh()
                                    stdscr.getch()
                                    windowalert.clear()
                                    key2 = ''
                                else:
                                    count3 = 0
                                    key3 = ''
                                    option2 = [emoji.emojize(':small_orange_diamond:Dinheiro'),emoji.emojize(':small_orange_diamond:Cartao'),emoji.emojize(':small_orange_diamond:Pix')]
                                    windowpagar = curses.newwin(5,22,13,69)
                                    while key3 not in [10,459]:
                                        windowpagar.clear()
                                        windowpagar.refresh()
                                        windowpagar.addstr(0,0,emoji.emojize(':money_bag: Forma de Pagamento'), blackorange)
                                        pos = 1
                                        for id, i in enumerate(option2):
                                            if id == count3:
                                                windowpagar.addstr(pos,0,'{}'.format(i),whiteblack|curses.A_BOLD)
                                                pos +=1
                                            if id != count3:
                                                windowpagar.addstr(pos,1,'{}'.format(i),blackout|curses.A_BOLD)
                                                pos +=1
                                        windowpagar.refresh()
                                        key3 = stdscr.getch()
                                        if key3 == 27:
                                            key2 = ''
                                            windowpagar.clear()
                                            windowpagar.refresh()
                                            break
                                        if key3 == 258:
                                            count3+=1
                                        if key3 == 259:
                                            count3 -=1
                                        if count3 < 0:
                                            count3 = 2
                                        if count3 > 2:
                                            count3 = 0
                                        if key3 in [10,459]:   
                                            windowqtd = curses.newwin(1,21,18,69)
                                            windowqtd.addstr(0,0,emoji.emojize(':heavy_dollar_sign:Insira o Valor'), newgreen)
                                            windowqtd.refresh()
                                            windowqtd2 = curses.newwin(1,10,19,71)
                                            windowqtd2 = Textbox(windowqtd2)
                                            def enter_is_terminate(x):
                                                if x in [10,459]:
                                                    return 7
                                                elif x in [27]:
                                                    Textbox.do_command(windowqtd2, 7)            
                                                elif x not in [48,49,50,51,52,53,54,55,56,57,82,36,46,44,8]:
                                                    return 9
                                                else:
                                                    return x
                                            curses.curs_set(1)
                                            valor = windowqtd2.edit(enter_is_terminate).replace('R','')
                                            valor = valor.replace('$','')
                                            valor = valor.replace(',','.')
                                            valor = valor.replace('\n','')
                                            windowconfirm = curses.newwin(3,26,21,69)
                                            while busy.isfloat(valor) == False:
                                                windowconfirm.addstr(0,0,emoji.emojize(':warning: Insira um valor valido'),redblack)
                                                windowconfirm.refresh()
                                                valor = windowqtd2.edit(enter_is_terminate).replace('R','')
                                                valor = valor.replace('$','')
                                                valor = valor.replace(',','.')
                                                valor = valor.replace('\n','')   
                                            curses.curs_set(0)
                                            windowconfirm.clear()
                                            windowconfirm.refresh()
                                            valor = float(valor)
                                            if valor > saldo:
                                                valor = saldo
                                            key5 = ''
                                            count5 = 0
                                            while key5 not in [10,459]:
                                                windowconfirm.clear()
                                                windowconfirm.refresh()
                                                windowconfirm.addstr(0,0,emoji.emojize(':warning:Confirmar Operacao'),blackyellow)
                                                if count5 == 0:
                                                    windowconfirm.addstr(1,1,'Sim',whiteblack|curses.A_BOLD)
                                                    windowconfirm.addstr(2,2,'Nao',blackout|curses.A_BOLD)
                                                if count5 == 1:
                                                    windowconfirm.addstr(1,2,'Sim',blackout|curses.A_BOLD)
                                                    windowconfirm.addstr(2,1,'Nao',whiteblack|curses.A_BOLD)
                                                windowconfirm.refresh()
                                                key5 = stdscr.getch()
                                                if key5 == 258:
                                                    count5+=1
                                                if key5 == 259:
                                                    count5 -=1
                                                if count5 > 1:
                                                    count5 = 0
                                                if count5 < 0:
                                                    count5 = 1
                                                if key5 in [10,459]:
                                                    if count5 == 0:
                                                        if count3 == 0:
                                                            q = """update conta{} set Dinheiro = Dinheiro + {} WHERE ID_venda = {};""".format(mesa.conta,valor,mesa.conta)
                                                            din = din + valor
                                                        if count3 == 1:
                                                            q = """update conta{} set Cartao = Cartao + {} WHERE ID_venda = {};""".format(mesa.conta,valor,mesa.conta)
                                                            card = card + valor
                                                        if count3 == 2:
                                                            q = """update conta{} set Pix = Pix + {} WHERE ID_venda = {};""".format(mesa.conta,valor,mesa.conta)
                                                            pix = pix + valor
                                                        data.exec_query(q)
                                                        windowconfirm.clear()
                                                        windowconfirm.refresh()
                                                        windowqtd2 = curses.newwin(1,10,19,71)
                                                        windowqtd2.addstr(0,0,' ')
                                                        windowqtd2.refresh()
                                                        stdscr.refresh()
                                                        windowpagar.clear()
                                                        windowpagar.refresh()
                                                        windowqtd.clear()
                                                        windowqtd.refresh()
                                                        windowpagar.addstr(0,0,emoji.emojize(':check_mark_button: Pagamento Realizado  '),grennblack|curses.A_BOLD)
                                                        windowpagar.refresh()
                                                        stdscr.getch()
                                                        windowpagar.clear()
                                                        windowpagar.refresh()
                                                        key2 = ''
                                                    if count5 == 1:
                                                        windowconfirm.clear()
                                                        windowconfirm.refresh()
                                                        windowqtd2 = curses.newwin(1,10,19,71)
                                                        windowqtd2.addstr(0,0,' ')
                                                        windowqtd2.refresh()
                                                        stdscr.refresh()
                                                        windowpagar.clear()
                                                        windowpagar.refresh()
                                                        windowqtd.clear()
                                                        windowqtd.refresh()
                                                        windowpagar.addstr(0,0,emoji.emojize(':check_mark_button: Pagamento Cancelado  '),redblack)
                                                        windowpagar.refresh()
                                                        stdscr.getch()
                                                        windowpagar.clear()
                                                        windowpagar.refresh()
                                                        key2 = ''
                            #Fechar Conta
                            if count2 == 1:
                                windowalert = curses.newwin(2,21,9,69)
                                #Fechar Conta Paga
                                if saldo <=0:
                                    windowoptions.clear()
                                    windowoptions.refresh()
                                    lista = [din,card,pix]
                                    count3 = 0
                                    for i in lista:
                                        if i == 0:
                                            count3+=1
                                        continue
                                    if count3 == 1:
                                        for id, i in enumerate(lista):
                                            if i != 0:
                                                if id == 0:
                                                    tipo = 'Dinheiro'
                                                if id == 1:
                                                    tipo = 'Cartao'
                                                if id == 2:
                                                    tipo = 'Pix'
                                            break
                                    else:
                                        tipo = 'Splitted'
                                    q1 = """update venda set Tipo = '{}',Total = {}, Total_Pago = {}, Dinheiro = {}, Cartao = {},Pix ={} WHERE ID_venda = {};""".format(tipo,total2,total_pago,din,card,pix,mesa.conta)
                                    data.exec_query(q1)
                                    if busy.check_titulo(mesa.titulo) == False:
                                        busy.mesas_disponiveis.append('{}'.format(mesa.titulo))
                                        busy.mesas_ocupadas1.remove('{}'.format(mesa.titulo))
                                        del busy.mesas_ocupadas['{}'.format(mesa.titulo)]
                                        data.backup_mesas(dict=busy.mesas_ocupadas,file='mesas.txt')
                                    else:
                                        busy.militantes.remove('{}'.format(mesa.titulo))
                                        del busy.mesas_ocupadas['{}'.format(mesa.titulo)]
                                        data.backup_mesas(dict=busy.mesas_ocupadas,file='mesas.txt')
                                    windowalert.addstr(0,0,emoji.emojize(':check_mark_button: Conta Fechada'))
                                    windowalert.refresh()
                                    stdscr.getch()
                                    pass
                                #Conta Pendente
                                else:
                                    windowoptions.clear()
                                    windowoptions.refresh()
                                    windowalert.addstr(0,0,emoji.emojize(':warning: Pagamento Pendente'),redblack)
                                    windowalert.refresh()
                                    macetinho = stdscr.getch()
                                    if macetinho == 38:
                                        q1 = """update venda set Total = {}, Total_Pago = {}, Dinheiro ={}, Cartao = {},Pix = {} WHERE ID_venda = {};""".format(total2,total_pago,din,card,pix,mesa.conta)
                                        data.exec_query(q1)
                                        if busy.check_titulo(mesa.titulo) == False:
                                            busy.mesas_disponiveis.append('{}'.format(mesa.titulo))
                                            busy.mesas_ocupadas1.remove('{}'.format(mesa.titulo))
                                            del busy.mesas_ocupadas['{}'.format(mesa.titulo)]
                                            data.backup_mesas(dict=busy.mesas_ocupadas,file='mesas.txt')
                                        else:
                                            busy.militantes.remove('{}'.format(mesa.titulo))
                                            del busy.mesas_ocupadas['{}'.format(mesa.titulo)]
                                            data.backup_mesas(dict=busy.mesas_ocupadas,file='mesas.txt')
                                        windowalert.clear()
                                        windowalert.addstr(0,0,emoji.emojize(':pirate_flag: Conta Fechada'),roxobaby)
                                        windowalert.refresh()
                                        stdscr.getch()
                                        pass
                                    else:
                                        windowalert.clear()
                                        key2 = ''                                    
                            #Retornar
                            if count2 == 2:
                                pass                    
                #RETORNAR AO MENU
                if count ==3:
                    return
    wrapper(menu)
    return