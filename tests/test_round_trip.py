"""
Focused round-trip tests for forex-trio-atlas.

No external packages are required.

Run from the project root with:

    python tests/test_round_trip.py
"""

import sys
from pathlib import Path


# ----------------------------------------------------------------------
# PROJECT PATH
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ----------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------

from src.transformer import (
    DIRECTIONS,
    CLASSES,
    WEAK_RELATIONS,
    WEAK_RELATION_NAMES,
    TRIO_COUNT,
    VARIANT_COUNT,
    VARIANTS_PER_DIRECTION,
    trio_from_number,
    number_from_trio,
    weak_relation_from_number,
    number_from_weak_relation,
    number_from_weak_relation_name,
    variant_from_number,
    number_from_variant,
    number_from_variant_names,
)


# ----------------------------------------------------------------------
# TEST HELPERS
# ----------------------------------------------------------------------

passed = 0
failed = 0


def check(condition, message):
    global passed
    global failed

    if condition:
        print(f"PASS: {message}")
        passed += 1
    else:
        print(f"FAIL: {message}")
        failed += 1


def check_equal(actual, expected, message):
    check(
        actual == expected,
        f"{message} "
        f"(expected={expected!r}, actual={actual!r})",
    )


# ----------------------------------------------------------------------
# BASIC CONSTANTS
# ----------------------------------------------------------------------

def test_constants():
    print()
    print("=== CONSTANTS ===")

    check_equal(
        len(DIRECTIONS),
        8,
        "8 candle directions",
    )

    check_equal(
        len(CLASSES),
        4,
        "4 strict relation classes",
    )

    check_equal(
        len(WEAK_RELATIONS),
        13,
        "13 weak relations",
    )

    check_equal(
        len(WEAK_RELATION_NAMES),
        13,
        "13 weak relation names",
    )

    check_equal(
        TRIO_COUNT,
        512,
        "512 Trios",
    )

    check_equal(
        VARIANTS_PER_DIRECTION,
        2197,
        "2197 Variants per direction",
    )

    check_equal(
        VARIANT_COUNT,
        17576,
        "17576 total Variants",
    )


# ----------------------------------------------------------------------
# TRIO ROUND-TRIP
# ----------------------------------------------------------------------

def test_trio_round_trip():
    print()
    print("=== TRIO ROUND-TRIP ===")

    local_failures = []

    for number in range(1, TRIO_COUNT + 1):
        trio = trio_from_number(number)

        result = number_from_trio(
            trio["direction"],
            trio["body_class"],
            trio["upper_class"],
            trio["lower_class"],
        )

        if result != number:
            local_failures.append(
                (number, result, trio)
            )

    check(
        not local_failures,
        "All 512 Trio numbers round-trip correctly",
    )

    if local_failures:
        print(
            "First Trio failure:",
            local_failures[0],
        )


# ----------------------------------------------------------------------
# TRIO BOUNDARIES
# ----------------------------------------------------------------------

def test_trio_boundaries():
    print()
    print("=== TRIO BOUNDARIES ===")

    expected = {
        1: (
            "BBB",
            "Rising",
            "Rising",
            "Rising",
        ),
        2: (
            "BBB",
            "Rising",
            "Rising",
            "Falling",
        ),
        64: (
            "BBB",
            "Valley",
            "Valley",
            "Valley",
        ),
        65: (
            "BBS",
            "Rising",
            "Rising",
            "Rising",
        ),
        128: (
            "BBS",
            "Valley",
            "Valley",
            "Valley",
        ),
        129: (
            "BSB",
            "Rising",
            "Rising",
            "Rising",
        ),
        256: (
            "BSS",
            "Valley",
            "Valley",
            "Valley",
        ),
        257: (
            "SBB",
            "Rising",
            "Rising",
            "Rising",
        ),
        512: (
            "SSS",
            "Valley",
            "Valley",
            "Valley",
        ),
    }

    for number, expected_value in expected.items():
        trio = trio_from_number(number)

        actual = (
            trio["direction"],
            trio["body_class"],
            trio["upper_class"],
            trio["lower_class"],
        )

        check_equal(
            actual,
            expected_value,
            f"Trio {number:03d}",
        )


# ----------------------------------------------------------------------
# WEAK RELATION ROUND-TRIP
# ----------------------------------------------------------------------

