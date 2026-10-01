from lot.parameters import set_parameters
from lot.syntax import MOVE_AND_PLAY, REPEAT
from lot.semantics import exe
from lot.complexity import (
    complexity,
    complexities_and_minprog,
    write_complexities_and_minprog_json,
)
from lot.search import write_strings_with_initial_repetition_json


if __name__ == "__main__":

    # Load the language parameters.
    set_parameters("para.json")


    # ------------------------------------------------------------
    # 1. Define and execute a LoT program
    # ------------------------------------------------------------

    program = [REPEAT(3, [MOVE_AND_PLAY(1)])]

    print(exe(program, 0))


    # ------------------------------------------------------------
    # 2. Compute the complexity of a single sequence
    # ------------------------------------------------------------

    print(complexity("01234"))


    # ------------------------------------------------------------
    # 3. Search for sequences of prescribed complexity
    # ------------------------------------------------------------
    # The output contains sequences whose complexity is between
    # k_min and k_max, whose length is between length_min and
    # length_max, and for which at least one minimal program has
    # a repetition instruction as its outermost constructor.

    write_strings_with_initial_repetition_json(
        "results.json",
        3,   # k_min
        8,   # k_max
        8,   # length_min
        10,  # length_max
    )


    # ------------------------------------------------------------
    # 4. Compute complexities and minimal programs for several
    #    named sequences
    # ------------------------------------------------------------

    sequences = {
        "my_seq_name": "0000000",
        "Repetition-2": "010101010101",
    }

    print(complexities_and_minprog(sequences))


    # ------------------------------------------------------------
    # 5. Read named sequences from JSON and save their
    #    complexities and minimal programs to another JSON file
    # ------------------------------------------------------------

    write_complexities_and_minprog_json(
        "sequences.json",
        "complexities_output.json",
    )
