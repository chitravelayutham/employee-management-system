import pytest

def pytest_addoption(parser):
    parser.addoption("--empid", action="store", default="EMP1000")
    parser.addoption("--name", action="store", default="Test User")
    parser.addoption("--email", action="store", default="test.user@example.com")
    parser.addoption("--department", action="store", default="IT")
    parser.addoption("--position", action="store", default="Tester")
    parser.addoption("--status", action="store", default="Active")


@pytest.fixture
def employee_data(request):
    return {
        "employeeId": request.config.getoption("--empid"),
        "name": request.config.getoption("--name"),
        "email": request.config.getoption("--email"),
        "department": request.config.getoption("--department"),
        "position": request.config.getoption("--position"),
        "status": request.config.getoption("--status"),
    }