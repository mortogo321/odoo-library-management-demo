from odoo import models, fields, api
from datetime import timedelta


class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Library Borrowing'
    _order = 'borrow_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    book_id = fields.Many2one('library.book', string='Book', required=True, ondelete='restrict')
    member_id = fields.Many2one('library.member', string='Member', required=True, ondelete='restrict')
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today, required=True)
    due_date = fields.Date(string='Due Date', required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], string='Status', default='borrowed', required=True)
    notes = fields.Text(string='Notes')
    days_borrowed = fields.Integer(string='Days Borrowed', compute='_compute_days_borrowed')
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue')

    @api.depends('borrow_date', 'return_date')
    def _compute_days_borrowed(self):
        for borrowing in self:
            if borrowing.return_date and borrowing.borrow_date:
                delta = borrowing.return_date - borrowing.borrow_date
                borrowing.days_borrowed = delta.days
            elif borrowing.borrow_date:
                delta = fields.Date.today() - borrowing.borrow_date
                borrowing.days_borrowed = delta.days
            else:
                borrowing.days_borrowed = 0

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for borrowing in self:
            borrowing.is_overdue = (
                borrowing.state == 'borrowed' and
                borrowing.due_date and
                borrowing.due_date < today
            )

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.due_date = self.borrow_date + timedelta(days=14)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.borrowing') or 'New'

        # Set book status to borrowed
        if vals.get('book_id'):
            book = self.env['library.book'].browse(vals['book_id'])
            book.write({'state': 'borrowed'})

        return super(LibraryBorrowing, self).create(vals)

    def action_return_book(self):
        self.ensure_one()
        self.write({
            'return_date': fields.Date.today(),
            'state': 'returned',
        })
        self.book_id.write({'state': 'available'})
        return True

    def action_mark_overdue(self):
        self.write({'state': 'overdue'})

    @api.model
    def _cron_check_overdue_books(self):
        """Scheduled action to mark overdue borrowings"""
        today = fields.Date.today()
        overdue_borrowings = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '<', today),
        ])
        overdue_borrowings.write({'state': 'overdue'})
