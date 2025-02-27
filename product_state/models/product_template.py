# Copyright 2017-2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    state = fields.Char(
        string="Product Status",
        index=True,
        compute="_compute_product_state",
        inverse="_inverse_product_state",
        readonly=True,
        store=True,
    )
    product_state_id = fields.Many2one(
        comodel_name="product.state",
        string="State",
        help="Select a state for this product",
        group_expand="_read_group_state_id",
        inverse="_inverse_product_state_id",
        default=lambda self: self._get_default_product_state_id(),
        index=True,
        tracking=10,
    )

    def _inverse_product_state_id(self):
        """
        Allow to ease triggering other stuff when product state changes
        without a write()
        """

    @api.model
    def _get_default_product_state_id(self):
        return self.env["product.state"].search([("default", "=", True)], limit=1).id

    @api.depends("product_state_id")
    def _compute_product_state(self):
        for product_tmpl in self:
            product_tmpl.state = product_tmpl.product_state_id.code

    def _inverse_product_state(self):
        ProductState = self.env["product.state"]
        for product_tmpl in self:
            product_state = ProductState.search(
                [("code", "=", product_tmpl.state)], limit=1
            )
            if product_tmpl.state and not product_state:
                product_state = ProductState.create({"name": product_tmpl.state})
            product_tmpl.product_state_id = product_state.id

    @api.model
    def _read_group_state_id(self, states, domain, order):
        return states.search([])
