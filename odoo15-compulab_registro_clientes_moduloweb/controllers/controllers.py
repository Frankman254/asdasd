# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class WebsiteRegistrationClient(http.Controller):
    @http.route('/client_registration', type='http', auth="public", website=True)
    def register(self, **post):
        
        if post.get('clab_RUC'):
            update_partner = False
            ruc = post.get('clab_RUC')
            existing_partner_registro_clientes_web = request.env['registro.clientes.web'].sudo().search([('clab_RUC', '=', ruc)], limit=1)
            existing_partner = request.env['res.partner'].sudo().search([('vat', '=', ruc)], limit=1)
            
            if existing_partner_registro_clientes_web and existing_partner:
                update_partner = True
                # If RUC exists in both 'registro.clientes.web' and 'res.partner', render the confirmation template
                return request.render('odoo15-compulab_registro_clientes_moduloweb.confirmation_template', {
                'update_partner': update_partner,
                # 'existing_partner_registro_clientes_web': existing_partner_registro_clientes_web,
                'post_data': post,  # Agregamos todos los datos de 'post' al contexto
                
            }) 
            elif existing_partner_registro_clientes_web:
                update_partner = True
                # If RUC exists in 'registro.clientes.web', update the existing partner
                return request.render('odoo15-compulab_registro_clientes_moduloweb.confirmation_template', {
                'update_partner': update_partner,
                # 'existing_partner_registro_clientes_web': existing_partner_registro_clientes_web,
                'post_data': post,  # Agregamos todos los datos de 'post' al contexto
                
            })
            elif existing_partner:
                update_partner = False
                return request.render('odoo15-compulab_registro_clientes_moduloweb.confirmation_template', {
                'update_partner': update_partner,
                # 'existing_partner_registro_clientes_web': existing_partner_registro_clientes_web,
                'post_data': post,  # Agregamos todos los datos de 'post' al contexto
                
            })            
            else:    

                partner = request.env['registro.clientes.web'].sudo().create({
                    'clab_business_name': post.get('clab_business_name'),
                    'clab_business_reason': post.get('clab_business_reason'),
                    'clab_email': post.get('clab_email'),
                    'clab_website': post.get('clab_website'),
                    'clab_RUC': post.get('clab_RUC'),
                    'clab_DV':post.get('clab_DV'),
                    'clab_company_type': 'company',
                    'sent_to_partner': False,
                    
                    'clab_phone':post.get('clab_phone'),
                    'clab_mobile':post.get('clab_mobile'),
                    'clab_direction':post.get('clab_direction'),
                    
                    'clab_contact_name':post.get('clab_contact_name'),
                    'clab_contact_function':post.get('clab_contact_function'),
                    'clab_contact_email':post.get('clab_contact_email'),
                    'clab_contact_phone':post.get('clab_contact_phone'),
                    'clab_contact_mobile':post.get('clab_contact_mobile'),
                    
                    'clab_billing_name':post.get('clab_billing_name'),
                    'clab_billing_function':post.get('clab_billing_function'),
                    'clab_billing_email':post.get('clab_billing_email'),
                    'clab_billing_phone':post.get('clab_billing_phone'),
                    'clab_billing_mobile':post.get('clab_billing_mobile'),
                    'clab_state': '0_clab_nuevo'
                    
                    })
                
                return request.render('odoo15-compulab_registro_clientes_moduloweb.registration_success_template')#request.redirect('/')           
    
    @http.route('/confirmed', type='http', auth="public", website=True)     
    def _update_partner_data(self, **post_data):
            # Actualizar los datos del partner
        update_partner = post_data.get('update_partner')
        ruc = post_data.get('clab_RUC')
        write_ruc = request.env['registro.clientes.web'].sudo().search([('clab_RUC', '=', ruc)], limit=1)
        write_ruc_id = write_ruc.id
        state = '2_clab_editado'
        datos = {
                'clab_business_name': post_data.get('clab_business_name'),
                'clab_business_reason': post_data.get('clab_business_reason'),
                'clab_email': post_data.get('clab_email'),
                'clab_website': post_data.get('clab_website'),
                'clab_DV': post_data.get('clab_DV'),
                'clab_company_type': 'company',
                'sent_to_partner': False,
                
                
                'clab_phone':post_data.get('clab_phone'),
                'clab_mobile':post_data.get('clab_mobile'),
                'clab_direction':post_data.get('clab_direction'),
                
                'clab_contact_name':post_data.get('clab_contact_name'),
                'clab_contact_function':post_data.get('clab_contact_function'),
                'clab_contact_email':post_data.get('clab_contact_email'),
                'clab_contact_phone':post_data.get('clab_contact_phone'),
                'clab_contact_mobile':post_data.get('clab_contact_mobile'),
                
                'clab_billing_name':post_data.get('clab_billing_name'),
                'clab_billing_function':post_data.get('clab_billing_function'),
                'clab_billing_email':post_data.get('clab_billing_email'),
                'clab_billing_phone':post_data.get('clab_billing_phone'),
                'clab_billing_mobile':post_data.get('clab_billing_mobile'),
                'clab_state': state
            }
        if update_partner and write_ruc_id:
            # Si el usuario confirmó actualizar y hay un ID válido
            state = '2_clab_editado'            
            write_ruc.write(datos)
            return request.render('odoo15-compulab_registro_clientes_moduloweb.registration_success_template')#request.redirect('/')           

        else:
            state = '0_clab_nuevo'
            # de no existir entonces se crea normalmente 
            partner = request.env['registro.clientes.web'].sudo().create(datos)
            return request.render('odoo15-compulab_registro_clientes_moduloweb.registration_success_template')#request.redirect('/')           
        # else:
        #     return request.render('odoo15-compulab_registro_clientes_moduloweb.registration_failure_template')#request.redirect('/')           

    @http.route('/registrar_cliente_web', type='http', auth="public", website=True)
    def regiCliente(self):
        res_partner = request.env['res.partner'].sudo().search([])
        partner_vats = res_partner.mapped("vat")  # Obtén los RUCs
        values = {'partner_vats': partner_vats}  # Agrega partner_vats al contexto
        return request.render('odoo15-compulab_registro_clientes_moduloweb.register_template', values)
