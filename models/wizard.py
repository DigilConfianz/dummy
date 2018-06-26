# -*- coding:utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _active_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2one('openacademy.session', string='Session', required=True, default=_active_session)
    attendee_id = fields.Many2many('res.partner', string='Attendees')

    # @api.multi
    def subscribe(self):
        self.session_id.attendee_ids |= self.attendee_id
        return {}

