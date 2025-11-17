from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Background settings
    login_background_image = fields.Binary('Login Background Image')

    # Form container
    login_form_opacity = fields.Float('Form Opacity (%)', default=85.0)
    login_form_blur = fields.Float('Form Blur (px)', default=8.0)
    login_form_radius = fields.Float('Form Border Radius (px)', default=15.0)
    login_form_color = fields.Char('Form Background Color', default='#ffffff')


    # Form dimensions
    login_form_width = fields.Integer('Form Width (px)', default=400)
    login_form_height = fields.Integer('Form Height (px)', default=500)

    # Form positioning
    login_form_position = fields.Selection([
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    ], 'Form Position', default='center')

    # Login form container positioning
    login_container_position = fields.Selection([
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    ], 'Login Form Container Position', default='center')

    # Outer section styling
    login_outer_color = fields.Char('Outer Section Color', default='#f8f9fa')
    login_outer_opacity = fields.Float('Outer Section Opacity (%)', default=95.0)

    # Glassmorphism effect
    login_glass_transparency = fields.Float('Glass Transparency (%)', default=20.0)
    login_glass_border_opacity = fields.Float('Glass Border Opacity (%)', default=30.0)

    # Form fields styling
    login_field_bg_color = fields.Char('Field Background Color', default='#ffffff')
    login_field_border_color = fields.Char('Field Border Color', default='#ced4da')
    login_field_text_color = fields.Char('Field Text Color', default='#495057')

    # Button styling
    login_button_bg_color = fields.Char('Button Background Color', default='#007bff')
    login_button_text_color = fields.Char('Button Text Color', default='#ffffff')
    login_button_hover_color = fields.Char('Button Hover Color', default='#0056b3')

    def set_values(self):
        super().set_values()
        params = self.env['ir.config_parameter'].sudo()
        if self.login_background_image:
            params.set_param('login_bg_minimal.background_image', self.login_background_image)

        # Save all parameters
        form_params = {
            'form_opacity': self.login_form_opacity,
            'form_blur': self.login_form_blur,
            'form_radius': self.login_form_radius,
            'form_color': self.login_form_color,
            'form_width': self.login_form_width,
            'form_height': self.login_form_height,
            'form_position': self.login_form_position,
            'container_position': self.login_container_position,
            'outer_color': self.login_outer_color,
            'outer_opacity': self.login_outer_opacity,
            'glass_transparency': self.login_glass_transparency,
            'glass_border_opacity': self.login_glass_border_opacity,
            'field_bg_color': self.login_field_bg_color,
            'field_border_color': self.login_field_border_color,
            'field_text_color': self.login_field_text_color,
            'button_bg_color': self.login_button_bg_color,
            'button_text_color': self.login_button_text_color,
            'button_hover_color': self.login_button_hover_color,
        }

        for key, value in form_params.items():
            params.set_param(f'login_bg_minimal.{key}', value)

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()

        res.update({
            'login_background_image': params.get_param('login_bg_minimal.background_image', False),
            'login_form_opacity': float(params.get_param('login_bg_minimal.form_opacity', 85.0)),
            'login_form_blur': float(params.get_param('login_bg_minimal.form_blur', 8.0)),
            'login_form_radius': float(params.get_param('login_bg_minimal.form_radius', 15.0)),
            'login_form_color': params.get_param('login_bg_minimal.form_color', '#ffffff'),
            'login_form_width': int(params.get_param('login_bg_minimal.form_width', 400)),
            'login_form_height': int(params.get_param('login_bg_minimal.form_height', 500)),
            'login_form_position': params.get_param('login_bg_minimal.form_position', 'center'),
            'login_container_position': params.get_param('login_bg_minimal.container_position', 'center'),
            'login_outer_color': params.get_param('login_bg_minimal.outer_color', '#f8f9fa'),
            'login_outer_opacity': float(params.get_param('login_bg_minimal.outer_opacity', 95.0)),
            'login_glass_transparency': float(params.get_param('login_bg_minimal.glass_transparency', 20.0)),
            'login_glass_border_opacity': float(params.get_param('login_bg_minimal.glass_border_opacity', 30.0)),
            'login_field_bg_color': params.get_param('login_bg_minimal.field_bg_color', '#ffffff'),
            'login_field_border_color': params.get_param('login_bg_minimal.field_border_color', '#ced4da'),
            'login_field_text_color': params.get_param('login_bg_minimal.field_text_color', '#495057'),
            'login_button_bg_color': params.get_param('login_bg_minimal.button_bg_color', '#007bff'),
            'login_button_text_color': params.get_param('login_bg_minimal.button_text_color', '#ffffff'),
            'login_button_hover_color': params.get_param('login_bg_minimal.button_hover_color', '#0056b3'),
        })
        return res


