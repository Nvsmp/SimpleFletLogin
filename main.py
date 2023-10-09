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
            print(r)
            for itens in r:
                resp_serv = f"{resp_serv}{itens.decode('utf-8')}"
            resp_serv = eval(resp_serv)
            rs = list(resp_serv)[0]
            print(rs)
            if rs != "" and resp_serv.get(os.environ['b3']) == tf_upswd.value:
                print(f"Login Autorizado\nLogin:{ resp_serv.get(os.environ['b1']) }\nEmail:{ resp_serv.get(os.environ['b2']) }\nSenha:{resp_serv.get(os.environ['b3'])}")
                ############## 2 FACTOR #####################
                pagina.dialog = pop_up_2fl
                pop_up_2fl.open = True
                pagina.update()
            elif rs == "":
                print("DEU RUIM NO SERV KKK")
                pagina.dialog = pop_up_erroserv
                pop_up_erroserv.open = True
                tf_elogin.read_only = False
                tf_upswd.read_only = False
                eb_confirmar_login.disabled = False
                pagina.update()
            else:
                tf_elogin.read_only = False
                tf_upswd.read_only = False
                eb_confirmar_login.disabled = False
                pagina.update()

    def tela_sucesso_login():
        pop_up_2fl.open = False
        pagina.remove(col_login)
        pagina.add(txt_logado)
        pagina.update()
    
    def tela_home(evento):
        pagina.remove_at(0)
        pagina.add(col_home)
        pagina.update()

    def fpop_up_erros(evento):
        pop_up_erroserv.open = False
        pagina.update()

    def testar_cod(evento):
        el_mail = tf_elogin.value
        el_codigo = tf_cod2fl.value
        if el_codigo != "" and len(el_codigo) == 5:
            r_api_2f = requests.get(f"{os.environ['b4']}{el_mail},{el_codigo}").text ###################
            if r_api_2f == 'True':
                tela_sucesso_login()
            else: 
                pop_up_2fl.title = ft.Text('COD ERRADO')
                pagina.update()



    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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
    eb_confirmar_registrar = ft.ElevatedButton(text='CONFIRMAR')
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
    pop_up_erroserv = ft.AlertDialog( open=False, modal=True, title=ft.Text(value='FALHA NO SERVIDOR'), actions=[ft.ElevatedButton("OK", on_click=fpop_up_erros)])

    #POP UP 2FACTOR LOGIN
    tf_cod2fl = ft .TextField(label="COD", keyboard_type=ft.KeyboardType.NUMBER, max_length=5)
    pop_up_2fl = ft.AlertDialog( 
        open=False, 
        modal=False, 
        title=ft.Text(f'Codigo enviado ao email cadastrado!'), 
        content=tf_cod2fl, 
        actions=[ ft.ElevatedButton("OK", on_click=testar_cod) ]
        )

    pagina.add(col_home)

    

ft.app(target=main) #, view=ft.WEB_BROWSER