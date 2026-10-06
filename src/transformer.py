"""
Transformation and numbering logic for Forex Trio Atlas.

This module contains only mathematical classification and numbering
logic. It does not contain rendering or image-generation logic.

Main Trio space:
    8 directions × 4 body classes × 4 upper classes × 4 lower classes
    = 512 Trios

Universal Variant space:
    8 directions × 13 weak body relations
    × 13 weak upper relations × 13 weak lower relations
    = 17,576 Variants
"""


# ----------------------------------------------------------------------
# DIRECTIONS
# ----------------------------------------------------------------------

DIRECTIONS = (
    "BBB",
    "BBS",
    "BSB",
    "BSS",
    "SBB",
    "SBS",
    "SSB",
    "SSS",
)


# ----------------------------------------------------------------------
# STRICT RELATION CLASSES
# ----------------------------------------------------------------------

CLASSES = (
    "Rising",
    "Falling",
    "Peak",
    "Valley",
)


# ----------------------------------------------------------------------
# WEAK RELATIONS
# ----------------------------------------------------------------------
#
# The 13 weak orderings of three values A, B, C.
#
# Each relation is represented by the rank of A, B and C.
#
# Example:
#
#     A=B<C
#
# means:
#     A and B have the same value
#     C is greater than both
#
# The numerical representation is only an internal representation.
# The human-readable name is stored separately below.
# ----------------------------------------------------------------------

