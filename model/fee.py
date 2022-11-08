from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Fee(models.Model):
    _name = 'x.fee'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('name'), required=True, copy=False)
    play_day = fields.Date(string=_('Date'), required=True, tracking=True)
    location = fields.Char(string=_('Location'), required=True, tracking=True)
    fee_total = fields.Float(string=_('Fee total (VND)'), required=True, tracking=True)
    payer = fields.Many2one('res.users', index=True, string=_("Who pays?"),
                            default=lambda self: self.env.user, required=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('refunded', 'Refunded')], string=_('State'), default='draft',
                             tracking=True)
    note = fields.Text(string=_('Note'))
    budget_id = fields.Many2one('x.budget', string=_('Refund by'), required=True)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('x.fee') or 'New'
    #     result = super(Fee, self).create(vals)
    #     return result

    def refund_button(self):
        for record in self:
            if record.budget_id.amount < record.fee_total:
                raise ValidationError('The fee is greater than the budget')
            else:
                record.state = 'refunded'
                record.budget_id.compute_fee()
