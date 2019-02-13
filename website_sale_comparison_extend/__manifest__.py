# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Comparison And Product Attribute Category Extend',
    'description': 'Product Comparison, Product Attribute Category and specification table',
    'author': 'Rosen Vladimirov',
    'website': 'https://www.odoo.com',
    'category': 'Website',
    'version': '1.0',
    'depends': ['website_sale_extend', 'website_sale_comparison'],
    'data': [
        'views/website_sale_comparison_template.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
