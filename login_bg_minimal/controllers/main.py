from odoo import http
from odoo.http import request
import base64

class LoginBackgroundController(http.Controller):

    @http.route('/login_bg_minimal/background_image', type='http', auth='none')
    def get_background_image(self):
        try:
            image_data = request.env['ir.config_parameter'].sudo().get_param('login_bg_minimal.background_image', False)
            if image_data:
                return request.make_response(
                    base64.b64decode(image_data),
                    headers=[('Content-Type', 'image/png')]
                )
        except:
            pass
        return request.not_found()

    @http.route('/login_bg_minimal/dynamic_css', type='http', auth='none')
    def get_dynamic_css(self):
        try:
            params = request.env['ir.config_parameter'].sudo()

            # Get parameters with defaults
            opacity = float(params.get_param('login_bg_minimal.form_opacity', '85.0')) / 100
            blur = float(params.get_param('login_bg_minimal.form_blur', '8.0'))
            radius = float(params.get_param('login_bg_minimal.form_radius', '15.0'))
            color = params.get_param('login_bg_minimal.form_color', '#ffffff')
            width = int(params.get_param('login_bg_minimal.form_width', '400'))
            height = int(params.get_param('login_bg_minimal.form_height', '500'))
            position = params.get_param('login_bg_minimal.form_position', 'center')

            # Convert hex to rgba
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

            # Set justify-content based on position
            justify_content = 'center'
            if position == 'left':
                justify_content = 'flex-start'
            elif position == 'right':
                justify_content = 'flex-end'

            css = f"""
            /* Apply only to login page */
            .oe_login html,
            .oe_login body,
            body:has(.oe_login_form) {{
                background: url('/login_bg_minimal/background_image'), linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%) !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
                min-height: 100vh !important;
                margin: 0 !important;
                padding: 20px !important;
                display: flex !important;
                justify-content: {justify_content} !important;
                align-items: center !important;
            }}

            /* Login form styling */
            .o_database_list,
            .oe_login_form,
            .card {{
                background: rgba({r}, {g}, {b}, {opacity}) !important;
                border-radius: {radius}px !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
                backdrop-filter: blur({blur}px) !important;
                -webkit-backdrop-filter: blur({blur}px) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                width: {width}px !important;
                min-height: {height}px !important;
                max-width: 90% !important;
                padding: 30px !important;
                margin: 0 auto !important;
                position: relative !important;
            }}
            """

            return request.make_response(
                css,
                headers=[('Content-Type', 'text/css')]
            )
        except Exception as e:
            # Return basic CSS if there's an error
            return request.make_response(
                "body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }",
                headers=[('Content-Type', 'text/css')]
            )

