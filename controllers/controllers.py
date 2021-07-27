# -*- coding: utf-8 -*-
from odoo import http


class SismaisGatewayManager(http.Controller):
    @http.route('/sismais_gateway_manager/sismais_gateway_manager/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/sismais_gateway_manager/sismais_gateway_manager/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('sismais_gateway_manager.listing', {
            'root': '/sismais_gateway_manager/sismais_gateway_manager',
            'objects': http.request.env['sismais_gateway_manager.sismais_gateway_manager'].search([]),
        })

    @http.route('/sismais_gateway_manager/sismais_gateway_manager/objects/<model("sismais_gateway_manager.sismais_gateway_manager"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('sismais_gateway_manager.object', {
            'object': obj
        })
