from odoo import models, fields, _, api


class Fund(models.Model):
    _name = 'x.fund'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Fund No'), readonly=True, required=True, copy=False, default='New')
    amount = fields.Float(string=_('Amount'), required=True, tracking=True)
    player_id = fields.Many2one('res.users', index=True, string=_("Player"),
                            default=lambda self: self.env.user, required=True)
    charge_date = fields.Date(string=_('Charge date'), required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string=_('State'), default='draft')
    budget_id = fields.Many2one('x.budget', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('x.fund') or 'New'
        result = super(Fund, self).create(vals)
        return result

    def charge_button(self):
        for record in self:
            record.state = 'done'
            record.budget_id.compute_amount()
