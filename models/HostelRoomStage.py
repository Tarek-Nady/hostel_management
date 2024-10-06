from odoo import models, fields

class HostelRoomStage(models.Model):
    _name = 'hostel.room.stage'
    _order =  'sequence,name'
    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
    fold = fields.Boolean(string='Fold?')