"""
demo.py — Demonstrates the University Advising Ontology KBS.

Run:
    python demo.py
"""

from kbs import UniversityOntologyKBS


def build_kbs() -> UniversityOntologyKBS:
    kbs = UniversityOntologyKBS()

    # Courses (at least 6) 
    courses = [
        "Intro to Programming",   # level 0 – no prerequisites
        "Discrete Mathematics",   # level 0
        "Data Structures",        # requires Intro to Programming
        "Algorithms",             # requires Data Structures + Discrete Mathematics
        "Database Systems",       # requires Data Structures
        "Operating Systems",      # requires Algorithms
        "Software Engineering",   # requires Algorithms + Database Systems
        "Computer Networks",      # requires Operating Systems
    ]
    for c in courses:
        kbs.add_course(c)

    #  Prerequisites (at least 7 links, at least 2 depth levels) 
    #   Depth 1: Intro to Programming -> Data Structures
    #   Depth 2: Data Structures      -> Algorithms -> Operating Systems -> Computer Networks
    kbs.add_prerequisite("Data Structures",      "Intro to Programming")
    kbs.add_prerequisite("Algorithms",           "Data Structures")
    kbs.add_prerequisite("Algorithms",           "Discrete Mathematics")
    kbs.add_prerequisite("Database Systems",     "Data Structures")
    kbs.add_prerequisite("Operating Systems",    "Algorithms")
    kbs.add_prerequisite("Software Engineering", "Algorithms")
    kbs.add_prerequisite("Software Engineering", "Database Systems")
    kbs.add_prerequisite("Computer Networks",    "Operating Systems")

    # Students (at least 3) 
    kbs.add_student("Alice")
    kbs.add_student("Bob")
    kbs.add_student("Carol")

    # Alice — completed foundational courses (partially eligible for mid-level)
    kbs.complete_course("Alice", "Intro to Programming")
    kbs.complete_course("Alice", "Discrete Mathematics")

    # Bob — strong background (eligible for advanced courses)
    kbs.complete_course("Bob", "Intro to Programming")
    kbs.complete_course("Bob", "Discrete Mathematics")
    kbs.complete_course("Bob", "Data Structures")
    kbs.complete_course("Bob", "Algorithms")
    kbs.complete_course("Bob", "Database Systems")

    # Carol — brand-new student (no courses completed)

    return kbs


def print_separator(title: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def demo_eligibility(kbs: UniversityOntologyKBS) -> None:
    print_separator("ELIGIBILITY CHECKS")

    checks = [
        # (student, course, expected label)
        ("Bob",   "Operating Systems",    "ELIGIBLE (all prerequisites met)"),
        ("Alice", "Algorithms",           "PARTIALLY ELIGIBLE (some prerequisites missing)"),
        ("Carol", "Data Structures",      "NOT ELIGIBLE (no prerequisites completed)"),
    ]

    for student, course, label in checks:
        eligible, missing = kbs.can_take(student, course)
        status = " ELIGIBLE" if eligible else " NOT ELIGIBLE"
        print(f"\n  {student} → {course}")
        print(f"  Status  : {status}")
        if missing:
            print(f"  Missing : {', '.join(sorted(missing))}")
        print(f"  Scenario: {label}")


def demo_recommendations(kbs: UniversityOntologyKBS) -> None:
    print_separator("COURSE RECOMMENDATIONS")

    for student in ["Alice", "Bob", "Carol"]:
        recs = kbs.recommend_courses(student)
        completed = sorted(kbs.completed_courses(student))
        print(f"\n  Student   : {student}")
        print(f"  Completed : {completed if completed else '(none)'}")
        print(f"  Recommended: {recs if recs else '(none — complete more prerequisites)'}")


if __name__ == "__main__":
    
    print("[     University Advising Ontology KBS — Demo              ]")
    kbs = build_kbs()
    demo_eligibility(kbs)
    demo_recommendations(kbs)

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60 + "\n")