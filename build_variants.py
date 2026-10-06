"""
Build the complete Trio -> Variant reference tree.

The program creates:
    output/Trio001/Variants/
    output/Trio002/Variants/
    ...
    output/Trio512/Variants/

Each Trio receives only the weak variants compatible with
its Body, Upper and Lower classes.

The global Variant numbering space is:

    8 × 13 × 13 × 13 = 17,576
"""

import json
import shutil
from pathlib import Path

from src.transformer import (
    DIRECTIONS,
    CLASSES,
    WEAK_RELATIONS,
    WEAK_RELATION_NAMES,
    trio_from_number,
    variant_from_number,
    number_from_variant_names,
)


OUTPUT_ROOT = Path("output")
TRIOS_ROOT = OUTPUT_ROOT / "trios"
VARIANTS_ROOT = OUTPUT_ROOT / "variants"
REFERENCE_ROOT = OUTPUT_ROOT / "reference"


# ----------------------------------------------------------------------
# RELATION TEST
# ----------------------------------------------------------------------

def relation_matches_class(ranks, relation_class):
    """
    Check whether a weak relation is compatible with
    one of the four strict classes after replacing < / >
    with <= / >=.
    """

    a, b, c = ranks

    if relation_class == "Rising":
        return a <= b and b <= c

    if relation_class == "Falling":
        return a >= b and b >= c

    if relation_class == "Peak":
        return a <= b and c <= b

    if relation_class == "Valley":
        return a >= b and c >= b

    raise ValueError("Invalid relation class.")


def compatible_relations(relation_class):
    """Return all 13 weak relations compatible with a class."""

    result = []

    for index, ranks in enumerate(WEAK_RELATIONS):
        if relation_matches_class(ranks, relation_class):
            result.append(index + 1)

    return result


# ----------------------------------------------------------------------
# VARIANT ID
# ----------------------------------------------------------------------

def variant_id(number):
    return f"Variant{number:05d}"


def trio_id(number):
    return f"Trio{number:03d}"


# ----------------------------------------------------------------------
# BUILD
# ----------------------------------------------------------------------

def main():
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)

    TRIOS_ROOT.mkdir(parents=True)
    VARIANTS_ROOT.mkdir(parents=True)
    REFERENCE_ROOT.mkdir(parents=True)

    trio_to_variants = {}
    variant_to_trios = {}

    class_relation_cache = {
        class_name: compatible_relations(class_name)
        for class_name in CLASSES
    }

    print("Compatible weak relations:")
    for class_name in CLASSES:
        numbers = class_relation_cache[class_name]

        names = [
            WEAK_RELATION_NAMES[number - 1]
            for number in numbers
        ]

        print(f"  {class_name}: {len(numbers)}")
        for name in names:
            print(f"      {name}")

    print()

    total_memberships = 0

    # --------------------------------------------------------------
    # Create the 17,576 universal Variant descriptions.
    # --------------------------------------------------------------

    for number in range(1, 17577):
        data = variant_from_number(number)
        vid = variant_id(number)

        folder = VARIANTS_ROOT / vid
        folder.mkdir(parents=True)

        data["id"] = vid

        with open(
            folder / "variant.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        variant_to_trios[vid] = []

    # --------------------------------------------------------------
    # Build every Trio folder.
    # --------------------------------------------------------------

    for trio_number in range(1, 513):
        trio = trio_from_number(trio_number)

        tid = trio_id(trio_number)

        trio_folder = TRIOS_ROOT / tid
        variants_folder = trio_folder / "Variants"

        variants_folder.mkdir(parents=True)

        body_numbers = class_relation_cache[
            trio["body_class"]
        ]

        upper_numbers = class_relation_cache[
            trio["upper_class"]
        ]

        lower_numbers = class_relation_cache[
            trio["lower_class"]
        ]

        variant_numbers = []

        for body in body_numbers:
            for upper in upper_numbers:
                for lower in lower_numbers:

                    number = number_from_variant_names(
                        trio["direction"],
                        WEAK_RELATION_NAMES[body - 1],
                        WEAK_RELATION_NAMES[upper - 1],
                        WEAK_RELATION_NAMES[lower - 1],
                    )

                    if number not in variant_numbers:
                        variant_numbers.append(number)

        variant_numbers.sort()

        trio_to_variants[tid] = []

        for number in variant_numbers:
            vid = variant_id(number)

            trio_to_variants[tid].append(vid)
            variant_to_trios[vid].append(tid)

            # Store a small reference file in the Trio folder.
            reference_file = variants_folder / f"{vid}.json"

            variant_data = variant_from_number(number)

            variant_data["id"] = vid
            variant_data["trio"] = tid

            with open(
                reference_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    variant_data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            total_memberships += 1

    # --------------------------------------------------------------
    # Cross references.
    # --------------------------------------------------------------

    with open(
        REFERENCE_ROOT / "trio_to_variants.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            trio_to_variants,
            file,
            indent=4,
            ensure_ascii=False,
        )

    with open(
        REFERENCE_ROOT / "variant_to_trios.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            variant_to_trios,
            file,
            indent=4,
            ensure_ascii=False,
        )

    # --------------------------------------------------------------
    # Summary.
    # --------------------------------------------------------------

    membership_counts = [
        len(values)
        for values in trio_to_variants.values()
    ]

    unique_used_variants = sum(
        1
        for values in variant_to_trios.values()
        if values
    )

    maximum = max(membership_counts)
    minimum = min(membership_counts)

    summary = {
        "total_trios": 512,
        "total_universal_variants": 17576,
        "unique_used_variants": unique_used_variants,
        "total_trio_variant_memberships": total_memberships,
        "minimum_variants_per_trio": minimum,
        "maximum_variants_per_trio": maximum,
    }

    with open(
        REFERENCE_ROOT / "summary.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print("Build complete.")
    print()
    print(f"Trio count:                 {summary['total_trios']}")
    print(
        "Universal Variant count:    "
        f"{summary['total_universal_variants']}"
    )
    print(
        "Used unique Variants:       "
        f"{summary['unique_used_variants']}"
    )
    print(
        "Trio/Variant memberships:   "
        f"{summary['total_trio_variant_memberships']}"
    )
    print(
        "Minimum per Trio:           "
        f"{summary['minimum_variants_per_trio']}"
    )
    print(
        "Maximum per Trio:           "
        f"{summary['maximum_variants_per_trio']}"
    )


if __name__ == "__main__":
    main()
