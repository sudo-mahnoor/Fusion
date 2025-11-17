{
    'name': 'Login Background Minimal',
    'version': '19.0.1.0.0',
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['web', 'base_setup'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_bg_minimal/static/src/css/login_background.css',
        ],
        'web.assets_backend': [
            'login_bg_minimal/static/src/css/login_background.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}
