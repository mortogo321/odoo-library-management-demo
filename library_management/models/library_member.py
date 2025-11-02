from odoo import models, fields, api
import base64
import io


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    member_number = fields.Char(string='Member Number', required=True, copy=False, readonly=True, default='New')
    qr_code = fields.Binary(string='QR Code', compute='_compute_qr_code', store=False)
    join_date = fields.Date(string='Join Date', default=fields.Date.today, required=True)
    birth_date = fields.Date(string='Birth Date')
    member_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('public', 'Public'),
    ], string='Member Type', default='public', required=True)
    active = fields.Boolean(string='Active', default=True)

    # Relations
    borrowing_ids = fields.One2many('library.borrowing', 'member_id', string='Borrowing History')
    borrowed_books_count = fields.Integer(string='Borrowed Books', compute='_compute_borrowed_books_count')

    @api.depends('id', 'member_number', 'name')
    def _compute_qr_code(self):
        """Generate QR code for member card containing member information"""
        try:
            import qrcode
        except ImportError:
            for member in self:
                member.qr_code = False
            return

        for member in self:
            if member.id and member.member_number and member.member_number != 'New':
                # Create QR code content with member information
                qr_content = f"MEMBER:{member.member_number}|{member.name}|{member.member_type}"
                if member.email:
                    qr_content += f"|{member.email}"

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
                member.qr_code = base64.b64encode(buffer.getvalue())
            else:
                member.qr_code = False

    @api.depends('borrowing_ids.state')
    def _compute_borrowed_books_count(self):
        for member in self:
            member.borrowed_books_count = len(member.borrowing_ids.filtered(lambda b: b.state == 'borrowed'))

    @api.model
    def create(self, vals):
        if vals.get('member_number', 'New') == 'New':
            vals['member_number'] = self.env['ir.sequence'].next_by_code('library.member') or 'New'
        return super(LibraryMember, self).create(vals)

    def action_view_borrowings(self):
        self.ensure_one()
        return {
            'name': 'Borrowings',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'library.borrowing',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }
