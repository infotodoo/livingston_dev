from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cost_total = fields.Float('Cost Total', tracking=True)
    quantity = fields.Float('Quantity', tracking=True)
    unit_price = fields.Float('Unit Price', tracking=True)
    price_n_iva = fields.Float('Price Unit without IVA', tracking=True)
    contribution_percentage = fields.Float('Contribution Percentage', tracking=True)