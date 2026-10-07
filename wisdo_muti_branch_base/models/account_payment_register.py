from odoo import models, fields, api



# 2️⃣ تعديل wizard لفلترة الجورنال حسب مجموعات المستخدم
class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    available_journal_ids = fields.Many2many(
        'account.journal', 
        compute='_compute_available_journals',
        string='Available Journals'
    )

    journal_id = fields.Many2one(
        'account.journal',
        domain="[('id','in',available_journal_ids)]",
        string='Journal'
    )

    @api.depends()
    def _compute_available_journals(self):
        # استخدم sudo() للوصول لمجموعات المستخدم بدون قيود أمان
        user_groups = self.env.user.sudo().group_ids
        for rec in self:
            rec.available_journal_ids = self.env['account.journal'].sudo().search([
                ('type', 'in', ['cash', 'bank']),
                ('x_allowed_groups', 'in', user_groups.ids)
            ])