WEAK_RELATIONS = (
    (0, 0, 0),  # A=B=C

    (0, 0, 1),  # A=B<C
    (1, 1, 0),  # A=B>C

    (0, 1, 0),  # A=C<B
    (1, 0, 1),  # A=C>B

    (1, 0, 0),  # B=C<A
    (0, 1, 1),  # B=C>A

    (0, 1, 2),  # A<B<C
    (0, 2, 1),  # A<C<B
    (1, 0, 2),  # B<A<C
    (1, 2, 0),  # B<C<A
    (2, 0, 1),  # C<A<B
    (2, 1, 0),  # C<B<A
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


# ----------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------

TRIO_COUNT = (
    len(DIRECTIONS)
    * len(CLASSES)
    * len(CLASSES)
    * len(CLASSES)
)

WEAK_RELATION_COUNT = len(WEAK_RELATIONS)

VARIANTS_PER_DIRECTION = (
    WEAK_RELATION_COUNT ** 3
)

VARIANT_COUNT = (
    len(DIRECTIONS)
    * VARIANTS_PER_DIRECTION
)


# ----------------------------------------------------------------------
# TRIO NUMBERING
# ----------------------------------------------------------------------

def trio_from_number(number):
    """
    Convert a Trio number to its four classification components.

    Example:

        trio_from_number(1)

    returns:

        {
            "number": 1,
            "direction": "BBB",
            "body_class": "Rising",
            "upper_class": "Rising",
            "lower_class": "Rising",
        }
    """

    if not 1 <= number <= TRIO_COUNT:
        raise ValueError(
            f"Trio number must be between 1 and {TRIO_COUNT}."
        )

    zero_based = number - 1

    classes_per_direction = (
        len(CLASSES) ** 3
    )

    direction_index = (
        zero_based // classes_per_direction
    )

    remainder = (
        zero_based % classes_per_direction
    )

    body_index = (
        remainder // (len(CLASSES) ** 2)
    )

    remainder %= len(CLASSES) ** 2

    upper_index = (
        remainder // len(CLASSES)
    )

    lower_index = (
        remainder % len(CLASSES)
    )

    return {
        "number": number,
        "direction": DIRECTIONS[direction_index],
        "body_class": CLASSES[body_index],
        "upper_class": CLASSES[upper_index],
        "lower_class": CLASSES[lower_index],
    }


def number_from_trio(
    direction,
    body_class,
    upper_class,
    lower_class,
):
    """
    Convert Trio classification components to a Trio number.
    """

    if direction not in DIRECTIONS:
        raise ValueError("Invalid direction.")

    if body_class not in CLASSES:
        raise ValueError("Invalid body class.")

    if upper_class not in CLASSES:
        raise ValueError("Invalid upper class.")

    if lower_class not in CLASSES:
        raise ValueError("Invalid lower class.")

    direction_index = DIRECTIONS.index(direction)
    body_index = CLASSES.index(body_class)
    upper_index = CLASSES.index(upper_class)
    lower_index = CLASSES.index(lower_class)

    return (
        direction_index * (len(CLASSES) ** 3)
        + body_index * (len(CLASSES) ** 2)
        + upper_index * len(CLASSES)
        + lower_index
        + 1
    )


# ----------------------------------------------------------------------
# WEAK RELATION NUMBERING
# ----------------------------------------------------------------------

def weak_relation_from_number(number):
    """
    Convert weak relation number 1..13 to its representation.

    Returns a dictionary containing:

        number
        name
        relation
    """

    if not 1 <= number <= WEAK_RELATION_COUNT:
        raise ValueError(
            "Weak relation number must be between "
            f"1 and {WEAK_RELATION_COUNT}."
        )

    index = number - 1

    return {
        "number": number,
        "name": WEAK_RELATION_NAMES[index],
        "relation": WEAK_RELATIONS[index],
    }


def number_from_weak_relation(relation):
    """
    Convert a weak relation representation to its number.
    """

    try:
        return WEAK_RELATIONS.index(tuple(relation)) + 1
    except ValueError as exc:
        raise ValueError(
            "Invalid weak relation."
        ) from exc


def number_from_weak_relation_name(name):
    """
    Convert a weak relation name such as 'A<B<C'
    to its number.
    """

    if name not in WEAK_RELATION_NAMES:
        raise ValueError(
            f"Invalid weak relation name: {name}"
        )

    return WEAK_RELATION_NAMES.index(name) + 1


# ----------------------------------------------------------------------
# VARIANT NUMBERING
# ----------------------------------------------------------------------

def variant_from_number(number):
    """
    Convert a universal Variant number to its components.

    Variant numbering:

        Direction
        BodyWeak
        UpperWeak
        LowerWeak

    There are:

        13 × 13 × 13 = 2197

    variants for each direction.

    Therefore:

        Variant00001 = first BBB combination
        Variant02197 = last BBB combination
        Variant02198 = first BBS combination
        ...
        Variant17576 = last SSS combination.
    """

    if not 1 <= number <= VARIANT_COUNT:
        raise ValueError(
            f"Variant number must be between 1 and {VARIANT_COUNT}."
        )

    zero_based = number - 1

    direction_index = (
        zero_based // VARIANTS_PER_DIRECTION
    )

    remainder = (
        zero_based % VARIANTS_PER_DIRECTION
    )

    body_index = (
        remainder
        // (WEAK_RELATION_COUNT ** 2)
    )

    remainder %= WEAK_RELATION_COUNT ** 2

    upper_index = (
        remainder // WEAK_RELATION_COUNT
    )

    lower_index = (
        remainder % WEAK_RELATION_COUNT
    )

    body_number = body_index + 1
    upper_number = upper_index + 1
    lower_number = lower_index + 1

    return {
        "number": number,
        "direction": DIRECTIONS[direction_index],

        "body_relation_number": body_number,
        "body_relation": WEAK_RELATION_NAMES[
            body_index
        ],

        "upper_relation_number": upper_number,
        "upper_relation": WEAK_RELATION_NAMES[
            upper_index
        ],

        "lower_relation_number": lower_number,
        "lower_relation": WEAK_RELATION_NAMES[
            lower_index
        ],
    }


def number_from_variant(
    direction,
    body_relation,
    upper_relation,
    lower_relation,
):
    """
    Convert Variant components to the universal Variant number.

    The ordering is:

        Direction
        BodyWeak
        UpperWeak
        LowerWeak

    with LowerWeak changing fastest.
    """

    if direction not in DIRECTIONS:
        raise ValueError("Invalid direction.")

    body_index = (
        number_from_weak_relation(body_relation) - 1
    )

    upper_index = (
        number_from_weak_relation(upper_relation) - 1
    )

    lower_index = (
        number_from_weak_relation(lower_relation) - 1
    )

    direction_index = DIRECTIONS.index(direction)

    return (
        direction_index * VARIANTS_PER_DIRECTION
        + body_index * (WEAK_RELATION_COUNT ** 2)
        + upper_index * WEAK_RELATION_COUNT
        + lower_index
        + 1
    )


# ----------------------------------------------------------------------
# VARIANT NUMBERING USING RELATION NAMES
# ----------------------------------------------------------------------

def number_from_variant_names(
    direction,
    body_relation,
    upper_relation,
    lower_relation,
):
    """
    Convert a Variant described by human-readable relation names
    to its universal Variant number.

    Example:

        number_from_variant_names(
            "BBB",
            "A=B=C",
            "A=B=C",
            "A=B<C",
        )

    returns:

        2
    """

    return number_from_variant(
        direction,
        WEAK_RELATIONS[
            number_from_weak_relation_name(body_relation) - 1
        ],
        WEAK_RELATIONS[
            number_from_weak_relation_name(upper_relation) - 1
        ],
        WEAK_RELATIONS[
            number_from_weak_relation_name(lower_relation) - 1
        ],
    )


# ----------------------------------------------------------------------
# VARIANT NAME
# ----------------------------------------------------------------------

def variant_name(number):
    """
    Return the canonical folder name for a Variant.

    Examples:

        1     -> Variant00001
        9999  -> Variant09999
        10000 -> Variant10000
        17576 -> Variant17576
    """

    if not 1 <= number <= VARIANT_COUNT:
        raise ValueError(
            f"Variant number must be between 1 and {VARIANT_COUNT}."
        )

    return f"Variant{number:05d}"


# ----------------------------------------------------------------------
# TRIO NAME
# ----------------------------------------------------------------------

def trio_name(number):
    """
    Return the canonical folder name for a Trio.

    Examples:

        1   -> Trio001
        512 -> Trio512
    """

    if not 1 <= number <= TRIO_COUNT:
        raise ValueError(
            f"Trio number must be between 1 and {TRIO_COUNT}."
        )

    return f"Trio{number:03d}"

