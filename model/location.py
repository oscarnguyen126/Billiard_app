from odoo import models, fields


class Location(models.Model):
    _name = 'x.location'

    name = fields.Char(string=_('Location'))
    fee = fields.float(string=_('Fee'))
