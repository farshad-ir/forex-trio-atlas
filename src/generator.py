"""
Generator for Forex Trio Atlas.

The generator converts Trio and Variant definitions into
JSON-compatible image instructions.

It does not render images.

Architecture:

    transformer.py
          |
          v
    generator.py
          |
          | JSON-compatible data
          v
    renderer.py
          |
          v
       PNG image
"""

from __future__ import annotations

import json
from typing import Any

try:
    from .config import CANDLE_SPACING
    from .transformer import (
        DIRECTIONS,
        VARIANTS_PER_DIRECTION,
        trio_from_number,
        variant_from_number,
    )
except ImportError:
    from config import CANDLE_SPACING
    from transformer import (
        DIRECTIONS,
        VARIANTS_PER_DIRECTION,
        trio_from_number,
        variant_from_number,
    )


# ----------------------------------------------------------------------
# GENERATION SETTINGS
# ----------------------------------------------------------------------

BODY_SIZE = 1.0
WICK_SIZE = 0.5

# Relative x positions are controlled by config.py.
CANDLE_X_POSITIONS = (
    0.0,
    CANDLE_SPACING,
    CANDLE_SPACING * 2.0,
)


# ----------------------------------------------------------------------
# WEAK RELATION VALUES
# ----------------------------------------------------------------------
#
# Each weak relation is represented by three rank values for A, B, C.
#
# The actual magnitude is irrelevant here.
# Only the ordering matters.
#
# 1  A=B=C
# 2  A=B<C
# 3  A=B>C
# 4  A=C<B
# 5  A=C>B
# 6  B=C<A
# 7  B=C>A
# 8  A<B<C
# 9  A<C<B
# 10 B<A<C
# 11 B<C<A
# 12 C<A<B
# 13 C<B<A
# ----------------------------------------------------------------------

WEAK_RELATION_VALUES = {
    1: (1.0, 1.0, 1.0),
    2: (1.0, 1.0, 2.0),
    3: (2.0, 2.0, 1.0),
    4: (1.0, 2.0, 1.0),
    5: (2.0, 1.0, 2.0),
    6: (2.0, 1.0, 1.0),
    7: (1.0, 2.0, 2.0),
    8: (0.0, 1.0, 2.0),
    9: (0.0, 2.0, 1.0),
    10: (1.0, 0.0, 2.0),
    11: (2.0, 0.0, 1.0),
    12: (1.0, 2.0, 0.0),
    13: (2.0, 1.0, 0.0),
}


# ----------------------------------------------------------------------
# STRICT RELATION VALUES
# ----------------------------------------------------------------------

STRICT_RELATION_VALUES = {
    "Rising": (0.0, 1.0, 2.0),
    "Falling": (2.0, 1.0, 0.0),
    "Peak": (0.0, 2.0, 1.0),
    "Valley": (2.0, 0.0, 1.0),
}


# ----------------------------------------------------------------------
# VALIDATION
# ----------------------------------------------------------------------


def _validate_trio_number(trio_number: int) -> None:
    """Validate a Trio number."""

    if not isinstance(trio_number, int):
        raise TypeError("trio_number must be an integer")

    if not 1 <= trio_number <= 512:
        raise ValueError(
            "trio_number must be between 1 and 512"
        )


# ----------------------------------------------------------------------
# RELATION HELPERS
# ----------------------------------------------------------------------


def _strict_values(class_name: str) -> tuple[float, float, float]:
    """Return rank values for one strict relation."""

    try:
        return STRICT_RELATION_VALUES[class_name]
    except KeyError as exc:
        raise ValueError(
            f"Unknown strict relation: {class_name}"
        ) from exc


def _weak_values(relation_number: int) -> tuple[float, float, float]:
    """Return rank values for one weak relation."""

    try:
        return WEAK_RELATION_VALUES[relation_number]
    except KeyError as exc:
        raise ValueError(
            f"Invalid weak relation number: {relation_number}"
        ) from exc


# ----------------------------------------------------------------------
# CANDLE CREATION
# ----------------------------------------------------------------------


