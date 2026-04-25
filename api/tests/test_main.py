from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api import main


client = TestClient(main.app)


def test_create_job_returns_job_id(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(main, "r", mock_redis)

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


def test_get_job_returns_status_when_found(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.hget.return_value = b"queued"
    monkeypatch.setattr(main, "r", mock_redis)

    response = client.get("/jobs/test-job-id")

    assert response.status_code == 200
    assert response.json() == {
        "job_id": "test-job-id",
        "status": "queued"
    }


def test_get_job_returns_404_when_missing(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.hget.return_value = None
    monkeypatch.setattr(main, "r", mock_redis)

    response = client.get("/jobs/missing-job")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }

def test_health_check_returns_ok(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    monkeypatch.setattr(main, "r", mock_redis)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}