"""
University Advising Ontology KBS
=================================
Ontology concepts:
  - Student: a person enrolled in the university
  - Course:  an academic unit that may require prerequisites

Ontology relationships (properties):
  - requires(Course → Course):        a course depends on another course
  - completed(Student → Course):      a student has finished a course
  - eligibleFor(Student → Course):    inferred — student has completed ALL prerequisites
"""


class UniversityOntologyKBS:
    """Knowledge-Base System built on a small university-advising ontology."""

    def __init__(self):
        self._students: set[str] = set()
        self._courses: set[str] = set()
        # requires: course → set of direct prerequisites
        self._prerequisites: dict[str, set[str]] = {}
        # completed: student → set of completed courses
        self._completed: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Ontology population
    # ------------------------------------------------------------------

    def add_student(self, student: str) -> None:
        """Register a new student concept."""
        student = student.strip()
        if not student:
            raise ValueError("Student name must not be empty.")
        self._students.add(student)
        self._completed.setdefault(student, set())

    def add_course(self, course: str) -> None:
        """Register a new course concept."""
        course = course.strip()
        if not course:
            raise ValueError("Course name must not be empty.")
        self._courses.add(course)
        self._prerequisites.setdefault(course, set())

    def add_prerequisite(self, course: str, prereq: str) -> None:
        """Assert the *requires* relationship: course → prereq."""
        self._validate_course(course)
        self._validate_course(prereq)
        if course == prereq:
            raise ValueError(f"A course cannot be its own prerequisite: '{course}'.")
        self._prerequisites[course].add(prereq)

    def complete_course(self, student: str, course: str) -> None:
        """Assert the *completed* relationship: student → course."""
        self._validate_student(student)
        self._validate_course(course)
        self._completed[student].add(course)

    # ------------------------------------------------------------------
    # Inference / reasoning
    # ------------------------------------------------------------------

    def _all_prerequisites(self, course: str) -> set[str]:
        """Return the transitive closure of prerequisites for *course*."""
        self._validate_course(course)
        visited: set[str] = set()
        stack = list(self._prerequisites.get(course, set()))
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                stack.extend(self._prerequisites.get(current, set()) - visited)
        return visited

    def can_take(self, student: str, course: str) -> tuple[bool, set[str]]:
        """
        Infer the *eligibleFor* relationship.

        Returns (True, set()) if the student has completed all transitive
        prerequisites, otherwise (False, <set of missing prerequisites>).
        """
        self._validate_student(student)
        self._validate_course(course)
        all_prereqs = self._all_prerequisites(course)
        completed = self._completed[student]
        missing = all_prereqs - completed
        return (len(missing) == 0, missing)

    def recommend_courses(self, student: str) -> list[str]:
        """
        Return courses the student is eligible for but has not yet completed,
        sorted alphabetically.
        """
        self._validate_student(student)
        completed = self._completed[student]
        recommendations = []
        for course in self._courses:
            if course in completed:
                continue
            eligible, _ = self.can_take(student, course)
            if eligible:
                recommendations.append(course)
        return sorted(recommendations)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _validate_student(self, student: str) -> None:
        if student not in self._students:
            raise ValueError(f"Unknown student: '{student}'. Add them with add_student() first.")

    def _validate_course(self, course: str) -> None:
        if course not in self._courses:
            raise ValueError(f"Unknown course: '{course}'. Add it with add_course() first.")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def students(self) -> set[str]:
        return set(self._students)

    def courses(self) -> set[str]:
        return set(self._courses)

    def completed_courses(self, student: str) -> set[str]:
        self._validate_student(student)
        return set(self._completed[student])