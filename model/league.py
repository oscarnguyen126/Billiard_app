from odoo import fields, models, _


class League(models.Model):
    _name = 'x.league'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Name'), required=True)
    match_ids = fields.One2many('x.match', 'league_id')
    law_id = fields.Many2one('x.league.type')
    type = fields.Selection([('solo', 'Solo'), ('dual', 'Dual')])
    player_ids = fields.Many2many('x.player', 'x_player_x_league_rel', 'league_id', 'player_id')
    team_ids = fields.Many2many('x.team', 'x_team_x_league_rel', 'league_id', 'team_id')
    fee_ids = fields.One2many('x.fee', 'league_id')
    total_fee = fields.Float(string=_('Total fee'), compute='compute_fee')
    start_date = fields.Date(string=_('Begin on'))
    stop_date = fields.Date(string=_('End on'))
    status = fields.Selection([('progress', 'In progress'), ('completed', 'Completed')], default='progress')
    note = fields.Text(string=_('Note'))

    def compute_fee(self):
        for rec in self:
            rec.total_fee = 0
            fee = self.env['x.fee'].search([('league_id', '=', rec.id)])
            if fee:
                rec.total_fee = sum(x.fee_total for x in fee)

    def action_open_fee(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.list_fee').read()[0]
        action['domain'] = [
            ('league_id', '=', self.id)
        ]
        action['context'] = {}
        return action

    def action_show_matches(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.match_result').read()[0]
        action['domain'] = [
            ('league_id', '=', self.id)
        ]
        action['context'] = {}
        return action
