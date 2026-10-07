from __future__ import annotations

try:
    from .config import CANDLE_SPACING
except ImportError:
    from config import CANDLE_SPACING


BODY_UNIT = 5.0
WICK_UNIT = 5.0


def build_geometry(
    direction: str,
    body_values: tuple[float, float, float],
    upper_values: tuple[float, float, float],
    lower_values: tuple[float, float, float],
) -> dict:
    """
    Build the geometry of a three-candle pattern.

    Trio and Variant use the same geometry builder.

    The output contains only OHLC data for the three candles.
    """


    # Build the three bodies as one geometric structure.

    body_sizes = [
        (value + 1.0) * BODY_UNIT
        for value in body_values
    ]

    body_highs = [
        body_values[i] + body_sizes[i] / 2.0
        for i in range(3)
    ]

    body_lows = [
        body_values[i] - body_sizes[i] / 2.0
        for i in range(3)
    ]

    # Establish the common vertical frame.

    top = max(body_highs)
    bottom = min(body_lows)

    lower_max = max(lower_values)

    bottom -= (
        2.0
        * (lower_max + 1.0)
        * WICK_UNIT
    )

    # Build all three candles together.

    candles = []

    for i in range(3):
        body_center = body_values[i]
        body_size = body_sizes[i]

        if direction[i] == "B":
            open_value = (
                body_center - body_size / 2.0
            )
            close_value = (
                body_center + body_size / 2.0
            )
        else:
            open_value = (
                body_center + body_size / 2.0
            )
            close_value = (
                body_center - body_size / 2.0
            )

        high_value = (
            top
            + (upper_values[i] + 1.0)
            * WICK_UNIT
        )

        low_value = (
            bottom
            + (lower_values[i] + 1.0)
            * WICK_UNIT
        )

        candles.append(
            {
                "open": round(open_value, 6),
                "high": round(high_value, 6),
                "low": round(low_value, 6),
                "close": round(close_value, 6),
            }
        )

    return {
        "candles": candles,
    }
