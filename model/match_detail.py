from odoo import models, fields,_, api
from odoo.exceptions import ValidationError


class MatchDetail(models.Model):
    _name = 'x.match.detail'

    player_id = fields.Many2one('x.player', string='Player')
    team_id = fields.Many2one('x.team', string='Team',)
    ball = fields.Integer(string=_('Balls'))
    is_win = fields.Boolean(string=_('The winner'))
    x_match_id = fields.Many2one('x.match', string=_('Match'))
    league_id = fields.Many2one(related='x_match_id.league_id', store=True)
    participant_id = fields.Many2one('x.participants')

    @api.model
    def create(self, vals):
        match = super(MatchDetail, self).create(vals)
        if vals.get('ball') or vals.get('is_win'):
            player_league = self.env['x.participants']
            if vals.get('player_id'):
                player_league = self.env['x.participants'].search([
                    ('league_id', '=', self.league_id.id),
                    ('player_id', '=', self.player_id.id)
                ], limit=1)
            if vals.get('team_id'):
                player_league = self.env['x.participants'].search([
                    ('league_id', '=', self.league_id.id),
                    ('team_id', '=', self.team_id.id)
                ], limit=1)

            if player_league:
                player_league.ball_total += self.ball
                player_league.match_ids += 1
                if self.is_win:
                    player_league.win_total += 1
        return match

    def write(self, vals):
        match = super(MatchDetail, self).write(vals)
        if vals.get('ball') or vals.get('is_win'):
            player_league = self.env['x.participants']
            if self.player_id:
                player_league = self.env['x.participants'].search([
                    ('league_id', '=', self.league_id.id),
                    ('player_id', '=', self.player_id.id)
                ], limit=1)

            if self.team_id:
                player_league = self.env['x.participants'].search([
                    ('league_id', '=', self.league_id.id),
                    ('team_id', '=', self.team_id.id)
                ], limit=1)

            if player_league:
                player_league.ball_total += self.ball
                player_league.match_ids += 1
                if self.is_win:
                    player_league.win_total += 1
        return match
