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
             this.$buttons.find(".oe_action_button").click(this.proxy('receive_invoice'));
             }
       },
        
    receive_invoice: function () {
            var self = this
            var user = session.uid;
            /*var date = new Date();
            let day = date.getDate()
            let month = date.getMonth() + 1
            let year = date.getFullYear()*/
            rpc.query({
                model: 'mrp.prelimit',
                method: 'action_view_journal',
                args: [[]],
                }).then(function (e) {
                    self.do_action({
                        name: _t('Journal'),
                        context: {date: e.domain[0][2]},
                        type: e.type,
                        res_model: e.res_model,
                        views: [[false,'tree'],[false,'form']],
                    });
                    debugger;
                    window.location
                });
            },
    })
});