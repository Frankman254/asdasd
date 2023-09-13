# -*- coding: utf-8 -*-
{
    'name': 'Registo Clientes Web',
    'version': '1.0',
    'summary': 'Módulo simple para mostrar una vista tree',
    'description': """
        Módulo para enviar datos de un formulario web a un modelo de transicion y luego a contactos
    """,
    'category': 'Uncategorized',
    'author': 'Compulab Francisco R',
    'depends': ['base', 'mail', 'website', 'contacts'],  # Dependencia opcional si el módulo utiliza características de otros módulos.
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/views_web.xml',
        'views/form_registration.xml',
        'views/success_confirm.xml',

          # Incluye el archivo de la vista tree
    ],
    'qweb':[
        'views/form_registration.xml',
    ],

    
    'assets':{
        'web.assets_frontend': ['/odoo15-compulab_registro_clientes_moduloweb/static/css/custom_styles.css', '/odoo15-compulab_registro_clientes_moduloweb/static/js/form_registration.js']},
    'installable': True,
    'auto_install': False,
}