odoo.define('mrp_prelimit.action_button', function (require) {
    "use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var _t = core._t;
    ListController.include({
       renderButtons: function($node) {
       this._super.apply(this, arguments);
           if (this.$buttons) {
             this.$buttons.find(".oe_action_button").click(this.proxy('action_def'));
             }
       },
    })
})

function action_def() {
    var self = this
    var user = session.uid;
    rpc.query({
        model: "mrp.prelimit",
        method: receive_invoice,
        args: [[user],{'id':user}],
        });
    };

 function receive_invoice() {
    var self = this
    var user = session.uid;
    rpc.query({
        model: "account.move",
        method: 'get_values',
        args: [[user],{'id':user}],
        }).then(function () {
            self.do_action({
                name: _t('action_invoices'),
                type: "ir.actions.act_window",
                res_model: "name.name",
                views: [["tree", 'form']],
                view_mode: 'tree',
                target: 'new',
            });
            window.location
        });
    }