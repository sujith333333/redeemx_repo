from src.vendor.models import Vendor,Claim
import pytest
from datetime import datetime

def test_vendor_positive():
    v1=Vendor(vendor_name="Aruna",
              description="A test vendor",
              qr_code="",
              user_id=1,
              )
    assert v1.vendor_name=="Aruna"

# def test_vendor_negitive():
    # with pytest.raises(Exception):
#         v1=Vendor(vendor_name="Aruna@",
#                 description="A test vendor",
#                 qr_code="",
#                 user_id=1,
#                 )
        
# def test_vendor_negitive1():
#     with pytest.raises(Exception):
#         v1=Vendor(vendor_name="Aruna",
#                 description="A test vendor",
#                 qr_code=" ",
#                 user_id=1,
#                 )


def test_claim_positive():
    c1 = Claim(vendor_id="123e4567-e89b-12d3-a456-426614174000", points=100)
    assert c1.points == 100
    assert c1.status == "PENDING"
    assert c1.updated_at is None

def test_claim_negative_zero_points():
    with pytest.raises(ValueError, match="Points must be greater than 0."):
        Claim(vendor_id="123e4567-e89b-12d3-a456-426614174000", points=0)

def test_claim_negative_negative_points():
    with pytest.raises(ValueError, match="Points must be greater than 0."):
        Claim(vendor_id="123e4567-e89b-12d3-a456-426614174000", points=-10)

def test_claim_with_updated_status():
    now = datetime.utcnow()
    c2 = Claim(vendor_id="123e4567-e89b-12d3-a456-426614174000", points=500, status="APPROVED", updated_at=now)
    assert c2.status == "APPROVED"
    assert c2.updated_at == now
