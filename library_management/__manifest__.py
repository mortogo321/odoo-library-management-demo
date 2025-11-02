{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage library books, members and borrowing',
    'description': """
        Library Management System
        =========================
        This module allows you to:
        * Manage books catalog
        * Track library members
        * Handle book borrowing and returns
        * Monitor overdue books
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['base'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_borrowing_views.xml',
        'views/library_menu.xml',
        'data/library_demo_data.xml',
    ],
    'demo': [
        'data/library_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
