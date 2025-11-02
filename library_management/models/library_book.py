from odoo import models, fields, api
import base64
import io


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN', copy=False)
    author = fields.Char(string='Author', required=True)
    publisher = fields.Char(string='Publisher')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Number of Pages')
    category = fields.Selection([
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ], string='Category', default='other')
    description = fields.Text(string='Description')
    cover_image = fields.Binary(string='Cover Image')
    qr_code = fields.Binary(string='QR Code', compute='_compute_qr_code', store=False)
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('maintenance', 'Maintenance'),
        ('lost', 'Lost'),
    ], string='Status', default='available', required=True)
    active = fields.Boolean(string='Active', default=True)

    # Relations
    borrowing_ids = fields.One2many('library.borrowing', 'book_id', string='Borrowing History')
    current_borrower_id = fields.Many2one('library.member', string='Current Borrower', compute='_compute_current_borrower', store=True)

    @api.depends('id', 'isbn', 'name')
    def _compute_qr_code(self):
        """Generate QR code for book containing ISBN or ID and title"""
        try:
            import qrcode
        except ImportError:
            for book in self:
                book.qr_code = False
            return

        for book in self:
            if book.id:
                # Create QR code content with book information
                qr_content = f"BOOK-{book.id}"
                if book.isbn:
                    qr_content = f"ISBN:{book.isbn}"
                qr_content += f"|{book.name}|{book.author}"

                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_content)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                book.qr_code = base64.b64encode(buffer.getvalue())
            else:
                book.qr_code = False

    @api.depends('borrowing_ids.state')
    def _compute_current_borrower(self):
        for book in self:
            active_borrowing = book.borrowing_ids.filtered(lambda b: b.state == 'borrowed')
            book.current_borrower_id = active_borrowing[0].member_id if active_borrowing else False

    @api.constrains('pages')
    def _check_pages(self):
        for book in self:
            if book.pages and book.pages <= 0:
                raise models.ValidationError('Number of pages must be positive!')

    def action_set_available(self):
        self.write({'state': 'available'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})
