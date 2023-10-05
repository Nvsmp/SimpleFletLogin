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
            resp_serv = requests.get(f"{os.environ['link_api_login']}{tf_login.value},{tf_upswd.value}")
            print(resp_serv)

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

    linha_bemvindo = ft.Row([txt_bemvindo], alignment=ft.MainAxisAlignment.CENTER, spacing=1000)
    linha_bts = ft.Row([eb_login,eb_registrar],alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    pagina.add(linha_bemvindo, linha_bts)

    

ft.app(target=main)