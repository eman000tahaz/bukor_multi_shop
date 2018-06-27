odoo.define('bu_multi_shop.screens', function (require) {
"use strict";

var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var core = require('web.core');
var Model = require('web.DataModel');
var utils = require('web.utils');
var formats = require('web.formats');

var QWeb = core.qweb;
var _t = core._t;

var round_pr = utils.round_precision;

/*ADD model and order_model and pos_ref to change the reciep ref in the ticket .... Amy*/
var model = require('web.Model');
var order_model = new model('pos.order');
var screens = require('point_of_sale.screens');    

screens.ReceiptScreenWidget.include({
    
    render_receipt: function() {
        /*ADD pos_ref .... Amy*/
        var order = this.pos.get_order();
        var fun_this = this ;
        order_model.call('get_pos_ref').then(function (res) { 
            var pos_ref = res.pos_reference ;
            var customer_no = res.customer_order_no 
            fun_this.$('.pos-receipt-container').html(QWeb.render('PosTicket',{
                widget:fun_this,
                order: order,
                receipt: order.export_for_printing(),
                orderlines: order.get_orderlines(),
                paymentlines: order.get_paymentlines(),
                pos_ref: pos_ref,
                shop_name: res.shop_name,
                customer_no: customer_no,
            }));
        });
        
    },
});

/*gui.define_screen({name:'receipt', widget: ReceiptScreenWidget});
*/

});

