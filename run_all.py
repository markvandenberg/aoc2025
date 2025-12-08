#!/usr/bin/env python3
"""Run every AoC day and time each part."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Dict, Iterable, List, Optional

BASE_DIR = Path(__file__).parent.resolve()
DAY_PREFIX = "day"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run every available day and measure execution time for each part.",
    )
    parser.add_argument(
        "--days",
        nargs="+",
        metavar="DAY",
        help="Optional list of days to run (e.g. 1 2 day03). Defaults to all days.",
    )
    parser.add_argument(
        "--input",
        default="input.txt",
        help="Input filename to use inside each day folder (default: input.txt).",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop immediately when a day or part raises an exception.",
    )
    return parser.parse_args()


def normalize_day_name(label: str) -> Optional[str]:
    label = label.strip().lower()
    if not label:
        return None
    if label.startswith(DAY_PREFIX):
        label = label[len(DAY_PREFIX) :]
    try:
        number = int(label)
    except ValueError:
        return None
    return f"{DAY_PREFIX}{number:02d}"


def discover_day_dirs(selected: Optional[Iterable[str]]) -> List[Path]:
    if selected:
        day_names: List[str] = []
        for raw in selected:
            name = normalize_day_name(raw)
            if not name:
                print(f"Ignoring invalid day specifier: {raw}", file=sys.stderr)
                continue
            day_names.append(name)
        seen = {name: None for name in day_names}  # dedupe but keep order
        day_names = list(seen.keys())
        return [BASE_DIR / name for name in day_names]

    return sorted(
        path
        for path in BASE_DIR.iterdir()
        if path.is_dir() and path.name.startswith(DAY_PREFIX) and path.name[len(DAY_PREFIX) :].isdigit()
    )


def load_solution_module(day_dir: Path) -> ModuleType:
    solution_file = day_dir / "solution.py"
    if not solution_file.exists():
        raise FileNotFoundError(f"Missing {solution_file}")

    spec = importlib.util.spec_from_file_location(day_dir.name, solution_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {solution_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def read_day_input(module: ModuleType, input_path: Path) -> str:
    reader = getattr(module, "read_input", None)
    if callable(reader):
        return reader(str(input_path))  # type: ignore[no-any-return]
    return input_path.read_text().strip()


def run_part(module: ModuleType, func_name: str, data: str) -> Dict[str, object]:
    func = getattr(module, func_name, None)
    part_label = func_name.capitalize()
    if not callable(func):
        return {
            "label": part_label,
            "result": None,
            "duration": None,
            "error": f"Missing {func_name}()",
        }

    start = time.perf_counter()
    try:
        result = func(data)
    except Exception as exc:  # pragma: no cover - best-effort reporting
        return {
            "label": part_label,
            "result": None,
            "duration": None,
            "error": f"{exc.__class__.__name__}: {exc}",
        }
    duration = time.perf_counter() - start
    return {
        "label": part_label,
        "result": result,
        "duration": duration,
        "error": None,
    }


def format_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return "-"
    if seconds >= 1:
        return f"{seconds:.3f}s"
    return f"{seconds * 1_000:.2f}ms"


def main() -> int:
    args = parse_args()
    day_dirs = discover_day_dirs(args.days)

    if not day_dirs:
        print("No day directories found.", file=sys.stderr)
        return 1

    overall_total = 0.0
    had_error = False

    for day_dir in day_dirs:
        if not day_dir.exists():
            print(f"{day_dir.name}: directory does not exist, skipping.", file=sys.stderr)
            continue

        print(f"\n{day_dir.name.upper()}")
        try:
            module = load_solution_module(day_dir)
        except Exception as exc:
            had_error = True
            print(f"  Failed to load solution: {exc}")
            if args.fail_fast:
                return 1
            continue

        input_path = day_dir / args.input
        if not input_path.exists():
            had_error = True
            print(f"  Input file not found: {input_path}")
            if args.fail_fast:
                return 1
            continue

        try:
            data = read_day_input(module, input_path)
        except Exception as exc:
            had_error = True
            print(f"  Failed to read input: {exc}")
            if args.fail_fast:
                return 1
            continue

        for idx, func_name in enumerate(("part1", "part2"), start=1):
            part_result = run_part(module, func_name, data)
            label = f"Part {idx}"
            if part_result["error"]:
                had_error = True
                print(f"  {label}: ERROR - {part_result['error']}")
                if args.fail_fast:
                    return 1
                continue

            duration = part_result["duration"] or 0.0
            overall_total += duration
            print(
                f"  {label}: {part_result['result']} ({format_duration(part_result['duration'])})"
            )

    print(f"\nTotal runtime (parts only): {format_duration(overall_total)}")
    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
