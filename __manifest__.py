# -*- coding: utf-8 -*-
{
    'name': 'ESATTO',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 1,
    'summary': 'Módulo para ESATTO',
    'description':
    """Etiquetas personalizadas""",
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
        'report/report.xml',
        'report/formato_etiqueta_view.xml'
    ],
    'assets':{},
    'installable': True,
    'auto_install': False,
}
