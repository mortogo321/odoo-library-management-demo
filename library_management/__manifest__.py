{
    'name': 'Library Management',
    'version': '2.0',
    'category': 'Services',
    'summary': 'Complete library management with QR codes, reservations, fines & notifications',
    'description': """
        Library Management System
        =========================
        This comprehensive module allows you to:
        * Manage books catalog with QR codes
        * Track library members with member cards
        * Handle book borrowing and returns
        * Monitor overdue books with automatic notifications
        * Book reservation system
        * Fine/penalty management for overdue books
        * Email notifications for due dates and overdue books
        * PDF reports for books, members, and borrowings
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail'],
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_borrowing_views.xml',
        'views/library_reservation_views.xml',
        'views/library_menu.xml',
        'reports/library_reports.xml',
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
