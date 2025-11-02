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

    # Fine/Penalty System
    days_overdue = fields.Integer(string='Days Overdue', compute='_compute_days_overdue', store=True)
    fine_per_day = fields.Float(string='Fine per Day', default=1.0)
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount', store=True)
    fine_paid = fields.Boolean(string='Fine Paid', default=False)
    fine_payment_date = fields.Date(string='Fine Payment Date')

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

    @api.depends('due_date', 'return_date', 'state')
    def _compute_days_overdue(self):
        """Calculate days overdue"""
        today = fields.Date.today()
        for borrowing in self:
            if borrowing.state in ['overdue', 'returned'] and borrowing.due_date:
                if borrowing.return_date:
                    # If returned, calculate overdue days until return
                    if borrowing.return_date > borrowing.due_date:
                        delta = borrowing.return_date - borrowing.due_date
                        borrowing.days_overdue = delta.days
                    else:
                        borrowing.days_overdue = 0
                elif borrowing.state == 'overdue':
                    # Still overdue, calculate until today
                    delta = today - borrowing.due_date
                    borrowing.days_overdue = max(0, delta.days)
                else:
                    borrowing.days_overdue = 0
            else:
                borrowing.days_overdue = 0

    @api.depends('days_overdue', 'fine_per_day')
    def _compute_fine_amount(self):
        """Calculate fine amount based on days overdue"""
        for borrowing in self:
            if borrowing.days_overdue > 0:
                borrowing.fine_amount = borrowing.days_overdue * borrowing.fine_per_day
            else:
                borrowing.fine_amount = 0.0

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

    def action_pay_fine(self):
        """Mark fine as paid"""
        self.ensure_one()
        self.write({
            'fine_paid': True,
            'fine_payment_date': fields.Date.today(),
        })
        return True

    @api.model
    def _cron_check_overdue_books(self):
        """Scheduled action to mark overdue borrowings and send email notifications"""
        today = fields.Date.today()
        overdue_borrowings = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '<', today),
        ])
        overdue_borrowings.write({'state': 'overdue'})

        # Send email notifications for newly overdue books
        for borrowing in overdue_borrowings:
            borrowing._send_overdue_notification()

    def _send_overdue_notification(self):
        """Send email notification for overdue book"""
        self.ensure_one()
        if self.member_id.email:
            template = self.env.ref('library_management.email_template_overdue_book', raise_if_not_found=False)
            if template:
                template.send_mail(self.id, force_send=True)

    def _send_due_date_reminder(self):
        """Send email reminder before due date"""
        self.ensure_one()
        if self.member_id.email:
            template = self.env.ref('library_management.email_template_due_date_reminder', raise_if_not_found=False)
            if template:
                template.send_mail(self.id, force_send=True)

    @api.model
    def _cron_send_due_date_reminders(self):
        """Send reminders 2 days before due date"""
        reminder_date = fields.Date.today() + timedelta(days=2)
        borrowings_to_remind = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '=', reminder_date),
        ])
        for borrowing in borrowings_to_remind:
            borrowing._send_due_date_reminder()
