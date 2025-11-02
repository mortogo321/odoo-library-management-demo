# Library Management Module

A comprehensive library management extension for Odoo that allows you to manage books, members, and borrowing activities.

## Features

### Books Management
- **Catalog Management**: Add, edit, and organize your library's book collection
- **Book Details**: Track ISBN, author, publisher, publication date, pages, and categories
- **Book Status**: Monitor availability (Available, Borrowed, Maintenance, Lost)
- **Cover Images**: Upload book cover images
- **QR Code Generation**: Automatic QR code generation for each book containing ISBN, title, and author
- **Borrowing History**: View complete borrowing history for each book

### Members Management
- **Member Registration**: Register library members with complete contact information
- **Member Types**: Support for Students, Teachers, and Public members
- **Auto-generated Member Numbers**: Automatic member ID generation (MEM00001, MEM00002, etc.)
- **Member Card QR Code**: Automatic QR code generation for member cards
- **Borrowing Tracking**: Track books currently borrowed by each member
- **Member Statistics**: View borrowed books count for each member

### Borrowing System
- **Borrow Books**: Create borrowing records with automatic due date calculation (14 days default)
- **Return Books**: Simple one-click return process
- **Overdue Management**: Automatic overdue detection via scheduled task
- **Borrowing References**: Auto-generated borrowing numbers (BOR00001, BOR00002, etc.)
- **Days Borrowed Calculation**: Automatic calculation of borrowing duration
- **Fine/Penalty System**: Automatic calculation of fines for overdue books ($1 per day default)
- **Fine Payment Tracking**: Track fine payments with payment date

### Reservation System
- **Book Reservations**: Allow members to reserve books that are currently borrowed
- **Auto-generated Reservation Numbers**: (RES00001, RES00002, etc.)
- **Reservation Expiry**: Automatic expiry after 7 days
- **Ready for Pickup**: Automatic notification when reserved book becomes available
- **Complete Reservation**: Convert reservation to borrowing with one click

### Email Notifications
- **Due Date Reminders**: Automatic email 2 days before due date
- **Overdue Notifications**: Email alerts for overdue books with fine amount
- **Reservation Ready**: Email notification when reserved book is available

### Reports & Analytics
- **Book Catalog Report**: PDF report with book details and QR code
- **Member Card**: Printable member card with QR code
- **Borrowing Receipt**: Detailed borrowing receipt with fine information
- **Overdue Books Report**: Comprehensive report of all overdue books with fines

### Security & Access Rights
- **Library User**: Can view books and members, create borrowings and reservations
- **Library Manager**: Full access to all features (create, edit, delete)

### Automated Tasks (Cron Jobs)
- Daily check for overdue books
- Daily due date reminder emails (2 days before)
- Daily check for expired reservations
- Hourly check for available reserved books

### Demo Data
- 6 sample books across different categories
- 3 demo members (student, teacher, public)
- 2 borrowing records (one active, one returned)

## Technical Details

### Models
- `library.book`: Books catalog
- `library.member`: Library members
- `library.borrowing`: Borrowing transactions
- `library.reservation`: Book reservations

### Key Features Demonstrated
- **ORM Operations**: CRUD operations, computed fields, constraints
- **Workflows**: State management (available/borrowed/returned, pending/ready/completed)
- **Sequences**: Auto-numbering for members, borrowings, and reservations
- **Actions**: Button actions, smart buttons, wizard actions
- **Views**: Tree, Form, Search views with filters and grouping
- **Security**: Group-based access control with user roles
- **Scheduled Actions**: Multiple cron jobs for automation
- **Relations**: One2many, Many2one relationships
- **UI Features**: Status bars, decorations, smart buttons, stat buttons
- **QR Code Integration**: Dynamic QR code generation using Python qrcode library
- **Email Integration**: Automated email notifications using mail templates
- **PDF Reports**: QWeb reports for various documents
- **Business Logic**: Fine calculations, overdue detection, reservation expiry

## Module Structure

```
library_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_member.py
│   └── library_borrowing.py
├── views/
│   ├── library_book_views.xml
│   ├── library_member_views.xml
│   ├── library_borrowing_views.xml
│   └── library_menu.xml
├── security/
│   ├── library_security.xml
│   └── ir.model.access.csv
├── data/
│   └── library_demo_data.xml
├── static/
│   └── description/
│       └── icon.png
└── README.md
```

## Requirements
- Odoo 14.0, 15.0, 16.0, or 17.0
- Base module (automatically installed with Odoo)
- Mail module (automatically installed with Odoo)
- Python qrcode library (install via pip: `pip install qrcode[pil]`)

## Version History

### Version 2.0
- Added QR code generation for books and members
- Implemented book reservation system
- Added fine/penalty management for overdue books
- Integrated email notifications
- Created PDF reports (book catalog, member cards, borrowing receipts)
- Added automated cron jobs for reminders and checks

### Version 1.0
- Initial release with basic library management
- Books, members, and borrowing management
- Basic overdue detection

## License
LGPL-3

## Author
Your Name
