from datetime import timedelta

from odoo import models,fields,api
class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = "Hostel Student Information"

    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """method to check duration"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date-rec.admission_date).days




    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date-stu.admission_date).days
                if duration!= stu.duration:
                    stu.discharge_date = (stu.admission_date+timedelta(days=stu.duration)).strftime('%Y-%m-%d')




    _inherits = {'res.partner': 'partner_id'}
    name = fields.Char("Student Name")
    gender = fields.Selection([("male","Male"),("female","Female"),("other", "Other")],
    string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate Hostel record")
    room_id  = fields.Many2one("hostel.room", "Room", help="Select hostel room")
    partner_id = fields.Many2one("res.partner",ondelete='cascade')
    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')
    status = fields.Selection([("draft","Draft"),("reservation","Reservation"),("pending","Pending"),("paid","Done"),("discharge","Discharge"),("cancel","Cancel")],string="status",copy=False,default="draft",help="Status of the student hostel")
    admission_date = fields.Date(string="Admission Date",help="Date of Admission in hostel", default=fields.Datetime.today)
    discharge_date = fields.Date(string="Discharge Date",help="Date of Discharge", default=fields.Datetime.today)
    duration = fields.Integer("Duration", compute="_compute_check_duration",
                              inverse="_inverse_duration",
                              help="Enter duration of living")

