"""
Visualization functions designed specifically for the
emotion × working-memory crossover experiment.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .theme import apply_stats_theme
from .utils import save_figure
from ..utils import validate_columns

def stat_pre_post(
    data: pd.DataFrame,
    subject: str,
    time: str,
    outcome: str,
    *,
    group: str | None = None,
    order: list[str] | None = None,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Pre-post visualization preserving participant trajectories.
    """

    columns = [
        subject,
        time,
        outcome,
    ]

    if group:
        columns.append(group)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    df = data[
        columns
    ].dropna()

    fig, ax = plt.subplots()

    sns.pointplot(
        data=df,
        x=time,
        y=outcome,
        hue=group,
        order=order,
        errorbar=("ci", 95),
        ax=ax,
    )

    ax.set_title(
        title or f"{outcome}: pre-post change"
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax

def stat_crossover(
    data: pd.DataFrame,
    session: str,
    outcome: str,
    subject: str,
    *,
    sequence: str | None = None,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Visualize crossover trajectories between sessions.
    """

    columns = [
        subject,
        session,
        outcome,
    ]

    if sequence:
        columns.append(sequence)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    df = data[
        columns
    ].dropna()

    fig, ax = plt.subplots()

    for _, participant in df.groupby(subject):

        participant = participant.sort_values(
            session
        )

        ax.plot(
            participant[session],
            participant[outcome],
            alpha=0.15,
        )

    sns.pointplot(
        data=df,
        x=session,
        y=outcome,
        hue=sequence,
        errorbar=("ci", 95),
        ax=ax,
    )

    ax.set_title(
        title or f"Crossover: {outcome}"
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax

def stat_nback_load(
    data: pd.DataFrame,
    load: str,
    outcome: str,
    emotion: str,
    *,
    subject: str | None = None,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Visualize working-memory performance across n-back load.

    Typical load:
        1-back
        2-back
        3-back
        4-back
    """

    columns = [
        load,
        outcome,
        emotion,
    ]

    if subject:
        columns.append(subject)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    fig, ax = plt.subplots()

    sns.pointplot(
        data=data,
        x=load,
        y=outcome,
        hue=emotion,
        errorbar=("ci", 95),
        dodge=True,
        ax=ax,
    )

    ax.set_title(
        title
        or f"{outcome} across cognitive load"
    )

    ax.set_xlabel("n-back load")

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax

def stat_sam_trajectory(
    data: pd.DataFrame,
    timepoint: str,
    outcome: str,
    condition: str,
    *,
    order: list[str] | None = None,
    title: str | None = None,
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Plot SAM trajectories across experimental timepoints.

    Intended outcomes:
        Valence
        Arousal
        Dominance
    """

    validate_columns(
        data,
        [
            timepoint,
            outcome,
            condition,
        ],
    )

    apply_stats_theme()

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    sns.pointplot(
        data=data,
        x=timepoint,
        y=outcome,
        hue=condition,
        order=order,
        errorbar=("ci", 95),
        ax=ax,
    )

    ax.set_title(
        title
        or f"SAM {outcome} trajectory"
    )

    ax.set_xlabel("Experimental timepoint")

    ax.tick_params(
        axis="x",
        rotation=30,
    )

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax

def stat_speed_accuracy(
    data: pd.DataFrame,
    accuracy: str,
    reaction_time: str,
    *,
    condition: str | None = None,
    title: str = "Speed-Accuracy Relationship",
    save_path: str | Path | None = None,
    show: bool = True,
):
    """
    Explore the speed-accuracy trade-off.

    Useful for identifying patterns such as:

    - fast + inaccurate
    - slow + accurate
    - slow + inaccurate
    """

    columns = [
        accuracy,
        reaction_time,
    ]

    if condition:
        columns.append(condition)

    validate_columns(
        data,
        columns,
    )

    apply_stats_theme()

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=data,
        x=reaction_time,
        y=accuracy,
        hue=condition,
        alpha=0.65,
        ax=ax,
    )

    sns.regplot(
        data=data,
        x=reaction_time,
        y=accuracy,
        scatter=False,
        ax=ax,
    )

    ax.set_title(title)

    ax.set_xlabel("Reaction Time")
    ax.set_ylabel("Accuracy")

    fig.tight_layout()

    save_figure(fig, save_path)

    if show:
        plt.show()

    return fig, ax

