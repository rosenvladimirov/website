# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Customer Portal Extend',
    'summary': 'Customer Portal Expand',
    'category': 'Hidden',
    'description': """
This module adds same field and exned functionaly.""",
    'depends': ['portal', 'account', 'sale', 'purchase', 'website_crm_partner_assign'],
    'data': [
        'views/assets.xml',
        'views/portal_templates.xml',
    ],
    'qweb': [
    ],
}
