import qrcode
import base64
from io import BytesIO


def generate_qr_code(data: str) -> str:
    """
    Generate a QR code from the input data and return it as a base64-encoded string.
    """
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,  # QR Code version (1-40, adjusts the size)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Thickness of the border
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to a base64 string
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return qr_code_base64


def create_vendor_with_qr_code(vendor_name: str):
    """
    Create a vendor and generate a QR code for them.
    """
    # Generate a unique QR code
    qr_data = f"Vendor: {vendor_name}"
    qr_code_string = generate_qr_code(qr_data)

    return qr_code_string

    


