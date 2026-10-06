"""
Generator for Forex Trio Atlas.

The generator converts semantic Trio and Variant definitions
into JSON-compatible image instructions.

It does not:

    - classify Trios
    - define Weak Relations
    - calculate Weak Relations
    - calculate Variant membership
    - calculate Variant numbers
    - create folders
    - save JSON files
    - render PNG files

Those responsibilities belong to other layers.

Architecture:

    transformer.py
          |
          | Main Trio definition
          v
    orchestrator.py
          |
          | Variant JSON definitions
          v
    generator.py
          |
          | image instructions
          v
    renderer.py
          |
          v
       PNG images

The generator is intentionally simple:

    semantic definition in
            |
            v
    image instruction out

For Variants, all relation information is taken directly from
the existing Variant JSON definition. The generator contains
no second definition of the 13 Weak Relations.
"""

from __future__ import annotations

from typing import Any

try:
    from .config import CANDLE_SPACING
except ImportError:
    from config import CANDLE_SPACING


# ----------------------------------------------------------------------
# GENERATION SETTINGS
# ----------------------------------------------------------------------

BODY_UNIT = 5.0
WICK_SIZE = 7.5

CANDLE_X_POSITIONS = (
    0.0,
    CANDLE_SPACING,
    CANDLE_SPACING * 2.0,
)


# ----------------------------------------------------------------------
# STRICT TRIO RELATION VALUES
# ----------------------------------------------------------------------
#
# These values are only the current geometric representation used
# for the four strict Main Trio classes.
#
# They are not the 13 Weak Relations.
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


def _validate_direction(
    direction: str,
) -> None:
    """Validate a three-candle direction string."""

    if not isinstance(direction, str):
        raise TypeError(
            "direction must be a string"
        )

    if len(direction) != 3:
        raise ValueError(
            "direction must contain exactly three candles"
        )

    if any(
        candle not in ("B", "S")
        for candle in direction
    ):
        raise ValueError(
            "direction may contain only B and S"
        )


def _validate_trio_definition(
    trio: dict[str, Any],
) -> None:
    """Validate the semantic definition of a Main Trio."""

    required_keys = (
        "number",
        "direction",
        "body_class",
        "upper_class",
        "lower_class",
    )

    for key in required_keys:
        if key not in trio:
            raise ValueError(
                f"Trio definition is missing key: {key}"
            )

    _validate_direction(
        trio["direction"]
    )


def _validate_variant_definition(
    variant: dict[str, Any],
) -> None:
    """Validate the semantic definition of a Variant."""

    required_keys = (
        "number",
        "direction",
        "body_relation_number",
        "body_relation",
        "upper_relation_number",
        "upper_relation",
        "lower_relation_number",
        "lower_relation",
    )

    for key in required_keys:
        if key not in variant:
            raise ValueError(
                f"Variant definition is missing key: {key}"
            )

    _validate_direction(
        variant["direction"]
    )

    _validate_relation(
        variant["body_relation"],
        "body_relation",
    )

    _validate_relation(
        variant["upper_relation"],
        "upper_relation",
    )

    _validate_relation(
        variant["upper_relation"],
        "upper_relation",
    )

    _validate_relation(
        variant["lower_relation"],
        "lower_relation",
    )


def _validate_relation(
    relation: Any,
    field_name: str,
) -> None:
    """
    Validate a relation supplied by the Variant JSON.

    The generator does not know what the 13 relations are.
    It only requires the already-stored relation data to contain
    three numeric rank values.
    """

    if not isinstance(relation, (list, tuple)):
        raise TypeError(
            f"{field_name} must be a list or tuple"
        )

    if len(relation) != 3:
        raise ValueError(
            f"{field_name} must contain three values"
        )

    for value in relation:
        if not isinstance(
            value,
            (int, float),
        ):
            raise TypeError(
                f"{field_name} values must be numeric"
            )


# ----------------------------------------------------------------------
# STRICT RELATION HELPERS
# ----------------------------------------------------------------------


def _strict_values(
    class_name: str,
) -> tuple[float, float, float]:
    """
    Return geometric values for one strict Main Trio class.
    """

    try:
        return STRICT_RELATION_VALUES[class_name]
    except KeyError as exc:
        raise ValueError(
            f"Unknown strict relation: {class_name}"
        ) from exc


# ----------------------------------------------------------------------
# CANDLE CREATION
# ----------------------------------------------------------------------


