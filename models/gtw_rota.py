# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class GtwRota(models.Model):
    _name = 'gtw.rota'
    _description = 'Rotas Sismais'

    id_gtw_subdominio = fields.Many2one(
        comodel_name='gtw.subdominio',
        string='Subdomínio',
        required=True
    )
    porta_origem_inicial = fields.Integer(
        string='Porta Origem Inicial',
        required=True,
        default=80
    )
    porta_origem_final = fields.Integer(string='Porta Origem Final', required=True, default=80)
    porta_destino_inicial = fields.Integer(string='Porta Destino Inicial', required=True, default=80)
    porta_destino_final = fields.Integer(string='Porta Destino Final', required=True, default=80)
    modo_nginx = fields.Selection(selection=[('1', 'Proxy Reverse')], string='Modo Nginx', required=True, default='1')
    descricao = fields.Char(string='Descrição', required=True)
    id_gtw_vpn = fields.Many2one(
        comodel_name='gtw.vpn',
        string='VPN Destino',
        required=True
    )

    @api.model
    def create(self, vals_list):
        gtw_api = self.env['gtw.api']
        try:
            rota = super(GtwRota, self).create(vals_list)
            response = gtw_api.post(f'nginx/configs/', data={
                "id": rota.id,
                "subdominio": rota.id_gtw_subdominio.subdominio,
                "ip_vpn_cliente": rota.id_gtw_vpn.ip_vpn,
                "porta_origem_inicial": rota.porta_origem_inicial,
                "porta_origem_final": rota.porta_origem_final,
                "porta_destino_inicial": rota.porta_destino_inicial,
                "porta_destino_final": rota.porta_destino_final,
                "modo_nginx": rota.modo_nginx
            })
            if response.status_code == 201:
                return rota
            else:
                raise Exception(response.json())
        except Exception as e:
            raise UserError("Erro ao criar a VPN: " + e.__str__())

    @api.model
    def unlink(self, list_ids):
        gtw_api = self.env['gtw.api']
        try:
            for id in list_ids:
                obj = self.env['gtw.rota'].browse(id)
                id_nginx = f'{obj.id}-{obj.id_gtw_subdominio.subdominio}-{obj.id_gtw_vpn.ip_vpn}'
                id_nginx = id_nginx.replace('.', '@')
                response = gtw_api.delete(f'nginx/configs/{id_nginx}')
                if response.status_code == 204:
                    super(GtwRota, obj).unlink()
                else:
                    raise Exception(response.json())
        except Exception as e:
            raise UserError("Erro: " + e.__str__())


    def open_record(self, context=None):
        # first you need to get the id of your record
        # you didn't specify what you want to edit exactly
        rec_id = self.id
        # then if you have more than one form view then specify the form id
        form_id = self.env.ref('sismais_gateway_manager.gtw_rota_form')

        return {
                'type': 'ir.actions.act_window',
                'name': 'Rotas',
                'res_model': 'gtw.rota',
                'res_id': rec_id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_id.id,
                'context': {},  
                # if you want to open the form in edit mode direclty            
                'flags': {'initial_mode': 'edit'},
                'target': 'new',
            }
