# LoT Sequence Complexity

Research software for describing finite symbolic sequences with a small **Language of Thought (LoT)** programming language and assigning them a language-relative description complexity.

The complexity of a sequence is the minimum size of a program in the configured LoT that generates that sequence. The available instructions and their sizes are specified in `para.json`.

This is a computable, language-dependent description measure inspired by Kolmogorov complexity; it is not unrestricted Kolmogorov complexity.

## Requirements

Python 3.10 or later.

The Python package `graphviz` is installed automatically because the project includes program-tree visualization. Rendering those trees also requires the Graphviz system program.

## Installation

```bash
git clone https://github.com/sfigueir/lot-sequence-complexity.git
cd lot-sequence-complexity
python3 -m pip install -e .
```

On Windows, use `python` instead of `python3` if necessary.

## Running the example

From the repository root:

```bash
python3 example.py
```

On Windows:

```bash
python example.py
```

`example.py` demonstrates the main functionality: program execution, sequence complexity, batch complexity computation, search by complexity, and JSON output.

## Quick start

```python
from lot.parameters import set_parameters
from lot.syntax import MOVE_AND_PLAY, REPEAT
from lot.semantics import exe
from lot.complexity import complexity, min_progs

set_parameters("para.json")

program = [REPEAT(3, [MOVE_AND_PLAY(1)])]

print(exe(program, 0))
print(complexity("01234"))
min_progs("010101010101")
```

## Main functions

### Load the language configuration

```python
set_parameters("para.json")
```

Loads `BASE`, the enabled instruction families, and the instruction-size functions.

### Execute a program

```python
exe(program, start)
```

Returns:

```text
(output_string, final_peval)
```

### Complexity of one sequence

```python
complexity(sequence)
```

Returns:

```text
(minimum_complexity, number_of_minimal_programs)
```

### Minimal programs

```python
min_progs(sequence)
```

Displays the minimal programs generating a sequence.

### Several named sequences

```python
from lot.complexity import complexities_and_minprog

sequences = {
    "constant": "0000000",
    "alternating": "010101010101"
}

results = complexities_and_minprog(sequences)
```

Each entry contains the sequence, its complexity, and its list of minimal programs.

### Read sequences from JSON

An input file can have the form:

```json
{
  "constant": "0000000",
  "alternating": "010101010101"
}
```

Then:

```python
from lot.complexity import write_complexities_and_minprog_json

write_complexities_and_minprog_json(
    "sequences.json",
    "complexities_output.json"
)
```

writes the complexity and minimal programs of each sequence to JSON, together with the configuration used in the computation.

### Search for sequences of prescribed complexity

```python
from lot.search import write_strings_with_initial_repetition_json

write_strings_with_initial_repetition_json(
    "results.json",
    3,   # k_min
    8,   # k_max
    8,   # length_min
    10   # length_max
)
```

This searches for sequences whose complexity and length lie in the requested ranges and for which at least one minimal program has `REPEAT`, `REPEAT_APPLY_NOTES`, or `REPEAT_APPLY_PEVAL` as its outermost instruction, subject to the current configuration.

Sequences that differ only by a global cyclic shift are represented by the normalized version beginning with `0`.

## Language

Execution takes place over the cyclic alphabet

```text
{0, 1, ..., BASE-1}
```

with a current **point of evaluation** (`peval`). The principal instructions are:

- `MOVE_AND_PLAY(n)`: move by `n` modulo `BASE` and output the new point.
- `PLAY(n)`: output `n` without changing `peval`.
- `MOVE(n)`: move by `n` without output.
- `REPEAT(n, P)`: execute `P` `n` times, threading the final `peval` between repetitions.
- `REPEAT_APPLY_NOTES(n, P, appl)`: execute `P` once and obtain subsequent blocks by applying `appl` to each symbol of the preceding block.
- `REPEAT_APPLY_PEVAL(n, P, jump)`: execute repeated copies of `P`, transforming the starting `peval` between copies using `jump`.

The complete operational semantics of all implemented instructions are in [`docs/LANGUAGE_SEMANTICS.md`](docs/LANGUAGE_SEMANTICS.md).

## Program size and configuration

Program size is computed recursively using the rules loaded from `para.json`. Therefore, sequence complexity is always relative to the selected grammar and size model.

See [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) for the configuration format and size rules.

## API

A compact description of the main public functions is available in [`docs/API.md`](docs/API.md).

## Project structure

```text
lot-sequence-complexity/
├── lot/                     # implementation
├── docs/
│   ├── API.md
│   ├── CONFIGURATION.md
│   └── LANGUAGE_SEMANTICS.md
├── example.py               # main usage example
├── para.json                # language configuration
├── sequences.json           # example input sequences
├── pyproject.toml
├── CITATION.cff
└── LICENSE
```

## Citation

Citation metadata are provided in `CITATION.cff`.

## License

MIT License. See `LICENSE`.
