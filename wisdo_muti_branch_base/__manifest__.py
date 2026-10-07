# -*- coding: utf-8 -*-
{
    'name': 'wisdo | multi branch base',
    'description': """
           wisdo | multi branch base
    """,
    'summary': 'wisdo | multi branch base',
    'version': '1.0',
    'category': 'Customer',
    'author': 'wisdo.',
    'company': 'wisdo ',
    'maintainer': 'wisdo.',
    'website': "https://www.wisdo.ly",
    'depends': [
        'account', 
        'base',
        
    ],
    'data': [
        # Security
        # 'security/security_access.xml',
        # 'security/ir.model.access.csv',
        # Wizard
        # 'wizard/customer_statement_view.xml',
        # Report
        # 'report/customer_statement_report_pdf.xml',
        # Views
        # 'views/menus.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
