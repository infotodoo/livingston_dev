from odoo import models,fields,api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cost_total = fields.Float('Cost Total', tracking=True)
    quantity = fields.Float('Quantity', tracking=True)
    unit_price = fields.Float('Unit Price', tracking=True)
    price_n_iva = fields.Float('Price Unit without IVA', tracking=True)
    contribution_percentage = fields.Float('Contribution Percentage', tracking=True)

    @api.onchange('partner_id','order_line')
    def _onchage_partner_id(self):
        for record in self:
            if record.partner_id and not record.order_line:
                message = _("Invoice Condition: %s" % record.partner_id.invoice_condition)
                mess= {
                    'title': _('Invoice Condition!'),
                    'message' : message
                      }
                return {'warning': mess}
