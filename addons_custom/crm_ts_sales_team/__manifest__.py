# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Teams',
    'version': '1.1',
    'category': 'Sales/Sales',
    'summary': 'Sales Teams',
    'description': """
Using this application you can manage Sales Teams with crm_ts and/or Sales
=======================================================================
 """,
    'website': 'https://www.odoo.com/app/crm_ts',
    'depends': ['base', 'mail'],
    'data': [
        'security/sales_team_security.xml',
        'security/ir.model.access.csv',
        'data/crm_ts_team_data.xml',
        'views/crm_ts_tag_views.xml',
        'views/crm_ts_team_views.xml',
        'views/crm_ts_team_member_views.xml',
        'views/mail_activity_views.xml',
        ],
    'demo': [
        'data/crm_ts_team_demo.xml',
        'data/crm_ts_tag_demo.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'crm_ts_sales_team/static/**/*',
        ],
    },
    'license': 'LGPL-3',
}
