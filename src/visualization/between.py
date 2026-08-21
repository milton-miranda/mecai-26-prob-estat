"""
Between-group statistical visualizations.

Inspired by ggstatsplot::ggbetweenstats.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import seaborn as sns

from .theme import apply_stats_theme
from .utils import format_p_value, save_figure


def stat_between(
    data: pd.DataFrame,
    group: str,
    outcome: str,
    *,
    title: str | None = None,
    ylabel: str | None = None,
    order: list[str] | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Compare a continuous outcome between independent groups.

    Two groups:
        Welch t-test.

    Three or more groups:
        Welch ANOVA.

    Returns figure and statistical results.
    """

    apply_stats_theme()

    df = (
        data[[group, outcome]]
        .dropna()
        .copy()
    )

    levels = (
        order
        if order is not None
        else list(df[group].unique())
    )

    n_groups = len(levels)

    if n_groups < 2:
        raise ValueError(
            "At least two groups are required."
        )

    if n_groups == 2:

        group_1 = df.loc[
            df[group] == levels[0],
            outcome,
        ]

        group_2 = df.loc[
            df[group] == levels[1],
            outcome,
        ]

        result = pg.ttest(
            group_1,
            group_2,
            correction=True,
        )

        statistic = float(
            result["T"].iloc[0]
        )

        p_value = float(
            result["p-val"].iloc[0]
        )

        effect = float(
            result["cohen-d"].iloc[0]
        )

        stats_text = (
            "Welch t-test\n"
            f"t = {statistic:.2f}\n"
            f"{format_p_value(p_value)}\n"
            f"Cohen's d = {effect:.2f}"
        )

    else:

        result = pg.welch_anova(
            data=df,
            dv=outcome,
            between=group,
        )

        statistic = float(
            result["F"].iloc[0]
        )

        p_value = float(
            result["p-unc"].iloc[0]
        )

        effect = float(
            result["np2"].iloc[0]
        )

        stats_text = (
            "Welch ANOVA\n"
            f"F = {statistic:.2f}\n"
            f"{format_p_value(p_value)}\n"
            f"η²p = {effect:.3f}"
        )

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    sns.violinplot(
        data=df,
        x=group,
        y=outcome,
        order=levels,
        inner=None,
        cut=0,
        ax=ax,
    )

    sns.boxplot(
        data=df,
        x=group,
        y=outcome,
        order=levels,
        width=0.25,
        showfliers=False,
        ax=ax,
    )

    sns.stripplot(
        data=df,
        x=group,
        y=outcome,
        order=levels,
        alpha=0.55,
        jitter=0.18,
        ax=ax,
    )

    ax.text(
        0.98,
        0.97,
        stats_text,
        transform=ax.transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        bbox={
            "boxstyle": "round",
            "alpha": 0.08,
        },
    )

    ax.set_title(
        title or f"{outcome} by {group}"
    )

    ax.set_xlabel(group)

    ax.set_ylabel(
        ylabel or outcome
    )

    fig.tight_layout()

    save_figure(
        fig,
        save_path,
    )

    if show:
        plt.show()

    return fig, ax, result