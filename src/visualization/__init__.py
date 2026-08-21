"""
Statistical visualization API.
"""

from .univariate import stat_histogram
from .between import stat_between
from .within import stat_within

from .correlation import (
    stat_scatter,
    stat_corr_matrix,
)

from .categorical import stat_proportions

from .model import (
    coefficient_plot,
    interaction_plot,
    effect_plot,
)

from .experimental import (
    stat_pre_post,
    stat_crossover,
    stat_nback_load,
    stat_sam_trajectory,
    stat_speed_accuracy,
)

__all__ = [
    "stat_histogram",
    "stat_between",
    "stat_within",
    "stat_scatter",
    "stat_corr_matrix",
    "stat_proportions",
    "coefficient_plot",
    "interaction_plot",
    "effect_plot",
    "stat_pre_post",
    "stat_crossover",
    "stat_nback_load",
    "stat_sam_trajectory",
    "stat_speed_accuracy",
]