# Language semantics

This document describes the operational semantics implemented by `lot/semantics.py` and the instruction classes defined in `lot/syntax.py`.

The definitions below describe the **current code**, rather than an idealized or redesigned language.

## Execution model

Let

```text
A = {0, 1, ..., BASE-1}
```

be a cyclic alphabet. Execution has a current **point of evaluation** (`peval`) `p ∈ A`.

For a program `P`,

```python
exe(P, p)
```

returns

```text
(output, final_peval).
```

A program is a Python list of instructions. Instructions in a list are executed from left to right. Unless an instruction explicitly overrides this behavior, the final point of one instruction becomes the starting point of the next.

All movement is modulo `BASE`.

---

## `MOVE_AND_PLAY(n)`

**Python form**

```python
MOVE_AND_PLAY(n)
```

**Semantics**

From point `p`, move by `n` positions cyclically and emit the new point:

```text
q = (p + n) mod BASE
output = q
final peval = q
```

**Example (`BASE = 8`)**

```python
exe([MOVE_AND_PLAY(2)], 7)
# ('1', 1)
```

---

## `PLAY(n)`

**Python form**

```python
PLAY(n)
```

**Semantics**

Emit the constant symbol `n` without changing the point of evaluation:

```text
output = n
final peval = p
```

**Example**

```python
exe([PLAY(3)], 6)
# ('3', 6)
```

Whether `PLAY` participates in minimal-program search is controlled by `para.json`.

---

## `MOVE(n)`

**Python form**

```python
MOVE(n)
```

**Semantics**

Move the point of evaluation without emitting a symbol:

```text
q = (p + n) mod BASE
output = empty string
final peval = q
```

`MOVE` is particularly important as the transformation used by `REPEAT_APPLY_PEVAL`.

---

## `REPEAT(n, P)`

**Python form**

```python
REPEAT(n, P)
```

**Semantics**

Execute `P` exactly `n` times, threading the point of evaluation between copies.

If

```text
exe(P, p_i) = (w_i, p_{i+1}),
```

then

```text
output = w_1 w_2 ... w_n
final peval = p_{n+1}.
```

**Example**

```python
P = [REPEAT(3, [MOVE_AND_PLAY(1)])]
exe(P, 0)
# ('123', 3)
```

---

## `REPEAT_JUMP(n, P, jump)`

This constructor is present for legacy purposes and is forcibly disabled by `set_parameters` in the current configuration loader.

**Implemented semantics**

For each repetition:

1. execute `P` from the current point;
2. append its output;
3. apply `jump` to the ending point of `P`;
4. use the resulting point for the next repetition.

Thus, if execution of `P` ends at `e_i`, the next starting point is the endpoint of

```python
exe([jump], e_i)
```

The jump is also applied after the last copy, so the returned final point is the point after that final jump.

---

## `REPEAT_APPLY_NOTES(n, P, appl)`

The dataclass field containing the subprogram is named lowercase `p` in `syntax.py`; positional pattern matching makes it appear as `P` in the semantic description below.

**Python form**

```python
REPEAT_APPLY_NOTES(n, P, appl)
```

or, with keyword arguments matching the dataclass,

```python
REPEAT_APPLY_NOTES(n=n, p=P, appl=appl)
```

**Semantics**

1. Execute `P` once from the initial point and obtain an output block `w_1`.
2. To obtain `w_2`, execute `appl` independently from each symbol of `w_1` and concatenate the emitted symbols.
3. Apply the same transformation symbol-by-symbol to `w_2` to obtain `w_3`, and so on.
4. Emit

```text
w_1 w_2 ... w_n.
```

The final point of evaluation is explicitly reset to the **last emitted symbol**.

For the intended current use, `appl` is typically a `MOVE_AND_PLAY` instruction.

**Example**

```python
P = [
    REPEAT_APPLY_NOTES(
        3,
        [REPEAT(3, [MOVE_AND_PLAY(1)])],
        MOVE_AND_PLAY(1)
    )
]

exe(P, 0)
# ('123234345', 5)
```

---

## `REPEAT_APPLY_PEVAL(n, P, jump)`

**Python form**

```python
REPEAT_APPLY_PEVAL(n, P, jump)
```

**Semantics implemented in the current code**

Let `p_i` be the starting point of the `i`-th copy of `P`.

For every iteration:

1. execute `P` from `p_i` and append its output;
2. obtain the next starting point by applying `jump` to **`p_i` itself**, not to the ending point returned by `P`.

That is,

```text
p_{i+1} = endpoint of exe([jump], p_i).
```

After all repetitions, the final point of evaluation is reset to the **last emitted symbol**.

For the intended current use, `jump` is typically a `MOVE` instruction.

---

## `REFLECT(n)`

`REFLECT` is a legacy/optional instruction and is defined only for `BASE = 8`.

It transforms the current point and emits the transformed point. The four axes are represented by `n = 0,1,2,3`:

```text
n = 0: q = (3 - p) mod 8
n = 1: q = (7 - p) mod 8
n = 2: q = (5 - p) mod 8
n = 3: q = (1 - p) mod 8
```

The returned point is `q`.

If `BASE != 8`, execution raises `LoTSemanticsError`.

---

## `MIRROR(P)`

Execute `P` from the current point and let its emitted string be `w`.

The output is

```text
w + reverse(w).
```

The ending point returned by the internal execution of `P` is ignored. The final point is the last emitted symbol of the mirrored output.

Example for an inner output `012`:

```text
012210
```

---

## `MIRROR_BOUNCE(P)`

Execute `P` and let its output be `w`.

The output is

```text
w + reverse(w)[1:].
```

Thus the turning-point symbol is not duplicated. For inner output `012`, the result is

```text
01210.
```

The final point is the last emitted symbol.

---

## `SUB(start, P)`

Execute `P` from the explicitly supplied point `start`, independently of the current point.

Its output is appended to the surrounding program, but the surrounding point of evaluation is unchanged.

In other words, `SUB` changes the starting context of a subprogram without changing the outer state.

---

## `REFERENCE(refers_to, weight)`

`REFERENCE` is used by the experimental relative-complexity mechanism.

It stores a string directly with an externally assigned program-size weight.

In the current `exe` implementation:

```python
REFERENCE(s, weight)
```

sets the execution output buffer to `s` and leaves the current point unchanged. In particular, it **replaces** the output accumulated before that instruction rather than appending to it.

Its size contribution is exactly `weight`.

---

## `POINTER(points_to)`

`POINTER` is not intended as a semantic instruction of the LoT. It is a representation marker used by the pointer-factorization utilities in `program_ops.py`.

It is therefore best understood as part of an alternative representation of programs, not as an instruction to execute directly with `exe`.

---

## `REPEAT_CHUNK(n, P)`

`REPEAT_CHUNK` has the same execution semantics as `REPEAT`: execute `P` `n` times while threading the point of evaluation.

It is used only to mark repeated chunk structure when the optional chunk mechanism is enabled.

---

# Sequential composition

A program is a list:

```python
[I1, I2, ..., Im]
```

The instructions are executed left-to-right. Their output strings are normally concatenated, and the ending point of each instruction becomes the starting point of the next, except where the semantics above specify otherwise (`SUB`, `REFERENCE`, and some higher-level constructors).


# Alphabet representation

Sequences are represented as Python strings and the current implementation reads them one character at a time. The supplied experiments use `BASE = 8`, so every symbol is a single decimal digit. Configurations requiring multi-character symbol names would need a different sequence encoding.
