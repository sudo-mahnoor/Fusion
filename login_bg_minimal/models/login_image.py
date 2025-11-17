from odoo import models, fields

class LoginImage(models.Model):
    _name = 'login.image'
    _description = 'Login Background Images'

    name = fields.Char('Name', required=True)
    image = fields.Binary('Image', required=True)
    active = fields.Boolean('Active', default=True)
