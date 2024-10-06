from odoo import models, fields, api


class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"
    name = fields.Char("Name", help="Provided Hostel Amenity")
    active = fields.Boolean("Active", help="Activate/Deactivate whether the amenity should be given or not")
    color = fields.Integer()
    popularity = fields.Selection(
        [('no', 'No Demand'), ('low', 'Low Demand'), ('medium', 'Average Demand'), ('high', 'High Demand'), ])

    # hostel_amenities_ids = fields.Many2many(
    #     "hostel.amenities",
    #     "hostel_room_amenities_rel", "room_id", "amenitiy_id",
    #     string="Amenities", domain="[('active', '=', True)]",
    #     help="Select hostel room amenities")
