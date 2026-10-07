"""
Canonical relation definitions.

This file is the single source of truth for:

    - Strict Trio relations
    - Weak Variant relations
"""

DEFAULT_STRICT_RELATION = {
    "Rising":  (0, 1, 2),
    "Falling": (2, 1, 0),
    "Peak":    (0, 2, 1),
    "Valley":  (1, 0, 2),
}


STRICT_RELATIONS = {
    "Rising": (
        (0, 1, 2),
    ),

    "Falling": (
        (2, 1, 0),
    ),

    "Peak": (
        (0, 2, 1),
        (1, 2, 0),
    ),

    "Valley": (
        (1, 0, 2),
        (2, 0, 1),
    ),
}

WEAK_RELATIONS = (
    (0, 0, 0),

    (0, 0, 1),
    (1, 1, 0),

    (0, 1, 0),
    (1, 0, 1),

    (1, 0, 0),
    (0, 1, 1),

    (0, 1, 2),
    (0, 2, 1),
    (1, 0, 2),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0),
)


WEAK_RELATION_NAMES = (
    "A=B=C",

    "A=B<C",
    "A=B>C",

    "A=C<B",
    "A=C>B",

    "B=C<A",
    "B=C>A",

    "A<B<C",
    "A<C<B",
    "B<A<C",
    "B<C<A",
    "C<A<B",
    "C<B<A",
)
