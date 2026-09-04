import pathlib
from collections.abc import Callable

import matplotlib
import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np
from cmcrameri import cm as cm  # noqa: PLC0414
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.markers import MarkerStyle
from tudatpy.astro.time_representation import DateTime
from tudatpy.estimation import observations
from tudatpy.estimation.observable_models_setup import links, model_settings

POSTER_FIG_SIZE = (9, 5)
DEFAULT_COLOR_MAP_NAME = "cmc.batlow"


def get_color_cycle_from_colormap(colormap_name: str, n_colors: int):
    """Get a color cycle from a colormap."""
    colormap = mpl.colormaps[colormap_name].resampled(n_colors)
    hex_colors = [mpl.colors.to_hex(color) for color in colormap.colors]
    return cycler("color", hex_colors)


def default_residuals_color_cycle(n_colors=15):
    """Get the default color cycle for residuals plots."""

    return get_color_cycle_from_colormap(DEFAULT_COLOR_MAP_NAME, n_colors)


def save_figure(fig: matplotlib.figure.Figure, file_path: pathlib.Path):

    file_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(file_path)


def create_residual_timeseries_with_histogram_figure(figsize=POSTER_FIG_SIZE):
    fig, (ax, ax_hist) = plt.subplots(
        1,
        2,
        figsize=figsize,
        constrained_layout=True,
        gridspec_kw={"width_ratios": [4, 1], "wspace": 0.05},
    )

    ax.set_xlabel("Epoch")
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax_hist.set_xlabel("Count")
    ax_hist.tick_params()

    return fig, (ax, ax_hist)


dss_id_only_link_label_formatter: Callable[[links.LinkDefinition], str] = (
    lambda link_definition: (
        f"{link_definition.link_ends[links.LinkEndType.transmitter].station_name[-2:]} / "
        f"{link_definition.link_ends[links.LinkEndType.receiver].station_name[-2:]}"
    )
)


def plot_doppler_residuals_with_histogram_link_end_grouped(
    observation_collection: observations.ObservationCollection,
    figsize=POSTER_FIG_SIZE,
    add_legend=True,
    link_label_formatter: Callable[
        [links.LinkDefinition], str
    ] = dss_id_only_link_label_formatter,
    legend_title: str = "Transmitter / Receiver DSS: RMS [mHz]",
):
    link_definitions = observation_collection.get_link_definitions_for_observables(
        model_settings.ObservableType.dsn_n_way_averaged_doppler_type
    )
    fig, (ax, ax_hist) = create_residual_timeseries_with_histogram_figure(
        figsize=figsize
    )

    for ii, link_definition in enumerate(link_definitions):
        link_end_parser = observations.observations_processing.observation_parser(
            link_definition.link_ends
        )

        parsed_filtered_observation_times_dt = [
            DateTime.from_epoch(t).to_python_datetime()
            for t in observation_collection.get_concatenated_observation_times(
                link_end_parser
            )
        ]
        parsed_filtered_residuals = (
            observation_collection.get_concatenated_residuals(link_end_parser) * 1000
        )
        parsed_prefit_filtered_RMS = np.sqrt(
            np.square(parsed_filtered_residuals).mean()
        )

        ax.scatter(
            parsed_filtered_observation_times_dt,
            parsed_filtered_residuals,
            marker=MarkerStyle(["o", ">", "s", "D"][ii % 4]),
            alpha=0.5,
            s=10,
            label=f"{link_label_formatter(link_definition)}: {parsed_prefit_filtered_RMS:.2f}",
        )

        ax_hist.hist(
            parsed_filtered_residuals,
            bins=51,
            orientation="horizontal",
            alpha=0.5,
        )

    if add_legend:
        ax.legend(
            ncols=4,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.15),
            title=legend_title,
        )

    ax.set_ylabel("Doppler residuals [mHz]")
    return fig, (ax, ax_hist)


def set_doppler_residual_statistic_title(
    ax: matplotlib.axes.Axes,
    residual_threshold: float,
    filtered_observations: observations.ObservationCollection,
    original_observations: observations.ObservationCollection,
    mission_name: str,
):

    prefit_filtered_residuals = filtered_observations.get_concatenated_residuals()
    prefit_filtered_N_obs = len(prefit_filtered_residuals)
    prefit_filtered_RMS = np.sqrt(np.square(prefit_filtered_residuals).mean())
    prefit_filtered_mean = prefit_filtered_residuals.mean()

    remaining_residuals_percentage = (
        prefit_filtered_N_obs / original_observations.observation_vector_size
    ) * 100

    # manual escape to avoid LaTeX rendering issues
    ax.set_title(
        f"{mission_name} N-Way Doppler pre-fit filtered at {residual_threshold * 1000:.0f} mHz:\nN={prefit_filtered_N_obs} ({remaining_residuals_percentage:.2f}\\%), RMS={prefit_filtered_RMS * 1000:.2f} mHz, mean={prefit_filtered_mean * 1000:.3f} mHz"
    )