def test_weak_relation_round_trip():
    print()
    print("=== WEAK RELATION ROUND-TRIP ===")

    local_failures = []

    for number in range(1, 14):
        relation = weak_relation_from_number(number)

        result = number_from_weak_relation(
            relation["relation"]
        )

        if result != number:
            local_failures.append(
                (number, result, relation)
            )

    check(
        not local_failures,
        "All 13 weak relations round-trip correctly",
    )

    if local_failures:
        print(
            "First weak relation failure:",
            local_failures[0],
        )


# ----------------------------------------------------------------------
# WEAK RELATION NAMES
# ----------------------------------------------------------------------

def test_weak_relation_names():
    print()
    print("=== WEAK RELATION NAMES ===")

    local_failures = []

    for number, name in enumerate(
        WEAK_RELATION_NAMES,
        start=1,
    ):
        result = number_from_weak_relation_name(name)

        if result != number:
            local_failures.append(
                (number, name, result)
            )

    check(
        not local_failures,
        "All 13 weak relation names map correctly",
    )

    if local_failures:
        print(
            "First name failure:",
            local_failures[0],
        )


# ----------------------------------------------------------------------
# VARIANT ROUND-TRIP
# ----------------------------------------------------------------------

def test_variant_round_trip():
    print()
    print("=== VARIANT ROUND-TRIP ===")

    local_failures = []

    for number in range(1, VARIANT_COUNT + 1):
        variant = variant_from_number(number)

        body_relation = WEAK_RELATIONS[
            variant["body_relation_number"] - 1
        ]

        upper_relation = WEAK_RELATIONS[
            variant["upper_relation_number"] - 1
        ]

        lower_relation = WEAK_RELATIONS[
            variant["lower_relation_number"] - 1
        ]

        result = number_from_variant(
            variant["direction"],
            body_relation,
            upper_relation,
            lower_relation,
        )

        if result != number:
            local_failures.append(
                (number, result, variant)
            )

            # One failure is enough to diagnose the
            # numbering formula.
            break

    check(
        not local_failures,
        "All 17,576 Variant numbers round-trip correctly",
    )

    if local_failures:
        print(
            "First Variant failure:",
            local_failures[0],
        )


# ----------------------------------------------------------------------
# VARIANT NAME ROUND-TRIP
# ----------------------------------------------------------------------

def test_variant_name_round_trip():
    print()
    print("=== VARIANT NAME ROUND-TRIP ===")

    local_failures = []

    for number in range(1, VARIANT_COUNT + 1):
        variant = variant_from_number(number)

        result = number_from_variant_names(
            variant["direction"],
            variant["body_relation"],
            variant["upper_relation"],
            variant["lower_relation"],
        )

        if result != number:
            local_failures.append(
                (number, result, variant)
            )
            break

    check(
        not local_failures,
        "All Variant relation names round-trip correctly",
    )

    if local_failures:
        print(
            "First Variant name failure:",
            local_failures[0],
        )


# ----------------------------------------------------------------------
# VARIANT BOUNDARIES
# ----------------------------------------------------------------------

def test_variant_boundaries():
    print()
    print("=== VARIANT BOUNDARIES ===")

    expected = {
        1: (
            "BBB",
            1,
            1,
            1,
        ),
        2197: (
            "BBB",
            13,
            13,
            13,
        ),
        2198: (
            "BBS",
            1,
            1,
            1,
        ),
        4394: (
            "BBS",
            13,
            13,
            13,
        ),
        15380: (
            "SSS",
            1,
            1,
            1,
        ),
        17576: (
            "SSS",
            13,
            13,
            13,
        ),
    }

    for number, expected_value in expected.items():
        variant = variant_from_number(number)

        actual = (
            variant["direction"],
            variant["body_relation_number"],
            variant["upper_relation_number"],
            variant["lower_relation_number"],
        )

        check_equal(
            actual,
            expected_value,
            f"Variant {number:05d}",
        )


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------

def main():
    print("=" * 70)
    print("FOREX TRIO ATLAS - TRANSFORMER ROUND-TRIP TESTS")
    print("=" * 70)

    test_constants()
    test_trio_round_trip()
    test_trio_boundaries()
    test_weak_relation_round_trip()
    test_weak_relation_names()
    test_variant_round_trip()
    test_variant_name_round_trip()
    test_variant_boundaries()

    print()
    print("=" * 70)
    print(
        f"RESULT: {passed} passed, "
        f"{failed} failed"
    )
    print("=" * 70)

    if failed:
        return 1

    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


