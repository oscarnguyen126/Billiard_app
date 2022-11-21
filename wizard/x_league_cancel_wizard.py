from odoo import models, fields, _


class XLeagueCancelWizard(models.TransientModel):
    _name = 'x.league.cancel.wizard'

    reason = fields.Char(string=_('Input Reason'), required=True)

    def confirm_cancel(self):
        for record in self:
            leagues = self.env['x.league'].browse(self._context.get('active_ids', []))
            if leagues:
                leagues.state = 'cancelled'
                leagues.reason = record.reason
