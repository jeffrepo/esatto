# -*- coding: utf-8 -*-

from odoo import api, models
from datetime import date
from datetime import datetime, date, time, timedelta
import re
from html.parser import HTMLParser
import logging
from bs4 import BeautifulSoup

class ReportEsattoEtiqueta(models.AbstractModel):
    _name = 'reporte.esatto.etiqueta'
    nombre_reporte = ''

    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'sale.order'
        docs = self.env[model].browse(docids)
        dicc_etiquetas = {}

        logging.warning('Vamos a crear un dicc')


        paquetes = []
        correr_espacio_paquete = 0
        for sale in docs:
            direccion_texto = ""
            contador_dir = 1
            for i in re.findall("<p>(.*?)</p>",str(sale.note)):
                if contador_dir == 2:
                    direccion_texto = i
                contador_dir += 1
            lista_materiales_lista = []
            logging.warning(direccion_texto)
            if sale.id not in dicc_etiquetas:
                for linea_venta in sale.order_line:
                    if linea_venta.product_id.bom_ids:
                        lista_materiales_lista.append(linea_venta.product_id.bom_ids.product_tmpl_id.name)
                
                lista_materiales_join = ','.join(lista_materiales_lista)
                dicc_etiquetas[sale.id] = {'paquetes': {}, 'plataforma': sale.origin.split('-')[1],'direccion_texto': direccion_texto[10:], 'pedido': sale, 'lista_materiales_join': lista_materiales_join}
            
            if sale.picking_ids:
                
                for envio in sale.picking_ids:
                    
                    if envio.move_ids_without_package:
                        dicc_etiquetas[sale.id]['numero_paquetes'] = envio.x_studio_numero_de_paquetes
                        
                        for linea_m in envio.move_ids_without_package:
                            if linea_m.x_studio_paquete not in dicc_etiquetas[sale.id]['paquetes']:
                                dicc_etiquetas[sale.id]['paquetes'][linea_m.x_studio_paquete] = {'numero_paquete': linea_m.x_studio_paquete,'moves':[],'plataforma': sale.origin.split('-')[1],'direccion_texto': direccion_texto[10:], 'pedido': sale}
                                
                            dicc_etiquetas[sale.id]['paquetes'][linea_m.x_studio_paquete]['moves'].append(linea_m)
                            if correr_espacio_paquete % 2 == 0:
                                dicc_etiquetas[sale.id]['paquetes'][linea_m.x_studio_paquete]['correr_espacio_paquete'] = 1
                            else:
                                dicc_etiquetas[sale.id]['paquetes'][linea_m.x_studio_paquete]['correr_espacio_paquete'] = 2

                    correr_espacio_paquete += 1

        
            logging.warning('sale')
            logging.warning(dicc_etiquetas)
            
            


        logging.warning('sale')
        logging.warning(dicc_etiquetas)
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
