from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta


class Player(models.Model):
    _name = 'x.player'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Player name'), required=True, tracking=True)
    photo = fields.Binary(string=_('Photo'))
    bday = fields.Date(string=_("Birth day"), required=True, tracking=True)
    place_of_birth = fields.Char(string=_('Place of birth'), required=True, tracking=True)
    age = fields.Integer(string=_('Age'), compute='_compute_age', required=True, tracking=True)
    hand = fields.Selection([('right', 'Right'), ('left', 'Left')])
    phone = fields.Char(string=_('Mobile phone'), tracking=True)

    @api.depends('bday')
    def _compute_age(self):
        for record in self:
            if record.bday and record.bday <= fields.Date.today():
                record.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.bday)).years
            else:
                record.age = 0

    def league_participated(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('billiard_app.league_des').read()[0]
        action['domain'] = [
            ('player_ids', '=', self.id)
        ]
        action['context'] = {}
        return action
