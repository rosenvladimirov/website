{
    'name': 'Website sale product only usage attributes',
    'category': 'Website',
    "author" : "Rosen Vladimirov",
    'summary': 'Show product attribust only in use',
    'version': '11.0.1.0',
    'description': "",
    'conflicts': 'website_sales_categories_filters',
    'depends': ['product', 'website_sale'],
    'data': [
        'views/templates.xml',
        'views/product_attribute_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
