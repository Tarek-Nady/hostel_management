from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    is_hostel_rector = fields.Boolean(string="Hostel Rector", help="Activate if the following person is hostel rector")
    assign_room_ids = fields.Many2many('library.book', string="Authored Books")
    count_assign_room = fields.Integer(string="Count Assign Room", compute="_compute_count_room")

    @api.depends('assign_room_ids')
    def _compute_count_room(self):
        for partner in self:
            partner.count_assign_room = partner.count_assign_room + 1