def _build_candle(
    index: int,
    direction: str,
    body_center: float,
    upper_rank: float,
    lower_rank: float,
) -> dict[str, Any]:
    """
    Build one OHLC candle.

    direction:
        B = bullish
        S = bearish

    body_center:
        Position of the candle body center.

    upper_rank:
        Relative High ordering value.

    lower_rank:
        Relative Low ordering value.
    """

    if direction not in ("B", "S"):
        raise ValueError(
            f"Invalid candle direction: {direction}"
        )

    if direction == "B":
        open_value = body_center - BODY_SIZE / 2.0
        close_value = body_center + BODY_SIZE / 2.0
    else:
        open_value = body_center + BODY_SIZE / 2.0
        close_value = body_center - BODY_SIZE / 2.0

    body_high = max(open_value, close_value)
    body_low = min(open_value, close_value)

    high_value = (
        body_high
        + WICK_SIZE
        + upper_rank
    )

    low_value = (
        body_low
        - WICK_SIZE
        - lower_rank
    )

    return {
        "label": chr(ord("A") + index),
        "index": index,
        "x": CANDLE_X_POSITIONS[index],
        "direction": direction,
        "open": round(open_value, 6),
        "high": round(high_value, 6),
        "low": round(low_value, 6),
        "close": round(close_value, 6),
        "body": round(body_center, 6),
    }


def _build_candles(
    direction: str,
    body_values: tuple[float, float, float],
    upper_values: tuple[float, float, float],
    lower_values: tuple[float, float, float],
) -> list[dict[str, Any]]:
    """Build the three candles A, B and C."""

    candles: list[dict[str, Any]] = []

    for index in range(3):
        candles.append(
            _build_candle(
                index=index,
                direction=direction[index],
                body_center=body_values[index],
                upper_rank=upper_values[index],
                lower_rank=lower_values[index],
            )
        )

    return candles


# ----------------------------------------------------------------------
# TRIO
# ----------------------------------------------------------------------


def _build_trio_image(
    trio_number: int,
) -> dict[str, Any]:
    """Build the image instruction for one strict Trio."""

    trio = trio_from_number(trio_number)

    direction = trio["direction"]
    body_class = trio["body_class"]
    upper_class = trio["upper_class"]
    lower_class = trio["lower_class"]

    body_values = _strict_values(body_class)
    upper_values = _strict_values(upper_class)
    lower_values = _strict_values(lower_class)

    candles = _build_candles(
        direction=direction,
        body_values=body_values,
        upper_values=upper_values,
        lower_values=lower_values,
    )

    return {
        "name": f"Trio{trio_number:03d}",
        "type": "trio",
        "number": trio_number,
        "direction": direction,
        "body_class": body_class,
        "upper_class": upper_class,
        "lower_class": lower_class,
        "candles": candles,
    }


# ----------------------------------------------------------------------
# VARIANT COMPATIBILITY
# ----------------------------------------------------------------------


def _weak_relation_is_compatible(
    strict_class: str,
    relation_number: int,
) -> bool:
    """
    Determine whether a weak relation belongs to a strict class.

    Rising:
        A <= B <= C

    Falling:
        A >= B >= C

    Peak:
        A <= B >= C

    Valley:
        A >= B <= C
    """

    values = _weak_values(relation_number)

    a, b, c = values

    if strict_class == "Rising":
        return a <= b <= c

    if strict_class == "Falling":
        return a >= b >= c

    if strict_class == "Peak":
        return a <= b and c <= b

    if strict_class == "Valley":
        return a >= b and c >= b

    raise ValueError(
        f"Unknown strict class: {strict_class}"
    )


def _compatible_relations(
    strict_class: str,
) -> list[int]:
    """Return all weak relation numbers compatible with a class."""

    return [
        relation_number
        for relation_number in range(1, 14)
        if _weak_relation_is_compatible(
            strict_class,
            relation_number,
        )
    ]


# ----------------------------------------------------------------------
# VARIANT NUMBER
# ----------------------------------------------------------------------


