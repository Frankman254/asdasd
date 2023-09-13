// Este codigo sirve NO TOCAR O BORRAR********************************************************
// const sugerencias = document.querySelector('#suggestions')

// document.addEventListener("keyup", e => {
//     if (e.target.matches("#buscador")) {
//         console.log(e.target.value);
//         sugerencias.innerText = e.target.value;
//     }
// });

// Funciona esta parte del codigo**************************************************************

// odoo.define('odoo15-compulab_registro_clientes_moduloweb.form_registration', function (require) {
//     "use strict";

//     var rpc = require('web.rpc');
    
//     // Se espera que la página haya cargado para adjuntar los eventos
//     $(document).ready(function() {
//         $("#buscador").on("keyup", function(e) {
//             let searchTerm = e.target.value;

//             // Si searchTerm no está vacío, busca en la base de datos
//             if (searchTerm) {
//                 rpc.query({
//                     model: 'res.partner',
//                     method: 'search_read',
//                     domain: [['vat', 'ilike', searchTerm]],
//                     fields: ['name', 'vat'],
//                     limit: 1  // solo se obtiene el primer resultado
//                 }).then(function(partners) {
//                     if (partners.length) {
//                         // muestra el valor 'vat' del primer socio encontrado
//                         $('#suggestions').text(partners[0].vat);
//                     } else {
//                         $('#suggestions').text('No se encontraron resultados');
//                     }
//                 });
//             } else {
//                 // Si el campo de búsqueda está vacío, restablece las sugerencias
//                 $('#suggestions').text('Sugerencias');
//             }
//         });
//     });
// });


