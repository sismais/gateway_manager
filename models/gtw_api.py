# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api
from odoo.exceptions import UserError
from base64 import b64encode
from requests.exceptions import (
    ConnectTimeout
)


class GtwApi(models.Model):
    _name = 'gtw.api'
    _description = 'API Sismais Gateway Manager'
    _rec_name = 'url'

    url = fields.Char(string='URL base')
    usuario = fields.Char(string='Usuário')
    senha = fields.Char(string='Senha')

    def get(self, endpoint):
        """ 
        """
        try:
            response = requests.get(f'{self.url}{endpoint}', headers=self._get_api_headers())
            if response.status_code == 200:
                return response
            else:
                response.raise_for_status()
        except (ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise e
        except Exception as e:
            json_msg = None
            if isinstance(e, requests.exceptions.RequestException):
                # De acordo com a documentação da Scanntech, se erro=
                # 4XX, pode ser retornado um json com detalhes do erro.
                try:
                    json_msg = e.response.json()
                except ValueError:
                    json_msg = e.response.reason

            e.args = ('Erro no GET: ',) + e.args
            # adiciona o json na mensagem de exception
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def _get_api_headers(self):
        """Retorna o header para o http das requisições"""

        def auth_api():
            """Retorna a autenticação do tipo Basic + usuario:senha (em base64)
            conforme requerido pela Scanntech"""
            auth = b64encode(f'{self.usuario}:{self.senha}'.encode())
            return 'Basic ' + str(auth.decode())

        return {
            'Authorization': auth_api()
        }


