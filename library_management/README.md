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

### Security & Access Rights
- **Library User**: Can view books and members, create borrowings
- **Library Manager**: Full access to all features (create, edit, delete)

### Demo Data
- 6 sample books across different categories
- 3 demo members (student, teacher, public)
- 2 borrowing records (one active, one returned)

## Technical Details

### Models
- `library.book`: Books catalog
- `library.member`: Library members
- `library.borrowing`: Borrowing transactions

### Key Features Demonstrated
- **ORM Operations**: CRUD operations, computed fields, constraints
- **Workflows**: State management (available/borrowed/returned)
- **Sequences**: Auto-numbering for members and borrowings
- **Actions**: Button actions, smart buttons
- **Views**: Tree, Form, Search views with filters and grouping
- **Security**: Group-based access control
- **Scheduled Actions**: Automatic overdue detection
- **Relations**: One2many, Many2one relationships
- **UI Features**: Status bars, decorations, smart buttons
- **QR Code Integration**: Dynamic QR code generation using Python qrcode library

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

## License
LGPL-3

## Author
Your Name
