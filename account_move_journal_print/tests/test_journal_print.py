# -*- coding: utf-8 -*-

from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged('post_install', '-at_install')
class TestJournalPrint(AccountTestInvoicingCommon):

    REPORT = 'account_move_journal_print.action_report_journal_entry'
    REPORT_LANG = 'account_move_journal_print.action_report_journal_entry_partner_lang'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.company_data['default_journal_misc']
        cls.account_revenue = cls.company_data['default_account_revenue']
        cls.account_expense = cls.company_data['default_account_expense']
        cls.analytic_plan = cls.env['account.analytic.plan'].create({'name': 'Awins Plan'})
        cls.analytic_account = cls.env['account.analytic.account'].create({
            'name': 'Awins Project Alpha',
            'plan_id': cls.analytic_plan.id,
        })
        cls.foreign_currency = cls.env['res.currency'].create({
            'name': 'AWX',
            'symbol': 'AWX$',
            'rounding': 0.01,
        })

    def _create_entry(self, ref, amount, post=True, **line_vals):
        move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': self.journal.id,
            'date': fields.Date.from_string('2024-01-31'),
            'ref': ref,
            'partner_id': self.partner_a.id,
            'line_ids': [
                (0, 0, dict({
                    'name': 'Awins debit line',
                    'account_id': self.account_expense.id,
                    'debit': amount,
                    'credit': 0.0,
                    'analytic_distribution': {str(self.analytic_account.id): 100},
                }, **line_vals)),
                (0, 0, {
                    'name': 'Awins credit line',
                    'account_id': self.account_revenue.id,
                    'debit': 0.0,
                    'credit': amount,
                }),
            ],
        })
        if post:
            move.action_post()
        return move

    def _render(self, report_ref, moves):
        html, report_format = self.env['ir.actions.report']._render_qweb_html(report_ref, moves.ids)
        self.assertEqual(report_format, 'html')
        return html.decode() if isinstance(html, bytes) else html

    def test_report_bound_to_print_menu(self):
        for xmlid in (self.REPORT, self.REPORT_LANG):
            report = self.env.ref(xmlid)
            self.assertEqual(report.model, 'account.move')
            self.assertEqual(report.binding_model_id.model, 'account.move')
            self.assertEqual(report.binding_type, 'report')

    def test_render_single_entry(self):
        move = self._create_entry('AWINS-REF-001', 1234.5)
        html = self._render(self.REPORT, move)
        self.assertIn(move.name, html)
        self.assertIn('AWINS-REF-001', html)
        self.assertIn(self.journal.name, html)
        self.assertIn(self.partner_a.name, html)
        self.assertIn('Awins debit line', html)
        self.assertIn('Awins credit line', html)
        self.assertIn(self.account_expense.code, html)
        self.assertIn(self.account_revenue.name, html)
        self.assertIn('Awins Project Alpha 100%', html)
        # line amounts and both totals
        self.assertEqual(html.count('1,234.50'), 4)
        self.assertIn('Balanced', html)
        self.assertNotIn('Unbalanced', html)
        for label in ('Prepared by', 'Checked by', 'Approved by'):
            self.assertIn(label, html)
        self.assertNotIn('o_journal_entry_watermark', html)
        # no foreign currency on this entry
        self.assertNotIn('Amount in Currency', html)

    def test_analytic_labels_multi_account(self):
        second = self.env['account.analytic.account'].create({
            'name': 'Awins Project Beta',
            'plan_id': self.analytic_plan.id,
        })
        move = self._create_entry('AWINS-REF-ANA', 100.0, post=False, analytic_distribution={
            str(self.analytic_account.id): 60.0,
            str(second.id): 40.0,
        })
        debit_line = move.line_ids.filtered(lambda l: l.debit)
        self.assertEqual(
            sorted(debit_line._journal_print_analytic_labels()),
            ['Awins Project Alpha 60%', 'Awins Project Beta 40%'],
        )
        credit_line = move.line_ids.filtered(lambda l: l.credit)
        self.assertEqual(credit_line._journal_print_analytic_labels(), [])

    def test_mass_print_one_page_per_entry(self):
        moves = self._create_entry('AWINS-MASS-1', 100.0) | self._create_entry('AWINS-MASS-2', 200.0)
        html = self._render(self.REPORT, moves)
        for move in moves:
            self.assertIn(move.name, html)
        self.assertIn('AWINS-MASS-1', html)
        self.assertIn('AWINS-MASS-2', html)
        self.assertEqual(html.count('o_journal_entry_signatures'), 2)
        self.assertEqual(html.count('class="page o_journal_entry_print"'), 2)

    def test_foreign_currency_line(self):
        move = self._create_entry(
            'AWINS-FX', 500.0,
            currency_id=self.foreign_currency.id,
            amount_currency=750.0,
        )
        self.assertTrue(move._journal_print_show_amount_currency())
        html = self._render(self.REPORT, move)
        self.assertIn('Amount in Currency', html)
        self.assertIn('AWX$', html)
        self.assertIn('750.00', html)

    def test_draft_unbalanced_entry(self):
        move = self.env['account.move'].with_context(check_move_validity=False).create({
            'move_type': 'entry',
            'journal_id': self.journal.id,
            'date': fields.Date.from_string('2024-01-31'),
            'line_ids': [
                (0, 0, {'name': 'only debit', 'account_id': self.account_expense.id, 'debit': 80.0, 'credit': 0.0}),
                (0, 0, {'name': 'short credit', 'account_id': self.account_revenue.id, 'debit': 0.0, 'credit': 50.0}),
            ],
        })
        self.assertEqual(move.state, 'draft')
        totals = move._journal_print_totals()
        self.assertFalse(totals['balanced'])
        self.assertAlmostEqual(totals['difference'], 30.0)
        html = self._render(self.REPORT, move)
        self.assertIn('Unbalanced', html)
        self.assertIn('30.00', html)
        self.assertIn('o_journal_entry_watermark', html)

    def test_partner_language_report(self):
        lang = self.env['res.lang']._activate_lang('fr_FR')
        lang.date_format = '%d.%m.%Y'
        self.partner_a.lang = 'fr_FR'
        move = self._create_entry('AWINS-LANG', 10.0)
        html_user = self._render(self.REPORT, move)
        html_partner = self._render(self.REPORT_LANG, move)
        self.assertNotIn('31.01.2024', html_user)
        self.assertIn('31.01.2024', html_partner)
