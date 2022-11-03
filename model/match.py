from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Match(models.Model):
    _name = 'x.match'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Name'), compute='compute_name', store=True)
    type_league = fields.Selection(related='league_id.type', store=True)
    playing_type = fields.Many2one('x.league')
    player1_id = fields.Many2one('x.player', string=_('Player 1'), tracking=True)
    player2_id = fields.Many2one('x.player', string=_('Player 2'), tracking=True)
    line_ids = fields.One2many('x.match.detail', 'x_match_id')
    team_id1 = fields.Many2one('x.team', string=_('Team 1'), tracking=True)
    team_id2 = fields.Many2one('x.team', string=_('Team 2'), tracking=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True, required=True)
    start_time = fields.Date(string=_('Time '), tracking=True)
    winner = fields.Char(string=_('Winner'), compute='compute_winner')
    location = fields.Selection([('nvh', 'Sonic Club'), ('cf', 'Đây coffee')], tracking=True)
    status = fields.Selection([('draft', 'Draft'), ('progress', 'In progress'), ('completed', 'Completed')],
                              default='draft')

    @api.depends('player1_id', 'player2_id')
    def compute_name(self):
        for record in self:
            record.name = ''
            if record.player1_id and record.player2_id:
                record.name = record.player1_id.name + ' - ' + record.player2_id.name
            else:
                if record.team_id1 and record.team_id2:
                    record.name = record.team_id1.name + ' - ' + record.team_id2.name

    def create_line_ids(self):
        if self.type_league == 'dual':
            vals = [(5, 0, 0), (0, 0, {'team_id': self.team_id1.id}), (0, 0, {'team_id': self.team_id2.id})]
        else:
            vals = [(5, 0, 0), (0, 0, {'player_id': self.player1_id.id}), (0, 0, {'player_id': self.player2_id.id})]
        return vals

    @api.model
    def create(self, vals_list):
        res = super(Match, self).create(vals_list)
        res.write({
            'line_ids': res.create_line_ids()
        })
        return res

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in ['type_league', 'team_id1', 'team_id2', 'player1_id', 'player2_id']):
            for rec in self:
                rec.write({
                    'line_ids': rec.create_line_ids()
                })
        return res

    def compute_winner(self):
        for record in self:
            matches = self.env['x.match.detail'].search([('x_match_id', '=', record.id), ('is_win', '=', True)])
            record.winner = ''
            for match in matches:
                if match.player_id or match.team_id:
                    if match.player_id:
                        record.winner = match.player_id.name
                    if match.team_id:
                        record.winner = match.team_id.name

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

    def check_status(self):
        for record in self:
            if record.line_ids.is_win == True:
                record.status = 'completed'
