from odoo import fields, models, _, api


class League(models.Model):
    _name = 'x.league'
    _inherit = ['mail.thread']
    _order = 'start_date desc'

    name = fields.Char(string=_('Name'), required=True)
    match_ids = fields.One2many('x.match', 'league_id')
    law_id = fields.Many2one('x.league.type', required=True)
    type = fields.Selection([('solo', 'Solo'), ('dual', 'Dual')], required=True, default='solo')
    player_ids = fields.Many2many('x.player', 'x_player_x_league_rel', 'league_id', 'player_id', string=_('Players'), required=True)
    team_ids = fields.One2many('x.team', 'league_id', string=_('Teams'))
    fee_ids = fields.One2many('x.fee', 'league_id', required=True)
    total_fee = fields.Float(string=_('Total fee'), compute='compute_fee')
    start_date = fields.Date(string=_('Start date'), required=True)
    stop_date = fields.Date(string=_('End date'), required=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('progress', 'In progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft')
    note = fields.Text(string=_('Note'))
    champion = fields.Char(string=_('The champion'))
    location = fields.Char(string=_('Location'))
    total_player = fields.Integer(string='Total player', compute='compute_player', tracking=True)
    participant_ids = fields.One2many('x.participants', 'league_id')

    def compute_fee(self):
        for rec in self:
            rec.total_fee = 0
            fee = self.env['x.fee'].search([('league_id', '=', rec.id)])
            if fee:
                rec.total_fee = sum(x.fee_total for x in fee)

    def action_open_fee(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.list_fee').read()[0]
        action['domain'] = [
            ('league_id', '=', self.id)
        ]
        action['context'] = {}
        return action

    def action_show_matches(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.match_result').read()[0]
        action['domain'] = [
            ('league_id', '=', self.id)
        ]
        action['context'] = {}
        return action

    @api.depends('player_ids')
    def compute_player(self):
        for record in self:
            record.total_player = len(record.player_ids)

    def cancel_league_button(self):
        self.status = 'cancelled'
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://localhost:8014/web#cids=1&menu_id=143&action=164&model=x.league&view_type=list',
            'target': 'self'
        }

    def start_league_button(self):
        self.status = 'progress'

    def end_league_button(self):
        self.status = 'completed'

    @api.onchange('champion')
    def onchange_status(self):
        if self.champion:
            self.status = 'completed'

    # @api.onchange('total_player', 'total_team')
    # def compute_match(self):
    #     for record in self:
    #         if record.total_player:
    #             record.total_matches = (record.total_player - 1) * record.total_player
    #         if record.total_team:
    #             record.total_matches = (record.total_team - 1) * record.total_team
