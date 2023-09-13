# -*- coding: utf-8 -*-
# from odoo import http
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class RegistroClientesWeb(models.Model):
    _name = 'registro.clientes.web'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Registro Clientes'
    _rec_name = 'clab_business_name'
    
    clab_state = fields.Selection([('0_clab_nuevo', 'Cliente Nuevo'),
                                   ('1_clab_enviado', 'Enviado a Contactos'),
                                   ('2_clab_editado', 'Editado'),
                                   
                                   ],
                                #   default='0_clab_nuevo',
                                  string="Status",
                                  default = '0_clab_nuevo',
                                  invisible= True)
    
    
    clab_company_type = fields.Char(default='company', invisible= True)
    clab_business_name = fields.Char(string='Razón Social', required=True)
    clab_business_reason = fields.Char(string='Nombre Comercial')
    clab_email = fields.Char(string='Correo Electrónico de Contacto')
    clab_website = fields.Char(string='Sitio Web')
    clab_RUC = fields.Char(string='R.U.C')
    clab_DV = fields.Char(string='D.V')
    sent_to_partner = fields.Boolean(string='Enviado a Contactos', default = False, readonly=True)
    # campos faltantes de los datos de la compa;ia
    clab_phone = fields.Char(string='Teléfono')
    clab_mobile = fields.Char(string='Móvil')
    clab_direction = fields.Char(string="Dirección")
    #    variables de contacto principal
    clab_contact_name = fields.Char(string='Nombre Principal')
    clab_contact_function = fields.Char(string='Puesto de trabajo Principal')
    clab_contact_email = fields.Char(string='Correo Electrónico Principal')
    clab_contact_phone = fields.Char(string='Teléfono Principal')
    clab_contact_mobile = fields.Char(string='Móvil de Contacto Principal')
    
#    variables de contacto cobros
    clab_billing_name = fields.Char(string='Nombre Cobros')
    clab_billing_function = fields.Char(string='Puesto de trabajo Cobros')
    clab_billing_email = fields.Char(string='Correo Electrónico Cobros')
    clab_billing_phone = fields.Char(string='Teléfono Cobros')
    clab_billing_mobile = fields.Char(string='Móvil Cobros')

    def get_ruc_data(self):
        rucs = self.env['res.partner'].search([]).mapped('vat')
        return rucs
    def cambio_estado_etiqueta(self, state):
        self.clab_state = state
    def verify_state(self):
        existing_partner = self.env['res.partner'].search([('vat', '=', self.clab_RUC)], limit=1)
        if (existing_partner):
            self.cambio_estado_etiqueta('1_clab_enviado')
        else:
            self.cambio_estado_etiqueta('0_clab_nuevo')

        
    def funcion_enviar_email(self):
        values={

                'subject': 'Se ha creado el contacto',

                'email_from': 'no-reply@compulab.com.pa',

                'email_to': r.login,

                'body_html':f"""<html>

                    <head></head>

                    <body>

                    <div style="width: 100%;">

                            <div style="margin: 0 auto; width: 500; max-width: 500px;">

                                <div>

                                   <div>

                                            <img src="https://dim.mcusercontent.com/cs/8122d1b9e1e584e76efb896c3/images/e03ab170-80ed-b4be-5c2f-fc94664ed0bd.png" width="125px" width="125"/>

                                        </div>

                                        <div>

                                            Estimado <br/><h2 style="margin: 0px; margin: 0;"><strong>{r.name}</strong></h2>

                                           

                                        </div>

                                   

                                    </div>

                                    <div>

                                <hr/>    

                                

 

                                    <span>Por favor revísela para que la pueda autorizar!</span><br/><br/>

                                    <a target="_blank" href="https://erp.compulab.com.pa/web#id={id_clientes}&model=registro.clientes.web&view_type=form" style="margin-top: 25px; margin-top: 25; background-color: #54acdc; color: white; padding: 10px 15px; padding: 10 15; text-decoration: none;  border-radius: 2.5px; border-radius: 2.5;">Ver la Solicitud</a><br/><br/><br/>                              

                                </div>

                                <hr/>

                                <div style="text-align:center; color:grey;">

                                    Compulab S.A.<br/>

                                    <a>210 7100</a> | <a href="mailto:compulab@compulab.com.pa" style="text-decoration:none; color: inherit;" >compulab@compulab.com.pa</a> | <a target="_blank" href="http://www.compulab.com.pa" style="text-decoration:none; color: inherit;">http://www.compulab.com.pa</a>

                                </div>

                            </div>

                    </div>

                    </body>

                    </html>

                    """  ,

             

            'res_id': False

            }
        creditos_cobros = self.env['res.users'].search([('clab_creditos_y_cobros', '=', True)])
        mail_pool = self.env['mail.mail']
        for r in creditos_cobros:
            
            msg_id = mail_pool.create(values)
            if msg_id:

                msg_id.send()
        
    
