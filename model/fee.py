from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Fee(models.Model):
    _name = 'x.fee'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('name'), required=True, copy=False)
    play_day = fields.Date(string=_('Date'), required=True, tracking=True, default=datetime.now().strftime("%Y-%m-%d"))
    location = fields.Many2one('x.location', string=_('Location'), required=True, tracking=True)
    fee_total = fields.Float(string=_('Fee total (VND)'), required=True, tracking=True)
    payer = fields.Many2one('x.player', index=True, string=_("Who pays?"), required=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('refunded', 'Refunded')], string=_('State'), default='draft',
                             tracking=True)
    note = fields.Text(string=_('Note'))
    budget_id = fields.Many2one('x.budget', string=_('Refund by'), required=True)
    remain = fields.Float(related='budget_id.remain', string=_('Remain of budget'), store=True)
    photo = fields.Binary(string=_('Bill'))

    def refund_button(self):
        for record in self:
            if record.budget_id.remain < record.fee_total:
                raise ValidationError('The fee is greater than the budget')
            else:
                record.state = 'refunded'
                record.budget_id.compute_fee()

    @api.constrains('play_day')
    def check_invoice_date(self):
        for record in self:
            if record.play_day.strftime("%Y-%m-%d") > datetime.now().strftime("%Y-%m-%d"):
                raise ValidationError("Invalid time")
