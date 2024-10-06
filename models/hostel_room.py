from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active





class HostelRoom(models.Model):
    _name = "hostel.room"
    _inherit = ['base.archive']
    remarks  = fields.Text(string='Remarks')
    hostel_id = fields.Many2one("hostel.hostel","hostel", help="Name of hostel")
    name = fields.Char(string="Room Name", required=True)
    floor_no = fields.Integer("Floor No",default=1, help="Floor No")
    room_no = fields.Char("Room No", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter your rent amount per month")
    student_ids = fields.One2many("hostel.student","room_id", string="Students", help="Enter students")
    student_per_room = fields.Integer("Student Per Room", required=True, help="Students allocated per room")
    availability = fields.Float(compute="_compute_check_availability", string="Availability", help="Room availability in hostel")
    admission_date = fields.Date("Admission Date", help="Date of Admission of hostel", default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date", help="Date on which student discharge")
    duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration", help="Enter duration of living")
    stage_id = fields.Selection([('draft','Draft'),('available','Available')], default='draft')
    color = fields.Integer()
    popularity = fields.Selection(
        [('no', 'No Demand'), ('low', 'Low Demand'), ('medium', 'Average Demand'), ('high', 'High Demand'), ])

    hostel_amenities_ids = fields.Many2many(
        "hostel.amenities",
        "hostel_room_amenities_rel", "room_id", "amenitiy_id",
        string="Amenities", domain="[('active', '=', True)]",
        help="Select hostel room amenities")

    _sql_constraints = [
        ("room_no_unique", "unique(room_no)", "Room number must be unique")
    ]


    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """constraint on negative amount"""
        if self.rent_amount<0:
            raise ValidationError(_("Rent Amount Per Month should to be positive value"))


    @api.depends("student_per_room","student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room-len(rec.student_ids.ids)


    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date-rec.admission_date).days

    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date- stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date+timedelta(days=stu.duration)).strftime('%Y-%m-%d')



    def update_room_no(self):
        self.ensure_one()
        self.room_no  = "RM002"



    @api.model
    def room_with_multiple_rooms(self, all_rooms):
        return all_rooms.filter(lambda b: len(b.member_ids)>1)


    @api.model
    def get_members_names(self, rooms):
        return rooms.mapped('member_ids.name')

    @api.model
    def sort_rooms_by_rating(self,rooms):
        return rooms.sorted(key='room_id.rating')


    def write(self, values):
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify'
                    'manager_remarks'
                )
        return super(HostelRoom, self).write(values)

    @api.model
    def _default_room_stage(self):
        Stage = self.env['hostel.room.stage']
        return Stage.search([],limit=1)




    @api.model
    def _group_expand_stages(self, stages, domain, order):
        return stages.search([], order=order)

