# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError
from .api_sgm import ApiSGM


class GtwSubdominio(models.Model):
    _name = 'gtw.subdominio'
    _description = 'Subdomínio sismais'
    _rec_name = 'subdominio'

    ativo = fields.Boolean(string='Ativo')
    id_pessoa = fields.Many2one(comodel_name='res.partner', string='Cliente/Pessoa')
    subdominio = fields.Char(string='Subdomínio')
    id_gtw_dominio = fields.Many2one(
        comodel_name='gtw.dominio',
        string='Domínio',
        ondelete='restrict',
        domain="[('ativo', '=', True)]"
    )
    tipo_apontamento_dns = fields.Selection(
        string='Tipo DNS',
        selection=[('1', 'A'), ('2', 'CNAME')], default='1')
    id_gtw_servidor_destino = fields.Many2one(
        comodel_name='gtw.servidor',
        string='Servidor Destino',
        ondelete='restrict',
        domain="[('ativo', '=', True)]"
    )
    observacao = fields.Text(string='Observação')
    id_gtw_rota = fields.One2many(comodel_name='gtw.rota', inverse_name='id_gtw_subdominio', string='Rotas')

    @api.model
    def create(self, vals_list):
        api = ApiSGM()
        try:
            ip_name_server = ''
            dominio = self.env['gtw.dominio'].browse(vals_list['id_gtw_dominio'])
            servidor = self.env['gtw.servidor'].browse(vals_list['id_gtw_servidor_destino'])
            if vals_list['tipo_apontamento_dns'] == '1':
                ip_name_server = servidor.ip_servidor
            elif vals_list['tipo_apontamento_dns'] == '2':
                ip_name_server = servidor.endereco_dominio
            print(ip_name_server)
            response = api.post(
                f'route53/hosted_zones/{dominio.id_dominio_route53}/record_sets/',
                data={
                    'tipo_apontamento_dns': vals_list['tipo_apontamento_dns'],
                    'name': vals_list['subdominio'],
                    'values': ip_name_server,
                    'ttl': 60,
                    'comment': vals_list['observacao']
                }
            )
            if response.status_code == 201:
                return super(GtwSubdominio, self).create(vals_list)
            else:
                raise Exception(response.json())
        except Exception as e:
            raise AccessError("Erro ao registrar o domínio: " + e.__str__())

    @api.depends('id_gtw_rota')
    def write(self, vals_list):
        api = ApiSGM()
        try:
            id_subdominio_route53 = self.subdominio.replace('.', '@')
            data_update={
                'tipo_apontamento_dns': self.tipo_apontamento_dns,
                'name': vals_list['subdominio'] if 'subdominio' in vals_list.keys() else self.subdominio,
                'records': 
                    self.id_gtw_servidor_destino.ip_servidor \
                    if self.tipo_apontamento_dns == '1' else self.id_gtw_servidor_destino.endereco_dominio,
                'ttl': 60
            }
            response = api.put(
                f"route53/hosted_zones/" \
                f"{self.id_gtw_dominio.id_dominio_route53}/record_sets/{id_subdominio_route53}/",
                data=data_update
            )
            if response.status_code == 200:
                for element in self.id_gtw_rota:
                    print(element)
                return super(GtwSubdominio, self).write(vals_list)
            else:
                raise Exception(response.json())
        except Exception as e:
            raise AccessError("Erro ao registrar o domínio: " + e.__str__())        

    @api.model
    def unlink(self, list_ids):
        """
        Substituir . por @ ao enviar para a api do django, 
        pois o django não aceita o caractere . em ID
        """
        api = ApiSGM()
        try:
            for obj_id in list_ids:
                obj = self.env['gtw.subdominio'].browse(obj_id)
                vpn_obj = self.env['gtw.vpn']
                vpn_ids = vpn_obj.search([('id_gtw_subdominio', '=', obj.id)]).ids
                vpn_obj.unlink(vpn_ids)
                response = api.delete(
                    f"route53/hosted_zones/{obj.id_gtw_dominio.id_dominio_route53}" \
                    f"/record_sets/{obj.subdominio.replace('.', '@')}/"
                )
                if response.status_code == 204:
                    super(GtwSubdominio, obj).unlink()
                else:
                    raise Exception(response.json())
        except Exception as e:
            raise UserError("Erro ao excluir o domínio: " + e.__str__())
