from odoo import models, fields, _, api


class Budget(models.Model):
    _name = 'x.budget'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, copy=False)
    amount = fields.Float(string=_('Amount total (VND)'), compute='compute_amount', required=True, tracking=True)
    fee = fields.Float(string=_('Expenses (VND)'), compute='compute_fee')
    player_id = fields.Many2one('x.player', string=_('Holder'), required=True)
    remain = fields.Float(string=_('Remain (VND)'), compute='compute_remain', store=True)
    status = fields.Selection([('bad', 'Bad'), ('good', 'Good'), ('wealthy', 'Wealthy')], default='good')
    fund_ids = fields.One2many('x.fund', 'budget_id', string=_('Income'))
    fee_ids = fields.One2many('x.fee', 'budget_id', string=_('Outcome'))

    @api.depends('fund_ids')
    def compute_amount(self):
        for record in self:
            record.amount = 0
            if record.fund_ids:
                record.amount = sum(x.amount for x in record.fund_ids if x.state == 'done')

    @api.depends('fee')
    def compute_fee(self):
        for record in self:
            record.fee = 0
            if record.fee_ids:
                record.fee = sum(x.fee_total for x in record.fee_ids if x.state == 'refunded')

    @api.depends('fee_ids')
    def compute_remain(self):
        for record in self:
            record.remain = record.amount - record.fee

    def action_show_income(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.list_fund_action').read()[0]
        action['domain'] = [
            ('budget_id', '=', self.id)
        ]
        action['context'] = {}
        return action

    def action_show_fee(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.list_fee').read()[0]
        action['domain'] = [
            ('budget_id', '=', self.id)
        ]
        action['context'] = {}
        return action
