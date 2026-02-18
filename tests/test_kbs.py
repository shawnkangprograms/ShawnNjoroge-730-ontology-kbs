"""
tests/test_kbs.py — Unit tests for UniversityOntologyKBS

Run from the project root (recommended):
    python -m unittest

Or run this file directly:
    python tests/test_kbs.py
"""

import sys
import os
import unittest

# Allow running this file directly (adds project root to path)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from kbs import UniversityOntologyKBS


def _build_standard_kbs() -> UniversityOntologyKBS:
    """Return a populated KBS used across multiple tests."""
    kbs = UniversityOntologyKBS()
    for course in [
        "Intro to Programming",
        "Discrete Mathematics",
        "Data Structures",
        "Algorithms",
        "Database Systems",
        "Operating Systems",
        "Software Engineering",
        "Computer Networks",
    ]:
        kbs.add_course(course)

    kbs.add_prerequisite("Data Structures",      "Intro to Programming")
    kbs.add_prerequisite("Algorithms",           "Data Structures")
    kbs.add_prerequisite("Algorithms",           "Discrete Mathematics")
    kbs.add_prerequisite("Database Systems",     "Data Structures")
    kbs.add_prerequisite("Operating Systems",    "Algorithms")
    kbs.add_prerequisite("Software Engineering", "Algorithms")
    kbs.add_prerequisite("Software Engineering", "Database Systems")
    kbs.add_prerequisite("Computer Networks",    "Operating Systems")

    kbs.add_student("Alice")
    kbs.add_student("Bob")
    kbs.add_student("Carol")
    return kbs


class TestOntologyPopulation(unittest.TestCase):
    """Test 1 — add_student / add_course validation."""

    def test_add_unknown_student_raises(self):
        kbs = UniversityOntologyKBS()
        kbs.add_course("Math")
        with self.assertRaises(ValueError):
            kbs.complete_course("Ghost", "Math")

    def test_add_unknown_course_raises(self):
        kbs = UniversityOntologyKBS()
        kbs.add_student("Alice")
        with self.assertRaises(ValueError):
            kbs.complete_course("Alice", "Ghost Course")

    def test_self_prerequisite_raises(self):
        kbs = UniversityOntologyKBS()
        kbs.add_course("Math")
        with self.assertRaises(ValueError):
            kbs.add_prerequisite("Math", "Math")


class TestCanTake(unittest.TestCase):
    """Tests 2–4 — can_take inference."""

    def setUp(self):
        self.kbs = _build_standard_kbs()

    def test_eligible_no_prerequisites(self):
        """Test 2: A course with no prerequisites is always available."""
        eligible, missing = self.kbs.can_take("Carol", "Intro to Programming")
        self.assertTrue(eligible)
        self.assertEqual(missing, set())

    def test_not_eligible_missing_direct_prereq(self):
        """Test 3: Student missing a direct prerequisite."""
        eligible, missing = self.kbs.can_take("Carol", "Data Structures")
        self.assertFalse(eligible)
        self.assertIn("Intro to Programming", missing)

    def test_not_eligible_missing_transitive_prereq(self):
        """Test 4: Student missing transitive prerequisites."""
        # Alice has only Intro to Programming; Algorithms needs Data Structures too
        self.kbs.complete_course("Alice", "Intro to Programming")
        eligible, missing = self.kbs.can_take("Alice", "Algorithms")
        self.assertFalse(eligible)
        # Data Structures is missing (and it transitively needs Intro to Prog — but Alice has that)
        self.assertIn("Data Structures", missing)

    def test_eligible_after_completing_all_prereqs(self):
        """Test 5: Student becomes eligible once all prerequisites are done."""
        self.kbs.complete_course("Bob", "Intro to Programming")
        self.kbs.complete_course("Bob", "Discrete Mathematics")
        self.kbs.complete_course("Bob", "Data Structures")
        self.kbs.complete_course("Bob", "Algorithms")
        eligible, missing = self.kbs.can_take("Bob", "Operating Systems")
        self.assertTrue(eligible)
        self.assertEqual(missing, set())


class TestRecommendCourses(unittest.TestCase):
    """Tests 5–6 — recommend_courses inference."""

    def setUp(self):
        self.kbs = _build_standard_kbs()

    def test_no_completed_courses_recommends_entry_level(self):
        """Test 6: A new student only gets courses with no prerequisites."""
        recs = self.kbs.recommend_courses("Carol")
        # Only entry-level courses (no prereqs) should appear
        self.assertIn("Intro to Programming", recs)
        self.assertIn("Discrete Mathematics", recs)
        self.assertNotIn("Algorithms", recs)

    def test_recommendations_exclude_completed_courses(self):
        """Test 7: Completed courses are never recommended."""
        self.kbs.complete_course("Bob", "Intro to Programming")
        self.kbs.complete_course("Bob", "Discrete Mathematics")
        self.kbs.complete_course("Bob", "Data Structures")
        self.kbs.complete_course("Bob", "Algorithms")
        recs = self.kbs.recommend_courses("Bob")
        self.assertNotIn("Intro to Programming", recs)
        self.assertNotIn("Algorithms", recs)
        # Should now recommend courses that need Algorithms
        self.assertIn("Operating Systems", recs)

    def test_recommendations_are_sorted(self):
        """Test 8: Returned list must be sorted alphabetically."""
        recs = self.kbs.recommend_courses("Carol")
        self.assertEqual(recs, sorted(recs))

    def test_unknown_student_raises_in_recommend(self):
        """Test 9: Recommending for an unknown student raises ValueError."""
        with self.assertRaises(ValueError):
            self.kbs.recommend_courses("Nobody")

    def test_can_take_unknown_course_raises(self):
        """Test 10: can_take with an unknown course raises ValueError."""
        with self.assertRaises(ValueError):
            self.kbs.can_take("Alice", "Quantum Cooking")


if __name__ == "__main__":
    unittest.main()