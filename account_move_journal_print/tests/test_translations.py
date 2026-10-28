# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestTranslations(TransactionCase):
    """i18n/<lang>.po ships for ten languages; Odoo loads the file of each active language."""

    LABELS = {
        'fr_FR': 'Pièce comptable',
        'es_ES': 'Asiento contable',
        'de_DE': 'Journalbuchung',
        'it_IT': 'Registrazione contabile',
        'pt_BR': 'Lançamento de diário',
        'nl_NL': 'Boeking',
        'zh_CN': '日记账分录',
        'ja_JP': '仕訳',
        'ar_001': 'قيد اليومية',
        'ru_RU': 'Запись в журнале',
    }

    def _load(self, lang):
        self.env['res.lang']._activate_lang(lang)
        self.env['ir.module.module']._load_module_terms(['account_move_journal_print'], [lang], overwrite=True)
        self.env.invalidate_all()

    def _label(self, lang):
        env = self.env(context=dict(self.env.context, lang=lang))
        return self.env.ref('account_move_journal_print.action_report_journal_entry').with_env(env).name

    def test_label_translated_in_every_language(self):
        for lang, label in self.LABELS.items():
            with self.subTest(lang=lang):
                self._load(lang)
                self.assertEqual(self._label(lang), label)

    def test_regional_variant_uses_base_language_file(self):
        # es_MX has no file of its own: Odoo falls back to es.po
        self._load('es_MX')
        self.assertEqual(self._label('es_MX'), self.LABELS['es_ES'])

    def test_language_without_file_stays_english(self):
        self._load('sv_SE')
        self.assertEqual(self._label('sv_SE'), 'Journal Entry')
