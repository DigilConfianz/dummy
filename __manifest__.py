{
    'name': 'OpenAcademy',
    'author': 'Digil',
    'licence': 'OPL-1',
    'version': '11.0.1.0',
    'category': '',
    'summary': 'Odoo Docs Building a module',
    'description': 'An implementation of the Odoo docs',
    'maintainer': 'Digil',
    'depends': ['base', 'mail'],
    'data': [
                'views/openacademy.xml',
                'views/partner.xml',
                'security/security.xml',
                'security/ir.model.access.csv',
                'reports/report.xml',
                'views/session_board.xml',
            ],
    # 'demo_xml': ['demo/demo_data.xml'],
    'website': 'www.odoo.com',
    'images': [],
    'installable': 'True',
    'auto install': 'False',
    'application': 'True',
}