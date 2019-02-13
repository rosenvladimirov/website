{
    'name': 'Website quote extend',
    'category': 'Website',
    "author" : "Rosen Vladimirov",
    'summary': 'Added some additional information in website quote',
    'version': '11.0.1.0',
    'description': "",
    'depends': ['account', 'sale', 'sale_payment', 'website_sale', 'website_quote'],
    'data': [
        'views/sale_views.xml',
        'views/stock_picking_templates.xml',
        'views/stock_location_views.xml',
        'views/account_portal_templates.xml',
        'views/website_quote_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
