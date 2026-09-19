"""
Unit tests - business logic (grade/result calculation).
Ye tests DB ya web server pe depend nahi karte -> fastest tests.
"""
from app.models import Student


def make_student(marks):
    return Student(roll_no="T1", name="Test", email="t@t.com",
                   course="B.Tech CSE", year=1, marks=marks)


class TestGradeCalculation:
    def test_grade_a_plus(self):
        assert make_student(95).grade() == "A+"

    def test_grade_a(self):
        assert make_student(85).grade() == "A"

    def test_grade_b(self):
        assert make_student(75).grade() == "B"

    def test_grade_c(self):
        assert make_student(65).grade() == "C"

    def test_grade_d(self):
        assert make_student(55).grade() == "D"

    def test_grade_e(self):
        assert make_student(45).grade() == "E"

    def test_grade_f(self):
        assert make_student(20).grade() == "F"

    def test_boundary_90_is_a_plus(self):
        assert make_student(90).grade() == "A+"

    def test_boundary_40_is_e(self):
        assert make_student(40).grade() == "E"


class TestResult:
    def test_pass_at_40(self):
        assert make_student(40).result() == "PASS"

    def test_fail_below_40(self):
        assert make_student(39.9).result() == "FAIL"

    def test_pass_high_marks(self):
        assert make_student(100).result() == "PASS"
