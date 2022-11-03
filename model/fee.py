from odoo import models, fields, _, api
import pytz


class Fee(models.Model):
    _name = 'x.fee'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, copy=False)
    play_day = fields.Date(string=_('Date'), required=True, tracking=True)
    location = fields.Char(required=True, tracking=True)
    fee_total = fields.Float(string=_('Fee total (VND)'), required=True, tracking=True)
    payer = fields.Many2one('x.player', string=_('Who pay?'), required=True, tracking=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True)
    status = fields.Selection([('draft', 'Draft'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='draft',
                              tracking=True)
    note = fields.Text(string=_('Note'))
    budget_id = fields.Many2one('x.budget', string=_('Refund by'))

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('x.fee') or 'New'
    #     result = super(Fee, self).create(vals)
    #     return result
