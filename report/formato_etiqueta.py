# -*- coding: utf-8 -*-

from odoo import api, models
from datetime import date
from datetime import datetime, date, time, timedelta
import logging

class ReportEsattoEtiqueta(models.AbstractModel):
    _name = 'reporte.esatto.etiqueta'
    nombre_reporte = ''

    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'sale.order'
        docs = self.env[model].browse(docids)
        dicc_etiquetas = {}

        logging.warning('Vamos a crear un dicc')

        logging.warning(self)
        logging.warning(docs)
        logging.warning(docs.picking_ids)

        for sale in docs:
            for linea_materiales in sale.picking_ids.move_ids_without_package:
                if linea_materiales.x_studio_paquete not in dicc_etiquetas:
                    dicc_etiquetas[linea_materiales.x_studio_paquete]={
                    'numero_paquete': linea_materiales.x_studio_paquete,
                    'numero_paquetes': sale.picking_ids.x_studio_numero_de_paquetes,
                    'productos':[]
                    }
                dicc_etiquetas[linea_materiales.x_studio_paquete]['productos'].append(linea_materiales)


            # logging.warning(sale.name)
            # if sale.id not in dicc_etiquetas:
            #     dicc_etiquetas[sale.id]={
            #     'name':sale.name,
            #     'paquete_id':{},
            #     'names': ''
            #     }
            # lst_names = []
            # for linea in sale.order_line:
            #     if linea.product_template_id.bom_ids:
            #         if linea. not in dicc_etiquetas[sale.id]['paquete_id']:
            #             dicc_etiquetas[sale.id]['paquete_id'][linea.x_studio_paquete]=[]
            #
            #         for linea_materiales in sale.picking_ids.move_ids_without_package:
            #
            #             dicc_etiquetas[sale.id]['paquete_id'][linea.x_studio_paquete].append(linea_materiales)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'dicc_etiquetas':dicc_etiquetas
        }


class ReportEsattoEtiquetaClass(models.Model):
    _name = 'report.esatto.report_etiqueta_personalizada'
    _inherit = 'reporte.esatto.etiqueta'

    nombre_reporte = 'report_etiqueta_personalizada'
