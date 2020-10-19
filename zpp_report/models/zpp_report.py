from odoo import _, fields,api, models

class ZppReport(models.Model):
    _name = 'zpp.report'
    _description = 'This is the report ZPP'
    #_inherit = ['mrp.production', 'mrp.workorder','account.analytic.account']
    _rec_name = 'report_name'
    
    report_name = fields.Char('Report Name')
    start_date = fields.Datetime('Start Date')    
    final_date = fields.Datetime('Final Date')
    
    def generate_report(self):
        self.ensure_one()
        #self.line_ids.unlink()
        production_ids = self.env['mrp.production']
        mrp_var_line_obj = self.env['mrp.variation.line']
        domain = []
        if production_ids:
            domain.append(('production_id','in',production_ids.ids))
            domain.append(('date_planned_start','>',self.start_time))
            domain.append(('date_planned_start','<',self.final_time))
            
    
        workorders = self.env['mrp.workorder'].search(domain)
        

        workorder_prog = [x.display_name for x in workorders.filtered(lambda x: x.state == 'progress' and x.working_state in ('normal', 'done'))]
        if workorder_prog:
            raise ValidationError('Las siguientes Ordenes de Trabajo estan en proceso. \n' 
                                    'Por favor bloquearlas para generar el reporte. \n\n'
                                    '%s' % workorder_prog)

        
        var_lines_ids = []
        for workorder in workorders:
            time = sum([x.duration for x in workorder.time_ids])/60
            time_estimated = (workorder.duration_expected)/60
            time_real_operator = sum([x.real_time_operator_line for x in workorder.time_ids])/60

            # plannifiqued = self.production_ids.product_qty
            plannifiqued = workorder.qty_production
            
            if not production_ids.finished_move_line_ids:
                raise ValidationError('Deben haber productos finalizados en la orden seleccionada')
            else:
                produced=workorder.production_id.qty_produced

            # Costos Estandar
            mod_standard = time_estimated * workorder.workcenter_id.costs_hour_mod
            cif_standard = time_estimated * workorder.workcenter_id.costs_hour_cif
            maq_standard = time_estimated * workorder.workcenter_id.costs_hour_maq 
            # Costos Reales
            mod_real = time_real_operator * workorder.workcenter_id.costs_hour_mod_real
            cif_real = time * workorder.workcenter_id.costs_hour_cif_real
            maq_real = time * workorder.workcenter_id.costs_hour_maq_real
            # Costos de Variacion
            mod_variation = ((mod_standard - mod_real)/plannifiqued)*produced
            cif_variation = ((cif_standard - cif_real)/plannifiqued)*produced
            maq_variation = ((maq_standard - maq_real)/plannifiqued)*produced

            # mod_variation = mod_standard - mod_real
            # cif_variation = cif_standard - cif_real
            # maq_variation = maq_standard - maq_real

           
            vals = {
                'variation_id': self.id,
                'workorder_id': workorder.id,
                'production_id': workorder.production_id.id or False,
                'product_id': workorder.product_id.id or False,
                'qty_planned': workorder.qty_production,
                'qty_finished': workorder.qty_produced,
                'state': workorder.state,
                'cif_standard': cif_standard,
                'maq_standard': maq_standard,
                'mod_standard': mod_standard,
                'mod_real': mod_real,
                'cif_real': cif_real,
                'maq_real': maq_real,
                'mod_variation': mod_variation,
                'cif_variation': cif_variation,
                'maq_variation': maq_variation,
            }
            var_line = mrp_var_line_obj.create(vals)
            var_lines_ids.append(var_line.id)

        #  if  len(workorders)>0:
        #      cantidad_esperada = workorder.qty_production   
        #      cantidad_total = [y.qty_finished for y in self.line_ids][-1]
        #      total_real = sum([y.mod_real for y in self.line_ids]) + sum([y.cif_real for y in self.line_ids]) + sum([y.maq_real for y in self.line_ids])  
        #      total_standard = sum([y.mod_standard for y in self.line_ids]) + sum([y.cif_standard for y in self.line_ids]) + sum([y.maq_standard for y in self.line_ids])  
        #      total_variation = sum([y.mod_variation for y in self.line_ids]) + sum([y.cif_variation for y in self.line_ids]) + sum([y.maq_variation for y in self.line_ids])        
            
        #      self.production_ids.total_variation_real = (total_real/cantidad_esperada)*cantidad_total
        #      self.production_ids.total_variation_standard = (total_standard/cantidad_esperada)*cantidad_total
        #      self.production_ids.total_variation_variation = total_variation

        return {
            'type': 'ir.actions.act_window',
            'name': 'Anlálisis de Variaciones',
            # 'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'mrp.variation.line',
            # 'res_id': acc_move_ids,
            'domain': [('id','in',var_lines_ids)],
            'target': 'current'
        }