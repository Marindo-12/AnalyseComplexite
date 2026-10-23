from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["endpoint"] == "POST /analyze"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_valid_python():
    response = client.post(
        "/analyze",
        json={
            "code": (
                "def example(n):\n"
                "    total = 0\n"
                "    for i in range(n):\n"
                "        total += i\n"
                "    return total"
            ),
            "language": "python",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["language"] == "python"
    assert result["time_complexity"] == "O(n)"
    assert result["space_complexity"] == "O(1)"


def test_analyze_invalid_python():
    response = client.post(
        "/analyze",
        json={
            "code": "def example(:",
            "language": "python",
        },
    )

    assert response.status_code == 400


def test_unsupported_language():
    response = client.post(
        "/analyze",
        json={
            "code": "public class Example {}",
            "language": "java",
        },
    )

    assert response.status_code == 400
    assert "Python" in response.json()["detail"]


def test_empty_code_is_rejected():
    response = client.post(
        "/analyze",
        json={
            "code": "",
            "language": "python",
        },
    )

    assert response.status_code == 422


def test_missing_code_is_rejected():
    response = client.post(
        "/analyze",
        json={
            "language": "python",
        },
    )

    assert response.status_code == 422