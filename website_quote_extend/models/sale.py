# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools import float_is_zero

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_status = fields.Selection(selection=[
                            ('payment_draft', 'Draft'),
                            ('payment_pending', 'Pending payment'),
                            ('payment_authorized', 'Payment is authorized'),
                            ('payment_done', 'Paid'),
                            ('payment_refunding', 'Refunding'),
                            ('payment_refunded', 'Refunded'),
                            ('payment_error', 'Error'),
                            ('payment_cancel', 'Canceled'),
                            ('outgoing_draft', 'Draft'),
                            ('outgoing_waiting', 'Waiting Another Operation'),
                            ('outgoing_confirmed', 'Waiting'),
                            ('outgoing_assigned', 'Ready'),
                            ('outgoing_done', 'Done'),
                            ('outgoing_cancel', 'Cancelled'),
                            ('spedition', 'In Speditor'),
                            ('progress', 'In Progress')
                            ],
                            compute="_state__get")
    website_list_amount = fields.Monetary(string='Website List Amount', readonly=True, compute='_compute_list_amount')

    @api.one
    @api.depends('payment_tx_id','payment_tx_ids', 'picking_ids')
    def _state__get(self):
        if self.payment_tx_id.state == 'done' and self.picking_ids:
            self.order_status = "%s_%s" % ('outgoing', self.picking_ids.filtered(lambda r: r.picking_type_code == 'outgoing').mapped('state')[0])
        elif self.payment_tx_id.state in ['done', 'pending', 'authorized', 'refunding', 'refunded', 'cancel']:
            self.order_status = "%s_%s" % ('payment', self.payment_tx_id.state)
        elif self.order_status == 'outgoing_done':
            self.order_status = 'spedition'
        else:
            self.order_status = 'progress'

    #@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    @api.multi
    def _compute_list_amount(self):
        for order in self:
            for line in order.order_line:
                order.website_list_amount = order.website_list_amount + line.product_uom_qty*(line.website_list_price * (1 - (line.discount or 0.0) / 100.0))


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    website_list_price = fields.Float('Website public price', related="product_id.website_list_price")
    website_price_difference = fields.Boolean('Website price difference', compute='_website_price_difference')

    @api.one
    def _website_price_difference(self):
        price_with = self.product_uom_qty*((1-self.discount / 100.0)*self.website_list_price)
        price_without = self.env.user.has_group('sale.group_show_price_subtotal') and self.price_subtotal or self.price_total
        self.website_price_difference = False if float_is_zero(price_with - price_without, precision_rounding=self.order_id.pricelist_id.currency_id.rounding) else True
