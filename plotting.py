""" Shared plotting functions for the WSRA mean square slope notebooks """

from typing import Optional

import cartopy
import cmocean
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Colormap
from matplotlib.collections import QuadMesh, PathCollection, PatchCollection
from matplotlib.contour import QuadContourSet, ContourSet
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrow, Arc


# Define default plot keyword arguments
default_ocean_kwargs = {'color': 'white'}
default_land_kwargs = {'color':'whitesmoke', 'zorder':3, 'alpha':0.4}
default_coast_kwargs = {'edgecolor': 'grey', 'linewidth': 0.5, 'zorder': 4}
default_intensity_cmap = mpl.cm.get_cmap('YlOrRd', 7)
default_wsra_marker_size = 5
default_storm_colors = {
    'earl': 'rebeccapurple',
    'fiona': 'orchid',
    'ian': 'steelblue',
    'julia': 'teal',
    'idalia': 'darkseagreen',
    'lee': 'cadetblue',
}
default_storm_labels = {
    'earl': 'Earl (2022)',
    'fiona': 'Fiona (2022)',
    'ian': 'Ian (2022)',
    'julia': 'Julia (2022)',
    'idalia': 'Idalia (2023)',
    'lee': 'Lee (2023)',
}


def configure_figures() -> None:
    plt.rcParams.update({'font.size': 12})
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = 'Helvetica'


def plot_base_chart(
    ax: GeoAxes,
    extent: np.ndarray,
    ocean_kwargs=default_ocean_kwargs,
    land_kwargs=default_land_kwargs,
    coast_kwargs=default_coast_kwargs,
) -> GeoAxes:
    # Initialize the figure, crop it based on extent, and add gridlines
    ax.set_extent(extent)
    ax.set_aspect('equal')
    gridlines = ax.gridlines(draw_labels=True, dms=False,
                             x_inline=False, y_inline=False) # zorder=0)
    gridlines.top_labels = False
    gridlines.left_labels = False
    gridlines.right_labels = True

    # Add the ocean, land, coastline, and border features
    ax.add_feature(cartopy.feature.OCEAN, **ocean_kwargs)
    ax.add_feature(cartopy.feature.LAND, **land_kwargs)
    ax.add_feature(cartopy.feature.COASTLINE, **coast_kwargs)

    return ax


def plot_wsra_track(
    wsra_ds: pd.DataFrame,
    ax: GeoAxes,
    color_column_name: Optional[str] = None,
    **kwargs,
) -> PathCollection:
    if color_column_name:
        color_column = wsra_ds[color_column_name]
    else:
        color_column = None

    if 'color' not in kwargs:
        kwargs['color'] = default_storm_colors[wsra_ds.attrs['storm_name']]
    if 's' not in kwargs:
        kwargs['s'] = default_wsra_marker_size
    if 'label' not in kwargs:
        kwargs['label'] = default_storm_labels[wsra_ds.attrs['storm_name']]

    plot = ax.scatter(wsra_ds['longitude'],
                      wsra_ds['latitude'],
                      c=color_column,
                      **kwargs)
    return plot


def plot_best_track(
    pts_gdf: gpd.GeoDataFrame,
    lin_gdf: gpd.GeoDataFrame,
    windswath_gdf: gpd.GeoDataFrame,
    ax: GeoAxes,
    intensity_cmap: Colormap = default_intensity_cmap,
) -> GeoAxes:
    lin_gdf.plot(
        color='k',
        zorder=2,
        ax=ax
    )

    windswath_gdf[windswath_gdf['RADII'] == 64.0].plot(
        facecolor='dimgrey',
        alpha=0.3,
        ax=ax,
    )

    windswath_gdf[windswath_gdf['RADII'] == 50.0].plot(
        facecolor='darkgrey',
        alpha=0.3,
        ax=ax,
    )

    windswath_gdf[windswath_gdf['RADII'] == 34.0].plot(
        facecolor='lightgrey',
        alpha=0.3,
        ax=ax,
    )

    # Plot the best track points; color and label by intensity
    pts_gdf.plot(
        column='saffir_simpson_int',
        cmap=intensity_cmap,
        vmin=-1.5,
        vmax=5.5,
        edgecolor='k',
        zorder=4,
        markersize=200,
        alpha=1.0,
        ax=ax,
    )

    for x, y, label in zip(pts_gdf.geometry.x, pts_gdf.geometry.y, pts_gdf['saffir_simpson_label']):
        ax.annotate(
            label,
            xy=(x, y),
            annotation_clip=True,
            ha='center',
            va='center',
            zorder=10,
            fontsize=9,
            bbox=dict(boxstyle='circle,pad=0', fc='none', ec='none')
        )

    return ax

    # counter = 0
    # for x, y, label in zip(pts_gdf.geometry.x, pts_gdf.geometry.y, pts_gdf.index):
    #     if counter % 3 == 0:
    #         ax.annotate(label.strftime('%Y-%m-%d %HZ') + '     ', xy=(x, y), annotation_clip=True, ha='right', va='center', zorder=10, fontsize=11,
    #             bbox=dict(boxstyle='circle,pad=0', fc='none', ec='none'))
    #     counter += 1
        