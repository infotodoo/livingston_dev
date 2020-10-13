# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,date,timedelta

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    val_req_contact = fields.Boolean(string="Valid requirements")
    tiket_number_contract = fields.Char(string='Ticket number Legal management')
    maintenance_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Maintenance Equipment',
        )
    equipment_model = fields.Char(string='Model')
    equipment_serial = fields.Char(string='Brand')
    # equipment_customer = fields.Char(string='Equipment related customer')
    equipment_supplier = fields.Char(string='Supplier associated to the guarantee')
    guarantee_reply = fields.Char(string='Guarantee reply')
    inventory_ubication = fields.Selection([('product in cellar', 'product in cellar'),('product at supplier location','product at supplier location')], string='Inventory ubication')
    customer_response = fields.Char(string='Customer response')

################################################################################################
    ##########################################################################################################################

    ticket_type = fields.Selection([('incidents', 'Incidente'),('request','Solicitud')], string='Ticket type')
    service_id = fields.Many2one('helpdesk.service', string="Servicio", domain="[('team_id', '=?', team_id)]")
    subservice_id = fields.Many2one('helpdesk.subservice', string="Subservicio", domain="[('service_id', '=?', service_id)]")
    type_ticket_id = fields.Many2one('helpdesk.type', string="Ticket type" )
    activity_id = fields.Many2one('helpdesk.activity', string="Actividad", domain="[('subservice_id', '=?', subservice_id),('ticket_type', '=?', ticket_type)]") 
    problem = fields.Many2one('helpdesk.problem', string="Problem")
    helpdesk_id = fields.Many2one('helpdesk.helpdesk', string="Problem")
    team_id = fields.Many2one('helpdesk.team', string="Equipo de ayuda")
########################################################################################################
    group_users_id = fields.Many2one('helpdesk.groupusers', string="Group Users", related='activity_id.group_users_id')
    material_type = fields.Many2one('helpdesk.material.type', string="Tipo Material")
