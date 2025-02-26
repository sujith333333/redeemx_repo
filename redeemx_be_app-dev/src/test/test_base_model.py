import pytest
from datetime import datetime, timezone
from src.models import BaseModel
import uuid

def test_base_model_defaults():
    model_instance = BaseModel()
    assert isinstance(model_instance.id, str)
    try:
        uuid_obj = uuid.UUID(model_instance.id)
        assert isinstance(uuid_obj, uuid.UUID)
    except ValueError:
        pytest.fail(f"Generated id '{model_instance.id}' is not a valid UUID")
    
    assert isinstance(model_instance.created_at, datetime)
    created_at_utc = model_instance.created_at.astimezone(timezone.utc)
    assert created_at_utc.tzinfo == timezone.utc  
    now_utc = datetime.now(timezone.utc)
    assert created_at_utc <= now_utc
    assert (now_utc - created_at_utc).total_seconds() < 1

def test_id_uniqueness():
    model_instance_1 = BaseModel()
    model_instance_2 = BaseModel()
    assert model_instance_1.id != model_instance_2.id  


