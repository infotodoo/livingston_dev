# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class ZppReportLine(models.Model):
    _name = 'report.vnr'
    _auto = False
    _description = 'This is the lines in the VNR report'
    _rec_name = 'description'
    
    #name = fields.Char('Mayor Cte',readonly=True)
    default_code = fields.Char('Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    date = fields.Char('Date',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    total_stock = fields.Float('Total Stock',readonly=True)
    total = fields.Float('Total Value',readonly=True)
    unit_price = fields.Float('Unit Value',readonly=True)
    sale_price = fields.Float('Sale price',readonly=True)
    cost_by_sale = fields.Float('Cost by sale Unitary',readonly=True)
    vnr_estimate = fields.Float('VNR estimate',readonly=True)
    unit_adjustment = fields.Float('Unit Adjustment',readonly=True)
    minor = fields.Float('Minor between VNR and CTO',compute="_compute_minor")
    total_adjustment = fields.Float('Total Adjustment',compute="_compute_total_adjustment")
    
    
    @api.depends('unit_adjustment','total')
    def _compute_total_adjustment(self):
        for record in self:
            record.total_adjustment = 0
            if record.total != 0:
                record.total_adjustment = record.total*record.unit_adjustment
        
        
    @api.depends('sale_price','vnr_estimate')
    def _compute_minor(self):
        for record in self:
            if record.vnr_estimate > 0:
                record.minor = record.cost_by_sale
            elif record.vnr_estimate == 0:
                record.minor = 0
            else:
                record.minor = record.sale_price
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_vnr')
        query = """
        CREATE or REPLACE VIEW report_vnr AS(
        
        select 
        row_number() OVER (ORDER BY pp.id) as id,
        --(
        --    select aa.code from
        --    account_account aa letf join product_category pc 
        --    on (pc.property_account_creditor_price_difference_categ = aa.id)
        --    where pp.categ_id = pc.id
        --)as name,
        pp.id as product_id,
        pp.default_code,
        (
            select pt.name from
            product_template pt
            where pp.product_tmpl_id = pt.id
        )as description,
        (
            select to_char(svl.create_date,'DD/MM/YYYY')
            from stock_valuation_layer svl
            where pp.id = svl.product_id
            group by pp.id,to_char(svl.create_date,'DD/MM/YYYY')
        )as date,
        (
            select sum(svl.quantity)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as total_stock,
        (
            select sum(svl.value)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as total,
        (
            select sum(svl.value)/sum(svl.quantity)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as unit_price,
        (
            select sum(ppi.fixed_price)/count(ppi.product_id)
            from product_pricelist_item ppi
            where pp.id = ppi.product_id
        )as sale_price,
            (select  product_id,sum(value) as value,sum(quantity) as quantity  
            from stock_valuation_layer group by product_id) as a,
            (
            select  a.product_id,a.value,a.quantity,
            ROW_NUMBER () OVER (partition by svl.product_id,To_char(svl.create_date, 'DD/MM/YYYY')) as cont_fecha,
            To_char(svl.create_date, 'DD/MM/YYYY') as fecha
            from stock_valuation_layer svl
            join a on a.product_id=svl.product_id
            group by a.product_id,svl.product_id,svl.create_date,a.value,a.quantity
            order by 1
            ) as b,
            ( select product_id,avg(cost_by_sale) as cost from product_pricelist_item  group by product_id ) as c,
            ( select b.product_id,b.fecha,b.value, b.quantity, (b.value/ b.quantity) as prom, 
            c.cost from b full join c on c.product_id=b.product_id where cont_fecha=1) as d,
            (select (case when cost>0 then prom+cost end) as cost from d
        ) as cost_by_sale,
        (
            select sum(value)
            from (
               select (sum(ppi.fixed_price)/count(ppi.product_id)) as value
               from product_pricelist_item ppi
               where pp.id = ppi.product_id

                UNION ALL
                
                select (sum(ppi.cost_by_sale)/count(ppi.product_id) + (
                select sum(svl.value)/sum(svl.quantity) from stock_valuation_layer svl where pp.id = svl.product_id) * (-1)) as value
                from product_pricelist_item ppi
                where pp.id = ppi.product_id
                )as vnr
        )as vnr_estimate,
        (
            select sum(value)
            from (
               select (sum(ppi.fixed_price)/count(ppi.product_id)) as value
               from product_pricelist_item ppi
               where pp.id = ppi.product_id

                UNION ALL
                
                select (sum(ppi.cost_by_sale)/count(ppi.product_id) + (
                select sum(svl.value)/sum(svl.quantity) from stock_valuation_layer svl where pp.id = svl.product_id) * (-1)) as value
                from product_pricelist_item ppi
                where pp.id = ppi.product_id
                )as vnr
        )as unit_adjustment
        from product_product pp
        where 1=1
        );
        """
        self.env.cr.execute(query)
        
    
    def vnr_journal(self):
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        account_obj = self.env['account.move']
        vnr_ids = self.filtered(lambda vnr: vnr.product_id and vnr.unit_price != 0)
        _logger.error('------------------ prelimit_ids----------')
        _logger.error(vnr_ids)
        for record in vnr_ids:
            _logger.error(record.product_id)
            lines = []
            if record.vnr_estimate < 0 and (record.product_id.categ_id.property_stock_valuation_account_id,record.product_id.categ_id.property_stock_account_output_categ_id):
                line = {
                        'name': record.default_code,
                        'debit': 0.00,
                        'credit': abs(record.total_adjustment),
                        'account_id': record.product_id.categ_id.property_stock_valuation_account_id.id
                        #'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                lines.append((0,0,line))
                line = {
                        'name': record.default_code,
                        'debit': abs(record.total_adjustment),
                        'credit': 0.00,
                        'account_id': record.product_id.categ_id.property_stock_account_output_categ_id.id
                        #'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                lines.append((0,0,line))
            elif record.vnr_estimate >= 0 and (record.product_id.categ_id.property_stock_valuation_account_id,record.product_id.categ_id.property_stock_account_output_categ_id):
                line = {
                        'name': record.default_code,
                        'debit': abs(record.total_adjustment),
                        'credit': 0.00,
                        'account_id': record.product_id.categ_id.property_stock_valuation_account_id.id
                        #'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                lines.append((0,0,line))
                line = {
                        'name': record.default_code,
                        'debit': 0.00,
                        'credit': abs(record.total_adjustment),
                        'account_id': record.product_id.categ_id.property_stock_account_output_categ_id.id
                        #'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                lines.append((0,0,line))
            else:
                raise ValidationError(('La cuenta no esta definida en la categoria del producto'))
            if record.product_id:
                acc_move_ids = []
                if lines:
                    move = {
                            'journal_id': record.product_id.categ_id.property_stock_journal.id,
                            'line_ids': lines,
                            'date': fields.Date.today(),
                            'ref': record.product_id.name+'-'+record.default_code,
                            'type': 'entry',
                            }
                    account_move = account_obj.sudo().create(move)
                    acc_move_ids.append(account_move.id)
        res = {'type': 'ir.actions.client','tag': 'display_notification','params': {'title': _('Warning!'),'message': 'Asientos creados con exito','sticky': False, }}
        return res