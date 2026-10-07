"""
Generator for Forex Trio Atlas.

The generator receives already-built geometry and converts it
into the JSON instruction expected by the renderer.

Geometry is built by geometry.py.

The generator does not:

    - classify Trios
    - define Weak Relations
    - calculate Weak Relations
    - calculate geometry
    - calculate candle OHLC values
    - create folders
    - save JSON files
    - render PNG files

Those responsibilities belong to other layers.
"""

from __future__ import annotations

from typing import Any

try:
    from .geometry import build_geometry
    from .relations import DEFAULT_STRICT_RELATION
except ImportError:
    from geometry import build_geometry
    from relations import DEFAULT_STRICT_RELATION



CANDLE_SPACING = 1.5

CANDLE_X_POSITIONS = (
    0.0,
    CANDLE_SPACING,
    CANDLE_SPACING * 2.0,
)





def generate_trio(
    trio: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a Main Trio definition and its geometry
    into a Renderer instruction.
    """

    trio_number = int(
        trio["number"]
    )

    trio_name = (
        f"Trio{trio_number:03d}"
    )

    direction = trio["direction"]

    body_values = DEFAULT_STRICT_RELATION[ trio["body_class"] ]

    upper_values = DEFAULT_STRICT_RELATION[ trio["upper_class"] ]

    lower_values = DEFAULT_STRICT_RELATION[ trio["lower_class"] ]
    
    geometry = build_geometry(
        direction     = trio["direction"],
        body_values   = body_values,
        upper_values  = upper_values,
        lower_values  = lower_values,
    )

    candles = []

    for index, candle in enumerate(geometry["candles"]):
        candle = dict(candle)

        candle["label"] = chr(
            ord("A") + index
        )
        candle["index"] = index
        candle["x"] = CANDLE_X_POSITIONS[index]
        candle["direction"] = trio["direction"][index]

        candles.append(candle)

    return {
        "name": trio_name,
        "type": "trio",
        "number": trio_number,
        "json_path": (
            f"{trio_name}/"
            f"{trio_name}.json"
        ),
        "image_path": (
            f"{trio_name}/"
            f"{trio_name}.png"
        ),

        "label": chr(
            ord("A") + index
        ),
        "index": index,
        "x": CANDLE_X_POSITIONS[index],
        "candles": candles,
    }


def generate_variant(
    variant: dict[str, Any],
    trio_number: int,
) -> dict[str, Any]:
    """
    Convert a Variant definition and its geometry
    into a Renderer instruction.
    """

    variant_number = int(
        variant["number"]
    )

    variant_name = (
        f"Variant{variant_number:05d}"
    )

    trio_name = (
        f"Trio{trio_number:03d}"
    )

    geometry = build_geometry(
        direction    = variant["direction"],
        body_values  = tuple(
            variant["body_relation"]
        ),
        upper_values = tuple(
            variant["upper_relation"]
        ),
        lower_values = tuple(
            variant["lower_relation"]
        ),
    )

    candles = []

    for index, candle in enumerate(
        geometry["candles"]
    ):
        candle = dict(candle)

        candle["label"] = chr(
            ord("A") + index
        )
        candle["index"] = index
        candle["x"] = CANDLE_X_POSITIONS[index]
        candle["direction"] = variant["direction"][index]

        candles.append(candle)

    return {
        "name": variant_name,
        "type": "variant",
        "number": variant_number,
        "trio_number": trio_number,
        "direction": variant["direction"],

        "json_path": (
            f"{trio_name}/Variants/"
            f"{variant_name}.json"
        ),
        "image_path": (
            f"{trio_name}/Variants/"
            f"{variant_name}.png"
        ),
        "candles": candles,
    }
