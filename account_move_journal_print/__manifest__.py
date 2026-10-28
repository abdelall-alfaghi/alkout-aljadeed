# -*- coding: utf-8 -*-
{
    'name': 'Print Journal Entries',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': """Print any journal entry as a clean PDF voucher with balance check and signature boxes.
    Print Journal Entry, Journal Entry PDF, Journal Voucher Print, Account Move Print,
    Journal Entry Report, Accounting Voucher, Mass Print Journal Entries, Debit Credit Report,
    Analytic Distribution Print, Signature Block, Draft Watermark, Partner Language Report,
    --------
    Journal Entry Report, Print Journal Entries Report in Odoo, Journal Voucher Print,
    Journal Entry Print, Print Journal Entries (PDF), Journal Entry Report Pro,
    Account Move Print, Print Journal Entries, Journal Entry Voucher PDF,
    Odoo 20 Community and Enterprise Ready Tool
    """,
    'description': """
Print Journal Entries
=====================
Odoo has no printable layout for a plain journal entry, yet auditors, managers and
paper files still ask for a signed voucher. This module adds a "Journal Entry" PDF
report to every journal entry, invoice and bill, ready for review and signature.

Key Highlights:
---------------
* Journal Entry PDF in the Print menu of the form and of the list (mass print, one entry per page).
* Header with company layout, entry number, date, journal, reference, partner and status.
* Lines with account code and name, partner, label, analytic distribution, debit and credit.
* Amount in foreign currency column, shown only when a line uses another currency.
* Totals row plus a Balanced / Unbalanced control line with the difference.
* Draft and cancelled entries get a watermark so they are never mistaken for posted ones.
* Prepared by / Checked by / Approved by signature boxes, prepared-by user and print time.
* Second report prints in the partner's language, no settings needed.
    """,
    'author': 'Awins',
    'support': 'odoo.expert.111@gmail.com',
    'depends': ['account'],
    'data': [
        'report/account_move_journal_print_templates.xml',
        'report/account_move_journal_print_reports.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
