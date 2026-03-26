""" import pytest
from fastapi import status
import httpx
import pytest
import httpx
from fastapi import status
from app.main import app

@pytest.mark.anyio
async def test_register_duplicate_username():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "username": "dupeuser",
            "email": "dupe@test.com",
            "password": "StrongPass123",
            "role": "user"
        }
        await client.post("/auth/register", json=payload)
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 409

@pytest.mark.anyio
async def test_register_weak_password():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "username": "weakuser",
            "email": "weak@test.com",
            "password": "123",
            "role": "user"
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 422

@pytest.mark.anyio
async def test_register_missing_fields():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {"username": "incomplete"}
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 422

@pytest.mark.anyio
async def test_login_success():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        reg_payload = {
            "username": "loginuser",
            "email": "login@test.com",
            "password": "StrongPass123",
            "role": "user"
        }
        await client.post("/auth/register", json=reg_payload)
        login_payload = {
            "username": "loginuser",
            "password": "StrongPass123"
        }
        response = await client.post("/auth/login", data=login_payload)
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.anyio
async def test_login_invalid_credentials():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        login_payload = {
            "username": "nouser",
            "password": "wrongpass"
        }
        response = await client.post("/auth/login", data=login_payload)
        assert response.status_code == 401

@pytest.mark.anyio
async def test_token_validation():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        reg_payload = {
            "username": "tokenuser",
            "email": "token@test.com",
            "password": "StrongPass123",
            "role": "user"
        }
        await client.post("/auth/register", json=reg_payload)
        login_payload = {
            "username": "tokenuser",
            "password": "StrongPass123"
        }
        login_resp = await client.post("/auth/login", data=login_payload)
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        # Replace /protected-route with an actual protected endpoint in your app
        # response = await client.get("/protected-route", headers=headers)
        # assert response.status_code == 200
        assert token is not None


@pytest.mark.anyio
async def test_register_user_success():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "StrongPass123",
            "role": "user"
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User registered successfully"

@pytest.mark.anyio
async def test_login_success_returns_jwt(client, create_user):
    await create_user(username="loginuser", password="StrongPass123")

    response = await client.post("/auth/login", json={
        "username": "loginuser",
        "password": "StrongPass123"
    })

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_wrong_password_returns_401(client, create_user):
    await create_user(username="user1", password="CorrectPass123")

    response = await client.post("/auth/login", json={
        "username": "user1",
        "password": "WrongPass"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.anyio
async def test_login_nonexistent_user_returns_401(client):
    response = await client.post("/auth/login", json={
        "username": "nouser",
        "password": "any"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.anyio
async def test_login_missing_fields_returns_422(client):
    response = await client.post("/auth/login", json={
        "username": "onlyusername"
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# -----------------------------------
# 🔒 PROTECTED ROUTE TESTS
# -----------------------------------

@pytest.mark.anyio
async def test_protected_route_without_token_returns_401(client):
    response = await client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_protected_route_with_valid_token_succeeds(client, create_user):
    await create_user(username="validuser")

    token = create_access_token({
        "username": "validuser",
        "role": "user"
    })

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "validuser"


@pytest.mark.anyio
async def test_protected_route_with_expired_token_returns_401(client):
    expired_token = jwt.encode(
        {
            "username": "user",
            "role": "user",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=10)
        },
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_protected_route_with_invalid_token_returns_401(client):
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# -----------------------------------
# 🛡️ RBAC TESTS
# -----------------------------------

@pytest.mark.anyio
async def test_admin_route_with_user_role_returns_403(client, create_user):
    await create_user(username="normaluser", role="user")

    token = create_access_token({
        "username": "normaluser",
        "role": "user"
    })

    response = await client.get(
        "/users/admin-dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_admin_route_with_admin_role_succeeds(client, create_user):
    await create_user(username="adminuser", role="admin")

    token = create_access_token({
        "username": "adminuser",
        "role": "admin"
    })

    response = await client.get(
        "/users/admin-dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK


# -----------------------------------
# 🔍 JWT VALIDATION TESTS
# -----------------------------------

@pytest.mark.anyio
async def test_jwt_contains_correct_payload(client, create_user):
    await create_user(username="payloaduser", role="user")

    response = await client.post("/users/login", json={
        "username": "payloaduser",
        "password": "StrongPass123"
    })

    token = response.json()["access_token"]

    decoded = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")]
    )

    assert decoded["username"] == "payloaduser"
    assert decoded["role"] == "user"
    assert "exp" in decoded


@pytest.mark.anyio
async def test_token_without_role_fails(client):
    token = create_access_token({"username": "user"})  # missing role

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED  

     """