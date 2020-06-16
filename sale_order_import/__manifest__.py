# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Import",
    "version": "13.0.1.0.0",
    "category": "Sales Management",
    "license": "AGPL-3",
    "summary": "Import RFQ or sale orders from files",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/oca/edi",
    "depends": [
        # OCA/sale-workflow
        "sale_commercial_partner",
        # OCA/edi
        "base_business_document_import",
        # OCA/server-tools
        "onchange_helper",
    ],
    "data": ["wizard/sale_order_import_view.xml"],
    "installable": True,
}
