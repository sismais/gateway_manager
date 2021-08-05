# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import AccessError, RedirectWarning, UserError, ValidationError

class GtwVpn(models.Model):
    _name = 'gtw.vpn'
    _description = 'VPN sismais'
    _rec_name = 'ip_vpn'

    id_pessoa = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente/Pessoa',
        required=True
    )
    descricao = fields.Char(string='Descrição')
    nome_client_vpn = fields.Char(string='Nome Interno')
    ip_vpn = fields.Char(string='IP VPN')

    @api.model
    def unlink(self, list):
        gtw_api = self.env['gtw.api']
        try:
            for obj_id in list:
                response = gtw_api.delete(f'openvpn/vpns/{obj_id}')
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
        gtw_api = self.env['gtw.api']
        try:
            vpn = super(GtwVpn, self).create(vals_list)
            response = gtw_api.post(f'openvpn/vpns/', data={"id":vpn.id})
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
        gtw_api = self.env['gtw.api']
        try:
            response = gtw_api.get(f'openvpn/vpns/{self.id}/download_file/')
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

    def ping(self):
        gtw_api = self.env['gtw.api']
        try:
            response = gtw_api.get(f'openvpn/vpns/{self.id}/ping/')
            if response.status_code != 200:
                raise Exception(response.json())
        except Exception as e:
            raise AccessError(e.__str__().replace('\\n', '\n'))
        raise RedirectWarning(message=response.json()['message'].__str__().replace('\\n', '\n'), action=self.env.ref('sismais_gateway_manager.gtw_vpn_list').id, button_text='OK')
