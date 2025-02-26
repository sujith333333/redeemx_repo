import pytest
from src.vendor.utils import generate_qr_code, create_vendor_with_qr_code
import base64
import qrcode

def test_generate_qr_code():
    data = "Test QR Code Data"
    qr_code = generate_qr_code(data)
    assert isinstance(qr_code, str)

def test_create_vendor_with_qr_code():
    vendor_name = "Aruna"
    qr_code = create_vendor_with_qr_code(vendor_name)
    assert isinstance(qr_code, str)