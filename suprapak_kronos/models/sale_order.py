# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    client_order_ref = fields.Char(string="Orden de compra")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    # Info Tec
    material_id = fields.Many2one('data.material','Material')
    drawn_type_id = fields.Many2one('data.drawn.type', 'Drawn type')
    movie_type_id = fields.Many2one('data.movie.type', 'Movie type')
    # Info cant
    specification_width = fields.Float('Specification width')
    specification_long = fields.Float('Specification long')
    caliber_id = fields.Many2one('data.caliber.type', 'Specification caliber')
    # Boolean
    tongue = fields.Boolean('Tongue')
    thermal_adhesive = fields.Boolean('Thermal adhesive')
    # from here Cristian Casas Rodriguez
    presentation_id = fields.Many2one('presentation','Presentación')
    seal_type_id = fields.Many2one('seal.type','Tipo de presentación')
    number_of_colors = fields.Integer('Numero de colores')
    type_print_kronos = fields.Selection([("1", "1"),
                                    ("2", "2"),
                                    ("3", "3"),
                                    ("4", "4"),
                                    ("5", "5"),
                                    ("6", "6"),
                                    ("7", "7"),
                                    ("8", "8"),
                                    ("9", "9"),
                                    ("10", "10"),
                                    ("11", "NA")]
                                         , string="Impresion")
    seal_type = person_type = fields.Selection([("1", "Recto"),
                                    ("2", "Curvo")], string="Tipo de selle")