# funcion al tocar el boton enviar a contactos     
    def toggle_state(self):

        
        country_panama = self.env['res.country'].search([('name', '=', 'Panamá')], limit=1)
        # Buscar si ya existe un registro con el mismo RUC en el módulo de contactos
        existing_partner = self.env['res.partner'].search([('vat', '=', self.clab_RUC)], limit=1)
        exitting_billing_contact= self.env['res.partner'].search([('name', '=', self.clab_billing_name)], limit=1)
        exitting_principal_contact=self.env['res.partner'].search([('name', '=', self.clab_contact_name)], limit=1)
        #raise UserError(f'exitting_billing_contact = {exitting_billing_contact.id} , exitting_principal_contact = {exitting_principal_contact.id}')
        ids_contact = []

        if self.clab_contact_name:
            if exitting_principal_contact.id:
                exitting_principal_contact.write({
                                            # insertando los valores de la variables clab_ en su equivalente en res.partner
                                            #'clab_tipo_compania': 'individual',
                                            'company_type': 'person',
                                            'name': self.clab_contact_name,
                                            'email':self.clab_contact_email,
                                            'phone':self.clab_contact_phone,
                                            'mobile':self.clab_contact_mobile,
                                            'function':self.clab_contact_function,
                                            'user_id':self.env.uid,
                                            'x_clab_tipo_contacto': 'clab_customer'
                                            })
                ids_contact.append(exitting_principal_contact.id)
                
            else:
                contact_id=self.env['res.partner'].create({
                                            # insertando los valores de la variables clab_ en su equivalente en res.partner
                                            #'clab_tipo_compania': 'individual',
                                            'company_type': 'person',
                                            'name': self.clab_contact_name,
                                            'email':self.clab_contact_email,
                                            'phone':self.clab_contact_phone,
                                            'mobile':self.clab_contact_mobile,
                                            'function':self.clab_contact_function,
                                            'user_id':self.env.uid,
                                            'x_clab_tipo_contacto': 'clab_customer'
                                            })
                ids_contact.append(contact_id.id)
            
        if self.clab_billing_name:
            if exitting_billing_contact.id:
                exitting_billing_contact.write({
                                            # insertando los valores de la variables clab_ en su equivalente en res.partner
                                            #'clab_tipo_compania': 'individual',
                                            'company_type': 'person',
                                            'name': self.clab_billing_name,
                                            'email':self.clab_billing_email,
                                            'phone':self.clab_billing_phone,
                                            'mobile':self.clab_billing_mobile,
                                            'function':self.clab_billing_function,
                                            'user_id':self.env.uid,
                                            'x_clab_tipo_contacto': 'clab_customer'
                                            })
                
                ids_contact.append(exitting_billing_contact.id)
            else:
                billing_id=self.env['res.partner'].create({
                                            # insertando los valores de la variables clab_ en su equivalente en res.partner
                                            #'clab_tipo_compania': 'individual',
                                            'company_type': 'person',
                                            'name': self.clab_billing_name,
                                            'email':self.clab_billing_email,
                                            'phone':self.clab_billing_phone,
                                            'mobile':self.clab_billing_mobile,
                                            'function':self.clab_billing_function,
                                            'user_id':self.env.uid,
                                            'x_clab_tipo_contacto': 'clab_customer'
                                            })
                ids_contact.append(billing_id.id)
    # if self.sent_to_partner:
    #    pass # raise UserError('El Cliente ya fue agregado en Contactos)')
    # else:
        if existing_partner.id:
            self.sent_to_partner = True
            # Si ya existe un registro con el mismo RUC, mostrar el cuadro de diálogo
            # self.contact_id = existing_partner.id

            existing_partner.write({
                'company_type': self.clab_company_type,
                #'clab_tipo_compania': 'compania',
                'name': self.clab_business_name,
                'clab_business_reason': self.clab_business_reason,
                'email': self.clab_email,
                'website': self.clab_website,
                'vat': self.clab_RUC,
                'clab_dv': self.clab_DV,
                'phone':self.clab_phone,
                'mobile':self.clab_mobile,
                'street':self.clab_direction,
                'country_id': country_panama.id,
                'child_ids':ids_contact,
                'user_id': self.env.uid,
                'x_clab_tipo_contacto': 'clab_customer'
                
            # Otros campos que desees actualizar...
            })
            
            self.cambio_estado_etiqueta('2_clab_editado')
            # Enviar notificación de que el contacto ya existe
            # Enviar notificación de que el contacto ya existe

            #self.message_post(body="El contacto se ha enviado correctamente a res.partner.")
        
            return {
            'type': 'ir.actions.act_window',
            'name': 'Registro Existente',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_id': self.env.ref('base.view_partner_form').id,# le dice a la vista que datos debe mostrar
            'target': 'new',# Muestra la ventana como ventana flotante
            'res_id': existing_partner.id,
                # 'context': dict(self._context,active_ids=[existing_partner.id])
                
            }
        else:
            # Si no existe un registro con el mismo RUC, crear uno nuevo
            #self.clab_company_type = 'company'
            new_partner = self.env['res.partner'].create({
                'company_type': 'company',
                #'clab_tipo_compania': 'compania',
                'name': self.clab_business_name,
                'clab_business_reason': self.clab_business_reason,
                'email': self.clab_email,
                'website': self.clab_website,
                'vat': self.clab_RUC,
                'clab_dv': self.clab_DV,
                'phone':self.clab_phone,
                'mobile':self.clab_mobile,
                'street':self.clab_direction,
                'country_id': country_panama.id,
                'child_ids':ids_contact,
                'user_id': self.env.uid,
                'x_clab_tipo_contacto': 'clab_customer'
                # Otros campos que quieras crear...
                # 'user_id': self.env.uid, obtiene el id del usuario que estacreando el contacto
            })
            self.cambio_estado_etiqueta('1_clab_enviado')
            # raise UserError('El contacto se ha creado')
            #self.message_post(body="El contacto se ha enviado correctamente a res.partner.")
            
            # self.contact_id = new_partner.id
            # self.sent_to_partner = True

        # Enviar notificación de que el contacto se ha creado
        
