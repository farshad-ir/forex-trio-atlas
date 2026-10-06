"""
Global rendering configuration for Forex Trio Atlas.

All visual parameters should be adjusted here rather than inside
the renderer. This keeps the rendering logic independent from the
final appearance of generated images.
"""


# ----------------------------------------------------------------------
# IMAGE
# ----------------------------------------------------------------------

# Final image size in pixels.
IMAGE_WIDTH = 1600
IMAGE_HEIGHT = 900

# Output resolution.
DPI = 200

# Image format.
IMAGE_FORMAT = "png"

# Background.
BACKGROUND_COLOR = "white"

# Transparency.
TRANSPARENT_BACKGROUND = False


# ----------------------------------------------------------------------
# CANDLE
# ----------------------------------------------------------------------

# Width of each candle body.
BODY_WIDTH = 0.55

# Width of candle wick.
WICK_WIDTH = 1.5

# Horizontal distance between candle centers.
CANDLE_SPACING = 1.5


# ----------------------------------------------------------------------
# IMAGE MARGINS
# ----------------------------------------------------------------------

# Horizontal margin around the three candles.
LEFT_MARGIN = 0.8
RIGHT_MARGIN = 0.8

# Vertical margin around the price range.
TOP_MARGIN = 0.10
BOTTOM_MARGIN = 0.10


# ----------------------------------------------------------------------
# CLASS SCALE
# ----------------------------------------------------------------------

# Visual size of the four relation classes.
#
# These values are not Forex price values.
# They control how clearly the differences appear in the image.

RISING_SIZE = 20.0
FALLING_SIZE = 20.0
PEAK_SIZE = 30.0
VALLEY_SIZE = 30.0


# ----------------------------------------------------------------------
# CANDLE COLORS
# ----------------------------------------------------------------------

BULLISH_COLOR = "green"
BEARISH_COLOR = "red"

WICK_COLOR = "black"


# ----------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------

# Default directory for generated images.
OUTPUT_DIRECTORY = "output"

# Default filename pattern.
OUTPUT_FILENAME_PATTERN = "Trio{number:03d}.png"
