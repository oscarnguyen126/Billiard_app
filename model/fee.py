from odoo import models, fields, _, api
import pytz


class Fee(models.Model):
    _name = 'x.fee'

    name = fields.Char(string=_('Fee'))
    play_day = fields.Date(string=_('Play day'), tracking=True)
    playing_time = fields.Float(string=_('Playing time'), tracking=True)
    location = fields.Selection([('nvh', 'Sonic Club'), ('cf', 'Đây coffee')], default='cf', tracking=True)
    fee_total = fields.Float(string=_('Fee total'), compute='compute_fee_total', tracking=True)
    payer = fields.Many2one('x.player', string=_('Who pay?'), tracking=True)
    league_id = fields.Many2one('x.league', string=_('League'), tracking=True)

    @api.depends('playing_time')
    def compute_fee_total(self):
        for rec in self:
            rec.fee_total = rec.playing_time * 60000
