# -*- coding: utf-8 -*-

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _journal_print_lines(self):
        """Journal items printed on the Journal Entry report (no section/note lines)."""
        self.ensure_one()
        return self.line_ids.filtered(lambda line: line.display_type not in ('line_section', 'line_note'))

    def _journal_print_totals(self):
        """Debit/credit totals in company currency and whether the entry balances."""
        self.ensure_one()
        lines = self._journal_print_lines()
        currency = self.company_currency_id
        debit = sum(lines.mapped('debit'))
        credit = sum(lines.mapped('credit'))
        return {
            'debit': debit,
            'credit': credit,
            'difference': debit - credit,
            'balanced': currency.is_zero(debit - credit),
        }

    def _journal_print_show_amount_currency(self):
        """True when at least one line is expressed in a foreign currency."""
        self.ensure_one()
        return any(line.currency_id and line.currency_id != self.company_currency_id
                   for line in self._journal_print_lines())


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _journal_print_analytic_labels(self):
        """Analytic distribution as readable labels, e.g. ['Project A 60%', 'Project B 40%']."""
        self.ensure_one()
        labels = []
        Analytic = self.env['account.analytic.account'].sudo()
        for key, percentage in (self.analytic_distribution or {}).items():
            account_ids = [int(account_id) for account_id in str(key).split(',') if account_id.strip().isdigit()]
            accounts = Analytic.browse(account_ids).exists()
            if not accounts:
                continue
            name = ' / '.join(accounts.mapped('name'))
            labels.append('%s %s%%' % (name, ('%.2f' % percentage).rstrip('0').rstrip('.')))
        return labels
