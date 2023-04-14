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
            logging.warning(sale.name)
            if sale.id not in dicc_etiquetas:
                dicc_etiquetas[sale.id]={
                'name': sale.name,
                'kit': {},
                'nombre_paquetes':''
                }
            nombres_paquete = []
            for line in docs.picking_ids.move_ids_without_package:
                logging.warning(line.bom_line_id)
                logging.warning(line.bom_line_id.bom_id.display_name)
                logging.warning('')
                if sale.id in dicc_etiquetas:
                    if line.bom_line_id.bom_id.id not in dicc_etiquetas[sale.id]['kit']:
                        dicc_etiquetas[sale.id]['kit'][line.bom_line_id.bom_id.id]={
                        'name_kit':line.bom_line_id.bom_id.display_name
                        }
                        nombres_paquete.append(line.bom_line_id.bom_id.display_name)
                        dicc_etiquetas[sale.id]['nombre_paquetes'] = " ".join(nombres_paquete)



        logging.warning('')    
        logging.warning(dicc_etiquetas)

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
