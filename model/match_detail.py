from odoo import models, fields,_, api


class MatchDetail(models.Model):
    _name = 'x.match.detail'

    player_id = fields.Many2one('x.player', string='Player')
    team_id = fields.Many2one('x.team', string='Team',)
    ball = fields.Integer(string='Balls')
    is_win = fields.Boolean(string='Win')
    x_match_id = fields.Many2one('x.match', string=_('Match'))
    league_id = fields.Many2one(related='x_match_id.league_id', store=True)
    score_win = fields.Integer('Win', compute='compute_score_win', store=True)

    @api.depends('is_win')
    def compute_score_win(self):
        for rec in self:
            rec.score_win = 1 if rec.is_win else 0
