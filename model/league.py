from odoo import fields, models, _


class League(models.Model):
    _name = 'x.league'

    name = fields.Char(string=_('Name'), required=True)
    match_ids = fields.One2many('x.match', 'league_id')
    law_id = fields.Many2one('x.league.type')
    player_ids = fields.Many2many('x.player', 'x_player_x_league_rel', 'league_id', 'player_id')
    team_ids = fields.Many2many('x.team', 'x_team_x_league_rel', 'league_id', 'team_id')
    fee_ids = fields.One2many('x.fee', 'league_id')
    total_fee = fields.Float(string=_('Total fee'), compute='compute_fee')


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
