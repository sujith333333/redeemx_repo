import pytest
from datetime import datetime
from src.vendor.schemas import VendorInputSchema, UpdateVendorInputSchema,ClaimRequest, ClaimResponse, ClaimUpdate

def test_vendor_input_positive():
    v1 = VendorInputSchema(
        name="Aruna",
        username="aruna",
        password="ArunaArun1@",
        emp_id="AJA1000",
        email="aruna@email.com",
        mobile_number="9876543210",
        is_vendor=1,
        vendor_name="Aruna",
        description="A trusted vendor"
    )
    assert v1.name == "Aruna"
    assert v1.email == "aruna@email.com"
    assert v1.mobile_number == "9876543210"
    assert v1.vendor_name == "Aruna"

def test_vendor_input_negitive():
    with pytest.raises(ValueError) as exc_info:
        v1=VendorInputSchema(
            name="Aruna",
            username="aruna",
            password="arunarun",
            emp_id="AJA1000",
            email="aruna@email.com",
            mobile_number="9876543210",
            is_vendor=1,
            vendor_name="Aruna",
            description="A trusted vendor")
    error_message = str(exc_info.value)
    print("Actual Error Message:", error_message)  
    assert "String should have at least 8 characters" in error_message or "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character." in error_message

def test_update_vendor_schema():
    v2 = UpdateVendorInputSchema(
        name="New Aruna",
        email="new_aruna@email.com"
    )
    assert v2.name == "New Aruna"
    assert v2.email == "new_aruna@email.com"

def test_claim_request_schema():
    c1 = ClaimRequest(points=100)
    assert c1.points == 100

def test_claim_response_schema():
    c2 = ClaimResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        vendor_id="vendor123",
        points=200,
        status="Pending",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None
    )
    assert c2.id == "123e4567-e89b-12d3-a456-426614174000"
    assert c2.vendor_id == "vendor123"
    assert c2.points == 200
    assert c2.status == "Pending"
    assert c2.created_at == datetime(2024, 1, 1, 12, 0, 0)
    assert c2.updated_at is None

def test_claim_update_schema():
    c3 = ClaimUpdate(approved_points=150)
    assert c3.approved_points == 150