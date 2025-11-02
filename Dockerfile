FROM odoo:17.0

USER root

# Install Python dependencies for QR code generation
RUN pip3 install --no-cache-dir qrcode[pil]

USER odoo
