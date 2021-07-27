# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError
from .api_sgm import ApiSGM


class GtwVpn(models.Model):
    _name = 'gtw.vpn'
    _description = 'VPN sismais'
    _rec_name = 'ip_vpn'

    id_gtw_subdominio = fields.Many2one(
        comodel_name="gtw.subdominio",
        ondelete='cascade',
        required=True,
        string="Subdomínio"
    )
    descricao = fields.Char(string='Descrição')
    nome_client_vpn = fields.Char(string='Nome Interno')
    ip_vpn = fields.Char(string='IP VPN')
    id_gtw_rota = fields.One2many(comodel_name='gtw.rota', inverse_name='id_gtw_vpn', string='Rotas')
    ovpn_binary = fields.Binary()

    @api.model
    def unlink(self, list):
        api_sgm = ApiSGM()
        try:
            for obj_id in list:
                response = api_sgm.delete(f'openvpn/vpns/{obj_id}')
                if response.status_code == 204:
                    obj = self.env['gtw.vpn'].browse(obj_id)
                    super(GtwVpn, obj).unlink()
                else:
                    raise Exception(response.json())
        except Exception as e:
            raise UserError(e.__str__())
        print(list)
        

    @api.model
    def create(self, vals_list):
        api_sgm = ApiSGM()
        try:
            vpn = super(GtwVpn, self).create(vals_list)
            response = api_sgm.post(f'openvpn/vpns/', data={"id":vpn.id})
            if response.status_code == 201:
                vpn.nome_client_vpn = response.json()['name']
                vpn.ip_vpn = response.json()['ip']
                return vpn
            else:
                raise Exception(response.json())
        except Exception as e:
            raise UserError("Erro ao criar a VPN: " + e.__str__())

    def download_vpn_file(self):
        """ Baixar o arquivo de configuração OVPN """
        api_sgm = ApiSGM()
        try:
            response = api_sgm.get(f'openvpn/vpns/{self.id}/download_file/')
            if response.status_code == 200:  
                result = base64.b64encode(response.content)
                attachment_obj = self.env['ir.attachment'] 
                attachment_id = attachment_obj.create ( 
                    {'name': f"client{self.id}.ovpn", 'datas': result}) 
                download_url ='/web/content/'+ str(attachment_id.id) +'?download=true' 
                return { 
                    "type": "ir.actions.act_url", 
                    "url": str(download_url),
                    "destino": "self", 
                }
        except Exception as e:
            raise UserError("Erro ao tentar baixar o arquivo de configuração OVPN: " + e.__str__())