odoo.define('odoo15-compulab_registro_clientes_moduloweb.form_registration', function (require) {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        const button = document.getElementById("mySubmitButton");
        const image = document.createElement("img");
        image.src = "/odoo15-compulab_registro_clientes_moduloweb/static/description/registrer.png";
        image.alt = "Registrar";
        button.appendChild(image);
    });
    var rpc = require('web.rpc');

    $(document).ready(function() {
        
    // Manejador de evento para el checkbox contacto principal
    $('#showContactInfo').on('change', function() {
        if ($(this).prop('checked')) {
            // Si el checkbox está marcado, mostramos los campos
            $('#contactInfo').html(`
            <div class="divider"></div>
            <div class="form-title">Contacto Principal</div>
            <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="contactName">Nombre:</label>
                    <input type="text" id="contactName" name="clab_contact_name" class="form-control" required="true" placeholder="Nombre y Apellido de Contacto Principal"/>
                </div>
            </div>

            <!-- Puesto de trabajo -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="jobPosition">Puesto de trabajo:</label>
                    <input type="text" id="jobPosition" name="clab_contact_function" class="form-control"  placeholder="Puesto de Trabajo del Contacto Principal"/>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Telefono -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="phone">Teléfono:</label>
                    <input type="text" id="phone" name="clab_contact_phone" class="form-control" placeholder="Teléfono de Contacto Principal"/>
                </div>
            </div>

            <!-- Celular -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="cellphone">Celular:</label>
                    <input type="text" id="cellphone" name="clab_contact_mobile" class="form-control" required="true" placeholder="Móvil de Contacto Principal"/>
                </div>
            </div>
        </div>        

        <div class="row">
            <!-- Email  -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="clab_contact_email" class="form-control"  placeholder="Correo de Contacto Principal"/>
                </div>
            </div>

            <!-- Otro campo -->
            <div class="col-md-6">
                <div class="form-group">

                </div>
            </div>
        </div>                                                                                           
            `)
            $('#contactInfo').slideDown(); // Puedes usar .show() si no quieres una transición
            // $('#contactInfo input').prop('disabled', false);

        } else {
            // Si el checkbox no está marcado, ocultamos y limpiamos los campos
            $('#contactInfo').slideUp(function() {
                $('#contactInfo input').val('');  // Limpiar todos los inputs dentro de #contactInfo
                // $('#contactInfo input').prop('disabled', true);
                $('#contactInfo').empty();
            });
        }
    });

    $('#showContactCobrosInfo').on('change', function() {
        if ($(this).prop('checked')) {
            // Si el checkbox está marcado, mostramos los campos
            $('#contactCobrosInfo').html(`
            <div class="divider"></div>
            <div class="form-title">Contacto Cobros</div>

            <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="contactName">Nombre:</label>
                    <input type="text" id="contactName" name="clab_billing_name" class="form-control" required="true" placeholder="Nombre y Apellido de Contacto de Cobros"/>
                </div>
            </div>

            <!-- Puesto de trabajo -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="jobPosition">Puesto de trabajo:</label>
                    <input type="text" id="jobPosition" name="clab_billing_function" class="form-control"  placeholder="Puesto de Trabajo del Contacto de Cobros"/>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- Telefono -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="phone">Teléfono:</label>
                    <input type="text" id="phone" name="clab_billing_phone" class="form-control" placeholder="Teléfono de Contacto de Cobros"/>
                </div>
            </div>

            <!-- Celular -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="cellphone">Celular:</label>
                    <input type="text" id="cellphone" name="clab_billing_mobile" class="form-control" required="true" placeholder="Móvil de Contacto de Cobros"/>
                </div>
            </div>
        </div>        

        <div class="row">
            <!-- Email  -->
            <div class="col-md-6">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="clab_billing_email" class="form-control"  placeholder="Correo de Contacto de Cobros"/>
                </div>
            </div>

            <!-- Otro campo -->
            <div class="col-md-6">
                <div class="form-group">

                </div>
            </div>
        </div>                                                                                           
            `)
            $('#contactCobrosInfo').slideDown(); // Puedes usar .show() si no quieres una transición
            // $('#contactCobrosInfo input').prop('disabled', false);

        } else {
            // Si el checkbox no está marcado, ocultamos y limpiamos los campos
            $('#contactCobrosInfo').slideUp(function() {
                $('#contactCobrosInfo input').val('');  // Limpiar todos los inputs dentro de #contactInfo
                $('#contactCobrosInfo input').prop('disabled', true);
            });
        }
    });


        $("#buscador").on("keyup", function(e) {
            let searchTerm = e.target.value;
            // Limpiar sugerencias anteriores
            $('#suggestions').empty();
            
            if (searchTerm) {
                rpc.query({
                    model: 'res.partner',
                    method: 'search_read',
                    domain: [['vat', 'ilike', searchTerm]],
                    fields: ['name', 'vat'],
                    limit: 10  // obtener hasta 10 resultados
                }).then(function(partners) {
                    if (partners.length) {
                        partners.forEach(function(partner){
                            // Agregar tanto el vat (RUC) como el name en el dropdown
                            var suggestionContent = partner.name + " | " + partner.vat + " | ";
                            $('#suggestions').append('<div class="suggestion-item" data-vat="' + partner.vat + '">' + suggestionContent + '</div>');
                        });
                    } else {
                        $('#suggestions').append('<div class="suggestion-item">No se encontraron resultados</div>');
                    }
                });
            }
        });
        // Cuando se hace clic en una sugerencia, coloca solo el RUC en el campo de búsqueda
        $(document).on('click', '.suggestion-item', function() {
            $('#buscador').val($(this).data('vat'));  // Usar el valor del atributo data-vat
            $('#suggestions').empty();  // Limpiar sugerencias después de seleccionar
        });

    // Limpiar sugerencias al hacer clic en cualquier otro lugar del documento
        $(document).on("click", function(event) {
            if (!$(event.target).closest("#buscador").length) {
                $('#suggestions').empty();
            }
        });
    
        // Restaurar las sugerencias si el usuario hace clic en el campo de búsqueda nuevamente
        $("#buscador").on("click", function() {
            let searchTerm = $(this).val();
            if (searchTerm) {
                rpc.query({
                    model: 'res.partner',
                    method: 'search_read',
                    domain: [['vat', 'ilike', searchTerm]],
                    fields: ['name', 'vat'],
                    limit: 10  // obtener hasta 10 resultados
                }).then(function(partners) {
                    if (partners.length) {
                        partners.forEach(function(partner){
                            // Agregar tanto el vat (RUC) como el name en el dropdown
                            var suggestionContent = partner.name + " | " + partner.vat + " | ";
                            $('#suggestions').append('<div class="suggestion-item" data-vat="' + partner.vat + '">' + suggestionContent + '</div>');
                        });
                    } else {
                        $('#suggestions').append('<div class="suggestion-item">No se encontraron resultados</div>');
                    }
                });
            }
        });
    });


});





