from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Participants(models.Model):
    _name = 'x.participants'
    _order = 'total_point desc'

    name = fields.Char(compute='compute_name')
    player_id = fields.Many2one('x.player', string=_('Player'), tracking=True)
    team_id = fields.Many2one('x.team', string=_('Team'), trackind=True)
    ball_total = fields.Integer(string=_('Balls'))
    win_total = fields.Integer(string=_('Win'))
    total_point = fields.Integer(string=_('Pts'))
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True, required=True)
    match_ids = fields.One2many('x.match.detail', 'participant_id', string=_('Match'))
    type = fields.Selection(related='league_id.type', store=True)

    @api.depends('player_id')
    def compute_name(self):
        for record in self:
            record.name = ''
            if record.type == 'solo':
                record.name = record.player_id.name
            else:
                if record.team_id:
                    record.name = record.team_id.name
