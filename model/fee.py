from odoo import models, fields, _, api
import pytz


class Fee(models.Model):
    _name = 'x.fee'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Fee No'), readonly=True, required=True, copy=False, default='New')
    play_day = fields.Date(string=_('Play day'), tracking=True)
    location = fields.Selection([('nvh', 'Sonic Club'), ('cf', 'Đây coffee')], default='cf', tracking=True)
    fee_total = fields.Float(string=_('Fee total (VND)'), tracking=True)
    payer = fields.Many2one('x.player', string=_('Who pay?'), tracking=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True)
    status = fields.Selection([('draft', 'Draft'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='draft',
                              tracking=True)
    note = fields.Text(string=_('Note'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('x.fee') or 'New'
        result = super(Fee, self).create(vals)
        return result
