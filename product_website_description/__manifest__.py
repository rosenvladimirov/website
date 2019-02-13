# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Description fixing',
    'category': 'Website',
    'sequence': 50,
    'summary': 'Website Description replaces',
    'version': '1.0',
    'description': """
Odoo Website Descriptions
=========================
Replace description_sale with description

        """,
    'depends': ['website_sale'],
    'installable': True,
    'data': [
        'views/product_views.xml',
        'views/templates.xml',
    ],
    'demo': [
    ],
}
