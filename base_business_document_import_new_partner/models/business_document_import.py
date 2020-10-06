# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import api, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class BusinessDocumentImport(models.AbstractModel):
    _inherit = "business.document.import"

    @api.model
    def _match_partner(self, partner_dict, chatter_msg, partner_type="supplier"):
        try:
            res = super()._match_partner(partner_dict, chatter_msg, partner_type)
        except UserError:
            # Should be sure it is a not found partner
            if not self._new_partner_must_be_created(partner_dict):
                raise
            partner = self._create_new_partner(partner_dict, partner_type)
            if not partner:
                raise
            return partner
        else:
            return res

    def _new_partner_must_be_created(self, partner_idct):
        """For some logic on should partner be created or not."""
        return True

    def _create_new_partner(self, partner_dict, partner_type):
        """Create new partner base on data from import."""
        new_partner = self.env["res.partner"].create(partner_dict)
        # If it could not be created :
        #   log error, return false, and previous error will be raised
        return new_partner
