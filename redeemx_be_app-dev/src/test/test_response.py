import pytest
from response import RestResponse
from fastapi.responses import JSONResponse
import json

def test_rest_response_default_values():
    response = RestResponse()
    assert response.data is None
    assert response.message == ""
    assert response.error == ""
    assert response.metadata == {}

def test_rest_response_with_data():
    response_data = {"key": "value"}
    response = RestResponse(data=response_data)
    assert response.data == response_data
    assert response.message == ""
    assert response.error == ""
    assert response.metadata == {}

def test_rest_response_with_message():
    response = RestResponse(message="Success")
    assert response.data is None
    assert response.message == "Success"
    assert response.error == ""
    assert response.metadata == {}

def test_rest_response_with_error():
    response = RestResponse(error="An error occurred")
    assert response.data is None
    assert response.message == ""
    assert response.error == "An error occurred"
    assert response.metadata == {}

def test_rest_response_with_metadata():
    metadata = {"page": 1, "total": 10}
    response = RestResponse(metadata=metadata)
    assert response.data is None
    assert response.message == ""
    assert response.error == ""
    assert response.metadata == metadata

def test_to_json_method():
    response = RestResponse(data={"key": "value"}, message="Success", error="", metadata={"page": 1})
    json_response = response.to_json()
    assert isinstance(json_response, JSONResponse)
    assert json.loads(json_response.body) == {
        "data": {"key": "value"},
        "message": "Success",
        "error": "",
        "metadata": {"page": 1},
    }
