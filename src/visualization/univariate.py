"""
Univariate statistical visualizations inspired by ggstatsplot::gghistostats.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns

from .theme import apply_stats_theme
from .utils import format_p_value, save_figure


def stat_histogram(
    data: pd.DataFrame,
    variable: str,
    *,
    test_value: float | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    bins: int | str = "auto",
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Plot a numerical distribution with statistical information.

    Inspired by ggstatsplot::gghistostats.

    Parameters
    ----------
    data:
        Input dataframe.

    variable:
        Numerical column to analyse.

    test_value:
        Optional value used for a one-sample t-test.

    title:
        Figure title.

    xlabel:
        Custom x-axis label.

    bins:
        Histogram bins.

    save_path:
        Optional location where the figure will be saved.

    show:
        Whether matplotlib should display the figure.

    Returns
    -------
    fig, ax, statistics
    """

    apply_stats_theme()

    if variable not in data.columns:
        raise ValueError(
            f"Column '{variable}' was not found."
        )

    values = (
        pd.to_numeric(
            data[variable],
            errors="coerce",
        )
        .dropna()
        .astype(float)
    )

    if len(values) < 3:
        raise ValueError(
            "At least three valid observations are required."
        )

    mean = values.mean()
    median = values.median()
    sd = values.std(ddof=1)
    n = len(values)

    normality = pg.normality(values)

    normality_p = float(
        normality["pval"].iloc[0]
    )

    test_result = None

    if test_value is not None:
        test_result = pg.ttest(
            values,
            test_value,
        )

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    sns.histplot(
        x=values,
        bins=bins,
        kde=True,
        ax=ax,
    )

    ax.axvline(
        mean,
        linestyle="--",
        linewidth=1.5,
        label=f"Mean = {mean:.2f}",
    )

    ax.axvline(
        median,
        linestyle=":",
        linewidth=1.5,
        label=f"Median = {median:.2f}",
    )

    if test_value is not None:
        ax.axvline(
            test_value,
            linestyle="-.",
            linewidth=1.5,
            label=f"Test value = {test_value:g}",
        )

    statistics_text = (
        f"n = {n}\n"
        f"Mean = {mean:.2f}\n"
        f"SD = {sd:.2f}\n"
        f"Median = {median:.2f}\n"
        f"Normality: {format_p_value(normality_p)}"
    )

    if test_result is not None:

        t_value = float(
            test_result["T"].iloc[0]
        )

        p_value = float(
            test_result["p-val"].iloc[0]
        )

        dof = float(
            test_result["dof"].iloc[0]
        )

        cohen_d = float(
            test_result["cohen-d"].iloc[0]
        )

        statistics_text += (
            "\n\nOne-sample t-test"
            f"\nt({dof:.0f}) = {t_value:.2f}"
            f"\n{format_p_value(p_value)}"
            f"\nCohen's d = {cohen_d:.2f}"
        )

    ax.text(
        0.98,
        0.97,
        statistics_text,
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        bbox={
            "boxstyle": "round",
            "alpha": 0.08,
        },
    )

    ax.set_title(
        title or f"Distribution of {variable}"
    )

    ax.set_xlabel(
        xlabel or variable
    )

    ax.set_ylabel(
        "Frequency"
    )

    ax.legend()

    fig.tight_layout()

    save_figure(
        fig,
        save_path,
    )

    statistics = {
        "n": n,
        "mean": mean,
        "median": median,
        "sd": sd,
        "normality_p": normality_p,
        "test": test_result,
    }

    if show:
        plt.show()

    return fig, ax, statistics