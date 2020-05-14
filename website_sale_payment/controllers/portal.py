# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import consteq
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class CustomerPortal(CustomerPortal):

    @http.route(['/my/quotes/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, res_id, access_token=None, partner_name=None, signature=None):
        if not self._portal_quote_user_can_accept(res_id):
            return {'error': _('Operation not allowed')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo = self._order_check_access(res_id, access_token=access_token)
        except AccessError:
            return {'error': _('Invalid order')}
        if order_sudo.state != 'sent':
            return {'error': _('Order is not in a state requiring customer validation.')}
        if order_sudo.check_payment():
            return {'error': _('Operation not complete. You are not pay the sale order.')}

        order_sudo.action_confirm()

        _message_post_helper(
            res_model='sale.order',
            res_id=order_sudo.id,
            message=_('Order signed by %s') % (partner_name,),
            attachments=[('signature.png', base64.b64decode(signature))] if signature else [],
            **({'token': access_token} if access_token else {}))
        return {
            'success': _('Your Order has been confirmed.'),
            'redirect_url': '/my/orders/%s?%s' % (order_sudo.id, access_token and 'access_token=%s' % order_sudo.access_token or ''),
        }

portal_pager.portal_quote_accept = portal_quote_accept
