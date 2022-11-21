from odoo import models, fields,_, api


class MatchDetail(models.Model):
    _name = 'x.match.detail'

    player_id = fields.Many2one('x.player', string='Player')
    team_id = fields.Many2one('x.team', string='Team',)
    ball = fields.Integer(string=_('Balls'))
    is_win = fields.Boolean(string=_('The winner'))
    points = fields.Integer(string=_('Pts'))
    match_id = fields.Many2one('x.match', string=_('Match'))
    league_id = fields.Many2one(related='match_id.league_id', store=True)
    participant_id = fields.Many2one('x.participants')

    @api.model
    def create(self, vals):
        a = self.points
        b = self.ball
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

            matches = self.env['x.match'].search(['&', ('state', '=', 'done'), ('league_id', '=', self.league_id.id)])
            for match in matches:
                if player_league:
                    player_league.ball_total += (self.ball - b) if player_league.ball_total != 0 else self.ball
                    player_league.total_point += (self.points - a) if player_league.total_point != 0 else self.points
                    if self.is_win:
                        player_league.win_total += 1
        return match

    def write(self, vals):
        a = self.points
        b = self.ball
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

            matches = self.env['x.match'].search(['&', ('state', '=', 'done'), ('league_id', '=', self.league_id.id)])
            for match in matches:
                if player_league:
                    player_league.ball_total += (self.ball - b) if player_league.ball_total != 0 else self.ball
                    player_league.total_point += (self.points - a) if player_league.total_point != 0 else self.points
                    if self.is_win:
                        player_league.win_total += 1
        return match
