#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from transformer import (
    trio_from_number,
    number_from_weak_relation_name,
    weak_relation_from_number,
)
from generator import generate_trio, generate_variant
from renderer import render_document


ATLAS_ROOT = Path("output/trios")


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )
        file.write("\n")


def find_variants(trio_number):
    trio_name = f"Trio{trio_number:03d}"

    variants_dir = (
        ATLAS_ROOT
        / trio_name
        / "Variants"
    )

    if not variants_dir.exists():
        return []

    return sorted(
        variants_dir.glob("Variant*.json")
    )


def relation_values(relation_name):
    """
    Convert the human-readable Weak Relation name
    into its stored numeric relation values.

    The 13 relations are not defined here.
    Transformer remains the single source of truth.
    """

    relation_number = (
        number_from_weak_relation_name(
            relation_name
        )
    )

    relation = weak_relation_from_number(
        relation_number
    )

    return relation["relation"]


def prepare_variant(variant):
    """
    Adapt the human-readable Variant JSON for Generator.

    The original Variant JSON remains human-readable.
    Generator receives a temporary copy containing
    numeric relation values.
    """

    prepared = dict(variant)

    prepared["body_relation"] = relation_values(
        variant["body_relation"]
    )

    prepared["upper_relation"] = relation_values(
        variant["upper_relation"]
    )

    prepared["lower_relation"] = relation_values(
        variant["lower_relation"]
    )

    return prepared


def render_instruction(
    instruction,
    output_directory,
):
    document = {
        "images": [instruction]
    }

    render_document(
        document,
        output_directory,
    )


def build_trio(trio_number):
    trio_name = f"Trio{trio_number:03d}"

    trio_dir = (
        ATLAS_ROOT
        / trio_name
    )

    trio_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"\nBuilding {trio_name}"
    )

    # Main Trio comes from Transformer.
    trio = trio_from_number(
        trio_number
    )

    trio["id"] = trio_name

    # Generator creates Main Trio instructions.
    trio_instruction = generate_trio(
        trio
    )

    # Orchestrator saves Main Trio JSON.
    trio_json = (
        trio_dir
        / f"{trio_name}.json"
    )

    save_json(
        trio_json,
        trio_instruction,
    )

    # Renderer creates Main Trio PNG.
    render_instruction(
        trio_instruction,
        ATLAS_ROOT,
    )

    # Existing Variant JSON files.
    variant_paths = find_variants(
        trio_number
    )

    print(
        f"  Variants found: "
        f"{len(variant_paths)}"
    )

    variants_dir = (
        trio_dir
        / "Variants"
    )

    variants_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for variant_path in variant_paths:
        variant = load_json(
            variant_path
        )

        # Convert human-readable relation names
        # only for Generator.
        prepared_variant = prepare_variant(
            variant
        )

        variant_instruction = (
            generate_variant(
                prepared_variant,
                trio_number,
            )
        )

        # Keep the original human-readable
        # Variant JSON untouched.
        render_instruction(
            variant_instruction,
            ATLAS_ROOT,
        )

    print(
        f"  Done: {trio_name}"
    )


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python3 src/orchestrator.py N"
        )
        return 1

    try:
        maximum = int(
            sys.argv[1]
        )
    except ValueError:
        print(
            "N must be an integer."
        )
        return 1

    if not 1 <= maximum <= 512:
        print(
            "N must be between 1 and 512."
        )
        return 1

    for trio_number in range(
        1,
        maximum + 1,
    ):
        build_trio(
            trio_number
        )

    print(
        f"\nCompleted "
        f"Trio001 through "
        f"Trio{maximum:03d}."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
