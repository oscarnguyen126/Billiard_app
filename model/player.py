from odoo import models, fields, _


class Player(models.Model):
    _name = 'x.player'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('Player name'), required=True, tracking=True)
    photo = fields.Binary(string=_('photo'))
    bday = fields.Date(string=_("Birth day"), required=True, tracking=True)
    level = fields.Selection([('s', 'S'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], required=True,
                             string="Level", tracking=True)
