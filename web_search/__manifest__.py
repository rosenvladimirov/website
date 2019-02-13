{
    'name': 'Website Search Autocomplete',
    'category': 'Website',
    'sequence': 10,
    'author': 'D.Jane',
    'summary': 'Website e-commerce search autocomplete with high-light match words and image',
    'version': '1.0.0',
    'description': "Website Search Suggestions",
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/search.xml',
        'views/header.xml'
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.jpg'],
    'license': 'OPL-1',
    'pre_init_hook': 'pre_init_hook',
}
