from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError
class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "information about hostel"
    _order = "id desc, name"
    _rec_name = 'hostel_code'
    name = fields.Char(string="hostel Name", required=True)
    hostel_code = fields.Char(string="code", required=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default = True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char('Phone', required=True)
    mobile = fields.Char('Mobile', required=True)
    email = fields.Char('Email')
    hostel_floors = fields.Integer(string ="total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate Hostel record")
    type = fields.Selection([("male", "Boys"),("female","Girls"),("common","Common")], "Type",help="Type os Hostel",required=True, default="common")
    other_info = fields.Text("Other Information", help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating', digits='Rating Value')
    category_id = fields.Many2one('hostel.category')
         

    @api.depends('hostel_code')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.hostel_code:
                name = f'{name} ({record.hostel_code})'
            record.display_name = name

    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'closed'),
                   ('closed', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')

    def log_all_room_members(self):
        hostel_room_obj = self.env['hostel.room.member']  # This is an empty recordset of model hostel.room.member
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def find_partner(self):
        PartnerObj = self.env['res.partner']
        domain = [
            '&',('name','like','SerpentCS'),
            ('company_id.name','=','SCS'),
        ]
        partner = PartnerObj.search([domain])

class HostelRoomMember(models.Model):
    _name = 'hostel.room.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Room Member"
    partner_id = fields.Many2one('res.partner', ondelete="cascade")
    date_start = fields.Date(string="member since")
    date_end = fields.Date(string="Termination Date")
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of Birth')

class RoomCategory(models.Model):
    _name = 'hostel.room.category'
    _description = 'Hostel Room Category'
    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        'hostel.room.category',
        string='Parent Category',
        ondelete="restrict",
        index=True,
    )
    child_ids = fields.One2many(
        'hostel.room.category',
        'parent_id',
        string='Child Categories',
    )

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description':'Description for child 1'
        }

        categ2 = {
            'name': 'Child category 2',
            'description':'Description for child 2'
        }

        parent_category_val = {
            'name': 'Parent category ',
            'description':'Description for parent category',
            'child_ids': [
                (0,0,categ1),
                (0,0,categ2),
            ]
        }
        self.env['hostel.room.category'].create(parent_category_val)
        return True



