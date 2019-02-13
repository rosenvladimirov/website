# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Wishlist Fixing',
    'description': 'Let returning shoppers save products in a wishlist',
    'author': 'Rosen Vladimirov',
    'website': 'https://www.odoo.com',
    'category': 'Website',
    'version': '1.0',
    'depends': ['website_sale_extend', 'website_sale_wishlist'],
    'data': [
        'views/website_sale_wishlist_template.xml',
    ],
    'installable': True,
}
