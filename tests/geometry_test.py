import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from geometry import build_geometry


geometry = build_geometry(
    direction="BBB",
    body_values=(0, 1, 2),
    upper_values=(0, 1, 2),
    lower_values=(2, 1, 0),
)

print(geometry)
