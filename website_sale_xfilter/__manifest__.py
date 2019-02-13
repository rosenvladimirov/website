{
    'name': 'Website header x-filter',
    'category': 'Website',
    "author" : "Rosen Vladimirov",
    'sequence': 55,
    'summary': 'Add x-filter in header',
    'version': '11.0.1.0',
    'description': "",
    'depends': ['website', 'website_sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_views.xml',
        'views/website_views.xml',
        'views/website_templates.xml',
        'views/res_config_settings_views.xml',
        #'wizard/website_category_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
