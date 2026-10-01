# Main API

This page summarizes the functions most likely to be used in experiments. It does not duplicate every internal helper.

All examples assume:

```python
from lot.parameters import set_parameters
set_parameters("para.json")
```

## `exe(program, start)`

Module: `lot.semantics`

Executes a Python LoT program from a specified starting point.

```python
from lot.syntax import MOVE_AND_PLAY, REPEAT
from lot.semantics import exe

P = [REPEAT(3, [MOVE_AND_PLAY(1)])]
exe(P, 0)
# ('123', 3)
```

Returns:

```text
(output_string, final_peval)
```


## `size(program)`

Module: `lot.program_ops`

Computes the size of a program using the currently loaded size functions.

```python
from lot.program_ops import size
size(P)
```

The exact formula is configuration-dependent; see `docs/CONFIGURATION.md`.

## `construct_dictionary(d, sequence, references={})`

Module: `lot.complexity`

Core dynamic-programming routine.

It fills a dictionary indexed by `(substring, start)` whose values are pairs

```text
(minimal_program, ending_point)
```

for minimal descriptions of the substring from that starting point.

Most users should call `complexity`, `min_progs`, or the batch functions rather than invoking this routine directly.

## `complexity(sequence)`

Module: `lot.complexity`

Computes the minimal program size over all possible starting points.

```python
from lot.complexity import complexity
complexity("01234")
# (4, 1) with the supplied para.json
```

Returns:

```text
(minimum_complexity, number_of_minimal_programs)
```

## `min_progs(sequence, start=-1, relative_to="")`

Module: `lot.complexity`

Prints the complexity and minimal programs for a sequence.

```python
from lot.complexity import min_progs
min_progs("010101010101")
```

If `start != -1`, the starting point is fixed. If `relative_to` is nonempty, its substrings of length greater than one are made available as `REFERENCE` candidates of weight `1`.

The number of fully displayed programs is bounded by `config.MAX_SHOWN`.

## `complexities_and_minprog(sequences_with_names)`

Module: `lot.complexity`

Computes complexity and minimal programs for a dictionary of named sequences.

```python
from lot.complexity import complexities_and_minprog

items = {
    "constant": "0000000",
    "alternating": "010101010101"
}

out = complexities_and_minprog(items)
```

For fixed `BASE`, the function incrementally reuses one dynamic-programming dictionary across the input sequences to avoid recomputing shared substrings.

Output shape:

```python
{
    "name": (
        "sequence",
        complexity_value,
        [minimal_program_1, minimal_program_2, ...]
    )
}
```

## `write_complexities_and_minprog_json(input_json_file, output_json_file)`

Module: `lot.complexity`

Reads named sequences from a JSON object:

```json
{
  "sequence A": "0000000",
  "sequence B": "010101010101"
}
```

and writes a JSON result containing:

- `interpretation`;
- `loaded_config`;
- `parameters`;
- `results`.

Each result records the original sequence, its complexity, and the minimal programs serialized with their normal Python string representation.

Example:

```python
from lot.complexity import write_complexities_and_minprog_json

write_complexities_and_minprog_json(
    "sequences.json",
    "complexities_output.json"
)
```

## `compute_strings_with_initial_repetition_table(k_min, k_max, length_min, length_max)`

Module: `lot.search`

Searches a rectangle of complexity and length values and returns

```text
results[k][l] = list of strings
```

such that:

1. the string has length `l`;
2. its complexity is exactly `k`;
3. at least one minimal program begins with `REPEAT`, `REPEAT_APPLY_NOTES`, or `REPEAT_APPLY_PEVAL`, subject to the active configuration;
4. strings equivalent by a global cyclic shift are represented by the normalized version beginning with `0`.

The search works by enumerating semantic program classes up to `k_max` and `length_max`, rather than by naively enumerating all strings.

## `write_strings_with_initial_repetition_json(file_path, k_min, k_max, length_min, length_max)`

Module: `lot.search`

JSON-writing wrapper around the previous search.

```python
from lot.search import write_strings_with_initial_repetition_json

write_strings_with_initial_repetition_json(
    "results.json",
    3, 8,
    8, 10
)
```

The JSON output contains:

- an explanation of the table;
- the loaded configuration;
- the search parameters;
- `results[k][l]`;
- `counts[k][l]`.

## `normalize_string_starting_at_zero(s)`

Module: `lot.search`

Chooses a representative modulo global cyclic translation by subtracting the first symbol from every symbol modulo `BASE`.

For `BASE = 8`:

```text
123456701 -> 012345670
111111111 -> 000000000
```

## Printing and visualization

`lot.printing.show(program, ...)` prints programs in the human-readable LoT notation used by `min_progs`.

`lot.visualization.program_to_tree(P)` creates a Graphviz representation of the syntactic program tree.
