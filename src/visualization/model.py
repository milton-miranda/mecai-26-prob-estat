"""
Statistical model visualization utilities.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .theme import apply_stats_theme
from .utils import save_figure
from ..utils import validate_columns


def coefficient_plot(
    results: pd.DataFrame,
    term: str = "term",
    estimate: str = "estimate",
    ci_low: str = "ci_low",
    ci_high: str = "ci_high",
    *,
    title: str = "Model Coefficients",
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Plot regression coefficients and confidence intervals.
    """

    validate_columns(
        results,
        [
            term,
            estimate,
            ci_low,
            ci_high,
        ],
    )

    apply_stats_theme()

    df = results.copy()

    y = np.arange(len(df))

    errors = np.vstack(
        [
            df[estimate] - df[ci_low],
            df[ci_high] - df[estimate],
        ]
    )

    fig, ax = plt.subplots()

    ax.errorbar(
        df[estimate],
        y,
        xerr=errors,
        fmt="o",
        capsize=4,
    )

    ax.axvline(
        0,
        linestyle="--",
        linewidth=1,
    )

    ax.set_yticks(y)
    ax.set_yticklabels(df[term])

    ax.set_xlabel("Estimate")
    ax.set_title(title)

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax


def interaction_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    moderator: str,
    *,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Visualize a statistical interaction.
    """

    validate_columns(
        data,
        [x, y, moderator],
    )

    apply_stats_theme()

    fig, ax = plt.subplots()

    sns.pointplot(
        data=data,
        x=x,
        y=y,
        hue=moderator,
        errorbar=("ci", 95),
        dodge=True,
        ax=ax,
    )

    ax.set_title(
        title
        or f"{x} × {moderator} interaction"
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax


def effect_plot(
    data: pd.DataFrame,
    predictor: str,
    predicted: str,
    *,
    group: str | None = None,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Plot model-predicted values.
    """

    columns = [
        predictor,
        predicted,
    ]

    if group:
        columns.append(group)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    fig, ax = plt.subplots()

    sns.lineplot(
        data=data,
        x=predictor,
        y=predicted,
        hue=group,
        ax=ax,
    )

    ax.set_title(
        title
        or "Estimated Model Effects"
    )

    ax.set_ylabel("Predicted value")

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax