from odoo import models, fields


class Team(models.Model):
    _name = 'x.team'

    name = fields.Char()
    player_ids = fields.Many2many('x.player', 'x_player_x_team_rel', 'team_id', 'player_id')
