from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Match(models.Model):
    _name = 'x.match'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Name'), compute='compute_name', store=True)
    type_league = fields.Selection(related='league_id.type', store=True)
    player1_id = fields.Many2one('x.player', string=_('Player 1'), tracking=True)
    player2_id = fields.Many2one('x.player', string=_('Player 2'), tracking=True)
    line_ids = fields.One2many('x.match.detail', 'x_match_id')
    team_id1 = fields.Many2one('x.team', string=_('Team 1'), tracking=True)
    team_id2 = fields.Many2one('x.team', string=_('Team 2'), tracking=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True, required=True)
    start_time = fields.Date(string=_('Time '), tracking=True)
    location = fields.Selection([('nvh', 'Sonic Club'), ('cf', 'Đây coffee')], tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')

    @api.model
    def create(self, vals_list):
        res = super(Match, self).create(vals_list)
        for record in res:
            if record.league_id.type == 'solo':
                player = record.line_ids.mapped('player_id')
                res.write({
                    'name': ' - '.join([x.name for x in player])
                })
            else:
                team = record.line_ids.mapped('team_id')
                res.write({
                    'name': ' - '.join([x.name for x in team])
                })
            line = self.line_ids.filtered(lambda r: r.is_win)
            if len(line) > 1:
                raise ValidationError('There are 2 winner')
            return res

    def write(self, vals):
        res = super(Match, self).write(vals)
        if vals.get('line_ids'):
            if self.league_id.type == 'solo':
                player = self.line_ids.mapped('player_id')
                self.write({
                    'name': ' - '.join([x.name for x in player])
                })
            else:
                team = self.line_ids.mapped('team_id')
                self.write({
                    'name': ' - '.join([x.name for x in team])
                })

        line = self.line_ids.filtered(lambda r: r.is_win is True)
        if len(line) > 1:
            raise ValidationError('There are 2 winner')
        return res

    @api.constrains('player1_id', 'player2_id')
    def check_duplicate_player(self):
        for record in self:
            if record.player1_id and record.player2_id and record.player1_id == record.player2_id:
                raise ValidationError('Two opponents are the same')

    @api.constrains('team_id1', 'team_id2')
    def check_duplicate_team(self):
        for record in self:
            if record.team_id1 == record.team_id2 and record.team_id1 and record.team_id2:
                raise ValidationError('Two opponents are the same')

    def done_button(self):
        for record in self:
            record.state = 'done'
