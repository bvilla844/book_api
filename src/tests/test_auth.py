from src.auth.schemas import UserCreateModel
from src.config import Config

auth_prefix = "/api/v1/auth"

def test_user_creation(fake_session, fake_user_service, test_client):
    signup_data = {
        "username": "jod35",
        "email": "jodes@gmail.com",
        "first_name": "jode",
        "last_name": "35",
        "password": "test123"
    }

    response = test_client.post(
        url=f"{auth_prefix}/signup",  # <- corregido
        json=signup_data,
    )

    user_data = UserCreateModel(**signup_data)

    # Asume que fake_user_service.user_exists es un mock
    fake_user_service.user_exists.assert_called_once_with(signup_data["email"], fake_session)
    fake_user_service.create_user.assert_called_once_with(user_data, fake_session)

    assert response.status_code == 201
    assert "user" in response.json()
    assert response.json()["user"]["email"] == signup_data["email"]
