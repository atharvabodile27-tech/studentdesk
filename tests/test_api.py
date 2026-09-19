"""
API tests - JSON endpoints (Jenkins/API consumers ke liye).
"""
import json


class TestStudentAPI:
    def test_list_students(self, client):
        res = client.get("/api/students")
        assert res.status_code == 200
        data = res.get_json()
        assert data["count"] == 6
        assert len(data["students"]) == 6

    def test_get_single_student(self, client):
        res = client.get("/api/students/1")
        assert res.status_code == 200
        assert res.get_json()["roll_no"] == "CS2021001"

    def test_get_missing_student_404(self, client):
        res = client.get("/api/students/9999")
        assert res.status_code == 404

    def test_create_student(self, client):
        payload = {"roll_no": "API001", "name": "API Student", "email": "api@example.com",
                   "course": "MCA", "year": 1, "marks": 81.0}
        res = client.post("/api/students", json=payload)
        assert res.status_code == 201
        assert res.get_json()["grade"] == "A"
        assert res.get_json()["result"] == "PASS"

    def test_create_student_missing_fields(self, client):
        res = client.post("/api/students", json={"name": "Incomplete"})
        assert res.status_code == 400
        assert "Missing fields" in res.get_json()["error"]

    def test_create_student_invalid_marks(self, client):
        payload = {"roll_no": "API002", "name": "X", "email": "x@x.com",
                   "course": "MCA", "year": 1, "marks": 250}
        res = client.post("/api/students", json=payload)
        assert res.status_code == 400

    def test_create_duplicate_roll_no_409(self, client):
        payload = {"roll_no": "CS2021001", "name": "Dup", "email": "dup2@example.com",
                   "course": "MCA", "year": 1, "marks": 50}
        res = client.post("/api/students", json=payload)
        assert res.status_code == 409

    def test_delete_student(self, client):
        res = client.delete("/api/students/2")
        assert res.status_code == 200
        assert res.get_json()["deleted"] == 2
        assert client.get("/api/students/2").status_code == 404

    def test_stats_endpoint(self, client):
        res = client.get("/api/stats")
        assert res.status_code == 200
        data = res.get_json()
        assert data["total_students"] == 6
        assert "average_marks" in data
