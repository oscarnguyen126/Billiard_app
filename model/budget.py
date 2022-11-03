from odoo import models, fields, _, api


class Budget(models.Model):
    _name = 'x.budget'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, copy=False)
    amount = fields.Float(string=_('Amount total (VND)'), compute='compute_amount', required=True, tracking=True)
    player_id = fields.Many2one('x.player', string=_('Holder'), required=True)
    remain = fields.Float(string=_('Remain (VND)'), compute='compute_remain', store=True)
    status = fields.Selection([('bad', 'Bad'), ('good', 'Good'), ('wealthy', 'Wealthy')], default='good',
                              compute='compute_amount', store=True)
    fund_id = fields.One2many('x.fund', 'budget_id', string=_('Income'))
    fee_ids = fields.One2many('x.fee', 'budget_id', string=_('Outcome'))

    @api.depends('fund_id')
    def compute_amount(self):
        for record in self:
            budget = self.env['x.fund'].search([('budget_id', '=', record.id)])
            record.amount = 0
            if budget:
                record.amount = sum(x.amount for x in budget)

    @api.depends('fee_ids', 'fund_id')
    def compute_remain(self):
        for record in self:
            fees = self.env['x.fee'].search([('budget_id', '=', record.id)])
            budget = self.env['x.fund'].search([('budget_id', '=', record.id)])
            record.remain = record.amount
            if fees or budget:
                record.remain = record.amount - sum(x.fee_total for x in fees if x.status == 'refunded')
            if record.remain < 100000:
                record.status = 'bad'
            elif record.remain > 1000000:
                record.status = 'wealthy'
            else:
                record.status = 'good'
