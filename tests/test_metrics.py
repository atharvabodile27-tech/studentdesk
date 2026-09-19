"""Test karo ki /metrics endpoint graceful hai (prometheus_client ho ya na ho)."""


def test_metrics_endpoint_exists(client):
    res = client.get("/metrics")
    # ya to 200 (prometheus_client installed) ya 501 (fallback message)
    assert res.status_code in (200, 501)


def test_metrics_contains_app_data_when_available(client):
    res = client.get("/metrics")
    if res.status_code == 200:
        body = res.get_data(as_text=True)
        assert "studentdesk_students_total" in body
    else:
        assert b"prometheus_client" in res.data
