# Odoo Library Management Demo

A complete demo Odoo module showcasing library management functionality with Docker setup for easy testing.

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Port 8069 available

### 1. Start Odoo

```bash
docker-compose up -d
```

### 2. Access Odoo

Open your browser: **http://localhost:8069**

### 3. Create Database

- Master Password: `admin`
- Database Name: `library_demo`
- Email: `admin@example.com`
- Password: `admin`
- Check **"Demo Data"** for sample data
- Click **Create Database**

### 4. Install Library Management Module

1. Go to **Apps** menu
2. Click **Update Apps List** (remove filters if needed)
3. Search for **"Library Management"**
4. Click **Install**

### 5. Test the Module

Go to **Library** menu and explore:
- **Books**: Manage book catalog (6 demo books included)
- **Members**: Register library members (3 demo members included)
- **Borrowings**: Track book borrowing and returns (2 demo records included)

### 6. Stop Odoo

```bash
# Stop containers
docker-compose down

# Stop and remove all data (fresh restart)
docker-compose down -v
```

## Module Features

### Books Management
- Add/edit books with ISBN, author, publisher, pages, categories
- Track book status (Available, Borrowed, Maintenance, Lost)
- Upload cover images
- **Auto-generated QR codes** for each book (ISBN, title, author)
- View borrowing history

### Members Management
- Register members with contact information
- Member types: Student, Teacher, Public
- Auto-generated member numbers (MEM00001, MEM00002...)
- **Auto-generated member card QR codes**
- Track borrowed books per member

### Borrowing System
- Create borrowing records with auto due date (14 days)
- One-click return process
- Automatic overdue detection
- Auto-generated borrowing references (BOR00001, BOR00002...)
- Calculate borrowing duration

### Security
- **Library User**: View books/members, create borrowings
- **Library Manager**: Full access to all features

## Testing the Module

### Create a Book
1. Library > Books > Create
2. Fill in: Title, Author, ISBN, Category
3. Save

### Register a Member
1. Library > Members > Create
2. Fill in: Name, Email, Member Type
3. Note the auto-generated member number
4. Save

### Borrow a Book
1. Library > Borrowings > Create
2. Select book and member
3. Due date auto-calculated (14 days)
4. Save - book status changes to "Borrowed"

### Return a Book
1. Open borrowing record
2. Click **Return Book** button
3. Book status changes back to "Available"

## Technical Details

### Technologies
- **Odoo**: Version 17.0
- **PostgreSQL**: Version 15
- **Docker**: Containerized setup

### Module Structure
```
library_management/
├── models/          # Python models (Book, Member, Borrowing)
├── views/           # XML views (Forms, Trees, Search)
├── security/        # Access rights and groups
├── data/           # Demo data
└── static/         # Module icon
```

### Key Odoo Concepts Demonstrated
- **Models**: ORM, computed fields, constraints
- **Views**: Tree, Form, Search with filters
- **Actions**: Button actions, smart buttons
- **Security**: Group-based access control
- **Sequences**: Auto-numbering
- **Relations**: One2many, Many2one
- **Workflows**: State management
- **Cron Jobs**: Scheduled tasks

## Troubleshooting

### Port already in use
```bash
# Edit docker-compose.yml and change port:
ports:
  - "8070:8069"  # Use 8070 instead
```

### View container logs
```bash
docker-compose logs -f odoo
docker-compose logs -f db
```

### Module not visible
1. Enable Developer Mode: Settings > Activate Developer Mode
2. Apps > Update Apps List
3. Search "Library Management"

### Clean restart
```bash
docker-compose down -v
docker-compose up -d
```

## Project Structure

```
.
├── docker-compose.yml          # Docker setup
├── library_management/         # Odoo module
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   ├── views/
│   ├── security/
│   ├── data/
│   └── README.md
└── README.md                   # This file
```

## Requirements
- Docker & Docker Compose
- ~500MB disk space for images
- Modern web browser

## License
LGPL-3

## Support
This is a demo module for learning Odoo development. For production use, additional features like user authentication, advanced reporting, and notifications would be recommended.