def _build_candle(
    index: int,
    direction: str,
    body_center: float,
    body_size: float,
    upper_rank: float,
    lower_rank: float,
    top: float,
    bottom: float,
) -> dict[str, Any]:
    """
    Build one OHLC candle.

    direction:
        B = bullish
        S = bearish

    body_center:
        Current geometric body-center value.

    body_size:
        Current geometric body size.

    upper_rank:
        Current geometric upper value.

    lower_rank:
        Current geometric lower value.
    """

    if direction not in ("B", "S"):
        raise ValueError(
            f"Invalid candle direction: {direction}"
        )

    if direction == "B":
        open_value = (
            body_center
            - body_size / 2.0
        )

        close_value = (
            body_center
            + body_size / 2.0
        )

    else:
        open_value = (
            body_center
            + body_size / 2.0
        )

        close_value = (
            body_center
            - body_size / 2.0
        )

    body_high = max(
        open_value,
        close_value,
    )

    body_low = min(
        open_value,
        close_value,
    )

    high_value = (
        top
        + (upper_rank + 1) * 5
    )

    low_value = (
        bottom
        + (lower_rank + 1) * 5
    )

    return {
        "label": chr(
            ord("A") + index
        ),
        "index": index,
        "x": CANDLE_X_POSITIONS[index],
        "direction": direction,
        "open": round(
            open_value,
            6,
        ),
        "high": round(
            high_value,
            6,
        ),
        "low": round(
            low_value,
            6,
        ),
        "close": round(
            close_value,
            6,
        ),
        "body": round(
            body_center,
            6,
        ),
    }


def _build_candles(
    direction: str,
    body_values: tuple[float, float, float],
    upper_values: tuple[float, float, float],
    lower_values: tuple[float, float, float],
) -> list[dict[str, Any]]:
    """Build the three candles A, B and C."""

    body_sizes = tuple(
        (value + 1.0) * BODY_UNIT
        for value in body_values
    )

    body_highs: list[float] = []
    body_lows: list[float] = []

    for index in range(3):
        body_center = body_values[index]
        body_size = body_sizes[index]

        body_highs.append(
            body_center
            + body_size / 2.0
        )

        body_lows.append(
            body_center
            - body_size / 2.0
        )

    top = max(body_highs)
    bottom = min(body_lows)

    lower_max = max(lower_values)

    bottom = (
        bottom
        - 2.0 * (lower_max + 1) * 5
    )

    candles: list[dict[str, Any]] = []

    for index in range(3):
        candles.append(
            _build_candle(
                index=index,
                direction=direction[index],
                body_center=body_values[index],
                body_size=body_sizes[index],
                upper_rank=upper_values[index],
                lower_rank=lower_values[index],
                top=top,
                bottom=bottom,
            )
        )

    return candles


# ----------------------------------------------------------------------
# MAIN TRIO
# ----------------------------------------------------------------------


def generate_trio(
    trio: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate image instructions for one Main Trio.

    The Trio definition is supplied by the orchestrator.

    The generator does not query transformer.py.
    """

    _validate_trio_definition(
        trio
    )

    trio_number = int(
        trio["number"]
    )

    trio_name = f"Trio{trio_number:03d}"

    direction = trio["direction"]

    body_values = _strict_values(
        trio["body_class"]
    )

    upper_values = _strict_values(
        trio["upper_class"]
    )

    lower_values = _strict_values(
        trio["lower_class"]
    )

    candles = _build_candles(
        direction=direction,
        body_values=body_values,
        upper_values=upper_values,
        lower_values=lower_values,
    )

    return {
        "name": trio_name,
        "type": "trio",
        "number": trio_number,
        "direction": direction,
        "body_class": trio["body_class"],
        "upper_class": trio["upper_class"],
        "lower_class": trio["lower_class"],
        "json_path": (
            f"{trio_name}/"
            f"{trio_name}.json"
        ),
        "image_path": (
            f"{trio_name}/"
            f"{trio_name}.png"
        ),
        "candles": candles,
    }


# ----------------------------------------------------------------------
# VARIANT
# ----------------------------------------------------------------------


def generate_variant(
    variant: dict[str, Any],
    trio_number: int,
) -> dict[str, Any]:
    """
    Generate image instructions for one Variant.

    The complete Variant definition comes directly from the
    existing Variant JSON file.

    No Weak Relation is reconstructed.

    No Weak Relation is looked up.

    No Variant number is calculated.

    No Variant membership is calculated.

    The relation rank values stored in the Variant JSON are
    passed directly to the candle builder.
    """

    _validate_variant_definition(
        variant
    )

    variant_number = int(
        variant["number"]
    )

    variant_name = (
        f"Variant{variant_number:05d}"
    )

    trio_name = (
        f"Trio{trio_number:03d}"
    )

    direction = variant["direction"]

    body_values = tuple(
        float(value)
        for value in variant[
            "body_relation"
        ]
    )

    upper_values = tuple(
        float(value)
        for value in variant[
            "upper_relation"
        ]
    )

    lower_values = tuple(
        float(value)
        for value in variant[
            "lower_relation"
        ]
    )

    candles = _build_candles(
        direction=direction,
        body_values=body_values,
        upper_values=upper_values,
        lower_values=lower_values,
    )

    return {
        "name": variant_name,
        "type": "variant",
        "number": variant_number,
        "trio_number": trio_number,
        "direction": direction,
        "body_relation_number": variant[
            "body_relation_number"
        ],
        "body_relation": variant[
            "body_relation"
        ],
        "upper_relation_number": variant[
            "upper_relation_number"
        ],
        "upper_relation": variant[
            "upper_relation"
        ],
        "lower_relation_number": variant[
            "lower_relation_number"
        ],
        "lower_relation": variant[
            "lower_relation"
        ],
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
