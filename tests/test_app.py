"""
Integration tests - Flask routes / pages (test client se).
"""


class TestHealthAndPages:
    def test_health_endpoint(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.get_json()["status"] == "ok"

    def test_login_page_loads(self, client):
        res = client.get("/login")
        assert res.status_code == 200
        assert b"StudentDesk" in res.data

    def test_dashboard_requires_login(self, client):
        res = client.get("/")
        assert res.status_code == 302
        assert "/login" in res.headers["Location"]

    def test_dashboard_after_login(self, auth_client):
        res = auth_client.get("/")
        assert res.status_code == 200
        assert b"Dashboard" in res.data

    def test_student_list_page(self, auth_client):
        res = auth_client.get("/students")
        assert res.status_code == 200
        assert b"Aarav Sharma" in res.data

    def test_wrong_password_rejected(self, client):
        res = client.post("/login", data={"username": "admin", "password": "wrong"},
                          follow_redirects=True)
        assert b"Galat username ya password" in res.data

    def test_logout(self, auth_client):
        res = auth_client.get("/logout", follow_redirects=True)
        assert res.status_code == 200


class TestStudentCRUDUI:
    def test_add_student_via_form(self, auth_client):
        res = auth_client.post("/students/new", data={
            "roll_no": "CS2025999", "name": "Test Student", "email": "test999@example.com",
            "course": "B.Tech CSE", "year": "2", "marks": "77.5", "status": "Active",
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Test Student" in res.data

    def test_duplicate_roll_no_rejected(self, auth_client):
        payload = {"roll_no": "CS2021001", "name": "Dup", "email": "dup@example.com",
                   "course": "MCA", "year": "1", "marks": "50", "status": "Active"}
        res = auth_client.post("/students/new", data=payload, follow_redirects=True)
        assert b"pehle se exist karta hai" in res.data

    def test_marks_out_of_range_rejected(self, auth_client):
        payload = {"roll_no": "CS999", "name": "Bad", "email": "bad@example.com",
                   "course": "MCA", "year": "1", "marks": "150", "status": "Active"}
        res = auth_client.post("/students/new", data=payload, follow_redirects=True)
        assert b"0 se 100" in res.data

    def test_delete_student(self, auth_client):
        res = auth_client.post("/students/1/delete", follow_redirects=True)
        assert res.status_code == 200

    def test_search_filters(self, auth_client):
        res = auth_client.get("/students?q=Aarav")
        assert b"Aarav Sharma" in res.data
        assert b"Kabir Joshi" not in res.data
