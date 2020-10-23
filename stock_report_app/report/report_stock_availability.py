# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, tools, api
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

class ReportStockAvailability(models.Model):
    _name = 'report.stock.availability'
    _auto = False
    _description = 'Cuadro de Stock'

    #date = fields.Date(string='Date', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id',readonly=True)
    product_id = fields.Many2one('product.product', string='Producto', readonly=True)
    #product_image = fields.Many2one('product.template', related='product_id.product_tmpl_id',readonly=True)
    #state = fields.Selection([
    #    ('forecast', 'Forecasted Stock'),
    #    ('in', 'Forecasted Receipts'),
    #    ('out', 'Forecasted Deliveries'),
    #], string='State', readonly=True)
    product_qty = fields.Float(compute='_compute_product_qty', string='Cantidad Disponible', readonly=True)
    #move_ids = fields.One2many('stock.move', readonly=True)
    #quant_ids = fields.One2many('stock.quant', 'product_id', readonly=True)
    company_id = fields.Many2one('res.company', related='product_id.product_tmpl_id.company_id', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen', readonly=True)
    product_image = fields.Binary(related='product_id.image_1920', string='imagen', readonly=True)
    product_sale_price = fields.Float(related='product_id.lst_price', string='Precio', readonly=True)
    produce_delay = fields.Float(related='product_id.produce_delay', string='Plazo de Entrega de Fabricación', readonly=True)
    sale_delay = fields.Float(related='product_id.sale_delay', string='Plazo de Entrega del Cliente', readonly=True)
    category_id = fields.Many2one('product.category', related='product_id.product_tmpl_id.categ_id', string='Categoría', readonly=True)

    #product_sold_out = fields.Boolean(related='product_id.sold_out',readonly=True)


    @api.model
    @api.depends('product_id','warehouse_id')
    def _compute_product_qty(self):
        self.ensure_one()
        for rec in self:
            ctx = {'warehouse': rec.warehouse_id.id, 'product_id': rec.product_id.id}
            if rec.product_id.type == 'consu':
                domain = []
                domain.append(('type','=','phantom'))
                domain.append(('product_tmpl_id','=',rec.product_id.product_tmpl_id.id))
                bom_id = self.env['mrp.bom'].search(domain)
                components = self.env['mrp.bom.line'].search([('bom_id','=',bom_id.id)])
                kit_qty_available = 0
                cont = 0
                for bom_line in components:
                    component_stock = bom_line.product_id.with_context(ctx)._compute_quantities_dict_for_sale(lot_id=False, owner_id=False, package_id=False, from_date=False, to_date=False)
                    component_available = int(component_stock.get(bom_line.product_id.id).get('free_qty') / bom_line.product_qty)
                    if not cont:
                        kit_qty_available = component_available
                    if component_available < kit_qty_available and cont:
                        kit_qty_available = component_available
                    cont+=1
                rec.product_qty = kit_qty_available if kit_qty_available else 0

                #if not rec.product_qty:
                #    query = """
                #        delete from report_stock_availability where product_id = %s
                #        and warehouse_id = %s
                #    """ % (rec.product_id.id, rec.warehouse_id.id)
                #    self.env.cr.execute(query)

            elif rec.product_id.type == 'product':
                component_stock = rec.product_id.with_context(ctx)._compute_quantities_dict_for_sale(lot_id=False, owner_id=False, package_id=False, from_date=False, to_date=False)
                kit_qty_available = component_stock.get(rec.product_id.id).get('free_qty')
                rec.product_qty = kit_qty_available if kit_qty_available else 0


    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_availability')
        query = """
            CREATE or REPLACE VIEW report_stock_availability AS (

            select 
                row_number() OVER (ORDER BY stock_report.product_id) as id,
                stock_report.product_id as product_id,
                stock_report.company_id as company_id,
                stock_report.warehouse_id as warehouse_id
            from (
                    SELECT 
                        product.id as product_id,
                        template.company_id as company_id,
                        ware.id as warehouse_id
                    FROM product_product product
                    LEFT JOIN product_template template on product.product_tmpl_id = template.id
                    LEFT JOIN mrp_bom bom on bom.product_tmpl_id = template.id and bom.type = 'phantom'
                    LEFT JOIN mrp_bom_line bomline on bomline.bom_id = bom.id
                    LEFT JOIN stock_move move on bomline.product_id = move.product_id
                    LEFT JOIN stock_warehouse ware on move.warehouse_id = ware.id
                    --LEFT JOIN stock_warehouse ware on true
                    WHERE 1=1
                    and template.company_id = %s
                    and template.type = 'consu'
                    --and product.id = 6793
                    and ware.id is not null
                    and ware.active =True
                    and ware.company_id = %s
                    group by product.id, template.company_id, ware.id

                    UNION ALL 

                    
                    SELECT 
                    product.id as product_id,
                    template.company_id as company_id,
                    ware.id as warehouse_id
                    FROM product_product product
                    LEFT JOIN product_template template on product.product_tmpl_id = template.id
                    LEFT JOIN stock_move move on product.id = move.product_id
                    --LEFT JOIN stock_warehouse ware on true
                    LEFT JOIN stock_warehouse ware on move.warehouse_id = ware.id
                    WHERE 1=1
                    and template.company_id = %s
                    and template.type = 'product'
                    --and product.id = 6793
                    and ware.id is not null
                    and ware.active =True
                    and ware.company_id = %s
                    group by product.id, template.company_id, ware.id

                ) as stock_report
                --left join product_product pro on pro.id = stock_report.product_id
                --left join product_template t on t.id = pro.product_tmpl_id
                --order by t.name
                --LIMIT 100
            );
        """ % (self.env.user.company_id.id, self.env.user.company_id.id, self.env.user.company_id.id, self.env.user.company_id.id)
        self.env.cr.execute(query)

