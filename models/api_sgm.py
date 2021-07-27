import requests
from base64 import b64encode
from requests.exceptions import (
    ConnectTimeout
)
from .gtw_api import GtwApi


class ApiSGM():
    """
    Classe responsável por centralizar toda comunicação com a API do SGM
    """

    def __init__(self):
        self.url_base = 'https://api-gateway.sismais.net/v1/'
        self._headers = self._get_api_headers()

    def get(self, endpoint):
        """ 
        """
        try:
            response = requests.get(f'{self.url_base}{endpoint}', headers=self._headers)
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

    def post(self, endpoint, data):
        """ 
        """
        try:
            response = requests.post(f'{self.url_base}{endpoint}', data=data, headers=self._headers)
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

            e.args = ('Erro no GET: ',) + e.args
            # adiciona o json na mensagem de exception
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e
    
    def delete(self, endpoint):
        """ 
        """
        try:
            response = requests.delete(f'{self.url_base}{endpoint}', headers=self._headers)
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

            e.args = ('Erro no GET: ',) + e.args
            # adiciona o json na mensagem de exception
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e

    def put(self, endpoint, data):
        """ 
        """
        try:
            response = requests.put(f'{self.url_base}{endpoint}', data=data, headers=self._headers)
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
            # adiciona o json na mensagem de exception
            if json_msg:
                e.args = e.args + (json_msg,)
            raise e


    def _get_api_headers(self):
        """Retorna o header para o http das requisições"""

        def auth_api():
            """Retorna a autenticação do tipo Basic + usuario:senha (em base64)
            conforme requerido pela Scanntech"""
            auth = b64encode('dev:dev@sis2020'.encode())
            return 'Basic ' + str(auth.decode())

        return {
            'Authorization': auth_api()
        }