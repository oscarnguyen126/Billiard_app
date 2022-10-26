from odoo import models, fields, _


class LeagueType(models.Model):
    _name = 'x.league.type'

    name = fields.Char(required=True)
    law = fields.Text()
    release_date = fields.Datetime(string=_('Release date'))
