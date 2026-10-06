"""
Renderer for Forex Trio Atlas.

Consumes the JSON-compatible document produced by generator.py
and renders the contained image instructions with Matplotlib.
"""

from __future__ import annotations

import json
import os
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

try:
    from . import config
except ImportError:
    import config


# ----------------------------------------------------------------------
# CANDLE GEOMETRY
# ----------------------------------------------------------------------

def _draw_candle(ax, candle: dict[str, Any]) -> None:
    """Draw one candlestick from a JSON candle definition."""

    x = float(candle["x"])
    open_price = float(candle["open"])
    high_price = float(candle["high"])
    low_price = float(candle["low"])
    close_price = float(candle["close"])

    direction = candle["direction"]

    if direction == "B":
        candle_color = config.BULLISH_COLOR
    else:
        candle_color = config.BEARISH_COLOR

    # Wick
    ax.plot(
        [x, x],
        [low_price, high_price],
        color=config.WICK_COLOR,
        linewidth=config.WICK_WIDTH,
        solid_capstyle="butt",
        zorder=1,
    )

    # Body
    body_low = min(open_price, close_price)
    body_high = max(open_price, close_price)
    body_height = body_high - body_low

    # A zero-height body is still visible.
    if body_height == 0:
        body_height = 0.02

    body = Rectangle(
        (
            x - config.BODY_WIDTH / 2.0,
            body_low,
        ),
        config.BODY_WIDTH,
        body_height,
        facecolor=candle_color,
        edgecolor=candle_color,
        linewidth=1.0,
        zorder=2,
    )

    ax.add_patch(body)


# ----------------------------------------------------------------------
# IMAGE RENDERING
# ----------------------------------------------------------------------

def render_image(image_data: dict[str, Any], output_path: str) -> None:
    """Render one image instruction to a PNG file."""

    candles = image_data["candles"]

    figure_width = config.IMAGE_WIDTH / config.DPI
    figure_height = config.IMAGE_HEIGHT / config.DPI

    fig, ax = plt.subplots(
        figsize=(figure_width, figure_height),
        dpi=config.DPI,
    )

    fig.patch.set_facecolor(config.BACKGROUND_COLOR)
    ax.set_facecolor(config.BACKGROUND_COLOR)

    # Draw candles.
    for candle in candles:
        _draw_candle(ax, candle)

    # --------------------------------------------------------------
    # AXIS LIMITS
    # --------------------------------------------------------------

    x_values = [float(candle["x"]) for candle in candles]

    low_values = [float(candle["low"]) for candle in candles]
    high_values = [float(candle["high"]) for candle in candles]

    x_min = min(x_values)
    x_max = max(x_values)

    y_min = min(low_values)
    y_max = max(high_values)

    x_range = max(x_max - x_min, 1.0)
    y_range = max(y_max - y_min, 1.0)

    left = x_min - x_range * config.LEFT_MARGIN
    right = x_max + x_range * config.RIGHT_MARGIN

    bottom = y_min - y_range * config.BOTTOM_MARGIN
    top = y_max + y_range * config.TOP_MARGIN

    ax.set_xlim(left, right)
    ax.set_ylim(bottom, top)

    # --------------------------------------------------------------
    # VISUAL APPEARANCE
    # --------------------------------------------------------------

    ax.axis("off")

    plt.subplots_adjust(
        left=0,
        right=1,
        top=1,
        bottom=0,
    )

    # --------------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------------

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fig.savefig(
        output_path,
        dpi=config.DPI,
        format=config.IMAGE_FORMAT,
        facecolor=config.BACKGROUND_COLOR,
        transparent=config.TRANSPARENT_BACKGROUND,
        bbox_inches=None,
        pad_inches=0,
    )

    plt.close(fig)


# ----------------------------------------------------------------------
# DOCUMENT RENDERING
# ----------------------------------------------------------------------

def render_document(
    document: dict[str, Any],
    output_directory: str | None = None,
) -> list[str]:
    """
    Render all image instructions contained in a Generator document.

    Returns a list of generated file paths.
    """

    if output_directory is None:
        output_directory = config.OUTPUT_DIRECTORY

    os.makedirs(output_directory, exist_ok=True)

    generated_files: list[str] = []

    for image_data in document["images"]:
        image_number = int(image_data["number"])

        filename = config.OUTPUT_FILENAME_PATTERN.format(
            number=image_number
        )

        output_path = os.path.join(
            output_directory,
            filename,
        )

        render_image(
            image_data,
            output_path,
        )

        generated_files.append(output_path)

    return generated_files


# ----------------------------------------------------------------------
# JSON FILE SUPPORT
# ----------------------------------------------------------------------

def render_json_file(
    json_path: str,
    output_directory: str | None = None,
) -> list[str]:
    """Read a Generator JSON file and render all contained images."""

    with open(
        json_path,
        "r",
        encoding="utf-8",
    ) as file:
        document = json.load(file)

    return render_document(
        document,
        output_directory,
    )


# ----------------------------------------------------------------------
# TEST ENTRY POINT
# ----------------------------------------------------------------------

def main() -> None:
    """
    Temporary pipeline test.

    Generator produces the JSON-compatible document.
    Renderer receives that document and produces PNG.

    This is only a test bridge for the current development stage.
    """

    try:
        from .generator import generate_trio
    except ImportError:
        from generator import generate_trio

    document = generate_trio(
        1,
        include_variants=False,
    )

    generated_files = render_document(document)

    print("Rendered files:")

    for path in generated_files:
        print(path)


if __name__ == "__main__":
    main()
