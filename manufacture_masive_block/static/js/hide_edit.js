odoo.define('manufacture_masive_block.block_edit', function (require) {
    var FormView = require('web.FormView');
    FormView.include({
     load_record: function() {
      this._super.apply(this, arguments);
      if (this.model === 'mrp.production') {
          if (this.datarecord && (this.datarecord.state_block === 'block')) {
            this.$buttons.find('.o_form_button_edit').css({'display':'none'});
          }
          else {
            this.$buttons.find('.o_form_button_edit').css({'display':''});
          }
                                        }
                            }
                        })
                    });