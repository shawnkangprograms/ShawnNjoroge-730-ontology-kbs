# University Advising Ontology KBS

A small Knowledge-Based System that helps students figure out which courses they can take and what to study next, based on their completed courses and prerequisite rules.

---

## Ontology

**Concepts:** `Student`, `Course`

**Relationships:**
- `requires(Course → Course)` — a course depends on another course
- `completed(Student → Course)` — a student has finished a course
- `eligibleFor(Student → Course)` — **inferred** automatically (never entered manually)

---

## Inference Logic

- **Can a student take a course?** The system finds all prerequisites (including transitive ones) and checks if the student has completed them all. If not, it returns what's missing.
- **What should a student take next?** The system checks every course, filters out completed ones, and returns eligible courses sorted alphabetically.

---

## Repo Structure

```
.
├── README.md
├── kbs.py          # Core KBS class and inference engine
├── demo.py         # Demo script
└── tests/
    └── test_kbs.py # Unit tests
```

---

## How to Run

```bash
python demo.py
python -m unittest
```

---

## Example Output

```
  Bob -> Operating Systems
  Status  : ELIGIBLE

  Alice -> Algorithms
  Status  : NOT ELIGIBLE
  Missing : Data Structures

  Carol -> Data Structures
  Status  : NOT ELIGIBLE
  Missing : Intro to Programming

  Student   : Bob
  Recommended: ['Operating Systems', 'Software Engineering']
```
