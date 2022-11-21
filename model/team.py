from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Team(models.Model):
    _name = 'x.team'

    name = fields.Char(string=_('Team No'), copy=False, compute='compute_name', store=True)
    player_ids = fields.Many2many('x.player', 'x_player_x_team_rel', 'team_id', 'player_id')
    league_id = fields.Many2one('x.league')

    @api.depends('name')
    def check_duplicate_team(self):
        teams = self.env['x.team'].search(
            ["&", ('name', '=', self.name), ('id', '!=', self.ids), ('league_id', '=', self.league_id.id)])
        if len(teams) > 0:
            raise ValidationError("Team's name existed")

    @api.depends('player_ids')
    def compute_name(self):
        for record in self:
            record.name = ' & '.join([x.name for x in record.player_ids])
