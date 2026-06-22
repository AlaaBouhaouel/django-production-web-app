# C Grader Setup

This folder contains:
- `c_grader.py`: hidden-test grader for multiple C functions
- `spec.json`: example test specification
- `student.c`: sample submission
- `reference.c`: sample reference solution

Run:
```bash
python3 c_grader.py student.c reference.c spec.json
```

Optional static analysis:
- set `"use_cppcheck": true`
- set `"use_clang_tidy": true`

Those tools are used as extra signals; the score still comes from hidden tests.
