from datetime import datetime
from odoo import models, fields, _, api


class Budget(models.Model):
    _name = 'x.budget'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('name'), default='New', copy=False)
    amount = fields.Float(string=_('Amount total (VND)'), compute='compute_amount', store=True, tracking=True)
    fee = fields.Float(string=_('Expenses (VND)'), compute='compute_fee', store=True)
    player_id = fields.Many2one('x.player', string=_('Holder'))
    remain = fields.Float(string=_('Remain (VND)'), compute='compute_fee_amount', store=True, copy=False, tracking=True)
    fund_ids = fields.One2many('x.fund', 'budget_id', string=_('Income'))
    fee_ids = fields.One2many('x.fee', 'budget_id', string=_('Outcome'))
    member = fields.Integer(string=_('Member'), compute='compute_member', store=True)
    total_pay_time = fields.Integer(string=_('Paytime'), compute='compute_pay_time', store=True)
    created_day = fields.Date(string=_('Created day'), default=datetime.now().strftime("%Y-%m-%d"))

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('x.budget') or 'New'
        result = super(Budget, self).create(vals)
        return result

    def input_outcome(self):
        for record in self:
            res = {
                'type': 'ir.actions.act_window',
                'name': _('Create Fee'),
                'res_model': 'x.fee',
                'view_mode': 'form',
                'view_id': self.env.ref('billiard_app.fee_form_2').id,
                'context': {
                    'default_budget_id': record.id,
                }
            }
            return res

    def input_income(self):
        for record in self:
            res = {
                'type': 'ir.actions.act_window',
                'name': _('Income'),
                'res_model': 'x.fund',
                'view_mode': 'form',
                'view_id': self.env.ref('billiard_app.fund_form_2').id,
                'context': {
                    'default_budget_id': record.id,
                }
            }
            return res

    @api.depends('fee_ids')
    def compute_pay_time(self):
        for record in self:
            fees = self.env['x.fee'].search(['&', ('state', '=', 'refunded'), ('league_id', '=', record.id)])
            if fees:
                record.total_pay_time = len(fees)

    @api.depends('fund_ids')
    def compute_member(self):
        for record in self:
            record.member = 0
            if record.fund_ids:
                record.member = len(record.fund_ids.mapped('player_id'))

    @api.depends('fund_ids')
    def compute_amount(self):
        for record in self:
            record.amount = 0
            if record.fund_ids:
                record.amount = sum(x.amount for x in record.fund_ids if x.state == 'done')

    @api.depends('fee', 'amount')
    def compute_fee(self):
        for record in self:
            record.fee = 0
            if record.fee_ids:
                record.fee = sum(x.fee_total for x in record.fee_ids if x.state == 'refunded')

    @api.depends('fee', 'amount')
    def compute_fee_amount(self):
        for record in self:
            record.remain = 0
            if record.amount:
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
