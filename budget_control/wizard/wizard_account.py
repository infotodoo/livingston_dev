from odoo import models,fields,api

class WizardAccount(models.Model):
    _name = 'wizard.account'
    _description = 'This is the wizard for account'

    message = fields.Char()
    users_ids = fields.Many2many('res.users','users_account_wizard_rel','account_id','user_id','Users')

    def action_create_activity(self):
        for record in self:
            account_id = self.env['account.move'].browse(self._context.get('active_id'))
            model_id = self.env.ref('account.model_account_move')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = 'El pedido ha sido bloqueado por superar el presupuesto, por favor revisar'
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': account_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].create(activity_data)
        return True