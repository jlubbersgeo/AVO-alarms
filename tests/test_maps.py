import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import shapely.geometry as sgeom


def make_map(latitude, longitude, main_dist=50, center_longitude=180):
    """Make the base maps for all AVO-alarms that require maps

    Args:
        latitude (_type_): _description_
        longitude (_type_): _description_
        main_dist (int, optional): _description_. Defaults to 50.
        inset_dist (int, optional): _description_. Defaults to 500.
        scale (int, optional): _description_. Defaults to 15.
        center_longitude (int, optional): _description_. Defaults to 180.
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
        projection=ccrs.Mercator(central_longitude=center_longitude),
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
    gl.ylocator = mticker.FixedLocator([latitude - (dlat / 2), latitude + (dlat / 2)])
    # these aren't working with stuff that straddles the anti-meridian
    gl.xlocator = mticker.FixedLocator([longitude - (dlon / 2), longitude + (dlon / 2)])
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

    return ax, inset_ax


# Shishaldin
latitude = 54.7554

longitude = -163.9711


fig = plt.figure(figsize=(4, 4))
make_map(latitude, longitude)
plt.savefig(
    r"C:\Users\jlubbers\OneDrive - DOI\Desktop\test_figures\AVO-alarms_maptest.png",
    bbox_inches="tight",
    dpi=250,
)
# plt.show()
