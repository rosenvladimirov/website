# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.website_quote.controllers.main import sale_quote as website_sale_quote
from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import get_records_pager
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import AccessError
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)

class SaleQuote(website_sale_quote):

    def _get_picking(self, Order, values, **kw):
        pickings = Order.sudo().mapped('picking_ids')

        values.update({
                'pickings': request.env['stock.picking'].sudo().search([('id', 'in', pickings.ids)]).sorted(key=lambda r: r.picking_type_id.sequence),
                })
        return values

    def _get_invoices(self, Order, values, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        partner = request.env.user.partner_id
        domain = [
                ('id', 'in', [x.id for x in Order.invoice_ids]),
                ('type', 'in', ['out_invoice', 'out_refund']),
                ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
                ('state', 'in', ['open', 'paid', 'cancel'])
                ]
        AccountInvoice = request.env['account.invoice']
        _logger.info("Domain %s" % domain)
        searchbar_sortings = {
            'date': {'label': _('Invoice Date'), 'order': 'date_invoice desc'},
            'duedate': {'label': _('Due Date'), 'order': 'date_due desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        archive_groups = CustomerPortal._get_archive_groups(CustomerPortal, 'account.invoice', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        invoice_count = AccountInvoice.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/invoices",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=invoice_count,
            page=page,
            step=CustomerPortal._items_per_page
        )
        # content according to pager and archive selected
        invoices = AccountInvoice.search(domain, order=order, limit=CustomerPortal._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'invoices': invoices,
            'page_name': 'invoice',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/invoices',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,

        })
        return values

    @http.route(['/quote/inv/pdf/<int:order_id>/<token>'], type='http', auth="public", website=True)
    def portal_order_report(self, order_id, token=None, **post):
        if token:
            Order = request.env['sale.order'].sudo().search([('id', '=', order_id), ('access_token', '=', token)])
        else:
            Order = request.env['sale.order'].search([('id', '=', order_id)])

        # print report as sudo, since it require access to taxes, payment term, ... and portal
        # does not have those access rights.
        pdf = request.env.ref('sale.action_report_pro_forma_invoice').sudo().render_qweb_pdf([Order.sudo().id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route('/quote/<int:order_id>/<token>', type='http', auth="public", website=True)
    def view(self, order_id, pdf=None, token=None, message=False, **post):
        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()
        if token:
            Order = request.env['sale.order'].sudo().search([('id', '=', order_id), ('access_token', '=', token)])
        else:
            Order = request.env['sale.order'].search([('id', '=', order_id)])
        # Log only once a day
        if Order and request.session.get('view_quote_%s' % Order.id) != now and request.env.user.share:
            request.session['view_quote_%s' % Order.id] = now
            body = _('Quotation viewed by customer')
            _message_post_helper(res_model='sale.order', res_id=Order.id, message=body, token=Order.access_token, message_type='notification', subtype="mail.mt_note", partner_ids=Order.user_id.sudo().partner_id.ids)
        if not Order:
            return request.render('website.404')

        # Token or not, sudo the order, since portal user has not access on
        # taxes, required to compute the total_amout of SO.
        order_sudo = Order.sudo()

        days = 0
        if order_sudo.validity_date:
            days = (fields.Date.from_string(order_sudo.validity_date) - fields.Date.from_string(fields.Date.today())).days + 1
        if pdf:
            pdf = request.env.ref('website_quote.report_web_quote').sudo().with_context(set_viewport_size=True).render_qweb_pdf([order_sudo.id])[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        transaction_id = request.session.get('quote_%s_transaction_id' % order_sudo.id)
        if not transaction_id:
            Transaction = request.env['payment.transaction'].sudo().search([('reference', '=', order_sudo.name)])
        else:
            Transaction = request.env['payment.transaction'].sudo().browse(transaction_id)
        values = {
            'quotation': order_sudo,
            'message': message and int(message) or False,
            'option': any(not x.line_id for x in order_sudo.options),
            'order_valid': (not order_sudo.validity_date) or (now <= order_sudo.validity_date),
            'days_valid': days,
            'action': request.env.ref('sale.action_quotations').id,
            'no_breadcrumbs': request.env.user.partner_id.commercial_partner_id not in order_sudo.message_partner_ids,
            'tx_id': Transaction.id if Transaction else False,
            'tx_state': Transaction.state if Transaction else False,
            'tx_post_msg': Transaction.acquirer_id.post_msg if Transaction else False,
            'payment_tx': Transaction,
            'need_payment': order_sudo.invoice_status == 'to invoice' and Transaction.state in ['draft', 'cancel', 'error'],
            'token': token,
            'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
        }

        if order_sudo.require_payment or values['need_payment']:
            domain = expression.AND([
                ['&', ('website_published', '=', True), ('company_id', '=', order_sudo.company_id.id)],
                ['|', ('specific_countries', '=', False), ('country_ids', 'in', [order_sudo.partner_id.country_id.id])]
            ])
            acquirers = request.env['payment.acquirer'].sudo().search(domain)

            values['form_acquirers'] = [acq for acq in acquirers if acq.payment_flow == 'form' and acq.view_template_id]
            values['s2s_acquirers'] = [acq for acq in acquirers if acq.payment_flow == 's2s' and acq.registration_view_template_id]
            values['pms'] = request.env['payment.token'].search(
                [('partner_id', '=', order_sudo.partner_id.id),
                ('acquirer_id', 'in', [acq.id for acq in values['s2s_acquirers']])])

            for acq in values['form_acquirers']:
                acq.form = acq.render('/', order_sudo.amount_total, order_sudo.pricelist_id.currency_id.id,
                    values={
                        'return_url': '/quote/%s/%s' % (order_id, token) if token else '/quote/%s' % order_id,
                        'type': 'form',
                        'alias_usage': _('If we store your payment information on our server, subscription payments will be made automatically.'),
                        'partner_id': order_sudo.partner_id.id,
                    })
        history = request.session.get('my_quotes_history', [])
        values.update(get_records_pager(history, order_sudo))
        values = self._get_invoices(Order, values)
        values = self._get_picking(Order, values)
        return request.render('website_quote.so_quotation', values)

website_sale_quote.view = SaleQuote.view
