# Advent of Code 2025

Solutions for [Advent of Code 2025](https://adventofcode.com/2025)

## Structure

Each day has its own directory (`day01` through `day12`) containing:
- `solution.py` - Python solution for both parts
- `input.txt` - Your puzzle input
- `example.txt` - Example input from problem description (optional)

## Usage

### Setup a New Day

```bash
# Copy template to a specific day
cp template.py day01/solution.py
```

### Run a Solution

```bash
cd dayXX
python solution.py
```

### Run Every Day & Measure Timings

```bash
python run_all.py
```

Options:
- `--input example.txt` – use a different input file name for every day.
- `--days 1 5 12` – limit execution to specific days (any mix of numbers or `dayXX`).
- `--fail-fast` – stop immediately on the first failure.

### Test with Example Input

```bash
cd dayXX
python solution.py example.txt
```

## Progress

| Day | Part 1 | Part 2 |
|-----|--------|--------|
| 01  | ⭐     | ⭐     |
| 02  | ⭐     | ⭐     |
| 03  | ⭐     | ⭐     |
| 04  | ⭐     | ⭐     |
| 05  | ⭐     | ⭐     |
| 06  | ⭐     | ⭐     |
| 07  | ⭐     | ⭐     |
| 08  | ⭐     | ⭐     |
| 09  | ⭐     | ⭐     |
| 10  | ⭐     | ⭐     |
| 11  |        |        |
| 12  |        |        |

## Speed Optimization

DAY01
  Part 1: 1.14ms > 1.18ms
  Part 2: 1.16ms > 1.19ms

DAY02
  Part 1: 395.44ms > 0.10ms
  Part 2: 1.079s > 0.12ms

DAY03
  Part 1: 95.62ms > 2.95ms
  Part 2: 6.51ms > 2.96ms

DAY04
  Part 1: 14.44ms > 13.94ms
  Part 2: 358.66ms > 25.81ms

DAY05
  Part 1: 4.67ms > 0.43ms
  Part 2: 0.25ms > 0.24ms

DAY06
  Part 1: 4.61ms > 4.03ms
  Part 2: 3.21ms > 2.77ms

DAY07
  Part 1: 3.46ms > 3.30ms
  Part 2: 1.91ms > 2.96ms

DAY08
  Part 1: 445.41ms > 161.11ms
  Part 2: 471.35ms > 533.95ms

DAY09
  Part 1: None (0.00ms)
  Part 2: None (0.00ms)

DAY10
  Part 1: None (0.00ms)
  Part 2: None (0.00ms)

DAY11
  Part 1: None (0.00ms)
  Part 2: None (0.00ms)

DAY12
  Part 1: None (0.00ms)
  Part 2: None (0.00ms)



Total runtime (parts only): 2.887s > 757.05ms