######################################################################################################

    team_name = fields.Selection([('incidents', 'Incidente'),('request','Solicitud')], string='Ticket type')
    service_incident = fields.Selection([('SOPORTE', 'SOPORTE USUARIO'),
                                      ('INFRAESTRUCTURA', 'INFRAESTRUCTURA'),
                                      ('TELECOMUNICACIONES', 'TELECOMUNICACIONES Y REDES'),
                                      ('TTI', 'TTI'),
                                      ('INCIDENTE', 'INCIDENTE INFORMATICO')], string="Incidente")

    service_request = fields.Selection([('MICROINFORMATICA', 'MICROINFORMATICA'),
                                      ('INFRAESTRUCTURA', 'INFRAESTRUCTURA'),
                                      ('TELECOMUNICACIONES', 'TELECOMUNICACIONES Y REDES'),
                                      ('ASESORÍA', 'ASESORÍA Y ACOMPAÑAMIENTO'),
                                      ('GESTIÓN', 'GESTIÓN DE CAMBIOS'),
                                      ('PRUEBAS', 'PRUEBAS DE DPR'),
                                      ('BACKUP', 'BACKUP Y COPIAS'),
                                      ('DESARROLLO', 'DESARROLLO E INGENIERÍA DE SOFTWARE')], string="Incidente")

    sub_service_incident = fields.Selection([('user_failure', 'FALLO DE USUARIO'),
                                      ('device_failure', 'FALLA DISPOSITIVOS E IMPRESORAS'),
                                      ('software_failure', 'FALLA EN PROGRAMA')], string="Sub Service")
    
    sub_service_request = fields.Selection([('management_user', 'GESTIÓN DE USUARIO'),
                                      ('management_software', 'GESTIÓN DE PROGRAMAS'),
                                      ('management_device', 'GESTIÓN DE EQUIPOS')], string="Sub Service")
    
    activity_detail = fields.Selection([('usuario', 'Creación de usuario de dominio Windows'),
                                      ('modificacion', 'Modificación de usuario de dominio Windows'),
                                      ('aplicaion', 'Creación de usuario Aplicación'),
                                      ('sap', 'Creación Usuario SAP')], string="Activity")
    
    software = fields.Selection([('development', 'DESARROLLO DE SOFTWARE '),
                                      ('change', 'GESTIÓN DE CAMBIO'),
                                      ('tecnology', 'INFRAESTRUCTURA DE TECNOLOGÍA'),
                                      ('turrisystem', 'SOFTWARE TURRISYTEM')], string="Software")


    team_users = fields.Many2one('helpdesk.users', string="Servicio")
    users_id = fields.Many2one('res.users', string="Service")
    departament = fields.Char(compute='_get_department_user', string='Departamento')
    request_contact = fields.Many2one('res.users', string="Solicitud de tercero")
    format_archive = fields.Binary(string="Format Archive", help="FORMATO: TE-R-010'\n'PARA LAS ACTIVIDADES:'\n'Nueva Funcionalidad'\n'Ajustes y Modificaciones'\n'Correctivo - Desempeño'\n'Correctivo - Usabilidad'\n'Correctivo - Procesamiento'\n'Reportes a la Medida'\n'Reportes en Sistema'\n'Diseño de plantillas'\n'Construcción de plantillas'\n'Modificación de plantillas'\n'-------------------------------------------------'\n'FORMATO: SOP-FOR-001 / SAP-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Creación'\n'-------------------------------------------------'\n'FORMATO: SAP / SAP-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Modificación y Reactivación '\n'-------------------------------------------------'\n'FORMATO: SOP-FOR-005'\n'PARA LAS ACTIVIDADES:'\n'Eliminación y Desactivación'\n'Retiro de Licencia Office 365'\n'-------------------------------------------------'\n'FORMATO: TEC-FOR-003'\n'PARA LAS ACTIVIDADES:'\n'Acceso y actualización de recursos compartidos'\n'Acceso a servicios SFTP/FTP'\n'Gestión de las plataformas e infraestructura local'\n'Control de cambios'\n'-------------------------------------------------'\n'FORMATO: Informe de análisis de vulnerabilidades'\n'PARA LAS ACTIVIDADES:'\n'Gestión de las vulnerabilidades'\n'-------------------------------------------------'\n'FORMATO: Acta de entrega'\n'PARA LAS ACTIVIDADES:'\n'Alistamiento y entrega de equipo de computo'\n'Alistamiento y entrega de servidores")
    format_archive_filename = fields.Char("File Name")
    groups_id = fields.Many2one(string="Asignado al grupo")
    assigned_to = fields.Many2one('res.users', string="Asignado a")


    priority = fields.Selection([('0', 'Baja'),
                                 ('1', 'Baja'),
                                ('2', 'Media'),
                                ('3', 'Alta')], string="Prioridad")
    
    urgency = fields.Selection([('0', 'Baja'),
                                ('2', 'Media'),
                                ('3', 'Alta')], string="Urgencia")

    required_information_ticket = fields.Selection([('Si', 'Si'),
                                      ('No', 'No')], string="Información requerida Completa")

    info_security = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], related='activity_id.info_security', string="Sub Service")
    
    info_security_scale = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Escalar a seguridad de la información")

    ans_date_selector = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Ans con Fecha")
    
    ans_datetime =fields.Datetime('Seleccione la fecha en la que se debe cumplir el ANS')

    resolved = fields.Selection([('Si', 'Si'),
                                      ('No', 'No'),], string="Resuelto")

    sla_check = fields.Boolean('Cumplió SLA')

    description_solution = fields.Char('Describa la solución del ticket')

    state_record= fields.Char('Estados', compute='_get_state_label')
    check_file_document = fields.Boolean(compute='_get_check_file_document', string='Check file')
    check_info_security = fields.Boolean(compute='_get_check_file_document', string='Check file')
    check_ans_fecha = fields.Boolean(compute='_get_check_ans_fecha', string='Check file')
    
    ############################### TIEMPOS ETAPAS TECNOLOGIA
    tiempo_1ra_aprobacion = fields.Char('Tiempo 1ra Aprobación',tracking=True)
    tiempo_2da_aprobacion = fields.Char('Tiempo 2da Aprobación',tracking=True)
    tiempo_3ra_aprobacion = fields.Char('Tiempo 3ra Aprobación',tracking=True)
    tiempo_aprobada_cliente = fields.Char('Tiempo Aprobada por el Cliente',tracking=True)
    tiempo_aprobada = fields.Char('Tiempo en Etapa Aprobada',tracking=True)
    tiempo_abierta = fields.Char('Tiempo en Etapa Abierta',tracking=True)
    tiempo_cerrada = fields.Char('Tiempo en Etapa Cerrada',tracking=True)
    tiempo_garantia = fields.Char('Tiempo en Etapa de Garantía',tracking=True)
    tiempo_hora_finalizada = fields.Char('Tiempo en Etapa de Garantía',tracking=True)
    tiempo_hora_solucion = fields.Char('Tiempo solucion',tracking=True)
    tiempo_total=fields.Char('Tiempo Total del Proceso', tracking=True)
    tiempo_gestion_tecnologia = fields.Char('Gestión de la tecnología', compute='_get_sum_tecnology', tracking=True)
    #FECHAS ETAPAS TECNOLOGIA
    tiempo_inicial=fields.Datetime('Fecha y hora de inicio',tracking=True, default= fields.Datetime().now())
    fecha_hora_1ra_aprobacion = fields.Datetime('Fecha y hora 1ra Aprobación', tracking=True, default= fields.Datetime().now())
    fecha_hora_2da_aprobacion = fields.Datetime('Fecha y hora 2da Aprobación', tracking=True)
    fecha_hora_3ra_aprobacion = fields.Datetime('Fecha y hora 3ra Aprobación', tracking=True)
    fecha_hora_aprobada_cliente = fields.Datetime('Fecha y hora Etapa Aprobada por el Cliente', tracking=True)
    fecha_hora_aprobacion = fields.Datetime('Fecha y hora Etapa de Aprobación', tracking=True)
    fecha_hora_abierta = fields.Datetime('Fecha y hora Etapa Abierta', tracking=True)
    fecha_hora_cerrada = fields.Datetime('Fecha y hora Etapa Cerrada', tracking=True)
    fecha_hora_garantia = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    fecha_hora_finalizada = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    fecha_hora_solucion = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    ##############################Tiempos SEGURIDAD#############################################################
    tiempo_1ra_aprobacion_2 = fields.Char('Tiempo 1ra Aprobación',tracking=True)
    tiempo_2da_aprobacion_2 = fields.Char('Tiempo 2da Aprobación',tracking=True)
    tiempo_3ra_aprobacion_2 = fields.Char('Tiempo 3ra Aprobación',tracking=True)
    tiempo_aprobada_cliente_2 = fields.Char('Tiempo Aprobada por el Cliente',tracking=True)
    tiempo_aprobada_2 = fields.Char('Tiempo en Etapa Aprobada',tracking=True)
    tiempo_abierta_2 = fields.Char('Tiempo en Etapa Abierta',tracking=True)
    tiempo_cerrada_2 = fields.Char('Tiempo en Etapa Cerrada',tracking=True)
    tiempo_garantia_2 = fields.Char('Tiempo en Etapa de Garantía',tracking=True)
    tiempo_hora_finalizada_2 = fields.Char('Tiempo en Etapa de Garantía',tracking=True)
    tiempo_hora_solucion_2 = fields.Char('Tiempo solucion',tracking=True)
    tiempo_total_2 =fields.Char('Tiempo Total del Proceso', tracking=True)
    #FECHAS ETAPAS SEGURIDAD
    tiempo_inicial_2 =fields.Datetime('Fecha y hora de inicio',tracking=True, default= fields.Datetime().now())
    fecha_hora_1ra_aprobacion_2 = fields.Datetime('Fecha y hora 1ra Aprobación', tracking=True, default= fields.Datetime().now())
    fecha_hora_2da_aprobacion_2 = fields.Datetime('Fecha y hora 2da Aprobación', tracking=True)
    fecha_hora_3ra_aprobacion_2 = fields.Datetime('Fecha y hora 3ra Aprobación', tracking=True)
    fecha_hora_aprobada_cliente_2 = fields.Datetime('Fecha y hora Etapa Aprobada por el Cliente', tracking=True)
    fecha_hora_aprobacion_2 = fields.Datetime('Fecha y hora Etapa de Aprobación', tracking=True)
    fecha_hora_abierta_2 = fields.Datetime('Fecha y hora Etapa Abierta', tracking=True)
    fecha_hora_cerrada_2 = fields.Datetime('Fecha y hora Etapa Cerrada', tracking=True)
    fecha_hora_garantia_2 = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    fecha_hora_finalizada_2 = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    fecha_hora_solucion_2 = fields.Datetime('Fecha y hora Etapa de Garantía', tracking=True)
    
    
    date_aper = fields.Datetime(string='Fecha de Apertura', required=True, readonly=True, index=True,  default=fields.Datetime.now)
    service_id_label = fields.Char(string='servicio', compute='_get_label_service_id')
    sub_service_id_label = fields.Char(string='Sub-servicio', compute='_get_label_subservice')
    team_label = fields.Char(string='Sub-servicio', compute='_get_team_label')
##################################SEGURIDAD########################################################
######################################ASEGURAMIENTO DE PRODUCTOS ######################################
    material = fields.One2many('helpdesk.material','material_ids', string='Material')
    solicitud_almacenamiento = fields.Datetime(string='Solicitud de Almacenamiento hasta: ')
    material_requiere = fields.Boolean(string='Material requiere investigación')
    reporte_indemnidad = fields.Binary(string='Reporte de imdemnidad')
    producto_incompleto = fields.Binary(string='Producto incompleto, auntentico')
    acta_destruccion = fields.Binary(string='Acta de destrucción')
    link_video = fields.Char(string='Link de video')

#####################################RECOLECCIÓN Y ENTREGAS SEGURIDAD #####################################
    nombre_servicio = fields.Char('Nombre del servicio')
    producto_entregar = fields.Char('Producto a recolectar o entregar')
    escolta_asignado_id = fields.Many2one('helpdesk.escolta', string='Escolta Asignado')
    escolta_asignado_entrega_id = fields.Many2one('helpdesk.escolta', string='Escolta Asignado')
    fecha_programacion = fields.Datetime(string='Fecha y hora de programación')
##################################ORDENES DE SALIDA #########################################
    producto_articulo = fields.One2many('helpdesk.producto','producto_ids', string='Producto/articulo')
    nombre_persona_retira = fields.Char('Nombre de la persona que retira')
    destino = fields.Char('Destino')
    aprobado_jede_departamento = fields.Selection([('Si', 'Si'),
                                                    ('No', 'No'),], string="Aprobado por jefe de departamento")
    aprobado_seguridad = fields.Selection([('Si', 'Si'),
                                            ('No', 'No'),], string="Aprobado por Seguridad")
    
    porteria = fields.Selection([('principal', 'Principal'),
                                      ('12', '12-80'),], string="Aprobado por jefe de departamento")
    
    devolutivo = fields.Selection([('Si', 'Si'),
                                            ('No', 'No'),], string="Devolutivo")
    
    fecha_devolucion = fields.Date(string='Fecha de devolucion')
    vigilantes_id = fields.Many2one('helpdesk.vigilante', string='Vigilante que verifica salida')
    

#######################################INFORME ANALISIS DE AUTENTICIDAD ########################
    cliente = fields.Char('Cliente')
    producto = fields.Char('Producto')
    ubicacion_producto = fields.Char('Ubicación o dirección del producto')
    fecha_solicitada_recoleccion = fields.Char('Fecha solicitada para recolección')
    numeracion = fields.Char('Numeración')
    no_sorteo = fields.Char('No del sorteo')
    serie = fields.Char('Serie')
    fraccion = fields.Char('Fracción')
    aprobado_gerencia_seguridad = fields.Boolean('Aprobado por gerencia de seguridad')
    analisis_tecnologia = fields.Boolean('*Análisis de Tecnología')
    verificacion_codigo_barras = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="1. VERIFICACION CODIGO DE BARRAS: ")
    verificacion_codigo_control = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="2. VERIFICACION CODIGO DE CONTROL:")
    verificacion_distribuidor = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="3. VERIFICACION DEL DISTRIBUIDOR:")
    verificacion_sorteo = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="4. VERIFICACION SORTEO:")
    verificacion_billete = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="5. VERIFICACION N° DE BILLETE:")
    verificacion_serie = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="6. VERIFICACION SERIE:")
    verificacion_variable = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="7. VER INF.VARIABLE TIRA DE CONTROL:")
    tira_control_virtual = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="8. TIRA CONTROL VIRTUAL:")
    analisis_realizado = fields.Many2one('hr.employee', string='Análisis realizado por')
    cargo = fields.Char(string='Cargo', compute='_get_cargo_label')
    analisis_preprensa = fields.Boolean('*Análisis por preprensa')
    fondos_especiales = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="A. FONDOS ESPECIALES UTILIZADOS")
    antifotocopias = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="B. ANTIFOTOCOPIAS NULO")
    verificacion_microtextos = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="C. VERIFICACION MICROTEXTOS")
    verificacion_impresion = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="D. VERIFICACION DE LA IMPRESIÓN LITOGRAFICA")
    cremocromaticas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="E. CREMOCROMATICAS")
    analisis_laboratorio = fields.Boolean('*Análisis de Laboratorio')
    fluorescente_invisible = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="A. FLUORESCENTE INVISIBLE")
    fluorescente_visible = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="B. FLUORESCENTE VISIBLE")
    fluoranulado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="C. FLUORANULADO")
    reactivo_moneda = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="D. REACTIVO A LA MONEDA")
    anulado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="E. ANULADO")
    sensible_borrado = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="F. SENSIBLE AL BORRADO")
    termocromicas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="G. TERMOCROMICAS")
    fotocromaticas = fields.Selection([('cumple', 'Cumple'),
                                            ('no_cumple', 'No cumple'),
                                            ('no_aplica', 'No aplica'),], string="H. FOTOCROMATICAS")
#########################################################INGRESO COMPAÑIA VISITANTES#########################################
    area_ingreso = fields.Selection([('administrativa', 'Administrativa'),
                                            ('planta', 'Planta'),], string="Area de ingreso")
    fecha_ingreso = fields.Datetime('Fecha y Hora de ingreso')
    fecha_salida = fields.Datetime('Fecha y Hora de salida')
    registro_personas = fields.One2many('helpdesk.personas','personas_ids', string='Registro de personas')
    registro_personas_adjunto = fields.One2many('helpdesk.personas','personas_ids', string='Registro de personas (Recuerde adjuntar la o las planillas de para-fiscales)')
#########################################################MUESTRAS#########################################
    clase_anulado = fields.Selection([('especimen', 'Espécimen'),
                                            ('sello', 'Sello'),], string="Clase de Anulado")
    entregar = fields.Many2one('hr.employee', string='Entregar a')
    aprobado_gerencia = fields.Boolean('Aprobado por gerencia')
    aprobado_laboratorio = fields.Boolean('Aprobado por laboratorio')
    notas_desaprobacion_laboratorio = fields.Text('Notas de desaprobación laboratorio')
    requiere_devolucion = fields.Boolean('Requiere devolución')
    fecha_devolucion_muestra = fields.Datetime('Fecha y hora de devolución de la muestra')
