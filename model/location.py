from odoo import models, fields, _


class Location(models.Model):
    _name = 'x.location'

    name = fields.Char(string=_('Location'))

