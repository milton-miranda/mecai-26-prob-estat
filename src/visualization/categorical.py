"""
Categorical statistical visualization.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import seaborn as sns

from .theme import apply_stats_theme
from .utils import save_figure
from ..utils import validate_columns


def stat_proportions(
    data: pd.DataFrame,
    x: str,
    *,
    hue: str | None = None,
    normalize: bool = False,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Plot categorical counts or proportions.
    """

    columns = [x]

    if hue is not None:
        columns.append(hue)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    fig, ax = plt.subplots()

    if normalize and hue is None:

        proportions = (
            data[x]
            .value_counts(normalize=True)
            .rename_axis(x)
            .reset_index(name="proportion")
        )

        sns.barplot(
            data=proportions,
            x=x,
            y="proportion",
            ax=ax,
        )

        ax.set_ylabel("Proportion")

    else:

        sns.countplot(
            data=data,
            x=x,
            hue=hue,
            ax=ax,
        )

    ax.set_title(
        title or f"Distribution of {x}"
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax