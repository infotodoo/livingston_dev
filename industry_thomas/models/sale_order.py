#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'sale.order'

    order_class = fields.Char(string="Clase de Pedido", default="ZP01")
    org_vtg = fields.Char(string="Org Vtas", default="1100")    
    channel = fields.Char(string="Canal", default="10")  
    sector = fields.Char(string="Sector", default="12")
    cebe = fields.Char(string="Cebe", default="1140010124")
    currency_tst = fields.Char(string="Moneda", default="CP1")
    sequence_maintenance = fields.Char(string="# de Petición")
    sap_code = fields.Char(related="partner_id.sap", string="Código SAP")
    time_of = fields.Char(string="Tiempo de Entrega")
     
    