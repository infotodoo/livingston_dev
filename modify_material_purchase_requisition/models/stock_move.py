from odoo import fields,api,models

class StockMove(models.Model):
    _inherit = 'stock.move'

    inspection_state = fields.Selection([('according','According'),('released','Released'),('inspection','Without Inspection')],'Inspection State')


    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        rslt = super(StockMove,self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
        po_obj = self.env['purchase.order'].search([('name','=',self.origin)])
        if po_obj:
            for line in po_obj.order_line:
                if line.product_id == self.product_id:
                    rslt['debit_line_vals']['analytic_account_id'] = line.account_analytic_id.id
        return rslt