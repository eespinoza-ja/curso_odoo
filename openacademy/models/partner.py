# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

class Partner(models.Model):
    _inherit = "res.partner"
    instructor = fields.Boolean(string='instructor', required=True)
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)