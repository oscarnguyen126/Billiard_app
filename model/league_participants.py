from odoo import models, fields, _, api


class Participants(models.Model):
    _name = 'x.participants'
    _order = 'total_point desc'

    name = fields.Char(compute='compute_name')
    player_id = fields.Many2one('x.player', string=_('Player'), tracking=True)
    team_id = fields.Many2one('x.team', string=_('Team'), trackind=True)
    ball_total = fields.Integer(string=_('Balls'), compute='compute_ball')
    win_total = fields.Integer(string=_('Win'), compute='compute_win')
    total_point = fields.Integer(string=_('Pts'))
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True, required=True)
    match_ids = fields.One2many('x.match.detail', 'participant_id', string=_('Match'))

    @api.depends('player_id')
    def compute_name(self):
        for record in self:
            record.name = ''
            if record.player_id:
                record.name = record.player_id.name
            else:
                if record.team_id:
                    record.name = record.team_id.name

    @api.depends('match_ids')
    def compute_ball(self):
        for record in self:
            record.ball_total = 0
            if record.match_ids:
                record.ball_total = sum(x.ball for x in record.match_ids)

    @api.depends('match_ids')
    def compute_win(self):
        for record in self:
            record.win_total = 0
            if record.match_ids:
                record.win_total = sum(x.score_win for x in record.match_ids)
