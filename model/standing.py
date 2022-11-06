from odoo import models, fields, _, api


class Standing(models.Model):
    _name = 'x.standing'

    player_id = fields.Many2one('x.player', string=_('Player'))
    balls = fields.Integer(string=_('Balls'))
    wins = fields.Integer(string=_('Wins'))
    points = fields.Integer(string=_('Pts'))
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True, required=True)
    match_detail_ids = fields.One2many('x.match.detail', 'standing_id')

