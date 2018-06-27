# -*- coding: utf-8 -*-
{
    'name': 'Bukor Multi Print',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'sequence': 20,
    'summary': 'Bukor Multi Print',
    'depends': ['pos_restaurant'],
    'data': [
            'security/bu_security.xml',
            'views/pos_config_views.xml',
            'views/hide_menus.xml',
    ],
    'qweb': [
        'static/src/xml/pos_restaurant.xml',
    ],
    'installable': True,
    'application': True,
    'Author': "Eman Taha @ Magnum Solutions"
}
