# coding: utf-8

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.onchange('payment_transaction_id')
    @api.depends('payment_date')
    def _onchange_payment_transaction_id(self):
        self.payment_transaction_id.write({"state": 'done', "type": 'form', "date_validate": self.payment_date})
