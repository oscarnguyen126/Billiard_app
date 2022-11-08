from odoo import models, fields, _


class LeagueType(models.Model):
    _name = 'x.league.type'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, string=_("name"))
    law = fields.Text(string=_("Law"))
    release_date = fields.Datetime(string=_('Release date'))
