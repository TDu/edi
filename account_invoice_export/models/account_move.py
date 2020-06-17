# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_sent_through_http = fields.Boolean()
    # invoice_sending_job_id = fields.Integer()

    def send_through_http(self):
        """Send invoice."""
        self.ensure_one()
        if not self.transmit_method_id.send_through_http:
            raise UserError(_("Transmit method does not allow HTTP Post"))
        # Generate the XML to send
        xml_string, level = self.generate_facturx_xml()
        # Generate the PDF report, not needed yet
        # r = self.env["ir.actions.report"]._get_report_from_name(
        #     "account.report_invoice"
        # )
        # pdf, _ = r.render([self.id])

        files = {"file": ("test_invoice", xml_string, "application/xml")}
        headers = self.transmit_method_id.get_transmition_http_header()
        res = requests.post(
            self.transmit_method_id.destination_url, headers=headers, files=files
        )
        if res.status_code != 200:
            values = {
                "job_id": self.invoice_sending_job_id
                or 123,  # Get the job id no need to store it,
                "send_error": res.status_code,
                "transmit_method_name": self.transmit_method_id.name,
            }
            self.log_error_sending_invoice(values)
            raise UserError(
                _(
                    "HTTP error {} sending invoice to {}".format(
                        res.status_code, self.transmit_method_id.name
                    )
                )
            )
        # TODO manage those send flags properly
        self.invoice_sent_through_http = True
        self.invoice_send = True
        self.message_post(
            body=_("Invoice successfuly sent to {}").format(
                self.transmit_method_id.name
            )
        )

    def log_error_sending_invoice(self, values):
        """Log an exception in the chatter of the invoice when job fails

        ToDo if the job run multiple times it should not post mulitple message ?!

        """
        self.ensure_one()
        message = self.env.ref(
            "account_invoice_export.exception_sending_invoice"
        ).render(values=values)
        self.activity_schedule(
            "mail.mail_activity_data_warning",
            summary="Job error sending invoice",
            note=message,
        )
