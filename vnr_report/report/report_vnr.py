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
    
    name = fields.Char('Mayor Cte',readonly=True)
    default_code = fields.Char('Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    total_stock = fields.Float('Total Stock',readonly=True)
    total = fields.Float('Total Value',readonly=True)
    unit_price = fields.Float('Unit Value',readonly=True)
    price_unit = fields.Float('Sale Value Unitary',readonly=True)
    sale_price = fields.Float('Sale price',readonly=True)
    cost_by_sale = fields.Float('Cost by sale Unitary',readonly=True)
    vnr_estimate = fields.Float('VNR estimate')
    unit_adjustment = fields.Float('Unit Adjustment')
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
          --  select aa.code from
            --account_account aa letf join product_category pc 
            --on (pc.property_account_creditor_price_difference_categ = aa.id)
            --where pp.categ_id = pc.id
        --)as name,
        pp.default_code,
        (
            select pt.name from
            product_template pt
            where pp.product_tmpl_id = pt.id
        )as description,
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
        (
            select sum(a) 
            --case when sum(a) <= 0 then 0
            --else sum(a)
            --end
            from
                (
                    select (sum(ppi.cost_by_sale)/count(ppi.product_id) + (select sum(svl.value)/sum(svl.quantity) 
                    from stock_valuation_layer svl where pp.id = svl.product_id)) as a
                    from product_pricelist_item ppi
                    where pp.id = ppi.product_id 
                    
                    UNION ALL
                    
                    select ((sum(ppi.cost_by_sale)/count(ppi.product_id)) * (-1)) as a
                    from product_pricelist_item ppi
                    where pp.id = ppi.product_id
                ) as b
        )as cost_by_sale,
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
        
    
    def prelimit_journal(self):
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        account_obj = self.env['account.move']
        prelimit_ids = self.filtered(lambda prelimit: prelimit.cost_cif != 0 and prelimit.cost_mod != 0)
        _logger.error('------------------ prelimit_ids----------')
        _logger.error(prelimit_ids)
        for record in prelimit_ids:
            mod = []
            cif = []
            if record.cost_mod and record.workcenter_id and record.production_id:
                line = {
                        'name': record.production_id.name + ' - ' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        'debit': record.cost_mod,
                        'credit': 0.00,
                        'account_id': record.workcenter_id.mod_account_id_real.id,
                        'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                mod.append((0,0,line))
                line = {
                        'name': record.production_id.name + ' - ' + 'Contrapartida -' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        'debit': 0.00,
                        'credit': record.cost_mod,
                        'account_id': record.workcenter_id.account_mod_id_real.id,
                        'analytic_account_id': record.workcenter_id.account_analytic_real.id
                        }
                mod.append((0,0,line))
            else:
                raise ValidationError(('Costos MOD debe ser diferente de Cero'))
            if record.cost_cif and record.workcenter_id and record.production_id:
            acc_move_ids = []
            if mod:
                move = {
                        'journal_id': record.production_id.product_id.categ_id.property_stock_journal.id,
                        'line_ids': mod,
                        'date': fields.Date.today(),
                        'ref': record.production_id.name + ' - MOD'+' - '+record.workcenter_id.account_analytic_real.name,
                        'type': 'entry',
                        'prelimit_id': record.id
                        }
                account_move = account_obj.sudo().create(move)
                acc_move_ids.append(account_move.id)
            if cif:
                move = {
                        'journal_id': record.production_id.product_id.categ_id.property_stock_journal.id,
                        'line_ids': cif,
                        'date': fields.Date.today(),
                        'ref': record.production_id.name + ' - CIF'+' - '+record.workcenter_id.account_analytic_real.name,
                        'type': 'entry',
                        'prelimit_id': record.id
                        }
                account_move = account_obj.sudo().create(move)
                acc_move_ids.append(account_move.id)
        res = {'type': 'ir.actions.client','tag': 'display_notification','params': {'title': _('Warning!'),'message': 'Asientos creados con exito','sticky': False, }}
        return res