import flet as ft
from flet import *
import requests, os

def main(pagina:Page):

    def tela_login(evento):
        pagina.remove_at(0)
        pagina.add(col_login)
        pagina.update()

    def tela_registrar(evento):
        pagina.remove_at(0)
        pagina.add(col_registro)
        pagina.update()

    def logar(evento):
        if tf_elogin.value != '' and tf_upswd.value != '':
            tf_elogin.read_only = True
            tf_upswd.read_only = True
            eb_confirmar_login.disabled = True
            pagina.update()
            resp_serv = ''
            r = requests.get(f"{os.environ['link_api_login']}{tf_elogin.value},{tf_upswd.value}")
            if r.status_code == 200:
                for itens in r:
                    resp_serv = f"{resp_serv}{itens.decode('utf-8')}"
                resp_serv = eval(resp_serv)
                rs = list(resp_serv)[0]
                print(rs)
                if rs != "" and resp_serv.get(os.environ['b3']) == tf_upswd.value:
                    #emailC = resp_serv.get(os.environ['b2'])
                    #print(f"Login Autorizado\nLogin:{ resp_serv.get(os.environ['b1']) }\nEmail:{emailC}\nSenha:{resp_serv.get(os.environ['b3'])}")

                    ############## 2 FACTOR #####################
                    pagina.dialog = pop_up_2fl
                    r2fr = requests.get(f"{os.environ['b7']}{tf_elogin.value}")
                    pop_up_2fl.open = True
                    pagina.update()
                elif rs == "":
                    print("LOGIN NEGADO")
                    pop_up_erroserv.title = ft.Text('DADOS NAO ENCONTRADOS NO SISTEMA')
                    pagina.dialog = pop_up_erroserv
                    pop_up_erroserv.open = True
                    tf_elogin.read_only = False
                    tf_upswd.read_only = False
                    eb_confirmar_login.disabled = False
                    pagina.update()
                elif eval(r.text).get('erro') == "bd":
                    print("BD OFF")
                    pop_up_erroserv.title = ft.Text('DADOS NAO ENCONTRADOS NO SISTEMA')
                    pagina.dialog = pop_up_erroserv
                    pop_up_erroserv.open = True
                    tf_elogin.read_only = False
                    tf_upswd.read_only = False
                    eb_confirmar_login.disabled = False
                    pagina.update()
                else:
                    pop_up_erroserv.title = ft.Text('ERRO')
                    pagina.dialog = pop_up_erroserv
                    pop_up_erroserv.open = True
                    tf_elogin.read_only = False
                    tf_upswd.read_only = False
                    eb_confirmar_login.disabled = False
                    pagina.update()
            else:
                print(F"ERRO : {r.status_code}")

    def tela_sucesso_login():
        pop_up_2fl.open = False
        pagina.remove(col_login)
        pagina.add(txt_logado)
        pagina.update()
    
    def tela_home(evento):
        pop_up_sucesso_cadastro.open = False
        pop_up_2fc.open = False
        pop_up_2fl.open = False
        pop_up_erroserv.open = False
        pop_up_ja_cadastrado.open = False
        pagina.remove_at(0)
        pagina.add(col_home)
        pagina.update()

    def fpop_up_erros(evento):
        pop_up_erroserv.open = False
        pagina.update()

    def testar_cod_login(evento):
        el_mail = eval( requests.get(f"{os.environ['link_api_login']}{tf_elogin.value},{tf_upswd.value}").text ).get('email')
        el_codigo = tf_cod2fl.value
        if el_codigo != "" and len(el_codigo) == 5:
            try:
                r_api_2f = requests.get(f"{os.environ['b4']}{el_mail},{el_codigo}").text ###################
                if r_api_2f == 'True':
                    tela_sucesso_login()
                else: 
                    pop_up_2fl.title = ft.Text('COD ERRADO')
                    pagina.update()
            except:
                print("CAIU NO EXCEPT DO TESTAR COD")

    def testar_cod_cadastro(evento):
        el_mail = tf_email.value
        el_codigo = tf_cod2fc.value
        if el_codigo != "" and len(el_codigo) == 5:
            try:
                r_api_2f = requests.get(f"{os.environ['b4']}{el_mail},{el_codigo}").text ###################
                if r_api_2f == 'True':
                    requests.get(f"{os.environ['b6']}/{tf_email.value},{tf_pswd.value}") 
                    tf_email.disabled = False
                    tf_pswd.disabled = False
                    tf_pswd2.disabled = False
                    pop_up_2fc.open = False
                    pagina.update()
                    pagina.dialog = pop_up_sucesso_cadastro
                    pop_up_sucesso_cadastro.open = True
                    pagina.update()
                else: 
                    tf_email.disabled = False
                    tf_pswd.disabled = False
                    tf_pswd2.disabled = False
                    pop_up_2fl.title = ft.Text('COD ERRADO')
                    pagina.update()
            except:
                print("CAIU NO EXCEPT DO TESTAR COD")

    def confirmar_registro(e):
        if tf_email.value != "" and tf_pswd.value != "" and tf_pswd2.value != "" and tf_pswd.value == tf_pswd2.value:
            tf_email.disabled = True
            tf_pswd.disabled = True
            tf_pswd2.disabled = True
            pagina.update()
            rte = requests.get(f"{os.environ['b5']}{tf_email.value}").text 
            if rte == '{"False": "False"}':
                print("Email nao cadastrado no sistema")
                r2fr2 = requests.get(f"{os.environ['b7']}{tf_email.value}")
                pagina.dialog = pop_up_2fc
                pop_up_2fc.open = True
                pagina.update()
            elif rte == '{"True": "True"}':
                print("Email no sistema")
                tf_email.disabled = False
                tf_pswd.disabled = False
                tf_pswd2.disabled = False
                pop_up_ja_cadastrado.open = True
                pagina.dialog = pop_up_ja_cadastrado
                pagina.update()
            elif rte == '{"erro": "bd"}':
                tf_email.disabled = False
                tf_pswd.disabled = False
                tf_pswd2.disabled = False
                print("BD OFF KKKKK")
                pagina.update()
            else:
                tf_email.disabled = False
                tf_pswd.disabled = False
                tf_pswd2.disabled = False
                print("N SEI Q ERRO DEU MAS DEU ERRO")
                pagina.update()
        elif tf_pswd.value != tf_pswd2.value:
            tf_pswd.border_color = ft.colors.RED
            tf_pswd2.border_color = ft.colors.RED
            pagina.update()

    def fechar_pop_up_emailexistente(e):
        pop_up_ja_cadastrado.open = False
        pagina.update()

    #CENTRALIZAR 
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #REUTILIZAVEL
    eb_home = ft.ElevatedButton(icon=ft.icons.ARROW_BACK, text='VOLTAR', on_click=tela_home)

    #PAG INICIAL
    eb_login = ft.ElevatedButton(text='LOGIN', on_click=tela_login)
    eb_registrar = ft.ElevatedButton(text='REGISTRAR', on_click=tela_registrar)
    txt_bemvindo = ft.Text(value='APP LOGIN')
    linha_bemvindo = ft.Row([txt_bemvindo], alignment=ft.MainAxisAlignment.CENTER, spacing=1000)
    linha_bts = ft.Row([eb_login,eb_registrar],alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    col_home = ft.Column(controls=[linha_bemvindo,linha_bts])

    #PAG REGISTRO
    tf_email = ft.TextField(label='Email', width=300)
    tf_pswd = ft.TextField(label='Senha',password=True, can_reveal_password=True, width=300)  
    tf_pswd2 = ft.TextField(label='Confirme a senha',password=True, can_reveal_password=True, width=300)
    eb_confirmar_registrar = ft.ElevatedButton(text='CONFIRMAR', on_click=confirmar_registro)
    linha_bts_registro = ft.Row([eb_home,eb_confirmar_registrar], alignment=ft.MainAxisAlignment.CENTER)
    col_registro = ft.Column(controls=[tf_email,tf_pswd,tf_pswd2,linha_bts_registro], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    #PAG LOGIN
    tf_elogin = ft.TextField(label='Login', width=300)
    tf_upswd = ft.TextField(label='Senha', password=True, can_reveal_password=True, width=300)
    eb_confirmar_login = ft.ElevatedButton(text='LOGAR', on_click=logar)
    linha_btn_login = ft.Row([eb_home,eb_confirmar_login],alignment=ft.MainAxisAlignment.CENTER)
    col_login = ft.Column(controls=[tf_elogin,tf_upswd, linha_btn_login], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
   
    #PAG LOGADO
    txt_logado = ft.Text(value='LOGADO COM SUCESSO')

    #POP UP PROBLEMA NO SERVIDOR
    pop_up_erroserv = ft.AlertDialog( open=False, modal=True, title=ft.Text(value='DADOS NAO CONFEREM'), actions=[ft.ElevatedButton("OK", on_click=fpop_up_erros)])

    #POP UP 2FACTOR LOGIN
    tf_cod2fl = ft .TextField(label="COD", keyboard_type=ft.KeyboardType.NUMBER, max_length=5)
    pop_up_2fl = ft.AlertDialog( 
        open=False, 
        modal=False, 
        title=ft.Text(f'Codigo enviado ao email cadastrado!'), 
        content=tf_cod2fl, 
        actions=[ ft.ElevatedButton("OK", on_click=testar_cod_login) ]
        )
    
    #POP UP DE EMAIL JA CADASTRADO
    pop_up_ja_cadastrado = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text('Ja existe uma conta associada a este email'),
        actions=[ft.ElevatedButton('Ok', on_click=fechar_pop_up_emailexistente )]
    )
    #POP UP SUCESSO DE CADASTRO
    pop_up_sucesso_cadastro = ft.AlertDialog(
        open=False,
        modal=False,
        title=ft.Text('Cadastro realizado com sucesso, redirecionando para tela principal...'),
        actions=[ft.ElevatedButton('Ok', on_click=tela_home )]
    )

    #POP UP 2FACTOR CADASTRO      #POP UP SEGUE PERSISTENTE AO FINALIZAR CADASTRO
    tf_cod2fc = ft .TextField(label="COD", keyboard_type=ft.KeyboardType.NUMBER, max_length=5)
    pop_up_2fc = ft.AlertDialog( 
        open=False, 
        modal=False,
        title=ft.Text(f'Codigo enviado ao email informado.'), 
        content=tf_cod2fc, 
        actions=[ ft.ElevatedButton("OK", on_click=testar_cod_cadastro) ]
        )
    
    pagina.add(col_home)

    

ft.app(target=main) #  , view=ft.WEB_BROWSER