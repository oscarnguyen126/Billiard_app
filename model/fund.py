from odoo import models, fields, _, api
from datetime import datetime
from odoo.exceptions import ValidationError


class Fund(models.Model):
    _name = 'x.fund'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Fund No'), readonly=True, required=True, copy=False, default='New')
    amount = fields.Float(string=_('Amount'), required=True, tracking=True)
    player_id = fields.Many2one('x.player', index=True, string=_("Player"), required=True)
    recharge_date = fields.Date(string=_('Recharge date'), required=True, tracking=True, default=datetime.now().strftime("%Y-%m-%d"))
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string=_('State'), default='draft')
    budget_id = fields.Many2one('x.budget')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('x.fund') or 'New'
        result = super(Fund, self).create(vals)
        return result

    def recharge_button(self):
        for record in self:
            record.state = 'done'
            record.budget_id.compute_amount()

    @api.constrains('charge_date')
    def check_recharge_date(self):
        for record in self:
            if record.recharge_date.strftime("%Y-%m-%d") > datetime.now().strftime("%Y-%m-%d"):
                raise ValidationError("Invalid time")
