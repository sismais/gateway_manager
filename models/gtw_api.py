# -*- coding: utf-8 -*-
from base64 import b64encode
from odoo.exceptions import UserError
import requests
from requests.exceptions import ConnectTimeout
from odoo import models, fields


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
            response = requests.get(f'{self.get_url()}{endpoint}', headers=self.get_headers())
            if response.status_code == 200:
                return response
            else:
                response.raise_for_status()
        except (ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise e
        except Exception as e:
            json_msg = None
            if isinstance(e, requests.exceptions.RequestException):
                try:
                    json_msg = e.response.json()
                except ValueError:
                    json_msg = e.response.reason
            e.args = ('Erro no GET: ',) + e.args
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def post(self, endpoint, data):
        """ 
        """
        try:
            response = requests.post(f'{self.get_url()}{endpoint}', data=data, headers=self.get_headers())
            if response.status_code == 201:
                return response
            else:
                response.raise_for_status()
        except (ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise e
        except Exception as e:
            json_msg = None
            if isinstance(e, requests.exceptions.RequestException):
                try:
                    json_msg = e.response.json()
                except ValueError:
                    json_msg = e.response.reason

            e.args = ('Erro no POST: ',) + e.args
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def delete(self, endpoint):
        """ 
        """
        try:
            response = requests.delete(f'{self.get_url()}{endpoint}', headers=self.get_headers())
            if response.status_code == 204:
                return response
            else:
                response.raise_for_status()
        except (ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise e
        except Exception as e:
            json_msg = None
            if isinstance(e, requests.exceptions.RequestException):
                try:
                    json_msg = e.response.json()
                except ValueError:
                    json_msg = e.response.reason
            e.args = ('Erro no DELETE: ',) + e.args
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def put(self, endpoint, data):
        """ 
        """
        try:
            response = requests.put(f'{self.get_url()}{endpoint}', data=data, headers=self.get_headers())
            if response.status_code == 200:
                return response
            else:
                response.raise_for_status()
        except (ConnectTimeout, requests.exceptions.ConnectionError) as e:
            raise e
        except Exception as e:
            json_msg = None
            if isinstance(e, requests.exceptions.RequestException):
                try:
                    json_msg = e.response.json()
                except ValueError:
                    json_msg = e.response.reason

            e.args = ('Erro no GET: ',) + e.args
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def get_url(self):
        try:
            obj = self.env['gtw.api'].search([], limit=1)
            return obj.url
        except Exception as e:
            raise UserError(f"Erro ao buscar url base. Por favor, verificar os parâmetros. Erro: {e}")

    
    def get_headers(self):
        try:
            obj = self.env['gtw.api'].search([], limit=1)
            auth = b64encode(f'{obj.usuario}:{obj.senha}'.encode())
            authorization = f'Basic {auth.decode()}'
            return {
                'Authorization': authorization
            }
        except Exception as e:
            raise UserError(f"Erro ao criar headers. Por favor, verificar os parâmetros. Erro: {e}")
