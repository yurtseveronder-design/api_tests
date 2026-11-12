import pytest
from schemas import UserResponseSchema

def test_get_user_with_schema_validation(api_client):
    """Test fetching a user and validating the response against Pydantic schema."""
    response = api_client.get("/users/1")
    assert response.status_code == 200
    
    # Parse and validate the response JSON against the Pydantic schema model
    user_data = response.json()
    validated_user = UserResponseSchema(**user_data)
    
    # Assertions using strongly-typed attributes
    assert validated_user.id == 1
    assert isinstance(validated_user.email, str)
    assert isinstance(validated_user.address.city, str)