from odoo import models, fields, api
from datetime import timedelta


class LibraryReservation(models.Model):
    _name = 'library.reservation'
    _description = 'Library Book Reservation'
    _order = 'reservation_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    book_id = fields.Many2one('library.book', string='Book', required=True, ondelete='restrict')
    member_id = fields.Many2one('library.member', string='Member', required=True, ondelete='restrict')
    reservation_date = fields.Date(string='Reservation Date', default=fields.Date.today, required=True)
    expiry_date = fields.Date(string='Expiry Date', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], string='Status', default='pending', required=True)
    notes = fields.Text(string='Notes')
    notification_sent = fields.Boolean(string='Notification Sent', default=False)

    @api.onchange('reservation_date')
    def _onchange_reservation_date(self):
        """Set expiry date to 7 days from reservation"""
        if self.reservation_date:
            self.expiry_date = self.reservation_date + timedelta(days=7)

    @api.model
    def create(self, vals):
        """Generate sequence and check if book is available"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.reservation') or 'New'
        return super(LibraryReservation, self).create(vals)

    def action_cancel(self):
        """Cancel reservation"""
        self.ensure_one()
        self.write({'state': 'cancelled'})
        return True

    def action_mark_ready(self):
        """Mark reservation as ready for pickup"""
        self.ensure_one()
        self.write({'state': 'ready'})
        self._send_ready_notification()
        return True

    def action_complete(self):
        """Complete reservation and create borrowing"""
        self.ensure_one()
        # Create borrowing record
        borrowing = self.env['library.borrowing'].create({
            'book_id': self.book_id.id,
            'member_id': self.member_id.id,
            'borrow_date': fields.Date.today(),
            'due_date': fields.Date.today() + timedelta(days=14),
        })
        self.write({'state': 'completed'})
        return {
            'name': 'Borrowing',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'library.borrowing',
            'res_id': borrowing.id,
        }

    def _send_ready_notification(self):
        """Send email notification when book is ready"""
        self.ensure_one()
        if self.member_id.email and not self.notification_sent:
            template = self.env.ref('library_management.email_template_reservation_ready', raise_if_not_found=False)
            if template:
                template.send_mail(self.id, force_send=True)
                self.notification_sent = True

    @api.model
    def _cron_check_expired_reservations(self):
        """Mark expired reservations"""
        today = fields.Date.today()
        expired_reservations = self.search([
            ('state', 'in', ['pending', 'ready']),
            ('expiry_date', '<', today),
        ])
        expired_reservations.write({'state': 'expired'})

    @api.model
    def _cron_check_available_reserved_books(self):
        """Check if reserved books become available and notify"""
        pending_reservations = self.search([
            ('state', '=', 'pending'),
        ], order='reservation_date asc')

        for reservation in pending_reservations:
            if reservation.book_id.state == 'available':
                reservation.action_mark_ready()
                break  # Only process one reservation per book
