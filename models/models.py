# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('website'):
                vals['website'] = self.env['res.partner']._clean_website(vals['website'])
        leads = super(Lead, self).create(vals_list)

        for lead, values in zip(leads, vals_list):
            if any(field in ['active', 'stage_id'] for field in values):
                lead._handle_won_lost(values)
            if lead.message_follower_ids:
                for follower in lead.message_follower_ids:
                    if follower.partner_id.customer_rank != 0:
                        follower.unlink()
                    if follower.partner_id.id == lead.partner_id.id:
                        follower.unlink()

        return leads

