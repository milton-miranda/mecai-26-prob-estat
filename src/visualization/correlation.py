"""
Correlation and scatterplot statistical figures.

Inspired by ggstatsplot::ggscatterstats and ggcorrmat.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import seaborn as sns

from .theme import apply_stats_theme

from ..utils import validate_columns

from .utils import (
    format_p_value,
    save_figure,
)


def stat_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    method: str = "pearson",
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Scatterplot with regression line and correlation statistics.

    method:
        pearson, spearman or kendall
    """

    validate_columns(data, [x, y])

    df = data[
        [x, y]
    ].dropna()

    result = pg.corr(
        x=df[x],
        y=df[y],
        method=method,
    )

    r = float(result["r"].iloc[0])
    p = float(result["p-val"].iloc[0])
    n = int(result["n"].iloc[0])

    apply_stats_theme()

    fig, ax = plt.subplots()

    sns.regplot(
        data=df,
        x=x,
        y=y,
        ax=ax,
        scatter_kws={
            "alpha": 0.6,
        },
    )

    text = (
        f"{method.title()} correlation\n"
        f"r = {r:.3f}\n"
        f"{format_p_value(p)}\n"
        f"n = {n}"
    )

    ax.text(
        0.03,
        0.97,
        text,
        transform=ax.transAxes,
        va="top",
        bbox={
            "boxstyle": "round",
            "alpha": 0.08,
        },
    )

    ax.set_title(
        title or f"{x} × {y}"
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax, result


def stat_corr_matrix(
    data: pd.DataFrame,
    variables: list[str],
    *,
    method: str = "pearson",
    annotate: bool = True,
    title: str = "Correlation Matrix",
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Statistical correlation matrix for multiple variables.
    """

    validate_columns(data, variables)

    df = data[
        variables
    ].apply(
        pd.to_numeric,
        errors="coerce",
    )

    corr = df.corr(
        method=method
    )

    apply_stats_theme()

    fig, ax = plt.subplots(
        figsize=(10, 8)
    )

    sns.heatmap(
        corr,
        annot=annotate,
        fmt=".2f",
        square=True,
        center=0,
        ax=ax,
    )

    ax.set_title(title)

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax, corr