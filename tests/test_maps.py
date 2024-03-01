from datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import shapely.geometry as sgeom
from matplotlib.path import Path
from matplotlib_scalebar.scalebar import ScaleBar


def add_watermark(text, ax=None):
    """Add a watermark to a figure

    Args:
        text (str): the text to add as a watermark
        ax (matplotlib Axes object, optional): the matplotlib axis to add the watermark to.
        Defaults to None. if `None` then `plt.gca` is used.
    """
    if ax is None:
        ax = plt.gca()

    ax.text(
        0.5,
        0.5,
        text,
        transform=ax.transAxes,
        fontsize=50,
        color="gray",
        alpha=0.5,
        va="center",
        ha="center",
    )


def make_map(latitude, longitude, main_dist=50, center_longitude=180, test=False):
    """
    Make the base maps for all AVO-alarms that require maps

    Args:
        latitude (float): latitude of volcano in decimal degrees

        longitude (float): longitude of volcano in decimal degrees

        main_dist (int, optional): WECH WHAT IS THIS...some way of establishing bounding box?.
        Defaults to 50.

        center_longitude (int, optional): center longitude of cartopy.ccrs.Mercator().Because
        we are near the anti-meridian this works better than API default. Defaults to 180.
    """
    dlat = 1 * (main_dist / 111.1)
    dlon = dlat / np.cos(latitude * np.pi / 180)

    latitude_min = latitude - dlat
    latitude_max = latitude + dlat

    if longitude > 0:
        longitude = (longitude - 180) - 180

    longitude_min = longitude - dlon
    longitude_max = longitude + dlon

    extent = [longitude_min, longitude_max, latitude_min, latitude_max]
    inset_extent = [
        longitude_min - 5,
        longitude_max + 5,
        latitude_min - 2,
        latitude_max + 2,
    ]
    # inset_extent = extent

    land_color = "silver"
    water_color = "lightblue"

    try:
        fig = plt.gcf()
    except:
        fig = plt.figure(figsize=(4, 4))

    fig.set_facecolor("w")

    ax = fig.add_subplot(
        1, 1, 1, projection=ccrs.Mercator(central_longitude=center_longitude)
    )
    # make the figure

    # Create an inset GeoAxes
    inset_ax = fig.add_axes(
        [0.75, 0.75, 0.2, 0.2],
        projection=ccrs.AlbersEqualArea(central_longitude=center_longitude),
    )

    ax.set_extent(extent, crs=ccrs.PlateCarree())
    inset_ax.set_extent(inset_extent, crs=ccrs.PlateCarree())

    try:
        ax.coastlines(linewidth=0.5)
        inset_ax.coastlines(linewidth=0.25)

    except:
        pass

    # add thick border around edge
    ax.spines["geo"].set_linewidth(2)
    inset_ax.spines["geo"].set_linewidth(1)

    # add land and ocean features
    ax.add_feature(cfeature.LAND, facecolor=land_color)
    ax.add_feature(cfeature.OCEAN, facecolor=water_color)

    inset_ax.add_feature(cfeature.LAND, facecolor=land_color)
    inset_ax.add_feature(cfeature.OCEAN, facecolor=water_color)

    # format the grid lines
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5,
        linestyle="--",
        color="gray",
        formatter_kwargs={
            "direction_label": True,
            "number_format": ".2f",
        },
    )
    # grid lines
    lon_line_locs = [longitude - (dlon / 2), longitude + (dlon / 2)]
    new_lon_locs = []
    for loc in lon_line_locs:
        if loc < -180:
            new_lon_locs.append(loc + 360)
        else:
            new_lon_locs.append(loc)

    gl.ylocator = mticker.FixedLocator([latitude - (dlat / 2), latitude + (dlat / 2)])
    # these aren't working with stuff that straddles the anti-meridian
    gl.xlocator = mticker.FixedLocator(new_lon_locs)
    gl.xlabel_style = {"fontsize": 6}
    gl.ylabel_style = {"fontsize": 6}
    gl.top_labels = False
    gl.left_labels = True
    gl.bottom_labels = True
    gl.right_labels = False

    # box around main map within inset
    extent_box = sgeom.box(extent[0], extent[2], extent[1], extent[3])
    inset_ax.add_geometries(
        [extent_box],
        ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="red",
        linewidth=0.35,
    )

    if test is True:
        add_watermark("TEST\nIMAGE", ax=ax)

    # making non-rectangular bounding box on inset
    # e.g., trim along lines of longitude
    lower_space = 0
    rect = Path(
        [
            [inset_extent[0], inset_extent[2]],
            [inset_extent[1], inset_extent[2]],
            [inset_extent[1], inset_extent[3]],
            [inset_extent[0], inset_extent[3]],
            [inset_extent[0], inset_extent[2]],
        ]
    ).interpolated(20)
    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(inset_ax) - inset_ax.transData
    rect_in_target = proj_to_data.transform_path(rect)

    inset_ax.set_boundary(rect_in_target)
    inset_ax.set_extent(
        [
            inset_extent[0],
            inset_extent[1],
            inset_extent[2] - lower_space,
            inset_extent[3],
        ]
    )

    # scale bar
    # https://github.com/ppinard/matplotlib-scalebar
    # need to check to see if this is the right dx
    ax.add_artist(
        ScaleBar(
            dx=1,
            location="lower left",
            box_color="none",
            scale_loc="right",
            font_properties={"size": 6},
        )
    )
    date_and_time = datetime.now()
    datetime_string = date_and_time.strftime("%d/%m/%Y %H:%M:%S")
    ax.set_title(datetime_string, loc="left")
    return ax, inset_ax


############################ TESTING THE ABOVE FUNCTION #########################################
# THIS TEST CHOOSES ONE VOLCANO COMPLETELY IN THE WESTERN HEMISPHERE, ONE COMPLETELY IN THE EAST,
# AND ONE THAT IS VERY CLOSE TO THE DATE LINE

# the major cost to performance is downloading the data for the small inset
# can we somehow cache this?
# https://discourse.holoviz.org/t/using-geoviews-tile-sources-offline/4859/5

# test locations
test_dict = {
    "name": ["Shishaldin", "Semisopochnoi", "Buldir"],
    "latitude": np.array([54.7554, 51.9288, 52.3488]),
    "longitude": np.array([-163.9711, 179.5977, 175.909]),
}
export_path = r"C:\Users\jlubbers\Desktop\test_figures"

for i in range(len(test_dict)):
    print(f"working on {test_dict['name'][i]}")
    fig = plt.figure(figsize=(4, 4))
    make_map(test_dict["latitude"][i], test_dict["longitude"][i], test=True)
    save_path = f"{export_path}\AVO-alarms_maptest_{test_dict['name'][i]}.png"
    print(save_path)
    plt.savefig(
        save_path,
        bbox_inches="tight",
        dpi=250,
    )
