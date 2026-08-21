"""
Shared visual configuration for statistical figures.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from ..config import (
    FIGURE_SIZE,
    FIGURE_DPI,
    FONT_SIZE,
    TITLE_FONT_SIZE,
    LABEL_FONT_SIZE,
)

from ..config import (
    FIGURE_SIZE,
    FIGURE_DPI,
    FONT_SIZE,
    TITLE_FONT_SIZE,
    LABEL_FONT_SIZE,
    LEGEND_FONT_SIZE,
)

def apply_stats_theme() -> None:

    plt.rcParams.update(
        {
            "figure.figsize": FIGURE_SIZE,
            "savefig.dpi": FIGURE_DPI,

            "font.size": FONT_SIZE,

            "axes.titlesize": TITLE_FONT_SIZE,
            "axes.labelsize": LABEL_FONT_SIZE,

            "legend.fontsize": LEGEND_FONT_SIZE,

            "axes.spines.top": False,
            "axes.spines.right": False,

            "legend.frameon": False,
        }
    )