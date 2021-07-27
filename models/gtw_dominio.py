# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api
from odoo.exceptions import AccessError
from .api_sgm import ApiSGM


class GtwDominio(models.Model):
    _name = 'gtw.dominio'
    _description = 'Domínio Sismais'
    _rec_name = 'dominio'

    dominio = fields.Char(string='Domínio')
    padrao_subdominio = fields.Boolean(string='Subdomínio Padrão')
    observacao = fields.Char(string='Observação')
    ativo = fields.Boolean(string='Ativo')
    id_dominio_route53 = fields.Char('ID Domínio Route53')

    @api.model
    def create(self, vals_list):
        api_sgm = ApiSGM()
        try:
            response = api_sgm.post(
                endpoint='route53/hosted_zones/',
                data={'name': vals_list['dominio'], 'comment': vals_list['observacao']}
            )
            if response.status_code == 201:
                vals_list['id_dominio_route53'] = response.json()['id']
                return super(GtwDominio, self).create(vals_list)
            raise Exception(response.json())
        except Exception as e:
            raise AccessError("Erro ao registrar o domínio: " + e.__str__())        

    def unlink(self):
        api_sgm = ApiSGM()
        try:
            subdominio_obj = self.env['gtw.subdominio']
            subdominio_ids = subdominio_obj.search([('id_gtw_dominio', '=', self.id)]).ids
            subdominio_obj.unlink(subdominio_ids)
            response = api_sgm.delete(f'route53/hosted_zones/{self.id_dominio_route53}/')
            if response.status_code == 204:
                return super(GtwDominio, self).unlink()
            raise Exception(response.json())
        except Exception as e:
            raise AccessError("Erro ao excluir o domínio." + e.__str__())
