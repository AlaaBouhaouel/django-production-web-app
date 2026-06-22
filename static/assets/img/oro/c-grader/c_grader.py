#!/usr/bin/env python3
"""
c_grader.py

Grades C submissions with:
- multiple functions
- weighted hidden tests
- optional clang-tidy / cppcheck checks
- compile/run sandboxing via timeout
- exact output comparison for scalar/string returns

Supported types:
int, long, long long, unsigned, unsigned long long,
float, double, char, bool, _Bool, char*, const char*

Spec JSON example:

{
  "timeout_sec": 1.0,
  "use_clang_tidy": false,
  "use_cppcheck": false,
  "functions": [
    {
      "name": "add",
      "return_type": "int",
      "arg_types": ["int", "int"],
      "tests": [
        {"args": [1, 2], "weight": 1},
        {"args": [0, 0], "weight": 1}
      ]
    }
  ]
}

Run:
  python3 c_grader.py student.c reference.c spec.json
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_TYPES = {
    "int",
    "long",
    "long long",
    "unsigned",
    "unsigned long long",
    "float",
    "double",
    "char",
    "bool",
    "_Bool",
    "char*",
    "const char*",
}


@dataclass
class FunctionSpec:
    name: str
    return_type: str
    arg_types: list[str]
    tests: list[dict[str, Any]]


def c_string_literal(s: str) -> str:
    return (
        '"'
        + s.replace("\\", "\\\\")
           .replace('"', '\\"')
           .replace("\n", "\\n")
           .replace("\r", "\\r")
           .replace("\t", "\\t")
        + '"'
    )


def c_char_literal(v: Any) -> str:
    if isinstance(v, int):
        ch = chr(v)
    elif isinstance(v, str) and len(v) == 1:
        ch = v
    else:
        raise ValueError(f"Invalid char literal: {v!r}")

    escapes = {
        "\\": r"\\",
        "'": r"\'",
        "\n": r"\n",
        "\r": r"\r",
        "\t": r"\t",
        "\0": r"\0",
    }
    return "'" + escapes.get(ch, ch) + "'"


def c_literal(value: Any, typ: str) -> str:
    if typ in {"int", "long", "long long", "unsigned", "unsigned long long"}:
        return str(int(value))
    if typ in {"float", "double"}:
        return format(float(value), ".17g")
    if typ in {"bool", "_Bool"}:
        return "1" if bool(value) else "0"
    if typ == "char":
        return c_char_literal(value)
    if typ in {"char*", "const char*"}:
        if value is None:
            return "NULL"
        return c_string_literal(str(value))
    raise ValueError(f"Unsupported type: {typ}")


def printf_fmt(typ: str) -> str:
    if typ == "int":
        return "%d"
    if typ == "long":
        return "%ld"
    if typ == "long long":
        return "%lld"
    if typ == "unsigned":
        return "%u"
    if typ == "unsigned long long":
        return "%llu"
    if typ in {"float", "double"}:
        return "%.17g"
    if typ in {"bool", "_Bool"}:
        return "%d"
    if typ == "char":
        return "%d"
    if typ in {"char*", "const char*"}:
        return "%s"
    raise ValueError(f"Unsupported return type: {typ}")


def check_types(name: str, ret_type: str, arg_types: list[str]) -> None:
    if ret_type not in SUPPORTED_TYPES:
        raise ValueError(f"{name}: unsupported return type {ret_type}")
    for t in arg_types:
        if t not in SUPPORTED_TYPES:
            raise ValueError(f"{name}: unsupported arg type {t}")


def build_harness(spec: FunctionSpec) -> str:
    check_types(spec.name, spec.return_type, spec.arg_types)

    params = [f"{t} a{i}" for i, t in enumerate(spec.arg_types)]
    call_args = ", ".join(f"a{i}" for i in range(len(spec.arg_types)))
    call_expr = f"{spec.name}({call_args})" if call_args else f"{spec.name}()"
    proto = f"extern {spec.return_type} {spec.name}({', '.join(params) if params else 'void'});"

    lines = [
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "#include <string.h>",
        "",
        proto,
        "",
        "int main(void) {",
    ]

    fmt = printf_fmt(spec.return_type)

    for idx, test in enumerate(spec.tests):
        args = test["args"]
        if len(args) != len(spec.arg_types):
            raise ValueError(
                f"{spec.name} test {idx}: expected {len(spec.arg_types)} args, got {len(args)}"
            )
        literals = [c_literal(v, t) for v, t in zip(args, spec.arg_types)]

        lines.append(f"    /* test {idx} */")
        if spec.return_type in {"char*", "const char*"}:
            lines.append(f"    {spec.return_type} __res = {spec.name}({', '.join(literals)});")
            lines.append('    printf("%s\\n", __res ? __res : "<NULL>");')
        elif spec.return_type in {"float", "double"}:
            lines.append(f"    double __res = (double)({spec.name}({', '.join(literals)}));")
            lines.append(f'    printf("{fmt}\\n", __res);')
        elif spec.return_type in {"bool", "_Bool", "char"}:
            lines.append(f"    int __res = (int)({spec.name}({', '.join(literals)}));")
            lines.append(f'    printf("{fmt}\\n", __res);')
        else:
            lines.append(f"    {spec.return_type} __res = {spec.name}({', '.join(literals)});")
            lines.append(f'    printf("{fmt}\\n", __res);')

    lines.extend(["    return 0;", "}", ""])
    return "\n".join(lines)


def run(cmd: list[str], timeout: float | None = None) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, e.stdout or "", e.stderr or "TIMEOUT"


def compile_program(source: Path, harness_code: str, out_path: Path) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as td:
        harness = Path(td) / "harness.c"
        harness.write_text(harness_code, encoding="utf-8")
        cmd = [
            "gcc",
            "-std=c11",
            "-O2",
            "-Wall",
            "-Wextra",
            str(source),
            str(harness),
            "-lm",
            "-o",
            str(out_path),
        ]
        rc, out, err = run(cmd, timeout=30)
        if rc != 0:
            msg = err.strip() or out.strip() or "compile failed"
            return False, msg
    return True, ""


def optional_static_analysis(source: Path, spec: dict[str, Any]) -> list[str]:
    messages: list[str] = []

    if spec.get("use_cppcheck", False) and shutil.which("cppcheck"):
        cmd = [
            "cppcheck",
            "--enable=warning,style,performance,portability",
            "--quiet",
            str(source),
        ]
        rc, out, err = run(cmd, timeout=60)
        if rc != 0 and (out.strip() or err.strip()):
            messages.append("[cppcheck]")
            if out.strip():
                messages.append(out.strip())
            if err.strip():
                messages.append(err.strip())

    if spec.get("use_clang_tidy", False) and shutil.which("clang-tidy"):
        # clang-tidy works best with compile_commands.json, but it can still provide signal
        cmd = [
            "clang-tidy",
            str(source),
            "--",
            "-std=c11",
        ]
        rc, out, err = run(cmd, timeout=60)
        if rc != 0 and (out.strip() or err.strip()):
            messages.append("[clang-tidy]")
            if out.strip():
                messages.append(out.strip())
            if err.strip():
                messages.append(err.strip())

    return messages


def normalize_output(text: str) -> list[str]:
    return text.splitlines()


def compare_line(expected: str, actual: str, typ: str) -> bool:
    if typ in {"float", "double"}:
        try:
            e = float(expected)
            a = float(actual)
            if math.isnan(e) and math.isnan(a):
                return True
            return math.isclose(e, a, rel_tol=1e-6, abs_tol=1e-6)
        except ValueError:
            return False
    return expected == actual


def grade(student_src: str, reference_src: str, spec_path: str) -> int:
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    timeout_sec = float(spec.get("timeout_sec", 1.0))

    functions = [
        FunctionSpec(
            name=f["name"],
            return_type=f["return_type"],
            arg_types=f.get("arg_types", []),
            tests=f.get("tests", []),
        )
        for f in spec["functions"]
    ]

    student_src = str(Path(student_src).resolve())
    reference_src = str(Path(reference_src).resolve())

    total_weight = 0.0
    earned = 0.0

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)

        if spec.get("use_cppcheck", False) or spec.get("use_clang_tidy", False):
            print("Static analysis:")
            for src in [Path(student_src), Path(reference_src)]:
                msgs = optional_static_analysis(src, spec)
                if msgs:
                    print(f"- {src.name}:")
                    for m in msgs:
                        print(m)
            print()

        for fn in functions:
            harness = build_harness(fn)
            student_exe = td_path / f"student_{fn.name}"
            reference_exe = td_path / f"reference_{fn.name}"

            ok, err = compile_program(Path(student_src), harness, student_exe)
            if not ok:
                print(f"[{fn.name}] student compile error:\n{err}\n")
                continue

            ok, err = compile_program(Path(reference_src), harness, reference_exe)
            if not ok:
                print(f"[{fn.name}] reference compile error:\n{err}\n")
                continue

            rc, ref_out, ref_err = run([str(reference_exe)], timeout=timeout_sec)
            if rc != 0:
                print(f"[{fn.name}] reference runtime error:\n{ref_err or ref_out}\n")
                continue

            rc, stu_out, stu_err = run([str(student_exe)], timeout=timeout_sec)
            if rc != 0:
                print(f"[{fn.name}] student runtime error:\n{stu_err or stu_out}\n")

            ref_lines = normalize_output(ref_out)
            stu_lines = normalize_output(stu_out)

            if len(ref_lines) != len(fn.tests) or len(stu_lines) != len(fn.tests):
                # Keep going; line-by-line scoring still applies to the minimum overlap.
                pass

            for i, test in enumerate(fn.tests):
                w = float(test.get("weight", 1.0))
                total_weight += w
                expected = ref_lines[i] if i < len(ref_lines) else "<MISSING>"
                actual = stu_lines[i] if i < len(stu_lines) else "<MISSING>"
                ok = compare_line(expected, actual, fn.return_type)

                if ok:
                    earned += w
                    print(f"[{fn.name}] test {i + 1}: PASS")
                else:
                    print(f"[{fn.name}] test {i + 1}: FAIL")
                    print(f"  expected: {expected}")
                    print(f"  actual:   {actual}")

            print()

    score = 100.0 * earned / total_weight if total_weight else 0.0
    print(f"Final score: {score:.2f}%")
    return 0


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python3 c_grader.py <student.c> <reference.c> <spec.json>", file=sys.stderr)
        return 2
    return grade(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    raise SystemExit(main())