###################################################SOLICITUD VIDEOS########################################
    solicitud_video_aprobado = fields.Boolean('Solicitud de video Aprobado')
    video_aprobado_entrega = fields.Boolean('Video aprobado para la entrega')
                            


    @api.onchange('group_users_id')
    def _onchange_dominio_users(self):
        users_ids=[]
        if self.group_users_id:
            for group in self.group_users_id:
                users_ids += group.user_id.ids
        return {'domain':{'user_id':[('id','in',users_ids)]}}
    

    @api.depends('stage_id')
    def _get_state_label(self):
        for record in self:
            if record.stage_id:
                record.state_record=(record.stage_id.name).upper()
            else:
                 record.state_record=False

    @api.depends('analisis_realizado')
    def _get_cargo_label(self):
        for record in self:
            if record.analisis_realizado:
                record.cargo=record.analisis_realizado.job_title
            else:
                 record.cargo=False

    @api.depends('activity_id')
    def _get_department_user(self):
        for record in self:
            record.departament = record.env.user.department_id.name
            
    @api.depends('activity_id')
    def _get_check_ans_fecha(self):
        for record in self:
            if record.activity_id.asn_date == True:
                record.check_ans_fecha=True
            else:
                 record.check_ans_fecha=False

    @api.depends('stage_id')
    def _get_sum_tecnology(self):
        for record in self:
            if record.state_record == 'SOLUCIONADO' and record.tiempo_1ra_aprobacion and record.tiempo_2da_aprobacion and record.tiempo_aprobada:
          #      if record.fecha_hora_finalizada and record.fecha_hora_aprobacion and record.fecha_hora_3ra_aprobacion and record.fecha_hora_2da_aprobacion  and record.date_aper:
                calc = (record.fecha_hora_finalizada - record.fecha_hora_aprobacion)+(record.fecha_hora_3ra_aprobacion - record.fecha_hora_2da_aprobacion)+(record.fecha_hora_2da_aprobacion - record.date_aper) 

                calc = calc.seconds/60

                hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                #vals.update(tiempo_garantia=calc)
                record.tiempo_gestion_tecnologia = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
                
            else:
                record.tiempo_gestion_tecnologia = False

    @api.depends('activity_id')
    def _get_check_file_document(self):
        for record in self:
            if record.activity_id.file_request == True:
                record.check_file_document = True
            else:
                record.check_file_document = False

    @api.depends('service_id') 
    def _get_label_service_id(self):
        for record in self:
            if record.service_id:
                record.service_id_label = record.service_id.name
            else:
                record.service_id_label = False
    
    @api.depends('subservice_id')
    def _get_label_subservice(self):
        for record in self:
            if record.subservice_id:
                record.sub_service_id_label = record.subservice_id.name
            else:
                record.sub_service_id_label = False


    @api.depends('team_id')
    def _get_team_label(self):
        for record in self:
            if record.team_id:
                record.team_label = record.team_id.name
            else:
                record.team_label = False

    def write(self, vals):

        res = super(HelpdeskTicket, self).write(vals)

        if 'stage_id' in vals:
            for record in self:    
                if record.state_record == 'EN REVISIÓN':
                    record.fecha_hora_2da_aprobacion=fields.Datetime().now()
                    calc = fields.Datetime.now() - self.date_aper
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_1ra_aprobacion = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'APROBACIÓN SEGURINFO':
                    if not record.fecha_hora_2da_aprobacion:
                        raise ValidationError("Para pasar a este estado, se debe encontrar EN REVISIÓN")

                    record.fecha_hora_3ra_aprobacion=fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_2da_aprobacion
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_2da_aprobacion = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'EN ESPERA DE INFORMACIÓN USUARIO':
                    if not record.fecha_hora_3ra_aprobacion:
                        raise ValidationError("Para pasar a este estado, se debe encontrar en APROBACIÓN SEGÚRINFO")

                    record.fecha_hora_aprobada_cliente=fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_3ra_aprobacion
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_3ra_aprobacion = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'EN GESTIÓN':
                    if not record.fecha_hora_aprobada_cliente:
                         raise ValidationError("Para pasar a este estado, se debe encontrar EN ESPERA DE INFORMACIÓN USUARIO")

                    record.fecha_hora_aprobacion=fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_aprobada_cliente
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_aprobada_cliente = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'ESCALADO A TERCEROS':
                    if not record.fecha_hora_aprobacion:
                        raise ValidationError("Para pasar a este estado, se debe encontrar EN GESTIÓN")

                    record.fecha_hora_finalizada = fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_aprobacion
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_aprobada = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
                
                if record.state_record == 'VERIFICACIÓN (SEGURIDAD. LABORATORIO)':
                    record.fecha_hora_2da_aprobacion_2 =fields.Datetime().now()
                    calc = fields.Datetime.now() - self.date_aper
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_1ra_aprobacion_2 = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'AUTORIZACIÓN O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
                   

                    record.fecha_hora_3ra_aprobacion_2 =fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_2da_aprobacion_2
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_2da_aprobacion_2 = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'DEVOLUCIÓN / DESTRUCCIÓN / ENTREGA':
                    

                    record.fecha_hora_aprobada_cliente_2 = fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_3ra_aprobacion_2
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_3ra_aprobacion_2 = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                if record.state_record == 'EN TERCERO':
                    

                    record.fecha_hora_aprobacion_2 =fields.Datetime().now()
                    calc = fields.Datetime.now() - record.fecha_hora_aprobada_cliente_2
                    calc = calc.seconds/60

                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
                    record.tiempo_aprobada_cliente_2 = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

                    

                if record.state_record == 'SOLUCIONADO':

                    record.fecha_hora_solucion_2 = fields.Datetime().now()
                    record.fecha_hora_solucion = fields.Datetime().now()
                    
                    calct = fields.Datetime.now() - record.date_aper
                    calct = calct.seconds/60

                    if record.team_label == 'MESA DE AYUDA SEGURIDAD':
                        calc = fields.Datetime.now() - record.fecha_hora_aprobacion_2
                        calc = calc.seconds/60
                    elif record.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                        calc = fields.Datetime.now() - record.fecha_hora_finalizada
                        calc = calc.seconds/60

                    hourst, secondst = divmod(calct * 60, 3600)  # split to hours and seconds
                    minutest, secondst = divmod(secondst, 60)  # split the seconds to minutes and seconds
                    hours, seconds = divmod(calc * 60, 3600)  # split to hours and seconds
                    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds


                    record.tiempo_total = "{:02.0f}:{:02.0f}:{:02.0f}".format(hourst, minutest, secondst)
                    if record.team_label == 'MESA DE AYUDA SEGURIDAD':
                         record.tiempo_aprobada_2 = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
                    elif record.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                        record.tiempo_hora_finalizada = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
                    
        return res
    
    def action_stage_next(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                if record.stage_id.name == 'NUEVO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN REVISIÓN')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN REVISIÓN':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','APROBACIÓN SEGURINFO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'APROBACIÓN SEGURINFO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN ESPERA DE INFORMACIÓN USUARIO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN ESPERA DE INFORMACIÓN USUARIO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN GESTIÓN')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN GESTIÓN':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','ESCALADO A TERCEROS')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'ESCALADO A TERCEROS':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CERRADO')])
                    record.write({'stage_id':ticket_sudo.id})

            else:
                if record.stage_id.name == 'REVISIÓN':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','VERIFICACIÓN (SEGURIDAD. LABORATORIO)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'VERIFICACIÓN (SEGURIDAD. LABORATORIO)':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','AUTORIZACIÓN O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'AUTORIZACIÓN O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','DEVOLUCIÓN / DESTRUCCIÓN / ENTREGA')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'DEVOLUCIÓN / DESTRUCCIÓN / ENTREGA':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN TERCERO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN TERCERO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CERRADO')])
                    record.write({'stage_id':ticket_sudo.id})
                    
    def action_stage_return(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                if record.stage_id.name == 'EN REVISIÓN': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','NUEVO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'APROBACIÓN SEGURINFO':  
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN REVISIÓN')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN ESPERA DE INFORMACIÓN USUARIO':  
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','APROBACIÓN SEGURINFO')])
                    record.write({'stage_id':ticket_sudo.id}) 
                elif record.stage_id.name == 'EN GESTIÓN':   
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN ESPERA DE INFORMACIÓN USUARIO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'ESCALADO A TERCEROS': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN GESTIÓN')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','ESCALADO A TERCEROS')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'CERRADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})

            else:
                if record.stage_id.name == 'VERIFICACIÓN (SEGURIDAD. LABORATORIO)': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','REVISIÓN')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'AUTORIZACIÓN O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)': 
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','VERIFICACIÓN (SEGURIDAD. LABORATORIO)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'DEVOLUCIÓN / DESTRUCCIÓN / ENTREGA':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','AUTORIZACIÓN O APROBACIONES (SOLICITANTE, SEGURINFO, SEGURIDAD, COMERCIAL, OPERACIONES, TGSC)')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'EN TERCERO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','DEVOLUCIÓN / DESTRUCCIÓN / ENTREGA')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'SOLUCIONADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','EN TERCERO')])
                    record.write({'stage_id':ticket_sudo.id})
                elif record.stage_id.name == 'CERRADO':
                    ticket_sudo = self.env['helpdesk.stage'].search([('name','=','SOLUCIONADO')])
                    record.write({'stage_id':ticket_sudo.id})
                    

    def action_stage_cancel(self):
        for record in self:
            if record.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                ticket_sudo = self.env['helpdesk.stage'].search([('name','=','CANCELADO')])
                record.write({'stage_id':ticket_sudo.id})
            elif record.team_label == 'MESA DE AYUDA SEGURIDAD':
                ticket_sudo = self.env['helpdesk.stage'].search([('name','=','RECHAZADO')])
                record.write({'stage_id':ticket_sudo.id})

