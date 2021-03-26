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
    
    name = fields.Char('Mayor Cte',compute='_compute_name')
    default_code = fields.Char('Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    date = fields.Char('Date',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    total_stock = fields.Float('Total Stock',readonly=True)
    total = fields.Float('Total Value',readonly=True)
    unit_price = fields.Float('Unit Value',readonly=True)
    sale_price = fields.Float('Sale price',readonly=True)
    vnr_estimate = fields.Float('VNR estimate',readonly=True)
    unit_adjustment = fields.Float('Unit Adjustment',readonly=True)
    minor = fields.Float('Minor between VNR and CTO',compute="_compute_minor")
    total_adjustment = fields.Float('Total Adjustment',compute="_compute_total_adjustment")
    test = fields.Float('Cost by sale Unitary',compute='_compute_test')
    
    @api.depends('product_id')
    def _compute_name(self):
        for record in self:
            record.name = ''
            _logger.error('\n name')
            _logger.error(record.name)
            if record.product_id.categ_id.property_stock_valuation_account_id.code:
                record.name = record.product_id.categ_id.property_stock_valuation_account_id.code
                _logger.error(record.name)
    
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
                record.minor = record.test
            elif record.vnr_estimate == 0:
                record.minor = 0
            else:
                record.minor = record.sale_price
                
                
    def _compute_test(self):
        list = []
        query = """
                WITH 

                a as (select  product_id,sum(value) as value,sum(quantity) as quantity  
                from stock_valuation_layer group by product_id),
                b as (select  a.product_id,a.value,a.quantity,
                ROW_NUMBER () OVER (partition by svl.product_id,To_char(svl.create_date, 'DD/MM/YYYY')) as cont_fecha ,
                To_char(svl.create_date, 'DD/MM/YYYY') as fecha
                from stock_valuation_layer svl
                join a on a.product_id=svl.product_id
                group by a.product_id,svl.product_id,svl.create_date,a.value,a.quantity
                order by 1),
                c as ( select product_id,avg(cost_by_sale) as cost 
                from product_pricelist_item  group by product_id ),
                d as( select b.product_id,b.fecha,b.value, b.quantity, (b.value/ b.quantity) as prom, c.cost 
                from b full join c on c.product_id=b.product_id where cont_fecha=1)
                select  d.product_id,(case when cost is null or cost<=0 then 0 else prom+cost  end) as cost from d;
                """
        self.env.cr.execute(query, (tuple(self.ids), ))
        for product_id, cost in self.env.cr.fetchall():
            _logger.error('\n lista')
            list.append([product_id, cost])
            _logger.error(list)
            for record,enumerate in list:
                for product in self:
                    _logger.error('\nlist.product_id')
                    _logger.error(record)
                    if product.product_id.id == record:
                        product.test = enumerate
                        
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_vnr')
        query = """
                CREATE or REPLACE VIEW report_vnr AS(
        
        select 
        row_number() OVER (ORDER BY pp.id) as id,
        pp.id as product_id,
        pp.default_code,
        (date(svl.create_date)) as date,
        (
            select pt.name from
            product_template pt
            where pp.product_tmpl_id = pt.id
        )as description,
        (
        sum(svl.quantity)
        )as total_stock,
        (
        sum(svl.value) 
        )as total,
        (
        sum(svl.value)/sum(svl.quantity)
        )as unit_price,
        (
            select avg(ppi.fixed_price)
            from product_pricelist_item ppi
            where pp.id = ppi.product_id
        )as sale_price,
        (
            select sum(value)
            from (
               select (avg(ppi.fixed_price)) as value
               from product_pricelist_item ppi
               where pp.id = ppi.product_id

                UNION ALL
                
                select (avg(ppi.cost_by_sale) + (
                select sum(svl.value)/sum(svl.quantity) 
                from stock_valuation_layer svl where pp.id = svl.product_id) * (-1)) as value
                from product_pricelist_item ppi
                where pp.id = ppi.product_id
                )as vnr
        )as vnr_estimate,
        (
            select sum(value)
            from (
               select (avg(ppi.fixed_price)) as value
               from product_pricelist_item ppi
               where pp.id = ppi.product_id

                UNION ALL
                
                select (avg(ppi.cost_by_sale) + (
                select sum(svl.value)/sum(svl.quantity) 
                from stock_valuation_layer svl where pp.id = svl.product_id) * (-1)) as value
                from product_pricelist_item ppi
                where pp.id = ppi.product_id
                )as vnr
        )as unit_adjustment
        from product_product pp
        left join stock_valuation_layer svl on (svl.product_id = pp.id)
        where 1=1 
        group by pp.id,date(svl.create_date)
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