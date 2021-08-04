# -*- coding: utf-8 -*-
from validators.domain import domain
import socket
from odoo.exceptions import UserError
from odoo import models, fields, api


class GtwServidor(models.Model):
    _name = 'gtw.servidor'
    _description = 'Servidor Sismais'
    _rec_name = 'descricao'

    descricao = fields.Char(string='Descrição', required=True)
    ip_servidor = fields.Char(string='IP Servidor')
    endereco_dominio = fields.Char(string='Endereço Domínio')
    ativo = fields.Boolean(string='Ativo')

    def name_get(self):
        res = []
        for record in self:
            if record.ip_servidor:
                res.append((record.id, f"{record.ip_servidor} ({record.descricao})"))
            elif record.endereco_dominio:
                res.append((record.id, f"{record.endereco_dominio} ({record.descricao})"))
        return res

    @api.model_create_single
    def create(self, vals_list):
        if 'ip_servidor' in vals_list:
            if vals_list['ip_servidor']:
                try:
                    socket.inet_aton(vals_list['ip_servidor'])
                except socket.error:
                    raise UserError('O IP do servidor não é válido!')
        if 'endereco_dominio' in vals_list:
            if vals_list['endereco_dominio']:
                resp = domain(vals_list['endereco_dominio'])
                if not resp:
                    raise UserError('O endereço de domínio do servidor não é válido!')
        return super(GtwServidor, self).create(vals_list)