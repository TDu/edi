# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class TransmitMethod(models.Model):
    _inherit = "transmit.method"

    send_through_http = fields.Boolean()
    destination_url = fields.Char(string="Url")
    destination_user = fields.Char(string="User", copy=False)
    destination_pwd = fields.Char(string="Password", copy=False)
