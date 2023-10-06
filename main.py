import flet as ft
from flet import *
import requests, os
def main(pagina:Page):

    def tela_login(evento):
        pagina.remove(linha_bts,linha_bemvindo)
        pagina.add(col_login)
        pagina.update()

    def tela_registrar(evento):
        pagina.remove(linha_bts, linha_bemvindo)
        pagina.add(eb_home,tf_email,tf_pswd,eb_confirmar_registrar)
        pagina.update()

    def logar(evento):
        if tf_login.value != '' and tf_upswd.value != '':
            tf_login.read_only = True
            tf_upswd.read_only = True
            eb_confirmar_login.disabled = True
            pagina.update()
            resp_serv = ''
            for itens in requests.get(f"{os.environ['link_api_login']}{tf_login.value},{tf_upswd.value}"):
                resp_serv = f"{resp_serv}{itens.decode('utf-8')}"
            resp_serv = eval(resp_serv)
            if list(resp_serv)[0] != "" and resp_serv.get(os.environ['b3']) == tf_upswd.value:
                print(f"Login Autorizado\nLogin:{ resp_serv.get(os.environ['b1']) }\nEmail:{ resp_serv.get(os.environ['b2']) }\nSenha:{resp_serv.get(os.environ['b3'])}")
                tela_sucesso_login()
                ############## 2 FACTOR #####################
            else:
                tf_login.read_only = False
                tf_upswd.read_only = False
                eb_confirmar_login.disabled = False
                pagina.update()
                
    def tela_sucesso_login():
        pagina.remove(col_login)
        pagina.add(txt_logado)
        pagina.update()

    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    eb_home = ft.ElevatedButton(icon=ft.icons.ARROW_BACK, text='VOLTAR')
    #PAG INICIAL
    eb_login = ft.ElevatedButton(text='LOGIN', on_click=tela_login)
    eb_registrar = ft.ElevatedButton(text='REGISTRAR', on_click=tela_registrar)
    txt_bemvindo = ft.Text(value='APP LOGIN')
    #PAG REGISTRO
    tf_email = ft.TextField(label='Email')
    tf_pswd = ft.TextField(label='Senha',password=True, can_reveal_password=True)
    eb_confirmar_registrar = ft.ElevatedButton(text='CONFIRMAR')
    #PAG LOGIN
    tf_login = ft.TextField(label='Login', width=300)
    tf_upswd = ft.TextField(label='Senha', password=True, can_reveal_password=True, width=300)
    eb_confirmar_login = ft.ElevatedButton(text='LOGAR', on_click=logar)
    linha_btn_login = ft.Row([eb_home,eb_confirmar_login],alignment=ft.MainAxisAlignment.CENTER)
    col_login = ft.Column(controls=[tf_login,tf_upswd, linha_btn_login], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    #PAG LOGADO
    txt_logado = ft.Text(value='LOGADO COM SUCESSO')

    linha_bemvindo = ft.Row([txt_bemvindo], alignment=ft.MainAxisAlignment.CENTER, spacing=1000)
    linha_bts = ft.Row([eb_login,eb_registrar],alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    pagina.add(linha_bemvindo, linha_bts)

    

ft.app(target=main)