def _variant_number(
    direction: str,
    body_relation: int,
    upper_relation: int,
    lower_relation: int,
) -> int:
    """
    Calculate the universal Variant number.

    Numbering:

        direction
        body relation
        upper relation
        lower relation
    """

    direction_index = DIRECTIONS.index(direction)

    return (
        direction_index * VARIANTS_PER_DIRECTION
        + (body_relation - 1) * 13 * 13
        + (upper_relation - 1) * 13
        + (lower_relation - 1)
        + 1
    )


# ----------------------------------------------------------------------
# VARIANT
# ----------------------------------------------------------------------


def _build_variant_image(
    variant_number: int,
    trio_number: int,
) -> dict[str, Any]:
    """Build one Variant image instruction."""

    variant = variant_from_number(variant_number)

    direction = variant["direction"]
    body_relation = variant["body_relation"]
    upper_relation = variant["upper_relation"]
    lower_relation = variant["lower_relation"]

    body_values = _weak_values(body_relation)
    upper_values = _weak_values(upper_relation)
    lower_values = _weak_values(lower_relation)

    candles = _build_candles(
        direction=direction,
        body_values=body_values,
        upper_values=upper_values,
        lower_values=lower_values,
    )

    return {
        "name": f"Variant{variant_number:05d}",
        "type": "variant",
        "number": variant_number,
        "trio_number": trio_number,
        "direction": direction,
        "body_relation": body_relation,
        "upper_relation": upper_relation,
        "lower_relation": lower_relation,
        "candles": candles,
    }


# ----------------------------------------------------------------------
# PUBLIC GENERATOR
# ----------------------------------------------------------------------


def generate_trio(
    trio_number: int,
    include_variants: bool = False,
) -> dict[str, Any]:
    """
    Generate JSON-compatible data for one Trio.

    Parameters
    ----------
    trio_number:
        Number from 1 to 512.

    include_variants:
        False:
            Generate only the Trio.

        True:
            Generate the Trio plus all compatible Variants.

    Returns
    -------
    dict
        JSON-compatible generator output.
    """

    _validate_trio_number(trio_number)

    trio = trio_from_number(trio_number)

    direction = trio["direction"]
    body_class = trio["body_class"]
    upper_class = trio["upper_class"]
    lower_class = trio["lower_class"]

    images: list[dict[str, Any]] = []

    # --------------------------------------------------------------
    # Main Trio
    # --------------------------------------------------------------

    images.append(
        _build_trio_image(trio_number)
    )

    # --------------------------------------------------------------
    # Compatible Variants
    # --------------------------------------------------------------

    if include_variants:

        body_relations = _compatible_relations(
            body_class
        )

        upper_relations = _compatible_relations(
            upper_class
        )

        lower_relations = _compatible_relations(
            lower_class
        )

        for body_relation in body_relations:
            for upper_relation in upper_relations:
                for lower_relation in lower_relations:

                    variant_number = _variant_number(
                        direction=direction,
                        body_relation=body_relation,
                        upper_relation=upper_relation,
                        lower_relation=lower_relation,
                    )

                    images.append(
                        _build_variant_image(
                            variant_number=variant_number,
                            trio_number=trio_number,
                        )
                    )

    return {
        "generator": "forex-trio-atlas",
        "version": 1,
        "trio": {
            "number": trio_number,
            "name": f"Trio{trio_number:03d}",
            "direction": direction,
            "body_class": body_class,
            "upper_class": upper_class,
            "lower_class": lower_class,
        },
        "include_variants": include_variants,
        "image_count": len(images),
        "images": images,
    }


# ----------------------------------------------------------------------
# JSON OUTPUT
# ----------------------------------------------------------------------


def generate_json(
    trio_number: int,
    include_variants: bool = False,
) -> str:
    """Generate serialized JSON text."""

    data = generate_trio(
        trio_number=trio_number,
        include_variants=include_variants,
    )

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )


# ----------------------------------------------------------------------
# COMMAND LINE TEST
# ----------------------------------------------------------------------


def main() -> int:
    """Generate Trio001 for a manual test."""

    print(
        generate_json(
            trio_number=1,
            include_variants=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
