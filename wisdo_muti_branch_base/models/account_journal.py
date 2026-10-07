from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    x_allowed_groups = fields.Many2many(
        'res.groups', string='Allowed Groups'
    )
