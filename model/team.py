from odoo import models, fields, api, _


class Team(models.Model):
    _name = 'x.team'

    name = fields.Char(string=_('Team No'), readonly=True, required=True, copy=False, default='New')
    player_ids = fields.Many2many('x.player', 'x_player_x_team_rel', 'team_id', 'player_id')
    league_id = fields.Many2one('x.league', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('x.team') or 'New'
        result = super(Team, self).create(vals)
        return result
