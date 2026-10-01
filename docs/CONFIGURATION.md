# Configuration and program size

The LoT is configured at runtime by

```python
from lot.parameters import set_parameters
set_parameters("para.json")
```

`set_parameters` loads the JSON file into the shared runtime configuration in `lot/config.py`.

## Configuration file

The supplied `para.json` is:

```json
{
  "BASE": "8",
  "MOVE_AND_PLAY": ["True", "lambda n: 2"],
  "PLAY": ["False", "lambda n: 2"],
  "MOVE": ["True", "lambda n: 2"],
  "REPEAT": ["True", "lambda n: (int(math.log2(n)),1)"],
  "REPEAT_JUMP": ["False", "None"],
  "REPEAT_APPLY_NOTES": ["True", "lambda n: (int(math.log2(n)),1,1)"],
  "REPEAT_APPLY_PEVAL": ["True", "lambda n: (int(math.log2(n)),1,1)"],
  "REFLECT": ["False", "None"],
  "MIRROR": ["False", "None"],
  "MIRROR_BOUNCE": ["False", "None"],
  "SUB": ["False", "None"],
  "REPEAT_CHUNKS": ["False", "None"],
  "POINTERS": ["False", "None"]
}
```

For most instruction families, the first entry enables/disables that family and the second entry specifies its size rule.

The current loader evaluates these strings as Python expressions. Parameter files must therefore be treated as trusted code/configuration, not as untrusted external input.

## Base

`BASE = B` defines the cyclic alphabet

```text
0, 1, ..., B-1.
```

Movement is always computed modulo `B`.

The current string representation assumes single-character symbols. The supplied experiments use `BASE = 8`.

## Atomic instruction sizes

For atomic instructions, the corresponding function is called on the instruction parameter.

For example, with

```json
"MOVE_AND_PLAY": ["True", "lambda n: 2"]
```

every `MOVE_AND_PLAY(n)` has size `2`.

Similarly:

```text
size([PLAY(n)])          = size_PLAY(n)
size([MOVE(n)])          = size_MOVE(n)
size([REFLECT(n)])       = size_REFLECT(n)
```

when the corresponding size function is configured.

## `REPEAT`

If

```python
config.size_REPEAT(n) == (a, b)
```

then

```text
size(REPEAT(n, P)) = a + b * size(P).
```

With the supplied configuration,

```text
a = floor(log2(n))
b = 1,
```

so

```text
size(REPEAT(n, P)) = floor(log2(n)) + size(P).
```

## `REPEAT_APPLY_NOTES`

If

```python
config.size_REPEAT_APPLY_NOTES(n) == (a, b, c)
```

then

```text
size(REPEAT_APPLY_NOTES(n, P, appl))
    = a + b * size([appl]) + c * size(P).
```

The supplied configuration uses

```text
(a, b, c) = (floor(log2(n)), 1, 1).
```

## `REPEAT_APPLY_PEVAL`

Analogously, if

```python
config.size_REPEAT_APPLY_PEVAL(n) == (a, b, c),
```

then

```text
size(REPEAT_APPLY_PEVAL(n, P, jump))
    = a + b * size([jump]) + c * size(P).
```

The supplied configuration again uses logarithmic repetition overhead and unit weights for the jump and subprogram.

## Other optional constructors

The implementation also contains configurable size rules for `MIRROR`, `MIRROR_BOUNCE`, `SUB`, `REPEAT_CHUNK`, pointers, and references. These mechanisms are disabled in the supplied `para.json` except where noted in the source.

`REFERENCE(s, weight)` contributes the explicitly stored `weight`.
