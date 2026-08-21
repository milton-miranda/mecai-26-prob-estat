"""
Utility functions used by statistical visualization modules.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ..config import FIGURE_DPI

def format_p_value(p: float) -> str:
    """Format a p-value for presentation."""

    if p < 0.001:
        return "p < 0.001"

    return f"p = {p:.3f}"


def significance_stars(p: float) -> str:
    """Convert a p-value to significance stars."""

    if p < 0.001:
        return "***"

    if p < 0.01:
        return "**"

    if p < 0.05:
        return "*"

    return "ns"


def save_figure(
    fig: Figure,
    path: str | Path | None,
    dpi: int = FIGURE_DPI,
) -> None:
    """Save a figure when a path is supplied."""

    if path is None:
        return

    output = Path(path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output,
        dpi=dpi,
        bbox_inches="tight",
    )