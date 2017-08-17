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
        'wizard/shop_order_details.xml',
        'wizard/user_order_details.xml',
        # 'wizard/pos_details.xml',
        'views/bu_orders_report_view.xml',
        'views/shop_views.xml',
        'views/product_views.xml',
        'views/report_shop_saledetails.xml',
        'views/report_user_saledetails.xml',
        'views/bu_report.xml',
        'views/pos_config_views.xml',
        'views/res_users_views.xml',
        'views/pos_order_views.xml',
        'views/bu_assets.xml',
    ],
    'demo': [
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'application': True,
    'Author': "Eman Taha"
}
