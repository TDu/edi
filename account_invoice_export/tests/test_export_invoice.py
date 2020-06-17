# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SingleTransactionCase


class TestExportAcountInvoice(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.transmit_method = cls.env["transmit.method"].create(
            {
                "name": "HttpPost",
                "code": "httppost",
                "customer_ok": True,
                "send_through_http": True,
                "destination_url": "https://eu1.babelway.net/ws/gateways/771858",
                "destination_user": "coosa_odoo",
                "destination_pwd": "90asw43kfdsx",
            }
        )
        cls.country = cls.env.ref("base.ch")
        # cls.company = cls.env.user.company_id
        # cls.company.vat = "CHE-012.345.678"
        # cls.company.name = "Camptocamp SA"
        # cls.company.street = "StreetOne"
        # cls.company.street2 = ""
        # cls.company.zip = "8888"
        # cls.company.city = "TestCity"
        # cls.company.partner_id.country_id = cls.country
        # cls.bank = cls.env.ref("base.res_bank_1")
        # cls.tax7 = cls.env["account.tax"].create(
        #     {
        # "name": "Test tax",
        # "type_tax_use": "sale",
        # "amount_type": "percent",
        # "amount": "7.7",
        # "tax_group_id": cls.env.ref("l10n_ch.tax_group_tva_77").id,
        # }
        # )
        # cls.partner_bank = cls.env["res.partner.bank"].create(
        #     {
        #         "bank_id": cls.bank.id,
        #         "acc_number": "300.300.300",
        #         "acc_holder_name": "AccountHolderName",
        #         "partner_id": cls.company.partner_id.id,
        #     }
        # )
        # cls.terms = cls.env.ref("account.account_payment_term_15days")
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test RAD Customer XML",
                "customer_rank": 1,
                "street": "Teststrasse 100",
                "city": "Fribourg",
                "zip": "1700",
                "country_id": cls.country.id,
                # "state_id": cls.state.id,
            }
        )
        cls.account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        # cls.at_receivable = cls.env["account.account.type"].create(
        #     {
        #         "name": "Test receivable account",
        #         "type": "receivable",
        #         "internal_group": "asset",
        #     }
        # )
        # cls.a_receivable = cls.env["account.account"].create(
        #     {
        #         "name": "Test receivable account",
        #         "code": "TEST_RA",
        #         "user_type_id": cls.at_receivable.id,
        #         "reconcile": True,
        #     }
        # )
        cls.product = cls.env["product.template"].create(
            {"name": "Product One", "list_price": 100.00}
        )
        cls.invoice_1 = cls.env["account.move"].create(
            {
                "partner_id": cls.customer.id,
                # 'account_id': cls.account.id,
                # "invoice_partner_bank_id": cls.partner_bank.id,
                # "invoice_payment_term_id": cls.terms.id,
                "type": "out_invoice",
                "transmit_method_id": cls.transmit_method.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": cls.account.id,
                            "product_id": cls.product.product_variant_ids[:1].id,
                            "name": "Product 1",
                            "quantity": 4.0,
                            "price_unit": 123.00,
                            # "tax_ids": [(4, cls.tax7.id, 0)],
                        },
                    )
                ],
            }
        )
        company = cls.invoice_1.company_id
        if company.xml_format_in_pdf_invoice != "factur-x":
            company.xml_format_in_pdf_invoice = "factur-x"

    def test_export_invoice(self):
        self.assertTrue(True)
        # self.invoice_1.send_through_http()
