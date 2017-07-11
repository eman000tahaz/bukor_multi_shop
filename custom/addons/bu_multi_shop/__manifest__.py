# -*- coding: utf-8 -*-
{
    'name': 'Bukor Multi Shops',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'sequence': 20,
    'summary': 'Bukor Multi Shops',
    'depends': ['product','point_of_sale'],
    'data': [
        'security/shop_security.xml',
        'security/ir.model.access.csv',
        'views/shop_views.xml',
        'views/product_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'Author': "Eman Taha"
}
