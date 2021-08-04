# -*- coding: utf-8 -*-
{
    'name': "Sismais Gateway Manager",

    'summary': """
        Gerenciar DNS e VPN Sismais
    """,

    'description': """
        Detalhes...
    """,
    'sequence': '1',

    'author': "Sismais Tecnologia",
    'website': "https://sismais.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'services',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gtw_servidor.xml',
        # 'views/gtw_dominio.xml',
        'views/gtw_subdominio.xml',
        'views/gtw_vpn.xml',
        'views/gtw_rota.xml',
        'views/gtw_api.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'instalable': True,
    'application': True
}
