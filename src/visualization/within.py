"""
Within-subject statistical figures.

Inspired by ggstatsplot::ggwithinstats.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pingouin as pg
import seaborn as sns

from .theme import apply_stats_theme
from .utils import format_p_value, save_figure


def stat_within(
    data: pd.DataFrame,
    condition: str,
    outcome: str,
    subject: str,
    *,
    title: str | None = None,
    order: list[str] | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Statistical visualization for repeated measures.

    Parameters
    ----------
    condition:
        Within-subject experimental condition.

    outcome:
        Continuous dependent variable.

    subject:
        Participant identifier.
    """

    apply_stats_theme()

    df = (
        data[
            [subject, condition, outcome]
        ]
        .dropna()
        .copy()
    )

    levels = (
        order
        if order is not None
        else list(df[condition].unique())
    )

    n_conditions = len(levels)

    if n_conditions == 2:

        wide = df.pivot(
            index=subject,
            columns=condition,
            values=outcome,
        ).dropna()

        result = pg.ttest(
            wide[levels[0]],
            wide[levels[1]],
            paired=True,
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
            "Paired t-test\n"
            f"t = {statistic:.2f}\n"
            f"{format_p_value(p_value)}\n"
            f"Cohen's d = {effect:.2f}"
        )

    else:

        result = pg.rm_anova(
            data=df,
            dv=outcome,
            within=condition,
            subject=subject,
            detailed=True,
        )

        row = result.iloc[0]

        statistic = float(
            row["F"]
        )

        p_value = float(
            row["p-unc"]
        )

        effect = float(
            row["np2"]
        )

        stats_text = (
            "Repeated-measures ANOVA\n"
            f"F = {statistic:.2f}\n"
            f"{format_p_value(p_value)}\n"
            f"η²p = {effect:.3f}"
        )

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    sns.violinplot(
        data=df,
        x=condition,
        y=outcome,
        order=levels,
        inner=None,
        cut=0,
        ax=ax,
    )

    sns.boxplot(
        data=df,
        x=condition,
        y=outcome,
        order=levels,
        width=0.22,
        showfliers=False,
        ax=ax,
    )

    sns.stripplot(
        data=df,
        x=condition,
        y=outcome,
        order=levels,
        jitter=0.08,
        alpha=0.65,
        ax=ax,
    )

    position = {
        level: index
        for index, level in enumerate(levels)
    }

    for _, participant in df.groupby(subject):

        participant = participant[
            participant[condition].isin(levels)
        ]

        participant = participant.sort_values(
            condition,
            key=lambda s: s.map(position),
        )

        if len(participant) > 1:

            ax.plot(
                [
                    position[value]
                    for value
                    in participant[condition]
                ],
                participant[outcome],
                alpha=0.15,
                linewidth=0.8,
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
        title
        or f"{outcome} across {condition}"
    )

    ax.set_xlabel(condition)
    ax.set_ylabel(outcome)

    fig.tight_layout()

    save_figure(
        fig,
        save_path,
    )

    if show:
        plt.show()

    return fig, ax, result