# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import base64

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError

# from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_send_through_http = fields.Boolean()
    invoice_sending_job_id = fields.Integer()

    def send_through_http(self):
        """ """
        self.ensure_one()
        # Double check the transmition method
        if not self.transmit_method_id.send_through_http:
            # raise UserError(_("Transmit method does not allow HTTP Post"))
            pass
        # Generate the XML to send

        xml_string, level = self.generate_facturx_xml()

        # Generate the report if not yet done ?
        # r = self.env["ir.actions.report"]._get_report_from_name(
        #     "account.report_invoice"
        # )
        # pdf, _ = r.render([self.id])
        # I thought we where sending a pdf with xml inside but no an xml file

        # Generate the url and header to Post
        auth = "{}:{}".format(
            self.transmit_method_id.destination_user,
            self.transmit_method_id.destination_pwd,
        )
        auth64 = base64.encodebytes(auth.encode("ascii"))[:-1]
        headers = {"Authorization": "Basic " + auth64.decode("utf-8")}
        files = {"file": ("test_invoice", xml_string, "application/xml")}

        # Use request to POST the invoice
        res = requests.post(
            self.transmit_method_id.destination_url, headers=headers, files=files
        )
        if res.status_code != 200:
            raise UserError(_("Error POST {}".format(res.status_code)))

        self.invoice_send_through_http = True
